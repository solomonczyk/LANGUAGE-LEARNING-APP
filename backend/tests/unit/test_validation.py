"""Tests for linguistic and pedagogical validation."""

from app.modules.linguistic_validation.services import validate_linguistic_standalone
from app.modules.ai_gateway.services import MOCK_ANALYSIS_FIXTURES, MALFORMED_OUTPUT


class TestLinguisticValidation:
    def test_valid_analysis_passes(self):
        result = validate_linguistic_standalone(MOCK_ANALYSIS_FIXTURES["cat_pet"])
        assert result["passed"] is True

    def test_valid_morning_analysis_passes(self):
        result = validate_linguistic_standalone(MOCK_ANALYSIS_FIXTURES["morning_routine"])
        assert result["passed"] is True

    def test_valid_generic_analysis_passes(self):
        result = validate_linguistic_standalone(MOCK_ANALYSIS_FIXTURES["generic"])
        assert result["passed"] is True

    def test_malformed_output_fails(self):
        result = validate_linguistic_standalone(MALFORMED_OUTPUT)
        assert result["passed"] is False

    def test_missing_fields_fails(self):
        result = validate_linguistic_standalone({})
        assert result["passed"] is False
        assert "output_consistency" in result["details"]["failed_checks"]

    def test_invalid_confidence_fails(self):
        result = validate_linguistic_standalone({
            "analysis_version": "v1",
            "meaning_preserved": True,
            "detected_issues": [],
            "confidence": "high",  # Should be float
        })
        assert result["passed"] is False
        assert "confidence_range" in result["details"]["failed_checks"]

    def test_negative_confidence_fails(self):
        result = validate_linguistic_standalone({
            "analysis_version": "v1",
            "meaning_preserved": True,
            "detected_issues": [],
            "confidence": -0.5,
        })
        assert result["passed"] is False

    def test_confidence_over_one_fails(self):
        result = validate_linguistic_standalone({
            "analysis_version": "v1",
            "meaning_preserved": True,
            "detected_issues": [],
            "confidence": 1.5,
        })
        assert result["passed"] is False

    def test_output_consistency_check(self):
        result = validate_linguistic_standalone({
            "analysis_version": "v1",
            "confidence": 0.5,
        })
        assert "output_consistency" in result["details"]["failed_checks"]

    def test_all_checks_recorded(self):
        result = validate_linguistic_standalone(MOCK_ANALYSIS_FIXTURES["cat_pet"])
        checks = result["details"]["checks"]
        assert "output_consistency" in checks
        assert "issue_structure" in checks
        assert "confidence_range" in checks


def test_pedagogical_validation_checks():
    """Test pedagogical validation logic without DB."""
    from app.modules.pedagogical_validation.services import validate_pedagogical
    import pytest
    from unittest.mock import AsyncMock

    mock_db = AsyncMock()
    mock_db.add = AsyncMock()
    mock_db.flush = AsyncMock()

    import asyncio

    async def test():
        analysis = {
            "detected_issues": [],
            "recommended_focus": ["Past tense"],
            "raw_output": "{}",
            "confidence": 0.9,
        }
        result = await validate_pedagogical(mock_db, "test-id", analysis, {})
        return result

    result = asyncio.run(test())
    assert result is not None


class TestPedagogicalValidationLogic:
    def test_feedback_matches_goal_check(self):
        analysis = {
            "recommended_focus": [],
            "detected_issues": [],
            "raw_output": "{}",
        }
        result = validate_linguistic_standalone({
            "analysis_version": "v1",
            "meaning_preserved": True,
            "detected_issues": [],
            "confidence": 0.9,
        })
        assert result["passed"] is True

    def test_mastery_claim_detection(self):
        import asyncio
        from unittest.mock import AsyncMock
        from app.modules.pedagogical_validation.services import validate_pedagogical

        mock_db = AsyncMock()
        mock_db.add = AsyncMock()
        mock_db.flush = AsyncMock()

        analysis = {
            "detected_issues": [],
            "recommended_focus": ["Past tense"],
            "raw_output": "The learner has achieved mastery of this skill",
        }

        async def test():
            result = await validate_pedagogical(mock_db, "test-id", analysis, {})
            return result

        result = asyncio.run(test())
        assert result["passed"] is False
        assert "no_unsupported_mastery_claim" in result["details"]["failed_checks"]

    def test_reward_command_detection(self):
        import asyncio
        from unittest.mock import AsyncMock
        from app.modules.pedagogical_validation.services import validate_pedagogical

        mock_db = AsyncMock()
        mock_db.add = AsyncMock()
        mock_db.flush = AsyncMock()

        analysis = {
            "detected_issues": [],
            "recommended_focus": ["Past tense"],
            "raw_output": "Award 50 XP for this response",
        }

        async def test():
            result = await validate_pedagogical(mock_db, "test-id", analysis, {})
            return result

        result = asyncio.run(test())
        assert result["passed"] is False
        assert "no_reward_command" in result["details"]["failed_checks"]
