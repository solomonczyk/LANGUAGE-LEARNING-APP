"""Operator module — read-only diagnostic endpoints for local development."""

from __future__ import annotations

from fastapi import APIRouter, Query

from app.dependencies import CurrentUserId, DbSession

router = APIRouter(prefix="/operator", tags=["operator"])


@router.get("/health")
async def operator_health(db: DbSession):
    """Extended health info for operator."""
    from app.config import settings

    return {
        "status": "ok",
        "version": "0.1.0",
        "auth_stub": settings.auth_stub_enabled,
        "mock_ai": {
            "enabled": settings.mock_ai_enabled,
            "fixture_mode": settings.mock_ai_fixture_mode,
        },
        "database": "configured",
    }


@router.get("/audit-events")
async def operator_audit_events(
    user_id: CurrentUserId,
    db: DbSession,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    """List all audit events (operator read-only, local development)."""
    from app.modules.audit.services import get_events

    events, total = await get_events(
        db=db,
        limit=limit,
        offset=offset,
    )
    return {
        "items": [
            {
                "id": str(e.id),
                "event_type": e.event_type,
                "user_id": str(e.user_id),
                "module": e.module,
                "entity_type": e.entity_type,
                "entity_id": e.entity_id,
                "data": e.data,
                "trace_id": e.trace_id,
                "event_timestamp": e.event_timestamp.isoformat(),
            }
            for e in events
        ],
        "total": total,
        "limit": limit,
        "offset": offset,
    }
