"""Audit module API router."""

from __future__ import annotations

from fastapi import APIRouter, Query

from app.dependencies import CurrentUserId, DbSession
from app.modules.audit.schemas import AuditEventListResponse, AuditEventResponse
from app.modules.audit.services import get_events, record_event

router = APIRouter(prefix="/audit", tags=["audit"])


@router.post("/events")
async def create_audit_event(
    body: dict,
    user_id: CurrentUserId,
    db: DbSession,
):
    """Record an audit event."""
    event = await record_event(
        db=db,
        event_type=body["event_type"],
        user_id=user_id,
        module=body.get("module", "unknown"),
        entity_type=body.get("entity_type", "unknown"),
        entity_id=body.get("entity_id", ""),
        data=body.get("data"),
        trace_id=body.get("trace_id"),
    )
    await db.commit()
    return {"id": str(event.id), "status": "recorded"}


@router.get("/events", response_model=AuditEventListResponse)
async def list_audit_events(
    user_id: CurrentUserId,
    db: DbSession,
    module: str | None = Query(None),
    event_type: str | None = Query(None),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    """List audit events (user-scoped)."""
    events, total = await get_events(
        db=db,
        user_id=user_id,
        module=module,
        event_type=event_type,
        limit=limit,
        offset=offset,
    )
    return AuditEventListResponse(
        items=[
            AuditEventResponse(
                id=str(e.id),
                event_type=e.event_type,
                user_id=str(e.user_id),
                module=e.module,
                entity_type=e.entity_type,
                entity_id=e.entity_id,
                data=e.data,
                trace_id=e.trace_id,
                event_timestamp=e.event_timestamp.isoformat(),
            )
            for e in events
        ],
        total=total,
        limit=limit,
        offset=offset,
    )
