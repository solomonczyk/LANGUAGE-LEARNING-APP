"""Audit services — append-only event recording."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AuditEvent
from app.shared.exceptions.domain import AuditWriteFailedError


async def record_event(
    db: AsyncSession,
    event_type: str,
    user_id: str,
    module: str,
    entity_type: str,
    entity_id: str,
    data: dict | None = None,
    trace_id: str | None = None,
) -> AuditEvent:
    """Record an audit event. Raises AuditWriteFailedError on failure."""
    try:
        event = AuditEvent(
            event_type=event_type,
            user_id=UUID(user_id),
            module=module,
            entity_type=entity_type,
            entity_id=entity_id,
            data=data or {},
            trace_id=trace_id,
        )
        db.add(event)
        await db.flush()
        await db.refresh(event)
        return event
    except Exception as e:
        raise AuditWriteFailedError(f"Failed to write audit event: {e}")


async def get_events(
    db: AsyncSession,
    user_id: str | None = None,
    module: str | None = None,
    event_type: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> tuple[list[AuditEvent], int]:
    """Get audit events with optional filters."""
    query = select(AuditEvent)
    count_query = select(AuditEvent)

    if user_id:
        uid = UUID(user_id)
        query = query.where(AuditEvent.user_id == uid)
        count_query = count_query.where(AuditEvent.user_id == uid)
    if module:
        query = query.where(AuditEvent.module == module)
        count_query = count_query.where(AuditEvent.module == module)
    if event_type:
        query = query.where(AuditEvent.event_type == event_type)
        count_query = count_query.where(AuditEvent.event_type == event_type)

    # Get total count
    count_result = await db.execute(count_query)
    total = len(count_result.scalars().all())

    # Get paginated results
    query = query.order_by(AuditEvent.event_timestamp.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    events = result.scalars().all()

    return list(events), total
