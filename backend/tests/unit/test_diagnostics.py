"""Tests for diagnostic score calculation and state machine."""

import pytest
from app.modules.diagnostics.services import _calculate_cefr, _assess_responses


class TestCefrCalculation:
    def test_a1_level(self):
        assert _calculate_cefr(40) == "A1"
        assert _calculate_cefr(50) == "A1"
        assert _calculate_cefr(64) == "A1"

    def test_a2_level(self):
        assert _calculate_cefr(65) == "A2"
        assert _calculate_cefr(75) == "A2"
        assert _calculate_cefr(84) == "A2"

    def test_b1_level(self):
        assert _calculate_cefr(85) == "B1"
        assert _calculate_cefr(95) == "B1"
        assert _calculate_cefr(100) == "B1"

    def test_boundary_values(self):
        assert _calculate_cefr(0) == "A1"
        assert _calculate_cefr(64.9) == "A1"
        assert _calculate_cefr(65) == "A2"
        assert _calculate_cefr(84.9) == "A2"
        assert _calculate_cefr(85) == "B1"


class TestAssessmentCalculation:
    def test_grammar_recognition_correct(self):
        responses = [
            {"question_key": "grammar_recognition", "response_data": {"is_correct": True}},
        ]
        result = _assess_responses(responses)
        assert result["grammar_recognition"]["cefr"] == "A2"
        assert result["grammar_recognition"]["score"] == 80.0

    def test_grammar_recognition_incorrect(self):
        responses = [
            {"question_key": "grammar_recognition", "response_data": {"is_correct": False}},
        ]
        result = _assess_responses(responses)
        assert result["grammar_recognition"]["cefr"] == "A1"

    def test_vocabulary_assessment(self):
        responses = [
            {"question_key": "active_vocabulary", "response_data": {"correct_count": 4, "total_words": 5}},
        ]
        result = _assess_responses(responses)
        assert result["active_vocabulary"]["cefr"] == "A2"
        assert result["active_vocabulary"]["confidence"] == 0.8

    def test_vocabulary_low_score(self):
        responses = [
            {"question_key": "active_vocabulary", "response_data": {"correct_count": 1, "total_words": 5}},
        ]
        result = _assess_responses(responses)
        assert result["active_vocabulary"]["cefr"] == "A1"

    def test_written_production_scoring(self):
        responses = [
            {"question_key": "written_production", "response_data": {"word_count": 25, "has_structure": True}},
        ]
        result = _assess_responses(responses)
        assert result["written_production"]["score"] == 85.0
        assert result["written_production"]["cefr"] == "B1"

    def test_narrative_coherence_correct(self):
        responses = [
            {"question_key": "narrative_coherence", "response_data": {"correct_order": True}},
        ]
        result = _assess_responses(responses)
        assert result["narrative_coherence"]["cefr"] == "B1"

    def test_narrative_coherence_incorrect(self):
        responses = [
            {"question_key": "narrative_coherence", "response_data": {"correct_order": False}},
        ]
        result = _assess_responses(responses)
        assert result["narrative_coherence"]["cefr"] == "A1"

    def test_multi_dimension_assessment(self):
        responses = [
            {"question_key": "grammar_recognition", "response_data": {"is_correct": True}},
            {"question_key": "active_vocabulary", "response_data": {"correct_count": 5, "total_words": 5}},
            {"question_key": "written_production", "response_data": {"word_count": 30, "has_structure": True}},
            {"question_key": "narrative_coherence", "response_data": {"correct_order": True}},
        ]
        result = _assess_responses(responses)
        assert len(result) == 4
        assert all(r["cefr"] in ("A2", "B1") for r in result.values())

    def test_empty_responses(self):
        result = _assess_responses([])
        assert len(result) == 0

    def test_grammar_with_selected_option_field(self):
        """Backend must ignore extra frontend fields (selected_option)."""
        responses = [
            {"question_key": "grammar_recognition", "response_data": {"is_correct": True, "selected_option": "b"}},
        ]
        result = _assess_responses(responses)
        assert result["grammar_recognition"]["cefr"] == "A2"
        assert result["grammar_recognition"]["score"] == 80.0

    def test_grammar_incorrect_with_selected_option(self):
        responses = [
            {"question_key": "grammar_recognition", "response_data": {"is_correct": False, "selected_option": "a"}},
        ]
        result = _assess_responses(responses)
        assert result["grammar_recognition"]["cefr"] == "A1"

    def test_vocabulary_with_selections_field(self):
        """Backend uses correct_count/total_words, ignores extra selections dict."""
        responses = [
            {
                "question_key": "active_vocabulary",
                "response_data": {
                    "correct_count": 3,
                    "total_words": 4,
                    "selections": {"Morning": "b", "Breakfast": "a", "Pet": "c", "Walk": "d"},
                },
            },
        ]
        result = _assess_responses(responses)
        assert result["active_vocabulary"]["score"] == 75.0
        assert result["active_vocabulary"]["cefr"] == "A2"

    def test_narrative_with_user_order_field(self):
        """Backend uses correct_order, ignores extra user_order array."""
        responses = [
            {
                "question_key": "narrative_coherence",
                "response_data": {
                    "correct_order": False,
                    "user_order": ["3", "1", "2", "5", "4"],
                },
            },
        ]
        result = _assess_responses(responses)
        assert result["narrative_coherence"]["cefr"] == "A1"
        assert result["narrative_coherence"]["score"] == 40.0
