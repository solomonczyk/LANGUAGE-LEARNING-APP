"""Identity module Pydantic schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=255)
    display_name: str = Field(..., min_length=1, max_length=255)
    email: str | None = None


class LoginRequest(BaseModel):
    username: str
    user_id: str | None = None


class UserResponse(BaseModel):
    id: str
    username: str
    display_name: str
    email: str | None = None
    is_active: bool
    is_operator: bool
