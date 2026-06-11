"""AI Gateway services — deterministic mock analysis provider with level-aware feedback."""

from __future__ import annotations

import copy
import uuid
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models import AIAnalysisRequest, AIAnalysisResult, Submission
from app.shared.exceptions.domain import NotFoundError

# Level-aware mock analysis fixtures (base versions — adapted per level below)
MOCK_ANALYSIS_FIXTURES = {
    "cat_pet": {
        "analysis_version": "mock-v2-level-aware",
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
        "analysis_version": "mock-v2-level-aware",
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
        "analysis_version": "mock-v2-level-aware",
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


def _adapt_fixture_by_level(fixture: dict, learner_level: str) -> dict:
    """Adapt a base fixture to be level-appropriate.

    A1: very short, very supportive, 1-2 corrections max, simple language.
    A2: short correction, simple reason, one suggested phrase.
    B1: grammar + vocabulary feedback, more precise, next-step suggestion.
    B2: nuance, collocation, naturalness, concise but more advanced.
    """
    adapted = copy.deepcopy(fixture)

    if learner_level.upper() == "A1":
        # A1: very short, very supportive, 1-2 max corrections
        adapted["detected_issues"] = adapted["detected_issues"][:1]
        for issue in adapted["detected_issues"]:
            issue["severity"] = "minor"
        adapted["strengths"] = [
            "Good job! You are sharing your ideas.",
        ]
        adapted["recommended_focus"] = adapted["recommended_focus"][:1]
        adapted["confidence"] = 0.85

    elif learner_level.upper() == "A2":
        # A2: short correction, simple reason, 2 corrections max
        adapted["detected_issues"] = adapted["detected_issues"][:2]
        adapted["strengths"] = [
            "You wrote a clear story. Well done!",
            "The order of events is easy to follow.",
        ][:1]
        adapted["recommended_focus"] = adapted["recommended_focus"][:2]
        adapted["confidence"] = 0.82

    elif learner_level.upper() == "B1":
        # B1: grammar + vocabulary feedback, more precise
        if len(adapted["detected_issues"]) > 0:
            adapted["detected_issues"][0]["suggestion"] = (
                f"Consider using: {adapted['detected_issues'][0]['suggestion']}"
            )
        adapted["strengths"] = [
            "Effective use of narrative structure.",
            "Good vocabulary choices for the topic.",
        ]
        adapted["recommended_focus"] = adapted["recommended_focus"]
        adapted["confidence"] = 0.88

    elif learner_level.upper() in ("B2", "C1", "C2"):
        # B2+: nuance, collocation, naturalness
        for issue in adapted["detected_issues"]:
            if issue["code"] in ("VERB_FORM", "TENSE"):
                issue["suggestion"] = (
                    f"For more natural phrasing, try: {issue['suggestion']}"
                )
        adapted["strengths"] = [
            "Good narrative flow with clear temporal progression.",
            "Effective topic-specific vocabulary choices.",
        ]
        adapted["recommended_focus"] = [
            *adapted["recommended_focus"],
            "Natural collocation",
            "Stylistic precision",
        ]
        adapted["confidence"] = 0.92

    return adapted


def _select_fixture(text: str, learner_level: str = "A2") -> dict:
    """Deterministically select a fixture based on text content and adapt by level."""
    lower = text.lower()
    if "cat" in lower or "pet" in lower or "dog" in lower:
        base = dict(MOCK_ANALYSIS_FIXTURES["cat_pet"])
    elif "morning" in lower or "wake" in lower or "breakfast" in lower:
        base = dict(MOCK_ANALYSIS_FIXTURES["morning_routine"])
    else:
        base = dict(MOCK_ANALYSIS_FIXTURES["generic"])
    return _adapt_fixture_by_level(base, learner_level)


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
    try:
        sid = UUID(submission_id) if isinstance(submission_id, str) else submission_id
    except (ValueError, AttributeError):
        sid = submission_id

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
        raw_output = _select_fixture(text, learner_level)
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
    try:
        sid = UUID(submission_id) if isinstance(submission_id, str) else submission_id
    except (ValueError, AttributeError):
        sid = submission_id
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
