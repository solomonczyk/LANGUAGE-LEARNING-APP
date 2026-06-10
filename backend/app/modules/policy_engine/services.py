"""Policy engine services — final authoritative decision."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Submission, ValidationResult


async def make_decision(
    db: AsyncSession,
    submission_id: str,
    user_id: str,
) -> dict:
    """Make final authoritative decision on lesson processing.

    Input: submission with validation results
    Logic:
    - Both linguistic and pedagogical pass → COMPLETE
    - Linguistic fails → RETRY (if attempts remain)
    - Pedagogical fails → REJECT (needs contract adjustment)
    - Both fail → FAIL
    """
    sid = UUID(submission_id)

    # Get the submission
    submission = await db.get(Submission, sid)
    if not submission:
        return {"decision": "FAIL", "reason": "Submission not found.", "allow_retry": False}

    # Get validation results
    v_stmt = select(ValidationResult).where(ValidationResult.submission_id == sid)
    v_result = await db.execute(v_stmt)
    validations = v_result.scalars().all()

    linguistic_passed = any(
        v.passed for v in validations if v.validation_type == "linguistic"
    )
    pedagogical_passed = any(
        v.passed for v in validations if v.validation_type == "pedagogical"
    )

    if linguistic_passed and pedagogical_passed:
        return {
            "decision": "COMPLETE",
            "reason": "All validations passed. Lesson completion allowed.",
            "allow_retry": False,
        }
    elif not linguistic_passed:
        # Check if attempts remain
        max_attempts = 3
        if submission.lesson_session and submission.lesson_session.current_attempt < max_attempts:
            return {
                "decision": "RETRY",
                "reason": "Linguistic validation failed. Learner can retry.",
                "allow_retry": True,
            }
        return {
            "decision": "REJECT",
            "reason": "Linguistic validation failed and no retries remain.",
            "allow_retry": False,
        }
    elif not pedagogical_passed:
        return {
            "decision": "REJECT",
            "reason": "Pedagogical validation failed. Contract adjustment needed.",
            "allow_retry": False,
        }
    else:
        return {
            "decision": "FAIL",
            "reason": "All validations failed.",
            "allow_retry": False,
        }
