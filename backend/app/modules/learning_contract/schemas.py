"""Learning Contract Pydantic schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ContractResponse(BaseModel):
    id: str
    target_language: str
    support_language: str
    lesson_duration_minutes: int
    active_vocabulary_budget: int
    grammar_focus_count: int
    max_primary_corrections: int
    scaffolding_mode: str
    lesson_complexity: str
    diagnostic_profile_snapshot: dict
    version: str
    status: str
    created_at: str
    updated_at: str
