"""Mastery module Pydantic schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CreateEvidenceRequest(BaseModel):
    submission_id: str
    lesson_session_id: str
    skill_name: str
    evidence_type: str = Field(..., pattern=r"^(introduced|recognized|guided_use)$")


class EvidenceResponse(BaseModel):
    id: str
    skill_name: str
    evidence_type: str
    status: str


class MasteryProfileResponse(BaseModel):
    records: list[dict]
    recent_evidence: list[dict]
