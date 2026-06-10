"""Lesson engine API router."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Header

from app.dependencies import CurrentUserId, DbSession
from app.modules.lesson_engine.schemas import (
    CreateSessionRequest,
    ProcessResponse,
    SessionResponse,
    SubmitTextRequest,
    SubmitTextResponse,
)
from app.modules.lesson_engine.services import (
    create_session,
    get_session,
    process_lesson_session,
)

router = APIRouter(prefix="/lesson-sessions", tags=["lesson-engine"])


@router.post("", response_model=SessionResponse)
async def start_lesson_session(
    body: CreateSessionRequest,
    user_id: CurrentUserId,
    db: DbSession,
    idempotency_key: str | None = Header(default=None, alias="X-Idempotency-Key"),
):
    """Start a new lesson session."""
    session = await create_session(db, user_id, body.lesson_definition_id)
    return SessionResponse(
        session_id=str(session.id),
        lesson_definition_id=str(session.lesson_definition_id),
        status=session.status,
        current_attempt=session.current_attempt,
        created_at=session.created_at.isoformat(),
    )


@router.get("/{session_id}", response_model=SessionResponse)
async def read_lesson_session(
    session_id: str,
    user_id: CurrentUserId,
    db: DbSession,
):
    """Get lesson session state."""
    session = await get_session(db, session_id, user_id)
    return SessionResponse(
        session_id=str(session.id),
        lesson_definition_id=str(session.lesson_definition_id),
        status=session.status,
        current_attempt=session.current_attempt,
        created_at=session.created_at.isoformat(),
    )


@router.post("/{session_id}/submissions", response_model=SubmitTextResponse)
async def submit_learner_text(
    session_id: str,
    body: SubmitTextRequest,
    user_id: CurrentUserId,
    db: DbSession,
    idempotency_key: str | None = Header(default=None, alias="X-Idempotency-Key"),
):
    """Submit learner text for a lesson session."""
    from app.modules.submission.services import create_submission

    submission = await create_submission(
        db=db,
        user_id=user_id,
        lesson_session_id=session_id,
        source_text=body.text,
        idempotency_key=idempotency_key,
    )

    return SubmitTextResponse(
        submission_id=str(submission.id),
        session_id=session_id,
        status=submission.status,
        text_preview=body.text[:50] + ("..." if len(body.text) > 50 else ""),
    )


@router.post("/{session_id}/process", response_model=ProcessResponse)
async def process_lesson(
    session_id: str,
    user_id: CurrentUserId,
    db: DbSession,
):
    """Process lesson through full validation pipeline."""
    # Find the latest submission for this session
    from sqlalchemy import select

    from app.models import Submission as SubmissionModel

    stmt = (
        select(SubmissionModel)
        .where(
            SubmissionModel.lesson_session_id == UUID(session_id),
            SubmissionModel.user_id == UUID(user_id),
        )
        .order_by(SubmissionModel.created_at.desc())
        .limit(1)
    )
    result = await db.execute(stmt)
    submission = result.scalar_one_or_none()

    if not submission:
        from app.shared.exceptions.domain import NotFoundError as NFE

        raise NFE("No submission found for this session. Submit text first.")

    session = await process_lesson_session(
        db, session_id, user_id, str(submission.id)
    )

    # Fetch validation results for response
    from app.models import ValidationResult

    v_stmt = select(ValidationResult).where(
        ValidationResult.submission_id == submission.id
    )
    v_result = await db.execute(v_stmt)
    validations = v_result.scalars().all()

    return ProcessResponse(
        session_id=str(session.id),
        status=session.status,
        decision="COMPLETE" if session.status == "COMPLETED" else None,
        corrections=[],
        strengths=[],
        validation_results={
            v.validation_type: {"passed": v.passed, "details": v.details}
            for v in validations
        },
    )
