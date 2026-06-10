"""Audit module Pydantic schemas."""

from __future__ import annotations

from pydantic import BaseModel


class AuditEventResponse(BaseModel):
    id: str
    event_type: str
    user_id: str
    module: str
    entity_type: str
    entity_id: str
    data: dict
    trace_id: str | None = None
    event_timestamp: str


class AuditEventListResponse(BaseModel):
    items: list[AuditEventResponse]
    total: int
    limit: int
    offset: int
