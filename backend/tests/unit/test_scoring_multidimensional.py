"""Tests for the multidimensional diagnostic scoring engine."""

from app.modules.diagnostics.scoring import (
    DIMENSION_REGISTRY,
    ITEM_CATALOG,
    ITEM_CATALOG_BY_KEY,
    ITEM_SCORERS,
    EvidenceContribution,
    DimensionResult,
    aggregate_dimension_scores,
    compute_dimension_results,
    compute_legacy_assessments,
    _calculate_cefr,
    _calculate_cefr_extended,
    _aggregate_confidence,
    _detect_contradictions,
)


# ---------------------------------------------------------------------------
# CEFR calculations
# ---------------------------------------------------------------------------

class TestCefrExtended:
    def test_extended_all_bands(self):
        assert _calculate_cefr_extended(0) == "A1"
        assert _calculate_cefr_extended(15) == "A1"
        assert _calculate_cefr_extended(30) == "A1"
        assert _calculate_cefr_extended(31) == "A2"
        assert _calculate_cefr_extended(50) == "A2"
        assert _calculate_cefr_extended(51) == "B1"
        assert _calculate_cefr_extended(70) == "B1"
        assert _calculate_cefr_extended(71) == "B2"
        assert _calculate_cefr_extended(85) == "B2"
        assert _calculate_cefr_extended(86) == "C1"
        assert _calculate_cefr_extended(95) == "C1"
        assert _calculate_cefr_extended(96) == "C2"
        assert _calculate_cefr_extended(100) == "C2"

    def test_extended_none_returns_not_measured(self):
        assert _calculate_cefr_extended(None) == "not_measured_yet"

    def test_backward_compat_legacy_cefr(self):
        """Original 3-band still works for old code paths."""
        assert _calculate_cefr(40) == "A1"
        assert _calculate_cefr(65) == "A2"
        assert _calculate_cefr(85) == "B1"
        assert _calculate_cefr(100) == "B1"


# ---------------------------------------------------------------------------
# EvidenceContribution and aggregation
# ---------------------------------------------------------------------------

class TestEvidenceAggregation:
    def test_aggregate_confidence_empty(self):
        assert _aggregate_confidence([]) == 0.0

    def test_aggregate_confidence_single(self):
        assert abs(_aggregate_confidence([0.8]) - 0.8) < 0.001

    def test_aggregate_confidence_multiple(self):
        # 1 - (1-0.8)*(1-0.7) = 1 - 0.06 = 0.94
        result = _aggregate_confidence([0.8, 0.7])
        assert abs(result - 0.94) < 0.01

    def test_aggregate_confidence_capped(self):
        result = _aggregate_confidence([0.99, 0.99])
        assert result <= 0.95

    def test_detect_no_contradictions_single(self):
        contribs = [EvidenceContribution(dimension="test", raw_score=80.0, confidence=0.8, source_key="src")]
        assert _detect_contradictions(contribs) == []

    def test_detect_no_contradictions_close(self):
        contribs = [
            EvidenceContribution(dimension="test", raw_score=80.0, confidence=0.8, source_key="a"),
            EvidenceContribution(dimension="test", raw_score=85.0, confidence=0.7, source_key="b"),
        ]
        assert _detect_contradictions(contribs) == []

    def test_detect_contradictions(self):
        contribs = [
            EvidenceContribution(dimension="test", raw_score=80.0, confidence=0.8, source_key="a"),
            EvidenceContribution(dimension="test", raw_score=40.0, confidence=0.7, source_key="b"),
        ]
        contradictions = _detect_contradictions(contribs)
        assert len(contradictions) == 1
        assert "80" in contradictions[0]
        assert "40" in contradictions[0]

    def test_aggregate_no_contributions(self):
        result = aggregate_dimension_scores([], "nonexistent")
        assert result.status == "not_measured_yet"
        assert result.estimated_level == "not_measured_yet"
        assert result.needs_follow_up is True

    def test_aggregate_measured(self):
        contribs = [
            EvidenceContribution(dimension="grammar", raw_score=80.0, confidence=0.75, source_key="grammar_recognition"),
        ]
        result = aggregate_dimension_scores(contribs, "grammar")
        assert result.status == "measured"
        assert result.estimated_level in ("A2", "B1", "B2")
        assert result.evidence_count == 1
        assert result.needs_follow_up is False

    def test_aggregate_uncertain_from_contradiction(self):
        contribs = [
            EvidenceContribution(dimension="test", raw_score=85.0, confidence=0.8, source_key="a"),
            EvidenceContribution(dimension="test", raw_score=35.0, confidence=0.8, source_key="b"),
        ]
        result = aggregate_dimension_scores(contribs, "test")
        assert result.status == "uncertain"
        assert len(result.contradictions) > 0
        assert result.needs_follow_up is True


