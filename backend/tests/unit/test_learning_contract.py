"""Tests for Learning Entry Contract calculation."""

from app.modules.learning_contract.services import _deduplicate_assessments, _derive_contract_params


def test_a1_contract_params():
    params = _derive_contract_params([])
    assert params["lesson_duration_minutes"] == 10
    assert params["active_vocabulary_budget"] == 3
    assert params["grammar_focus_count"] == 3
    assert params["max_primary_corrections"] == 5
    assert params["scaffolding_mode"] == "high"
    assert params["lesson_complexity"] == "simple"


class MockSkillAssessment:
    def __init__(self, cefr_level, skill_name="test", confidence=0.8):
        self.cefr_level = cefr_level
        self.skill_name = skill_name
        self.confidence = confidence


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


# ---------------------------------------------------------------------------
# Deduplication tests
# ---------------------------------------------------------------------------


def test_deduplicate_empty_list():
    assert _deduplicate_assessments([]) == []


def test_deduplicate_single_assessment():
    items = [MockSkillAssessment("A2", skill_name="grammar_recognition")]
    result = _deduplicate_assessments(items)
    assert len(result) == 1
    assert result[0].skill_name == "grammar_recognition"


def test_deduplicate_all_unique():
    items = [
        MockSkillAssessment("A2", skill_name="grammar_recognition"),
        MockSkillAssessment("A1", skill_name="active_vocabulary"),
        MockSkillAssessment("B1", skill_name="written_production"),
        MockSkillAssessment("A2", skill_name="narrative_coherence"),
    ]
    result = _deduplicate_assessments(items)
    assert len(result) == 4


def test_deduplicate_removes_duplicate_skills():
    items = [
        MockSkillAssessment("A2", skill_name="grammar_recognition"),
        MockSkillAssessment("A1", skill_name="active_vocabulary"),
        MockSkillAssessment("B1", skill_name="grammar_recognition"),  # duplicate
    ]
    result = _deduplicate_assessments(items)
    assert len(result) == 2
    # First occurrence (newest) is kept
    assert result[0].skill_name == "grammar_recognition"
    assert result[0].cefr_level == "A2"


def test_deduplicate_keeps_first_occurrence():
    items = [
        MockSkillAssessment("A2", skill_name="grammar_recognition"),
        MockSkillAssessment("A1", skill_name="active_vocabulary"),
        MockSkillAssessment("A1", skill_name="grammar_recognition"),  # duplicate, older
    ]
    result = _deduplicate_assessments(items)
    assert len(result) == 2
    # Should keep the A2 (first occurrence, newest) not the A1
    gr = [a for a in result if a.skill_name == "grammar_recognition"]
    assert len(gr) == 1
    assert gr[0].cefr_level == "A2"


def test_deduplicate_many_sessions():
    """Simulates 3 diagnostic sessions producing duplicates."""
    items = [
        # Session 3 (newest)
        MockSkillAssessment("B1", skill_name="grammar_recognition"),
        MockSkillAssessment("A2", skill_name="active_vocabulary"),
        MockSkillAssessment("B1", skill_name="written_production"),
        MockSkillAssessment("A2", skill_name="narrative_coherence"),
        # Session 2
        MockSkillAssessment("A2", skill_name="grammar_recognition"),
        MockSkillAssessment("A1", skill_name="active_vocabulary"),
        MockSkillAssessment("A2", skill_name="written_production"),
        MockSkillAssessment("A1", skill_name="narrative_coherence"),
        # Session 1 (oldest)
        MockSkillAssessment("A1", skill_name="grammar_recognition"),
        MockSkillAssessment("A1", skill_name="active_vocabulary"),
        MockSkillAssessment("A1", skill_name="written_production"),
        MockSkillAssessment("A1", skill_name="narrative_coherence"),
    ]
    result = _deduplicate_assessments(items)
    assert len(result) == 4
    # All should be at the newest session's level (B1/A2)
    skills_map = {a.skill_name: a.cefr_level for a in result}
    assert skills_map["grammar_recognition"] == "B1"
    assert skills_map["active_vocabulary"] == "A2"
    assert skills_map["written_production"] == "B1"
    assert skills_map["narrative_coherence"] == "A2"
