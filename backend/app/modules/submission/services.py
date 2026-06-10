"""Submission services — text reception, validation, and storage."""

from __future__ import annotations

import unicodedata
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import LessonSession, Submission
from app.shared.exceptions.domain import ConflictError, InvalidStateTransitionError, NotFoundError, ValidationError


def _normalize_text(text: str) -> str:
    """Normalize text: trim whitespace and normalize unicode."""
    normalized = unicodedata.normalize("NFC", text.strip())
    return normalized


async def create_submission(
    db: AsyncSession,
    user_id: str,
    lesson_session_id: str,
    source_text: str,
    idempotency_key: str | None = None,
) -> Submission:
    """Create a new submission with validation and deduplication."""
    uid = UUID(user_id)
    ls_id = UUID(lesson_session_id)

    # Validate minimum length
    if len(source_text.strip()) < 10:
        raise ValidationError("Text must be at least 10 characters long.")

    # Check idempotency
    if idempotency_key:
        stmt = select(Submission).where(
            Submission.idempotency_key == idempotency_key,
            Submission.user_id == uid,
        )
        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()
        if existing:
            return existing

    # Verify lesson session exists and is in valid state
    session = await db.get(LessonSession, ls_id)
    if not session:
        raise NotFoundError("Lesson session not found")
    if str(session.user_id) != user_id:
        raise InvalidStateTransitionError("Not the owner of this session")
    if session.status not in ("ACTIVE", "CREATED"):
        raise InvalidStateTransitionError(
            f"Cannot submit to session in state: {session.status}"
        )

    # Get lesson definition ID from session
    lesson_def_id = session.lesson_definition_id

    # Normalize text
    normalized = _normalize_text(source_text)

    # Create submission
    submission = Submission(
        user_id=uid,
        lesson_session_id=ls_id,
        lesson_definition_id=lesson_def_id,
        status="RECEIVED",
        source_text=source_text,
        normalized_text=normalized,
        idempotency_key=idempotency_key,
    )
    db.add(submission)

    # Update session state
    session.status = "SUBMITTED"
    session.current_attempt += 1

    await db.flush()
    await db.refresh(submission)
    return submission


async def get_submission(db: AsyncSession, submission_id: str, user_id: str) -> Submission:
    """Get a submission with ownership check."""
    sid = UUID(submission_id)
    submission = await db.get(Submission, sid)
    if not submission:
        raise NotFoundError("Submission not found")
    if str(submission.user_id) != user_id:
        raise InvalidStateTransitionError("Not the owner of this submission")
    return submission
