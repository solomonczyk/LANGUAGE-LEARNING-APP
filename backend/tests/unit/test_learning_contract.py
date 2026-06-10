"""Tests for Learning Entry Contract calculation."""

from app.modules.learning_contract.services import _derive_contract_params


def test_a1_contract_params():
    params = _derive_contract_params([])
    assert params["lesson_duration_minutes"] == 10
    assert params["active_vocabulary_budget"] == 3
    assert params["grammar_focus_count"] == 3
    assert params["max_primary_corrections"] == 5
    assert params["scaffolding_mode"] == "high"
    assert params["lesson_complexity"] == "simple"


class MockSkillAssessment:
    def __init__(self, cefr_level):
        self.cefr_level = cefr_level
        self.skill_name = "test"
        self.confidence = 0.8


def test_a2_contract_params():
    assessments = [MockSkillAssessment("A2")]
    params = _derive_contract_params(assessments)
    assert params["lesson_duration_minutes"] == 15
    assert params["active_vocabulary_budget"] == 5
    assert params["grammar_focus_count"] == 2
    assert params["max_primary_corrections"] == 3
    assert params["scaffolding_mode"] == "moderate"
    assert params["lesson_complexity"] == "moderate"


def test_b1_contract_params():
    assessments = [MockSkillAssessment("B1")]
    params = _derive_contract_params(assessments)
    assert params["lesson_duration_minutes"] == 20
    assert params["active_vocabulary_budget"] == 8
    assert params["grammar_focus_count"] == 1
    assert params["max_primary_corrections"] == 2
    assert params["scaffolding_mode"] == "light"
    assert params["lesson_complexity"] == "complex"


def test_lowest_level_determines_params():
    """The lowest CEFR level across all dimensions determines contract params."""
    assessments = [MockSkillAssessment("A2"), MockSkillAssessment("B1")]
    params = _derive_contract_params(assessments)
    assert params["lesson_duration_minutes"] == 15  # A2 determines


def test_multi_assessment_lowest():
    assessments = [MockSkillAssessment("A1"), MockSkillAssessment("B1")]
    params = _derive_contract_params(assessments)
    assert params["lesson_duration_minutes"] == 10  # A1 determines


def test_all_levels_deterministic():
    """Same inputs always produce same outputs."""
    a1 = _derive_contract_params([MockSkillAssessment("A1")])
    a1_again = _derive_contract_params([MockSkillAssessment("A1")])
    assert a1 == a1_again

    b1 = _derive_contract_params([MockSkillAssessment("B1")])
    b1_again = _derive_contract_params([MockSkillAssessment("B1")])
    assert b1 == b1_again
