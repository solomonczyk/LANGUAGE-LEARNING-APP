"""Shared Pydantic schemas for API contracts."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Canonical error response detail."""

    code: str
    message: str
    details: dict = Field(default_factory=dict)
    trace_id: str = ""
    retryable: bool = False


class ErrorResponse(BaseModel):
    """Canonical error response wrapper."""

    error: ErrorDetail


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "ok"
    version: str = "0.1.0"
    database: str = "connected"
    mock_ai: str = "ready"


class PaginationParams(BaseModel):
    """Pagination query parameters."""

    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class PaginatedResponse(BaseModel):
    """Generic paginated response."""

    items: list
    total: int
    limit: int
    offset: int
