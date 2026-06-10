"""AI Gateway API router."""

from __future__ import annotations

from fastapi import APIRouter

from app.config import settings
from app.dependencies import CurrentUserId, DbSession
from app.modules.ai_gateway.schemas import AnalyzeRequest
from app.modules.ai_gateway.services import analyze_submission

router = APIRouter(prefix="/ai-gateway", tags=["ai-gateway"])


@router.post("/analyze")
async def analyze_text(body: AnalyzeRequest, user_id: CurrentUserId, db: DbSession):
    """Run mock AI analysis on learner text."""
    result = await analyze_submission(
        db=db,
        submission_id=body.submission_id,
        user_id=user_id,
        text=body.text,
        learner_level=body.learner_level,
        lesson_type=body.lesson_type,
    )
    return result


@router.get("/status")
async def gateway_status():
    """Get AI Gateway status."""
    return {
        "status": "ready",
        "mock_mode": settings.mock_ai_enabled,
        "fixture_mode": settings.mock_ai_fixture_mode,
    }