# ---------------------------------------------------------------------------
# Dimension registry completeness
# ---------------------------------------------------------------------------

class TestDimensionRegistry:
    def test_registry_contains_required_dimensions(self):
        required = {
            "grammar_recognition", "productive_grammar",
            "passive_vocabulary", "active_vocabulary",
            "reading_comprehension", "listening_comprehension",
            "visual_comprehension", "written_production",
            "narrative_coherence", "mediation",
            "communication_strategies", "confidence_and_anxiety",
            "spoken_production", "spoken_interaction",
            "pronunciation",
        }
        for dim in required:
            assert dim in DIMENSION_REGISTRY, f"Missing required dimension: {dim}"

    def test_registry_has_3_deferred(self):
        deferred = [k for k, v in DIMENSION_REGISTRY.items() if v["deferred"]]
        assert len(deferred) == 3
        assert "spoken_production" in deferred
        assert "spoken_interaction" in deferred
        assert "pronunciation" in deferred

    def test_all_dimensions_have_labels(self):
        for key, info in DIMENSION_REGISTRY.items():
            assert "label" in info, f"Dimension {key} missing label"
            assert "description" in info, f"Dimension {key} missing description"


# ---------------------------------------------------------------------------
# Item catalog completeness
# ---------------------------------------------------------------------------

class TestItemCatalog:
    def test_catalog_has_10_items(self):
        assert len(ITEM_CATALOG) == 10

    def test_all_items_have_scorers(self):
        for item in ITEM_CATALOG:
            assert item["key"] in ITEM_SCORERS, f"No scorer for {item['key']}"

    def test_all_scorers_have_catalog_entry(self):
        for key in ITEM_SCORERS:
            assert key in ITEM_CATALOG_BY_KEY, f"No catalog entry for scorer {key}"

    def test_each_item_has_dimension_weights(self):
        for item in ITEM_CATALOG:
            assert len(item["dimension_weights"]) >= 1, f"{item['key']} has no dimension_weights"

    def test_catalog_covers_all_active_dimensions(self):
        """At least one item measures each non-deferred dimension."""
        measured_dims = set()
        for item in ITEM_CATALOG:
            measured_dims.update(item["dimension_weights"].keys())

        non_deferred = {k for k, v in DIMENSION_REGISTRY.items() if not v["deferred"]}
        missing = non_deferred - measured_dims
        assert not missing, f"Dimensions not measured by any item: {missing}"


# ---------------------------------------------------------------------------
# Item scorer functions
# ---------------------------------------------------------------------------

class TestItemScorers:
    def test_grammar_scorer_correct(self):
        result = ITEM_SCORERS["grammar_recognition"]({"is_correct": True})
        assert len(result) == 2  # grammar + productive_grammar
        assert result[0].dimension == "grammar_recognition"
        assert result[0].raw_score == 80.0
        assert result[1].dimension == "productive_grammar"

    def test_grammar_scorer_incorrect(self):
        result = ITEM_SCORERS["grammar_recognition"]({"is_correct": False})
        assert result[0].raw_score == 45.0

    def test_vocabulary_scorer(self):
        result = ITEM_SCORERS["active_vocabulary"]({"correct_count": 4, "total_words": 5})
        assert len(result) == 2
        assert result[0].dimension == "active_vocabulary"
        assert result[0].raw_score == 80.0

    def test_reading_scorer(self):
        result = ITEM_SCORERS["reading_comprehension"]({"mc_correct": 3, "mc_total": 3})
        assert len(result) == 3
        dims = {c.dimension for c in result}
        assert "reading_comprehension" in dims
        assert "passive_vocabulary" in dims
        assert "grammar_recognition" in dims

    def test_listening_scorer_perfect(self):
        result = ITEM_SCORERS["listening_fallback"]({"q1_correct": True, "q2_correct": True})
        assert result[0].dimension == "listening_comprehension"
        assert result[0].raw_score == 75.0

    def test_listening_scorer_half(self):
        result = ITEM_SCORERS["listening_fallback"]({"q1_correct": True, "q2_correct": False})
        assert result[0].raw_score == 50.0

    def test_listening_scorer_none(self):
        result = ITEM_SCORERS["listening_fallback"]({"q1_correct": False, "q2_correct": False})
        assert result[0].raw_score == 30.0

    def test_visual_scorer_correct(self):
        result = ITEM_SCORERS["visual_comprehension"]({"selected_description": "park_scene", "expected_key": "park_scene", "has_detail": True})
        assert result[0].dimension == "visual_comprehension"
        assert result[0].raw_score > 80

    def test_productive_grammar_scorer(self):
        result = ITEM_SCORERS["productive_grammar"]({"correct_count": 2, "total": 3})
        assert len(result) == 2
        assert result[0].dimension == "productive_grammar"
        assert abs(result[0].raw_score - 66.7) < 1.0

    def test_mediation_scorer(self):
        result = ITEM_SCORERS["mediation"]({"has_key_points": True, "word_count": 40})
        assert len(result) == 2
        assert result[0].dimension == "mediation"
        assert result[0].raw_score > 50
        assert result[1].dimension == "communication_strategies"

    def test_confidence_scorer(self):
        result = ITEM_SCORERS["confidence_anxiety"]({"ratings": [4, 3, 5, 2]})
        assert len(result) == 1
        assert result[0].dimension == "confidence_and_anxiety"
        # Average = (4+3+5+2)/4 = 3.5, score = (3.5-1)/4*100 = 62.5
        assert abs(result[0].raw_score - 62.5) < 0.1


