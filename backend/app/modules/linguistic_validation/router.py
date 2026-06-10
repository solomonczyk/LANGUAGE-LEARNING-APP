"""Linguistic validation API router."""

from __future__ import annotations

from fastapi import APIRouter

from app.dependencies import CurrentUserId, DbSession
from app.modules.linguistic_validation.services import validate_linguistic_standalone

router = APIRouter(prefix="/linguistic-validation", tags=["linguistic-validation"])


@router.post("/validate")
async def validate_analysis(
    body: dict,
    user_id: CurrentUserId,
    db: DbSession,
):
    """Validate analysis output linguistically."""
    result = await validate_linguistic_standalone(body.get("analysis", {}))
    return result
