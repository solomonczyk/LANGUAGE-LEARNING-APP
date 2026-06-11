"""Tests for mock AI deterministic responses."""

import pytest
from app.modules.ai_gateway.services import _select_fixture, MOCK_ANALYSIS_FIXTURES, MALFORMED_OUTPUT


class TestMockAIFixtureSelection:
    def test_cat_pet_fixture_default_a2(self):
        result = _select_fixture("I have a cat and it loves to play")
        assert result["analysis_version"] == "mock-v2-level-aware"
        assert "VERB_FORM" in [i["code"] for i in result["detected_issues"]]

    def test_morning_routine_fixture_default_a2(self):
        result = _select_fixture("This morning I woke up early")
        assert result["analysis_version"] == "mock-v2-level-aware"
        assert "TENSE" in [i["code"] for i in result["detected_issues"]]

    def test_generic_fixture_default_a2(self):
        result = _select_fixture("I went to the store yesterday")
        assert result["analysis_version"] == "mock-v2-level-aware"
        assert "WORD_ORDER" in [i["code"] for i in result["detected_issues"]]

    def test_empty_text_uses_generic(self):
        result = _select_fixture("")
        assert result["analysis_version"] == "mock-v2-level-aware"

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

    def test_a1_fixture_simplified(self):
        """A1 fixtures should have max 1 correction and simplified strengths."""
        result = _select_fixture("I have a cat", "A1")
        assert len(result["detected_issues"]) <= 1
        for issue in result["detected_issues"]:
            assert issue["severity"] == "minor"
        assert len(result["strengths"]) == 1
        assert "Good job" in result["strengths"][0]

    def test_b2_fixture_more_detailed(self):
        """B2 fixtures should have more recommended focus items."""
        result = _select_fixture("I have a cat", "B2")
        assert len(result["recommended_focus"]) >= 3  # base + extra
        assert "Natural collocation" in result["recommended_focus"]
        assert result["confidence"] > 0.9

    def test_level_aware_deterministic(self):
        """Same input + level always produces same output."""
        r1 = _select_fixture("I wake up", "A1")
        r2 = _select_fixture("I wake up", "A1")
        assert r1 == r2

    def test_different_levels_different_output(self):
        """Different levels should produce different feedback."""
        a1 = _select_fixture("I have a cat", "A1")
        b2 = _select_fixture("I have a cat", "B2")
        assert a1 != b2  # Different strengths, issues, etc.


class TestMockAIOutputStructure:
    def test_valid_fixture_has_all_fields(self):
        fixture = MOCK_ANALYSIS_FIXTURES["cat_pet"]
        assert "analysis_version" in fixture
        assert fixture["analysis_version"] == "mock-v2-level-aware"
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
