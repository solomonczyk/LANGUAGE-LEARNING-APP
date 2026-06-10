"""Lesson engine Pydantic schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CreateSessionRequest(BaseModel):
    lesson_definition_id: str


class SessionResponse(BaseModel):
    session_id: str
    lesson_definition_id: str
    status: str
    current_attempt: int
    created_at: str


class SubmitTextRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=5000)


class SubmitTextResponse(BaseModel):
    submission_id: str
    session_id: str
    status: str
    text_preview: str


class ProcessResponse(BaseModel):
    session_id: str
    status: str
    decision: str | None = None
    corrections: list[dict] | None = None
    strengths: list[str] | None = None
    validation_results: dict | None = None
