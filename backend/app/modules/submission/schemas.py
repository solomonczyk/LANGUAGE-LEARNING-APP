"""Submission module Pydantic schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class SubmissionResponse(BaseModel):
    id: str
    user_id: str
    lesson_session_id: str
    lesson_definition_id: str
    status: str
    source_text: str
    text_preview: str
    created_at: str
