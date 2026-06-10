"""Policy engine API router."""

from __future__ import annotations

from fastapi import APIRouter

from app.dependencies import CurrentUserId, DbSession
from app.modules.policy_engine.schemas import DecisionRequest
from app.modules.policy_engine.services import make_decision

router = APIRouter(prefix="/policy-engine", tags=["policy-engine"])


@router.post("/decide")
async def decide(body: DecisionRequest, user_id: CurrentUserId, db: DbSession):
    """Make final decision on lesson processing."""
    decision = await make_decision(
        db=db,
        submission_id=body.submission_id,
        user_id=body.user_id,
    )
    return decision
