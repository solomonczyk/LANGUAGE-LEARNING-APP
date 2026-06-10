"""Policy engine Pydantic schemas."""

from __future__ import annotations

from pydantic import BaseModel


class DecisionRequest(BaseModel):
    submission_id: str
    user_id: str


class DecisionResponse(BaseModel):
    decision: str
    reason: str
    allow_retry: bool
