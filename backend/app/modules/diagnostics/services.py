"""Diagnostics services with state machine and multidimensional scoring."""

from __future__ import annotations

import uuid
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DiagnosticResponse, DiagnosticSession, SkillAssessment
from app.shared.exceptions.domain import InvalidStateTransitionError, NotFoundError
from app.shared.state_machine import StateMachine

from app.modules.diagnostics.scoring import (
    ITEM_CATALOG,
    ITEM_SCORERS,
    compute_dimension_results,
    compute_legacy_assessments,
    EvidenceContribution,
    _calculate_cefr,
    _calculate_cefr_extended,
)

DIAGNOSTIC_STATES = {"CREATED", "IN_PROGRESS", "COMPLETED", "FAILED"}

# Expose for router backward compat
DIAGNOSTIC_STEPS = ITEM_CATALOG


def _create_machine(initial: str = "CREATED") -> StateMachine:
    sm = StateMachine(initial, DIAGNOSTIC_STATES)
    sm.add_transition("CREATED", "start", "IN_PROGRESS")
    sm.add_transition("IN_PROGRESS", "complete", "COMPLETED")
    sm.add_transition("IN_PROGRESS", "fail", "FAILED")
    sm.add_transition("CREATED", "fail", "FAILED")
    return sm


def _assess_responses(responses: list[dict]) -> dict[str, dict]:
    """Deterministically assess each skill dimension based on responses.

    Uses the multidimensional scoring engine from scoring.py.
    Returns the legacy flat dict format for backward compatibility.
    """
    # Collect evidence contributions from all responses
    all_contributions: list[EvidenceContribution] = []
    for response in responses:
        key = response.get("question_key", "")
        data = response.get("response_data", {})
        scorer = ITEM_SCORERS.get(key)
        if scorer:
            all_contributions.extend(scorer(data))

    # Compute full dimension profile
    dimension_results = compute_dimension_results(all_contributions)

    # Build backward-compatible flat dict
    assessments = {}
    for dim_name, result in dimension_results.items():
        if result.status in ("measured", "estimated") and result.raw_score is not None:
            assessments[dim_name] = {
                "score": result.raw_score,
                "cefr": _calculate_cefr(result.raw_score),
                "confidence": result.confidence,
            }

    return assessments


async def create_session(db: AsyncSession, user_id: str) -> DiagnosticSession:
    """Create a new diagnostic session."""
    from app.modules.audit.services import record_event

    uid = UUID(user_id)
    session = DiagnosticSession(
        user_id=uid,
        status="CREATED",
        current_step=0,
    )
    db.add(session)
    await db.flush()
    await db.refresh(session)

    # Transition to IN_PROGRESS
    sm = _create_machine("CREATED")
    sm.transition("start")
    session.status = sm.current_state
    await db.flush()

    await record_event(
        db,
        event_type="DIAGNOSTIC_STARTED",
        user_id=user_id,
        module="diagnostics",
        entity_type="diagnostic_session",
        entity_id=str(session.id),
    )

    await db.refresh(session)
    return session


async def submit_response(
    db: AsyncSession,
    session_id: str,
    user_id: str,
    question_key: str,
    response_data: dict,
) -> DiagnosticSession:
    """Submit a response for a diagnostic step."""
    sid = UUID(session_id)
    session = await db.get(DiagnosticSession, sid)
    if not session:
        raise NotFoundError("Diagnostic session not found")

    if str(session.user_id) != user_id:
        raise InvalidStateTransitionError("Not the owner of this session")

    if session.status != "IN_PROGRESS":
        raise InvalidStateTransitionError(
            f"Cannot submit response in state: {session.status}"
        )

    response = DiagnosticResponse(
        session_id=sid,
        question_key=question_key,
        response_data=response_data,
    )
    db.add(response)

    steps = len(DIAGNOSTIC_STEPS)
    current_step = session.current_step
    step_index = next(
        (i for i, s in enumerate(DIAGNOSTIC_STEPS) if s["key"] == question_key),
        current_step,
    )
    session.current_step = min(step_index + 1, steps)

    await db.flush()
    await db.refresh(session)
    return session


async def complete_session(
    db: AsyncSession,
    session_id: str,
    user_id: str,
) -> DiagnosticSession:
    """Complete a diagnostic session and compute assessments."""
    from app.modules.audit.services import record_event

    sid = UUID(session_id)
    session = await db.get(DiagnosticSession, sid)
    if not session:
        raise NotFoundError("Diagnostic session not found")

    if str(session.user_id) != user_id:
        raise InvalidStateTransitionError("Not the owner of this session")

    if session.status != "IN_PROGRESS":
        raise InvalidStateTransitionError(
            f"Cannot complete session in state: {session.status}"
        )

    # Collect all responses
    stmt = select(DiagnosticResponse).where(DiagnosticResponse.session_id == sid)
    result = await db.execute(stmt)
    responses = result.scalars().all()

    response_list = [
        {
            "question_key": r.question_key,
            "response_data": r.response_data,
        }
        for r in responses
    ]

    # Assess each dimension using the multidimensional scoring engine
    all_contributions: list[EvidenceContribution] = []
    for resp in response_list:
        key = resp.get("question_key", "")
        scorer = ITEM_SCORERS.get(key)
        if scorer:
            all_contributions.extend(scorer(resp.get("response_data", {})))

    dimension_results = compute_dimension_results(all_contributions)

    # Save SkillAssessment rows for all measured/estimated dimensions (backward compat)
    for dim_name, result_dr in dimension_results.items():
        if result_dr.status in ("measured", "estimated") and result_dr.raw_score is not None:
            skill_assessment = SkillAssessment(
                session_id=sid,
                skill_name=dim_name,
                cefr_level=_calculate_cefr(result_dr.raw_score),
                confidence=result_dr.confidence,
                evidence={
                    "score": result_dr.raw_score,
                    "status": result_dr.status,
                    "needs_follow_up": result_dr.needs_follow_up,
                    "contradictions": result_dr.contradictions,
                    "evidence_count": result_dr.evidence_count,
                },
            )
            db.add(skill_assessment)

    # Transition to COMPLETED
    sm = _create_machine("IN_PROGRESS")
    sm.transition("complete")
    session.status = sm.current_state
    await db.flush()

    # Audit event with the full dimension profile (no single overall_level)
    dim_snapshot = {
        dim: {
            "estimated_level": result.estimated_level,
            "confidence": result.confidence,
            "status": result.status,
            "needs_follow_up": result.needs_follow_up,
        }
        for dim, result in dimension_results.items()
    }
    await record_event(
        db,
        event_type="DIAGNOSTIC_COMPLETED",
        user_id=user_id,
        module="diagnostics",
        entity_type="diagnostic_session",
        entity_id=session_id,
        data={"dimensions": dim_snapshot},
    )

    await db.refresh(session)
    return session


async def get_session(db: AsyncSession, session_id: str, user_id: str) -> DiagnosticSession:
    """Get a diagnostic session."""
    sid = UUID(session_id)
    session = await db.get(DiagnosticSession, sid)
    if not session:
        raise NotFoundError("Diagnostic session not found")
    if str(session.user_id) != user_id:
        raise InvalidStateTransitionError("Not the owner of this session")
    return session
