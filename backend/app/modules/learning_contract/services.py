"""Learning Entry Contract services — deterministic contract creation."""

from __future__ import annotations

import json
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import LearningEntryContract, SkillAssessment
from app.shared.exceptions.domain import NotFoundError


def _derive_contract_params(assessments: list[SkillAssessment]) -> dict:
    """Deterministically derive contract parameters from diagnostic assessments.

    Uses the lowest CEFR level across all dimensions as the baseline.
    """
    levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
    cefr_values = [a.cefr_level for a in assessments] if assessments else ["A1"]

    # Find lowest level
    lowest = min(cefr_values, key=lambda x: levels.index(x) if x in levels else 0)

    params = {
        "lesson_duration_minutes": 10,
        "active_vocabulary_budget": 3,
        "grammar_focus_count": 3,
        "max_primary_corrections": 5,
        "scaffolding_mode": "high",
        "lesson_complexity": "simple",
    }

    if lowest == "A2":
        params.update({
            "lesson_duration_minutes": 15,
            "active_vocabulary_budget": 5,
            "grammar_focus_count": 2,
            "max_primary_corrections": 3,
            "scaffolding_mode": "moderate",
            "lesson_complexity": "moderate",
        })
    elif lowest in ("B1", "B2"):
        params.update({
            "lesson_duration_minutes": 20,
            "active_vocabulary_budget": 8,
            "grammar_focus_count": 1,
            "max_primary_corrections": 2,
            "scaffolding_mode": "light",
            "lesson_complexity": "complex",
        })

    return params


async def create_contract(db: AsyncSession, user_id: str) -> LearningEntryContract:
    """Create a Learning Entry Contract based on diagnostic results."""
    uid = UUID(user_id)

    # Get latest diagnostic skill assessments
    stmt = (
        select(SkillAssessment)
        .join(SkillAssessment.session)
        .where(SkillAssessment.session.has(user_id=uid))
        .order_by(SkillAssessment.created_at.desc())
    )
    result = await db.execute(stmt)
    assessments = result.scalars().all()

    if not assessments:
        raise NotFoundError("No completed diagnostic found. Complete diagnostic first.")

    # Get learner profile for language info
    from app.models import LearnerProfile

    profile_stmt = select(LearnerProfile).where(LearnerProfile.user_id == uid)
    profile_result = await db.execute(profile_stmt)
    profile = profile_result.scalar_one_or_none()

    if not profile:
        raise NotFoundError("Learner profile not found.")

    params = _derive_contract_params(assessments)
    diagnostic_snapshot = {
        "assessments": [
            {
                "skill": a.skill_name,
                "cefr": a.cefr_level,
                "confidence": a.confidence,
            }
            for a in assessments
        ]
    }

    # Build contract
    contract = LearningEntryContract(
        user_id=uid,
        target_language=profile.target_language,
        support_language=profile.native_language,
        lesson_duration_minutes=params["lesson_duration_minutes"],
        active_vocabulary_budget=params["active_vocabulary_budget"],
        grammar_focus_count=params["grammar_focus_count"],
        max_primary_corrections=params["max_primary_corrections"],
        scaffolding_mode=params["scaffolding_mode"],
        lesson_complexity=params["lesson_complexity"],
        diagnostic_profile_snapshot=diagnostic_snapshot,
        version="1.0.0",
        status="active",
    )
    db.add(contract)
    await db.flush()
    await db.refresh(contract)
    return contract


async def get_current_contract(db: AsyncSession, user_id: str) -> LearningEntryContract:
    """Get the current active contract for a user."""
    uid = UUID(user_id)
    stmt = (
        select(LearningEntryContract)
        .where(
            LearningEntryContract.user_id == uid,
            LearningEntryContract.status == "active",
        )
        .order_by(LearningEntryContract.created_at.desc())
        .limit(1)
    )
    result = await db.execute(stmt)
    contract = result.scalar_one_or_none()
    if not contract:
        raise NotFoundError("No active learning contract found. Create one first.")
    return contract
