"""Lesson engine services with full state machine."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import LessonDefinition, LessonSession, Submission
from app.shared.exceptions.domain import InvalidStateTransitionError, NotFoundError
from app.shared.state_machine import StateMachine

LESSON_STATES = {
    "CREATED", "ACTIVE", "SUBMITTED", "ANALYSIS_PENDING",
    "ANALYSIS_VALIDATED", "COMPLETED", "REJECTED", "FAILED",
}


def _create_lesson_machine(initial: str = "CREATED") -> StateMachine:
    sm = StateMachine(initial, LESSON_STATES)
    sm.add_transition("CREATED", "activate", "ACTIVE")
    sm.add_transition("ACTIVE", "submit", "SUBMITTED")
    sm.add_transition("SUBMITTED", "start_analysis", "ANALYSIS_PENDING")
    sm.add_transition("ANALYSIS_PENDING", "validate", "ANALYSIS_VALIDATED")
    sm.add_transition("ANALYSIS_VALIDATED", "complete", "COMPLETED")
    sm.add_transition("ANALYSIS_VALIDATED", "reject", "REJECTED")
    sm.add_transition("CREATED", "fail", "FAILED")
    sm.add_transition("ACTIVE", "fail", "FAILED")
    sm.add_transition("SUBMITTED", "fail", "FAILED")
    sm.add_transition("ANALYSIS_PENDING", "fail", "FAILED")
    sm.add_transition("ANALYSIS_VALIDATED", "fail", "FAILED")
    return sm


async def create_session(
    db: AsyncSession,
    user_id: str,
    lesson_definition_id: str,
) -> LessonSession:
    """Create a new lesson session."""
    uid = UUID(user_id)
    ld_id = UUID(lesson_definition_id)

    # Verify lesson definition exists
    lesson_def = await db.get(LessonDefinition, ld_id)
    if not lesson_def:
        raise NotFoundError("Lesson definition not found")

    session = LessonSession(
        user_id=uid,
        lesson_definition_id=ld_id,
        status="CREATED",
        current_attempt=0,
    )
    db.add(session)
    await db.flush()

    # Transition to ACTIVE
    sm = _create_lesson_machine("CREATED")
    sm.transition("activate")
    session.status = sm.current_state
    await db.flush()
    await db.refresh(session)
    return session


async def get_session(db: AsyncSession, session_id: str, user_id: str) -> LessonSession:
    """Get a lesson session with ownership check."""
    sid = UUID(session_id)
    session = await db.get(LessonSession, sid)
    if not session:
        raise NotFoundError("Lesson session not found")
    if str(session.user_id) != user_id:
        raise InvalidStateTransitionError("Not the owner of this session")
    return session


async def process_lesson_session(
    db: AsyncSession,
    session_id: str,
    user_id: str,
    submission_id: str,
) -> LessonSession:
    """Process lesson session through the full validation pipeline.

    This is the orchestration point that:
    1. Verifies the submission
    2. Calls mock AI analysis
    3. Runs linguistic validation
    4. Runs pedagogical validation
    5. Makes policy decision
    6. Updates session state accordingly
    """
    from app.modules.ai_gateway.services import analyze_submission
    from app.modules.audit.services import record_event
    from app.modules.linguistic_validation.services import validate_linguistic
    from app.modules.pedagogical_validation.services import validate_pedagogical
    from app.modules.policy_engine.services import make_decision

    sid = UUID(session_id)
    session = await db.get(LessonSession, sid)
    if not session:
        raise NotFoundError("Lesson session not found")
    if str(session.user_id) != user_id:
        raise InvalidStateTransitionError("Not the owner of this session")

    # Verify the submission belongs to this session
    sub_id = UUID(submission_id)
    sub_stmt = select(Submission).where(
        Submission.id == sub_id,
        Submission.lesson_session_id == sid,
        Submission.user_id == UUID(user_id),
    )
    sub_result = await db.execute(sub_stmt)
    submission = sub_result.scalar_one_or_none()
    if not submission:
        raise NotFoundError("Submission not found for this session")

    # Update submission status
    submission.status = "VALIDATED"

    # Transition to SUBMITTED then ANALYSIS_PENDING
    sm = _create_lesson_machine(session.status)
    try:
        sm.transition("submit")
        session.status = sm.current_state
        await db.flush()

        sm.transition("start_analysis")
        session.status = sm.current_state
        await db.flush()
    except ValueError as e:
        raise InvalidStateTransitionError(str(e))

    # Run mock AI analysis
    analysis_result = await analyze_submission(
        db, submission.id, user_id,
        submission.source_text,
        "A2",  # simplified — would come from profile
        "personal_narrative",
    )

    if not analysis_result.get("schema_valid", False):
        session.status = "FAILED"
        submission.status = "FAILED"
        await db.flush()
        await db.refresh(session)
        return session

    # Linguistic validation
    ling_result = await validate_linguistic(db, submission.id, analysis_result)
    submission.status = "ANALYSIS_PENDING"

    if not ling_result["passed"]:
        from app.models import ValidationResult

        vr = ValidationResult(
            submission_id=submission.id,
            validation_type="linguistic",
            passed=False,
            details=ling_result["details"],
        )
        db.add(vr)
        session.status = "REJECTED"
        submission.status = "REJECTED"
        await db.flush()
        await db.refresh(session)
        return session

    # Pedagogical validation
    ped_result = await validate_pedagogical(db, submission.id, analysis_result)

    if not ped_result["passed"]:
        from app.models import ValidationResult

        vr = ValidationResult(
            submission_id=submission.id,
            validation_type="pedagogical",
            passed=False,
            details=ped_result["details"],
        )
        db.add(vr)
        session.status = "REJECTED"
        submission.status = "REJECTED"
        await db.flush()
        await db.refresh(session)
        return session

    # Both validations passed — transition to ANALYSIS_VALIDATED
    try:
        sm = _create_lesson_machine(session.status)
        sm.transition("validate")
        session.status = sm.current_state
        await db.flush()
    except ValueError as e:
        raise InvalidStateTransitionError(str(e))

    # Policy decision
    decision = await make_decision(db, submission.id, user_id)

    # Save validation results
    from app.models import ValidationResult

    ling_vr = ValidationResult(
        submission_id=submission.id,
        validation_type="linguistic",
        passed=True,
        details=ling_result["details"],
    )
    ped_vr = ValidationResult(
        submission_id=submission.id,
        validation_type="pedagogical",
        passed=True,
        details=ped_result["details"],
    )
    db.add_all([ling_vr, ped_vr])

    # Apply decision
    if decision["decision"] == "COMPLETE":
        try:
            sm = _create_lesson_machine(session.status)
            sm.transition("complete")
            session.status = sm.current_state
            submission.status = "ACCEPTED"

            # Create mastery evidence
            from app.modules.mastery.services import create_evidence

            await create_evidence(
                db,
                user_id=str(session.user_id),
                submission_id=str(submission.id),
                lesson_session_id=str(session.id),
                skill_name="written_production",
                evidence_type="guided_use",
                evidence_data={
                    "analysis": analysis_result,
                    "decision": decision,
                },
            )
        except ValueError as e:
            raise InvalidStateTransitionError(str(e))
    elif decision["decision"] == "REJECT":
        session.status = "REJECTED"
        submission.status = "REJECTED"
    else:
        session.status = "FAILED"
        submission.status = "FAILED"

    await db.flush()
    await db.refresh(session)
    return session
