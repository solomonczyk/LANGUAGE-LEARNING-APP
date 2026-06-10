"""Pedagogical validation API router."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter

from app.dependencies import CurrentUserId, DbSession
from app.modules.pedagogical_validation.services import validate_pedagogical

router = APIRouter(prefix="/pedagogical-validation", tags=["pedagogical-validation"])


@router.post("/validate")
async def validate_pedagogical_endpoint(
    body: dict,
    user_id: CurrentUserId,
    db: DbSession,
):
    """Validate analysis output pedagogically."""
    from app.models import Submission

    submission_id = body.get("submission_id", "")
    analysis = body.get("analysis", {})
    contract = body.get("contract", {})

    result = await validate_pedagogical(
        db=db,
        submission_id=submission_id,
        analysis_result=analysis,
        contract=contract,
    )
    return result
