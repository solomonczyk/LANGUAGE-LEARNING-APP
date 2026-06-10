"""Learner profile Pydantic schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ProfileCreateRequest(BaseModel):
    target_language: str = Field(..., min_length=1, max_length=50)
    native_language: str = Field(..., min_length=1, max_length=50)
    learning_goal: str | None = None
    preferred_lesson_duration: int = Field(default=10, ge=5, le=60)
    self_reported_level: str = Field(default="A1", pattern=r"^(A1|A2|B1|B2|C1|C2)$")


class ProfileResponse(BaseModel):
    id: str
    user_id: str
    target_language: str
    native_language: str
    learning_goal: str | None = None
    preferred_lesson_duration: int
    self_reported_level: str
    profile_status: str
    created_at: str
    updated_at: str
