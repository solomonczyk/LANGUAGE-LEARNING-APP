"""Tests for mock AI deterministic responses."""

import pytest
from app.modules.ai_gateway.services import _select_fixture, MOCK_ANALYSIS_FIXTURES, MALFORMED_OUTPUT


class TestMockAIFixtureSelection:
    def test_cat_pet_fixture(self):
        result = _select_fixture("I have a cat and it loves to play")
        assert result["analysis_version"] == "mock-v1"
        assert "VERB_FORM" in [i["code"] for i in result["detected_issues"]]

    def test_morning_routine_fixture(self):
        result = _select_fixture("This morning I woke up early")
        assert result["analysis_version"] == "mock-v1"
        assert "TENSE" in [i["code"] for i in result["detected_issues"]]

    def test_generic_fixture(self):
        result = _select_fixture("I went to the store yesterday")
        assert result["analysis_version"] == "mock-v1"
        assert "WORD_ORDER" in [i["code"] for i in result["detected_issues"]]

    def test_empty_text_uses_generic(self):
        result = _select_fixture("")
        assert result["analysis_version"] == "mock-v1"

    def test_pet_variations(self):
        for text in ["my dog", "my pet", "the cat"]:
            result = _select_fixture(text)
            assert "VERB_FORM" in [i["code"] for i in result["detected_issues"]]

    def test_morning_variations(self):
        for text in ["wake up", "breakfast time", "morning routine"]:
            result = _select_fixture(text)
            assert "TENSE" in [i["code"] for i in result["detected_issues"]]

    def test_deterministic_output(self):
        """Same input always produces same output."""
        result1 = _select_fixture("I have a cat")
        result2 = _select_fixture("I have a cat")
        assert result1 == result2


class TestMockAIOutputStructure:
    def test_valid_fixture_has_all_fields(self):
        fixture = MOCK_ANALYSIS_FIXTURES["cat_pet"]
        assert "analysis_version" in fixture
        assert "meaning_preserved" in fixture
        assert "detected_issues" in fixture
        assert "strengths" in fixture
        assert "recommended_focus" in fixture
        assert "confidence" in fixture

    def test_detected_issues_structure(self):
        fixture = MOCK_ANALYSIS_FIXTURES["cat_pet"]
        for issue in fixture["detected_issues"]:
            assert "code" in issue
            assert "severity" in issue
            assert "span" in issue
            assert "suggestion" in issue

    def test_valid_severity_values(self):
        fixture = MOCK_ANALYSIS_FIXTURES["cat_pet"]
        for issue in fixture["detected_issues"]:
            assert issue["severity"] in ("major", "minor", "info")

    def test_valid_issue_codes(self):
        allowed = {"VERB_FORM", "ARTICLE", "PREPOSITION", "WORD_ORDER",
                   "COLLOCATION", "SPELLING", "TENSE", "PLURAL",
                   "SUBJECT_VERB_AGREEMENT", "MODAL"}
        for fixture in MOCK_ANALYSIS_FIXTURES.values():
            for issue in fixture["detected_issues"]:
                assert issue["code"] in allowed

    def test_confidence_range(self):
        for fixture in MOCK_ANALYSIS_FIXTURES.values():
            assert 0.0 <= fixture["confidence"] <= 1.0

    def test_malformed_output_missing_fields(self):
        """Malformed output should violate schema expectations."""
        issues = MALFORMED_OUTPUT.get("detected_issues")
        assert not isinstance(issues, list)  # Should be a string
        assert MALFORMED_OUTPUT.get("confidence") == "high"  # Should be float

    def test_strengths_is_list(self):
        for fixture in MOCK_ANALYSIS_FIXTURES.values():
            assert isinstance(fixture["strengths"], list)

    def test_recommended_focus_is_list(self):
        for fixture in MOCK_ANALYSIS_FIXTURES.values():
            assert isinstance(fixture["recommended_focus"], list)

    def test_no_randomness(self):
        """All fixtures should be purely deterministic."""
        import json
        texts = [json.dumps(f, sort_keys=True) for f in MOCK_ANALYSIS_FIXTURES.values()]
        assert len(set(texts)) == len(texts)  # All different but deterministic
