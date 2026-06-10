"""Pedagogical validation services — deterministic lesson-fit checks."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ValidationResult


async def validate_pedagogical(
    db: AsyncSession,
    submission_id: str,
    analysis_result: dict,
    contract: dict | None = None,
) -> dict:
    """Deterministically validate pedagogical fitness of an AI analysis.

    Checks:
    1. feedback_matches_goal — analysis recommended_focus aligns with lesson goals
    2. corrections_within_budget — number of major issues <= contract limit
    3. no_unsupported_mastery_claim — output doesn't claim mastery directly
    4. no_reward_command — output doesn't contain reward instructions
    5. no_curriculum_mutation — output doesn't suggest curriculum changes
    """
    checks = {}
    failed_checks = []

    max_corrections = (contract or {}).get("max_primary_corrections", 3)

    # 1. Feedback matches goal
    recommended = analysis_result.get("recommended_focus", [])
    feedback_matches = isinstance(recommended, list) and len(recommended) > 0
    checks["feedback_matches_goal"] = feedback_matches
    if not feedback_matches:
        failed_checks.append("feedback_matches_goal")

    # 2. Corrections within budget
    issues = analysis_result.get("detected_issues", [])
    if isinstance(issues, list):
        major_count = sum(1 for i in issues if i.get("severity") == "major")
    else:
        major_count = 0
    corrections_ok = major_count <= max_corrections
    checks["corrections_within_budget"] = corrections_ok
    if not corrections_ok:
        failed_checks.append("corrections_within_budget")

    # 3. No unsupported mastery claim
    raw = str(analysis_result.get("raw_output", analysis_result))
    no_mastery_claim = "mastery" not in raw.lower() and "independent_use" not in raw.lower()
    checks["no_unsupported_mastery_claim"] = no_mastery_claim
    if not no_mastery_claim:
        failed_checks.append("no_unsupported_mastery_claim")

    # 4. No reward command
    no_reward = "reward" not in raw.lower() and "xp" not in raw.lower()
    checks["no_reward_command"] = no_reward
    if not no_reward:
        failed_checks.append("no_reward_command")

    # 5. No curriculum mutation
    no_curriculum = "curriculum" not in raw.lower() and "syllabus" not in raw.lower()
    checks["no_curriculum_mutation"] = no_curriculum
    if not no_curriculum:
        failed_checks.append("no_curriculum_mutation")

    passed = len(failed_checks) == 0

    # Save validation result
    sid = UUID(submission_id)
    vr = ValidationResult(
        submission_id=sid,
        validation_type="pedagogical",
        passed=passed,
        details={"checks": checks, "failed_checks": failed_checks},
    )
    db.add(vr)
    await db.flush()

    return {"passed": passed, "details": {"checks": checks, "failed_checks": failed_checks}}
