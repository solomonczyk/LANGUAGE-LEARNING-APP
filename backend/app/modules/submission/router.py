"""Submission module API router."""

from __future__ import annotations

from fastapi import APIRouter, Header

from app.dependencies import CurrentUserId, DbSession
from app.modules.submission.schemas import SubmissionResponse
from app.modules.submission.services import create_submission, get_submission

router = APIRouter(prefix="/submissions", tags=["submission"])


@router.post("", response_model=SubmissionResponse)
async def submit_text(
    body: dict,
    user_id: CurrentUserId,
    db: DbSession,
    idempotency_key: str | None = Header(default=None, alias="X-Idempotency-Key"),
):
    """Submit learner text."""
    from app.shared.exceptions.domain import ValidationError

    text = body.get("text", "")
    lesson_session_id = body.get("lesson_session_id", "")

    if not text:
        raise ValidationError("Text is required.")
    if not lesson_session_id:
        raise ValidationError("lesson_session_id is required.")

    submission = await create_submission(
        db=db,
        user_id=user_id,
        lesson_session_id=lesson_session_id,
        source_text=text,
        idempotency_key=idempotency_key,
    )

    return SubmissionResponse(
        id=str(submission.id),
        user_id=str(submission.user_id),
        lesson_session_id=str(submission.lesson_session_id),
        lesson_definition_id=str(submission.lesson_definition_id),
        status=submission.status,
        source_text=submission.source_text,
        text_preview=submission.source_text[:100],
        created_at=submission.created_at.isoformat(),
    )


@router.get("/{submission_id}", response_model=SubmissionResponse)
async def read_submission(
    submission_id: str,
    user_id: CurrentUserId,
    db: DbSession,
):
    """Get a submission."""
    submission = await get_submission(db, submission_id, user_id)
    return SubmissionResponse(
        id=str(submission.id),
        user_id=str(submission.user_id),
        lesson_session_id=str(submission.lesson_session_id),
        lesson_definition_id=str(submission.lesson_definition_id),
        status=submission.status,
        source_text=submission.source_text,
        text_preview=submission.source_text[:100],
        created_at=submission.created_at.isoformat(),
    )
