"""Diagnostics services with state machine and deterministic scoring."""

from __future__ import annotations

import uuid
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DiagnosticResponse, DiagnosticSession, SkillAssessment
from app.shared.exceptions.domain import InvalidStateTransitionError, NotFoundError
from app.shared.state_machine import StateMachine

DIAGNOSTIC_STATES = {"CREATED", "IN_PROGRESS", "COMPLETED", "FAILED"}

DIAGNOSTIC_STEPS = [
    {"key": "grammar_recognition", "prompt": "Select the correct sentence."},
    {"key": "active_vocabulary", "prompt": "Choose the correct word for the picture."},
    {"key": "written_production", "prompt": "Write a short sentence about what you see."},
    {"key": "narrative_coherence", "prompt": "Arrange these sentences in the correct order."},
]


def _create_machine(initial: str = "CREATED") -> StateMachine:
    sm = StateMachine(initial, DIAGNOSTIC_STATES)
    sm.add_transition("CREATED", "start", "IN_PROGRESS")
    sm.add_transition("IN_PROGRESS", "complete", "COMPLETED")
    sm.add_transition("IN_PROGRESS", "fail", "FAILED")
    sm.add_transition("CREATED", "fail", "FAILED")
    return sm


def _calculate_cefr(score: float) -> str:
    """Convert a numeric score (0-100) to a CEFR level."""
    if score >= 85:
        return "B1"
    if score >= 65:
        return "A2"
    return "A1"


def _assess_responses(responses: list[dict]) -> dict[str, dict]:
    """Deterministically assess each skill dimension based on responses."""
    assessments = {}

    for response in responses:
        key = response.get("question_key", "")
        data = response.get("response_data", {})

        if key == "grammar_recognition":
            correct = data.get("is_correct", False)
            score = 80.0 if correct else 45.0
            assessments[key] = {
                "score": score,
                "cefr": _calculate_cefr(score),
                "confidence": 0.75,
            }

        elif key == "active_vocabulary":
            correct_count = data.get("correct_count", 0)
            total_words = data.get("total_words", 5)
            ratio = correct_count / max(total_words, 1)
            score = ratio * 100
            assessments[key] = {
                "score": score,
                "cefr": _calculate_cefr(score),
                "confidence": 0.8,
            }

        elif key == "written_production":
            word_count = data.get("word_count", 0)
            has_structure = data.get("has_structure", False)
            score = 50.0
            if word_count >= 20:
                score += 20.0
            if has_structure:
                score += 15.0
            assessments[key] = {
                "score": min(score, 100),
                "cefr": _calculate_cefr(score),
                "confidence": 0.65,
            }

        elif key == "narrative_coherence":
            correct_order = data.get("correct_order", False)
            score = 85.0 if correct_order else 40.0
            assessments[key] = {
                "score": score,
                "cefr": _calculate_cefr(score),
                "confidence": 0.7,
            }

    return assessments


async def create_session(db: AsyncSession, user_id: str) -> DiagnosticSession:
    """Create a new diagnostic session."""
    from app.modules.audit.services import record_event

    uid = UUID(user_id)
    session = DiagnosticSession(
        user_id=uid,
        status="CREATED",
        current_step=0,
    )
    db.add(session)
    await db.flush()
    await db.refresh(session)

    # Transition to IN_PROGRESS
    sm = _create_machine("CREATED")
    sm.transition("start")
    session.status = sm.current_state
    await db.flush()

    await record_event(
        db,
        event_type="DIAGNOSTIC_STARTED",
        user_id=user_id,
        module="diagnostics",
        entity_type="diagnostic_session",
        entity_id=str(session.id),
    )

    await db.refresh(session)
    return session


async def submit_response(
    db: AsyncSession,
    session_id: str,
    user_id: str,
    question_key: str,
    response_data: dict,
) -> DiagnosticSession:
    """Submit a response for a diagnostic step."""
    sid = UUID(session_id)
    session = await db.get(DiagnosticSession, sid)
    if not session:
        raise NotFoundError("Diagnostic session not found")

    if str(session.user_id) != user_id:
        raise InvalidStateTransitionError("Not the owner of this session")

    if session.status != "IN_PROGRESS":
        raise InvalidStateTransitionError(
            f"Cannot submit response in state: {session.status}"
        )

    response = DiagnosticResponse(
        session_id=sid,
        question_key=question_key,
        response_data=response_data,
    )
    db.add(response)

    steps = len(DIAGNOSTIC_STEPS)
    current_step = session.current_step
    step_index = next(
        (i for i, s in enumerate(DIAGNOSTIC_STEPS) if s["key"] == question_key),
        current_step,
    )
    session.current_step = min(step_index + 1, steps)

    await db.flush()
    await db.refresh(session)
    return session


async def complete_session(
    db: AsyncSession,
    session_id: str,
    user_id: str,
) -> DiagnosticSession:
    """Complete a diagnostic session and compute assessments."""
    from app.modules.audit.services import record_event

    sid = UUID(session_id)
    session = await db.get(DiagnosticSession, sid)
    if not session:
        raise NotFoundError("Diagnostic session not found")

    if str(session.user_id) != user_id:
        raise InvalidStateTransitionError("Not the owner of this session")

    if session.status != "IN_PROGRESS":
        raise InvalidStateTransitionError(
            f"Cannot complete session in state: {session.status}"
        )

    # Collect all responses
    stmt = select(DiagnosticResponse).where(DiagnosticResponse.session_id == sid)
    result = await db.execute(stmt)
    responses = result.scalars().all()

    response_list = [
        {
            "question_key": r.question_key,
            "response_data": r.response_data,
        }
        for r in responses
    ]

    # Assess each dimension
    assessments = _assess_responses(response_list)

    # Save skill assessments
    for skill_key, assessment in assessments.items():
        skill_assessment = SkillAssessment(
            session_id=sid,
            skill_name=skill_key,
            cefr_level=assessment["cefr"],
            confidence=assessment["confidence"],
            evidence={"score": assessment["score"]},
        )
        db.add(skill_assessment)

    # Transition to COMPLETED
    sm = _create_machine("IN_PROGRESS")
    sm.transition("complete")
    session.status = sm.current_state
    await db.flush()

    await record_event(
        db,
        event_type="DIAGNOSTIC_COMPLETED",
        user_id=user_id,
        module="diagnostics",
        entity_type="diagnostic_session",
        entity_id=session_id,
        data={"overall_level": assessments.get(list(assessments.keys())[0], {}).get("cefr", "A1") if assessments else "A1"},
    )

    await db.refresh(session)
    return session


async def get_session(db: AsyncSession, session_id: str, user_id: str) -> DiagnosticSession:
    """Get a diagnostic session."""
    sid = UUID(session_id)
    session = await db.get(DiagnosticSession, sid)
    if not session:
        raise NotFoundError("Diagnostic session not found")
    if str(session.user_id) != user_id:
        raise InvalidStateTransitionError("Not the owner of this session")
    return session
