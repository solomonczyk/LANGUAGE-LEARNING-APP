"""AI Gateway services — deterministic mock analysis provider."""

from __future__ import annotations

import uuid
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models import AIAnalysisRequest, AIAnalysisResult, Submission
from app.shared.exceptions.domain import NotFoundError

# Deterministic mock analysis fixtures
MOCK_ANALYSIS_FIXTURES = {
    "cat_pet": {
        "analysis_version": "mock-v1",
        "meaning_preserved": True,
        "detected_issues": [
            {
                "code": "VERB_FORM",
                "severity": "major",
                "span": "wants to the water closet",
                "suggestion": "wanted to go to the litter box",
            },
            {
                "code": "PREPOSITION",
                "severity": "minor",
                "span": "jump on the bed",
                "suggestion": "jumped on the bed",
            },
        ],
        "strengths": [
            "The sequence of events is understandable.",
            "Good use of time markers.",
        ],
        "recommended_focus": [
            "Past tense",
            "Natural verb phrase",
        ],
        "confidence": 0.91,
    },
    "morning_routine": {
        "analysis_version": "mock-v1",
        "meaning_preserved": True,
        "detected_issues": [
            {
                "code": "TENSE",
                "severity": "major",
                "span": "I wake up and go to kitchen",
                "suggestion": "I woke up and went to the kitchen",
            },
            {
                "code": "ARTICLE",
                "severity": "minor",
                "span": "go to kitchen",
                "suggestion": "go to the kitchen",
            },
        ],
        "strengths": [
            "Clear chronological order.",
            "Appropriate vocabulary for daily routines.",
        ],
        "recommended_focus": [
            "Past tense consistency",
            "Article usage",
        ],
        "confidence": 0.88,
    },
    "generic": {
        "analysis_version": "mock-v1",
        "meaning_preserved": True,
        "detected_issues": [
            {
                "code": "WORD_ORDER",
                "severity": "minor",
                "span": "sentence structure",
                "suggestion": "Consider restructuring for clarity.",
            },
        ],
        "strengths": [
            "The main idea is communicated.",
        ],
        "recommended_focus": [
            "Sentence structure",
            "Vocabulary expansion",
        ],
        "confidence": 0.75,
    },
}

MALFORMED_OUTPUT = {
    "analysis_version": "mock-v1",
    "meaning_preserved": True,
    "detected_issues": "malformed",  # Should be a list, not a string
    "strengths": None,  # Should not be None
    "confidence": "high",  # Should be a float
}


def _select_fixture(text: str) -> dict:
    """Deterministically select a fixture based on text content."""
    lower = text.lower()
    if "cat" in lower or "pet" in lower or "dog" in lower:
        return dict(MOCK_ANALYSIS_FIXTURES["cat_pet"])
    if "morning" in lower or "wake" in lower or "breakfast" in lower:
        return dict(MOCK_ANALYSIS_FIXTURES["morning_routine"])
    return dict(MOCK_ANALYSIS_FIXTURES["generic"])


async def analyze_submission(
    db: AsyncSession,
    submission_id: str,
    user_id: str,
    text: str,
    learner_level: str = "A2",
    lesson_type: str = "personal_narrative",
) -> dict:
    """Run mock AI analysis on a submission.

    Returns the analysis result dict. If in malformed mode, returns
    intentionally invalid output to test the validation pipeline.
    """
    sid = UUID(submission_id)

    # Create analysis request
    request = AIAnalysisRequest(
        submission_id=sid,
        status="RUNNING",
        analysis_type="text_analysis",
        request_data={
            "text": text,
            "learner_level": learner_level,
            "lesson_type": lesson_type,
        },
    )
    db.add(request)
    await db.flush()
    await db.refresh(request)

    # Generate deterministic output
    if settings.mock_ai_fixture_mode == "malformed":
        raw_output = dict(MALFORMED_OUTPUT)
        schema_valid = False
        status = "INVALID_OUTPUT"
    else:
        raw_output = _select_fixture(text)
        schema_valid = True
        status = "SUCCEEDED"

    # Store result
    result = AIAnalysisResult(
        submission_id=sid,
        request_id=request.id,
        analysis_version=raw_output.get("analysis_version", "mock-v1"),
        raw_output=raw_output,
        output_schema_valid=schema_valid,
        status=status,
    )
    db.add(result)

    # Update request status
    request.status = status
    await db.flush()
    await db.refresh(result)

    return {
        "analysis_version": raw_output.get("analysis_version"),
        "meaning_preserved": raw_output.get("meaning_preserved", True),
        "detected_issues": raw_output.get("detected_issues", []),
        "strengths": raw_output.get("strengths", []),
        "recommended_focus": raw_output.get("recommended_focus", []),
        "confidence": raw_output.get("confidence", 0.0),
        "schema_valid": schema_valid,
        "result_id": str(result.id),
        "request_id": str(request.id),
    }


async def get_analysis_result(db: AsyncSession, submission_id: str) -> dict | None:
    """Get the latest analysis result for a submission."""
    sid = UUID(submission_id)
    stmt = (
        select(AIAnalysisResult)
        .where(AIAnalysisResult.submission_id == sid)
        .order_by(AIAnalysisResult.created_at.desc())
        .limit(1)
    )
    result = await db.execute(stmt)
    analysis = result.scalar_one_or_none()
    if not analysis:
        return None

    return {
        "analysis_version": analysis.analysis_version,
        "raw_output": analysis.raw_output,
        "output_schema_valid": analysis.output_schema_valid,
        "status": analysis.status,
        "result_id": str(analysis.id),
    }
