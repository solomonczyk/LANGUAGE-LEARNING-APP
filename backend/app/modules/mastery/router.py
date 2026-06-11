"""Mastery module API router."""

from __future__ import annotations

from fastapi import APIRouter

from app.dependencies import CurrentUserId, DbSession
from app.modules.mastery.schemas import CreateEvidenceRequest, EvidenceResponse, MasteryProfileResponse
from app.modules.mastery.services import create_evidence, get_mastery_profile

router = APIRouter(prefix="/mastery", tags=["mastery"])


@router.post("/evidence", response_model=EvidenceResponse)
async def create_mastery_evidence(
    body: CreateEvidenceRequest,
    user_id: CurrentUserId,
    db: DbSession,
):
    """Create mastery evidence for a completed lesson."""
    evidence = await create_evidence(
        db=db,
        user_id=user_id,
        submission_id=body.submission_id,
        lesson_session_id=body.lesson_session_id,
        skill_name=body.skill_name,
        evidence_type=body.evidence_type,
    )
    await db.commit()
    return EvidenceResponse(
        id=str(evidence.id),
        skill_name=evidence.skill_name,
        evidence_type=evidence.evidence_type,
        status=evidence.status,
    )


@router.get("/profile", response_model=MasteryProfileResponse)
async def read_mastery_profile(
    user_id: CurrentUserId,
    db: DbSession,
):
    """Get user's mastery profile."""
    profile = await get_mastery_profile(db, user_id)
    return MasteryProfileResponse(**profile)
