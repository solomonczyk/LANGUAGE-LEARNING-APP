"""AI Gateway Pydantic schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    submission_id: str
    text: str = Field(..., min_length=1)
    learner_level: str = "A2"
    lesson_type: str = "personal_narrative"


class AnalysisResponse(BaseModel):
    analysis_version: str
    meaning_preserved: bool
    detected_issues: list[dict]
    strengths: list[str]
    recommended_focus: list[str]
    confidence: float


class GatewayStatusResponse(BaseModel):
    status: str
    mock_mode: bool
    fixture_mode: str
