"""Learning Entry Contract services — deterministic contract creation."""

from __future__ import annotations

import json
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import LearningEntryContract, SkillAssessment
from app.shared.exceptions.domain import NotFoundError

from app.modules.diagnostics.scoring import (
    DIMENSION_REGISTRY,
    ITEM_SCORERS,
    EvidenceContribution,
    compute_dimension_results,
    compute_legacy_assessments,
    _calculate_cefr,
    _calculate_cefr_extended,
)


def _deduplicate_assessments(
    assessments: list[SkillAssessment],
) -> list[SkillAssessment]:
    """Keep only the latest assessment per skill_name.

    Assumes the input list is ordered newest-first (e.g. by
    created_at.desc()).  The first occurrence of each skill_name is
    kept — that is the most recent assessment for that dimension.
    """
    seen: set[str] = set()
    unique: list[SkillAssessment] = []
    for a in assessments:
        if a.skill_name not in seen:
            seen.add(a.skill_name)
            unique.append(a)
    return unique


def _derive_contract_params(assessments: list[SkillAssessment]) -> dict:
    """Deterministically derive contract parameters from diagnostic assessments.

    Uses the lowest CEFR level across measured dimensions as the baseline.
    Dimensions that are not_measured_yet are ignored.
    """
    levels = ["A1", "A2", "B1", "B2", "C1", "C2"]

    # Filter to only measured/estimated dimensions
    measured_cefr = []
    for a in assessments:
        status = a.evidence.get("status", "measured") if isinstance(a.evidence, dict) else "measured"
        if status in ("measured", "estimated") and a.cefr_level in levels:
            measured_cefr.append(a.cefr_level)

    cefr_values = measured_cefr if measured_cefr else (["A1"] if not assessments else [a.cefr_level for a in assessments if a.cefr_level in levels])

    if not cefr_values:
        cefr_values = ["A1"]

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


async def _build_multidimensional_snapshot(
    db: AsyncSession,
    assessments: list[SkillAssessment],
) -> dict:
    """Build a version 2.0.0 snapshot with a full dimension map.

    Re-runs the item scorers on the original diagnostic responses to
    capture cross-dimension contributions, then fills in
    not_measured_yet for any unmeasured dimension.
    """
    # Find the latest completed diagnostic session from assessments
    if not assessments:
        # No assessments — return all not_measured_yet
        dims = _build_empty_dimensions_map()
        return {"version": "2.0.0", "dimensions": dims, "assessments": []}

    # Get the session from the first (newest) assessment
    session_id = assessments[0].session_id

    # Fetch original diagnostic responses
    from app.models import DiagnosticResponse

    resp_stmt = (
        select(DiagnosticResponse)
        .where(DiagnosticResponse.session_id == session_id)
    )
    resp_result = await db.execute(resp_stmt)
    response_records = resp_result.scalars().all()

    # Re-run scorers on original responses
    all_contributions: list[EvidenceContribution] = []
    for r in response_records:
        scorer = ITEM_SCORERS.get(r.question_key)
        if scorer:
            all_contributions.extend(scorer(r.response_data))

    dimension_results = compute_dimension_results(all_contributions)
    legacy_assessments = compute_legacy_assessments(dimension_results)

    dims = {}
    for dim_name in DIMENSION_REGISTRY:
        r = dimension_results.get(dim_name)
        if r:
            dims[dim_name] = {
                "raw_score": r.raw_score,
                "estimated_level": r.estimated_level,
                "confidence": r.confidence,
                "evidence_count": r.evidence_count,
                "contradictions": r.contradictions,
                "needs_follow_up": r.needs_follow_up,
                "status": r.status,
                "deferred": r.deferred,
            }

    return {
        "version": "2.0.0",
        "dimensions": dims,
        "assessments": legacy_assessments,
    }


def _build_empty_dimensions_map() -> dict:
    """Return a dimensions dict with all dimensions as not_measured_yet."""
    dims = {}
    for dim_name, info in DIMENSION_REGISTRY.items():
        dims[dim_name] = {
            "raw_score": None,
            "estimated_level": "not_measured_yet",
            "confidence": 0.0,
            "evidence_count": 0,
            "contradictions": [],
            "needs_follow_up": not info["deferred"],
            "status": "not_measured_yet",
            "deferred": info["deferred"],
        }
    return dims


async def create_contract(db: AsyncSession, user_id: str) -> LearningEntryContract:
    """Create a Learning Entry Contract based on diagnostic results.

    Idempotent: if an active contract already exists for this user it is
    returned instead of creating a duplicate.  Skill assessments are
    deduplicated so each skill dimension appears exactly once (the latest
    assessment per skill_name is kept).
    """
    uid = UUID(user_id)

    # Idempotency: return existing active contract if one already exists
    existing_stmt = (
        select(LearningEntryContract)
        .where(
            LearningEntryContract.user_id == uid,
            LearningEntryContract.status == "active",
        )
        .order_by(LearningEntryContract.created_at.desc())
        .limit(1)
    )
    existing_result = await db.execute(existing_stmt)
    existing = existing_result.scalar_one_or_none()
    if existing:
        return existing

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

    # Deduplicate: keep only the latest assessment per skill_name
    unique_assessments = _deduplicate_assessments(assessments)

    # Get learner profile for language info
    from app.models import LearnerProfile

    profile_stmt = select(LearnerProfile).where(LearnerProfile.user_id == uid)
    profile_result = await db.execute(profile_stmt)
    profile = profile_result.scalar_one_or_none()

    if not profile:
        raise NotFoundError("Learner profile not found.")

    params = _derive_contract_params(unique_assessments)
    diagnostic_snapshot = await _build_multidimensional_snapshot(db, unique_assessments)

    # Build contract with version 2.0.0
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
        version="2.0.0",
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
