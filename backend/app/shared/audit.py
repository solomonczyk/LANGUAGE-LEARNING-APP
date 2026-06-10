"""Audit event creation helpers."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone


def create_audit_event(
    event_type: str,
    user_id: str,
    module: str,
    entity_type: str,
    entity_id: str,
    data: dict | None = None,
    trace_id: str | None = None,
) -> dict:
    """Create a structured audit event dict.

    This is used as a data payload; persistence is handled by the audit module.
    """
    return {
        "id": str(uuid.uuid4()),
        "event_type": event_type,
        "user_id": user_id,
        "module": module,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "data": data or {},
        "trace_id": trace_id or str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
