"""Mastery services — evidence creation and profile reading."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import MasteryEvidence, MasteryRecord
from app.shared.exceptions.domain import InvalidStateTransitionError, ValidationError

ALLOWED_EVIDENCE_TYPES = {"introduced", "recognized", "guided_use"}
FORBIDDEN_EVIDENCE_TYPES = {"independent_use", "interactive_use", "transferred", "retained"}


async def create_evidence(
    db: AsyncSession,
    user_id: str,
    submission_id: str,
    lesson_session_id: str,
    skill_name: str,
    evidence_type: str,
    evidence_data: dict | None = None,
) -> MasteryEvidence:
    """Create mastery evidence for a completed lesson.

    Only allowed evidence types: introduced, recognized, guided_use.
    """
    if evidence_type in FORBIDDEN_EVIDENCE_TYPES:
        raise ValidationError(
            f"Evidence type '{evidence_type}' is not yet available."
        )
    if evidence_type not in ALLOWED_EVIDENCE_TYPES:
        raise ValidationError(
            f"Invalid evidence type '{evidence_type}'. "
            f"Allowed: {', '.join(sorted(ALLOWED_EVIDENCE_TYPES))}"
        )

    uid = UUID(user_id)
    sid = UUID(submission_id)
    lsid = UUID(lesson_session_id)

    evidence = MasteryEvidence(
        user_id=uid,
        submission_id=sid,
        lesson_session_id=lsid,
        skill_name=skill_name,
        evidence_type=evidence_type,
        evidence_data=evidence_data or {},
        status="RECORDED",
    )
    db.add(evidence)

    # Create or update mastery record
    stmt = select(MasteryRecord).where(
        MasteryRecord.user_id == uid,
        MasteryRecord.skill_name == skill_name,
    )
    result = await db.execute(stmt)
    record = result.scalar_one_or_none()

    if not record:
        record = MasteryRecord(
            user_id=uid,
            skill_name=skill_name,
            cefr_level="A1",
            current_state=evidence_type,
        )
        db.add(record)
    else:
        # Only upgrade state, never downgrade
        state_priority = {"introduced": 0, "recognized": 1, "guided_use": 2}
        current_prio = state_priority.get(record.current_state, -1)
        new_prio = state_priority.get(evidence_type, -1)
        if new_prio > current_prio:
            record.current_state = evidence_type

    await db.flush()
    await db.refresh(evidence)
    return evidence


async def get_mastery_profile(db: AsyncSession, user_id: str) -> list[dict]:
    """Get mastery profile for a user."""
    uid = UUID(user_id)

    stmt = select(MasteryRecord).where(MasteryRecord.user_id == uid)
    result = await db.execute(stmt)
    records = result.scalars().all()

    evidence_stmt = (
        select(MasteryEvidence)
        .where(MasteryEvidence.user_id == uid)
        .order_by(MasteryEvidence.created_at.desc())
        .limit(50)
    )
    evidence_result = await db.execute(evidence_stmt)
    evidence_list = evidence_result.scalars().all()

    return {
        "records": [
            {
                "skill": r.skill_name,
                "cefr_level": r.cefr_level,
                "current_state": r.current_state,
            }
            for r in records
        ],
        "recent_evidence": [
            {
                "id": str(e.id),
                "skill": e.skill_name,
                "type": e.evidence_type,
                "status": e.status,
                "created_at": e.created_at.isoformat(),
            }
            for e in evidence_list
        ],
    }