# ---------------------------------------------------------------------------
# compute_dimension_results integration
# ---------------------------------------------------------------------------

class TestComputeDimensionResults:
    def test_empty_contributions_all_not_measured(self):
        results = compute_dimension_results([])
        assert len(results) == len(DIMENSION_REGISTRY)
        for dim, result in results.items():
            assert result.status == "not_measured_yet"
            info = DIMENSION_REGISTRY[dim]
            if info["deferred"]:
                assert result.deferred is True
                assert result.needs_follow_up is False
            else:
                assert result.needs_follow_up is True

    def test_full_diagnostic_profile(self):
        """Simulate all 10 items with good responses."""
        contribs = []
        contribs.extend(ITEM_SCORERS["grammar_recognition"]({"is_correct": True}))
        contribs.extend(ITEM_SCORERS["active_vocabulary"]({"correct_count": 4, "total_words": 5}))
        contribs.extend(ITEM_SCORERS["written_production"]({"word_count": 35, "has_structure": True}))
        contribs.extend(ITEM_SCORERS["narrative_coherence"]({"correct_order": True}))
        contribs.extend(ITEM_SCORERS["reading_comprehension"]({"mc_correct": 3, "mc_total": 3}))
        contribs.extend(ITEM_SCORERS["listening_fallback"]({"q1_correct": True, "q2_correct": True}))
        contribs.extend(ITEM_SCORERS["visual_comprehension"]({"selected_description": "park_scene", "expected_key": "park_scene", "has_detail": True}))
        contribs.extend(ITEM_SCORERS["productive_grammar"]({"correct_count": 2, "total": 3}))
        contribs.extend(ITEM_SCORERS["mediation"]({"has_key_points": True, "word_count": 40}))
        contribs.extend(ITEM_SCORERS["confidence_anxiety"]({"ratings": [4, 3, 5, 2]}))

        results = compute_dimension_results(contribs)
        assert len(results) == len(DIMENSION_REGISTRY)

        # Active dimensions should be measured
        assert results["grammar_recognition"].status in ("measured", "uncertain")
        assert results["active_vocabulary"].status in ("measured",)
        assert results["reading_comprehension"].status in ("measured",)
        assert results["listening_comprehension"].status in ("measured",)
        assert results["visual_comprehension"].status in ("measured",)

        # Deferred dimensions should be not_measured_yet
        assert results["spoken_production"].status == "not_measured_yet"
        assert results["spoken_interaction"].status == "not_measured_yet"
        assert results["pronunciation"].status == "not_measured_yet"

    def test_no_single_global_level(self):
        """Verify no dimension is called 'overall' or 'global'."""
        for key in DIMENSION_REGISTRY:
            assert "overall" not in key
            assert "global" not in key


class TestLegacyAssessments:
    def test_legacy_assessments_empty(self):
        assert compute_legacy_assessments({}) == []

    def test_legacy_contains_only_measured(self):
        results = compute_dimension_results([])
        legacy = compute_legacy_assessments(results)
        for entry in legacy:
            assert entry["status"] in ("measured", "estimated")

    def test_legacy_uses_3band_cefr(self):
        """Legacy assessments should use the original 3-band for backward compat."""
        contribs = [EvidenceContribution(dimension="test", raw_score=80.0, confidence=0.8, source_key="test")]
        results = compute_dimension_results(contribs)
        legacy = compute_legacy_assessments(results)
        if legacy:
            # 80 with 3-band = A2, with extended = B2
            assert legacy[0]["cefr"] in ("A1", "A2", "B1")
