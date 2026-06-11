"""Diagnostics module API router."""

from __future__ import annotations

from fastapi import APIRouter

from app.dependencies import CurrentUserId, DbSession
from app.modules.diagnostics.schemas import (
    CompleteSessionResponse,
    CreateSessionResponse,
    SessionStatusResponse,
    SubmitResponseRequest,
    SubmitResponseResponse,
)
from app.modules.diagnostics.services import (
    DIAGNOSTIC_STEPS,
    complete_session,
    create_session,
    get_session,
    submit_response,
)

router = APIRouter(prefix="/diagnostics", tags=["diagnostics"])


@router.post("/sessions", response_model=CreateSessionResponse)
async def create_diagnostic_session(user_id: CurrentUserId, db: DbSession):
    """Create a new diagnostic session."""
    session = await create_session(db, user_id)
    await db.commit()
    return CreateSessionResponse(
        session_id=str(session.id),
        status=session.status,
        current_step=session.current_step,
        total_steps=len(DIAGNOSTIC_STEPS),
    )


@router.post("/sessions/{session_id}/responses", response_model=SubmitResponseResponse)
async def submit_diagnostic_response(
    session_id: str,
    body: SubmitResponseRequest,
    user_id: CurrentUserId,
    db: DbSession,
):
    """Submit a diagnostic response."""
    session = await submit_response(
        db, session_id, user_id, body.question_key, body.response_data
    )
    await db.commit()
    return SubmitResponseResponse(
        session_id=str(session.id),
        question_key=body.question_key,
        step=session.current_step,
        total_steps=len(DIAGNOSTIC_STEPS),
        status=session.status,
    )


@router.post("/sessions/{session_id}/complete", response_model=CompleteSessionResponse)
async def complete_diagnostic_session(
    session_id: str,
    user_id: CurrentUserId,
    db: DbSession,
):
    """Complete a diagnostic session and produce multidimensional results."""
    session = await complete_session(db, session_id, user_id)
    await db.commit()

    from sqlalchemy import select

    from app.models import SkillAssessment
    from app.modules.diagnostics.scoring import (
        compute_dimension_results,
        EvidenceContribution,
        ITEM_SCORERS,
        DIMENSION_REGISTRY,
        _calculate_cefr,
    )

    # Fetch all responses to rebuild dimension_results
    from app.models import DiagnosticResponse

    resp_stmt = select(DiagnosticResponse).where(DiagnosticResponse.session_id == session.id)
    resp_result = await db.execute(resp_stmt)
    response_records = resp_result.scalars().all()

    all_contributions: list[EvidenceContribution] = []
    for r in response_records:
        scorer = ITEM_SCORERS.get(r.question_key)
        if scorer:
            all_contributions.extend(scorer(r.response_data))

    dimension_results = compute_dimension_results(all_contributions)

    # Also fetch SkillAssessments for backward compat
    stmt = select(SkillAssessment).where(SkillAssessment.session_id == session.id)
    result = await db.execute(stmt)
    assessments = result.scalars().all()

    return CompleteSessionResponse(
        session_id=str(session.id),
        status=session.status,
        assessments=[
            {
                "skill": a.skill_name,
                "cefr": a.cefr_level,
                "confidence": a.confidence,
                "status": a.evidence.get("status", "measured"),
                "needs_follow_up": a.evidence.get("needs_follow_up", False),
            }
            for a in assessments
        ],
        dimension_results={
            dim: {
                "raw_score": r.raw_score,
                "estimated_level": r.estimated_level,
                "confidence": r.confidence,
                "evidence_count": r.evidence_count,
                "contradictions": r.contradictions,
                "needs_follow_up": r.needs_follow_up,
                "status": r.status,
                "deferred": r.deferred,
            }
            for dim, r in dimension_results.items()
        },
    )


@router.get("/sessions/{session_id}", response_model=SessionStatusResponse)
async def get_diagnostic_session(
    session_id: str,
    user_id: CurrentUserId,
    db: DbSession,
):
    """Get diagnostic session status."""
    session = await get_session(db, session_id, user_id)

    from sqlalchemy import select

    from app.models import SkillAssessment

    stmt = select(SkillAssessment).where(SkillAssessment.session_id == session.id)
    result = await db.execute(stmt)
    assessments = result.scalars().all()

    return SessionStatusResponse(
        session_id=str(session.id),
        status=session.status,
        current_step=session.current_step,
        total_steps=len(DIAGNOSTIC_STEPS),
        assessments=[
            {"skill": a.skill_name, "cefr": a.cefr_level, "confidence": a.confidence}
            for a in assessments
        ]
        if assessments
        else None,
    )
