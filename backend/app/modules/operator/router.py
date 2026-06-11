"""Operator module — read-only diagnostic endpoints for local development."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import CurrentUserId
from app.models import User

router = APIRouter(prefix="/operator", tags=["operator"])


async def _require_operator(user_id: CurrentUserId) -> str:
    """Verify the current user has operator privileges."""
    from app.config import settings

    from app.database import async_session_factory

    async with async_session_factory() as db:
        stmt = select(User).where(User.id == UUID(user_id))
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user or not user.is_operator:
            raise HTTPException(
                status_code=403,
                detail={
                    "error": {
                        "code": "FORBIDDEN",
                        "message": "Operator access required.",
                        "details": {},
                        "trace_id": "",
                        "retryable": False,
                    }
                },
            )
    return user_id


@router.get("/health")
async def operator_health():
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
    _operator: str = Depends(_require_operator),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    """List all audit events (operator read-only, local development)."""
    from app.database import async_session_factory
    from app.modules.audit.services import get_events

    async with async_session_factory() as db:
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
