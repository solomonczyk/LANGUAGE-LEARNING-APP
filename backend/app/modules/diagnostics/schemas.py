"""Diagnostics module Pydantic schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CreateSessionResponse(BaseModel):
    session_id: str
    status: str
    current_step: int = 0
    total_steps: int = 4


class DiagnosticStep(BaseModel):
    session_id: str
    current_step: int
    total_steps: int
    question_key: str
    prompt: str


class SubmitResponseRequest(BaseModel):
    question_key: str
    response_data: dict


class SubmitResponseResponse(BaseModel):
    session_id: str
    question_key: str
    step: int
    total_steps: int
    status: str


class CompleteSessionResponse(BaseModel):
    session_id: str
    status: str
    assessments: list[dict]
    overall_level: str


class SessionStatusResponse(BaseModel):
    session_id: str
    status: str
    current_step: int
    total_steps: int
    assessments: list[dict] | None = None
