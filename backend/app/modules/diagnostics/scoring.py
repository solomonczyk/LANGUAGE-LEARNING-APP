"""Multidimensional diagnostic scoring engine.

Declarative dimension registry, item catalog, per-item scorer functions,
evidence aggregation, contradiction detection, and CEFR level calculation.

Every public function in this module is pure (no DB, no I/O) and fully
deterministic.
"""

from __future__ import annotations

from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


class EvidenceContribution(BaseModel):
    """A single piece of scored evidence from one diagnostic item."""

    dimension: str
    raw_score: float
    confidence: float
    source_key: str


class DimensionResult(BaseModel):
    """Aggregated result for one language dimension."""

    raw_score: float | None = None
    estimated_level: str = "not_measured_yet"
    confidence: float = 0.0
    evidence_count: int = 0
    contradictions: list[str] = []
    needs_follow_up: bool = True
    status: str = "not_measured_yet"  # measured | estimated | uncertain | not_measured_yet
    deferred: bool = False


# ---------------------------------------------------------------------------
# Dimension registry — every dimension the app tracks
# ---------------------------------------------------------------------------

DIMENSION_REGISTRY: dict[str, dict] = {
    "grammar_recognition": {
        "label": "Grammar Recognition",
        "description": "Ability to recognise correct grammar patterns",
        "cefr_range": ["A1", "A2", "B1", "B2"],
        "deferred": False,
    },
    "productive_grammar": {
        "label": "Productive Grammar",
        "description": "Ability to produce grammatically correct sentences",
        "cefr_range": ["A1", "A2", "B1", "B2"],
        "deferred": False,
    },
    "passive_vocabulary": {
        "label": "Passive Vocabulary",
        "description": "Ability to recognise and understand words",
        "cefr_range": ["A1", "A2", "B1", "B2", "C1"],
        "deferred": False,
    },
    "active_vocabulary": {
        "label": "Active Vocabulary",
        "description": "Ability to recall and use words correctly",
        "cefr_range": ["A1", "A2", "B1", "B2"],
        "deferred": False,
    },
    "reading_comprehension": {
        "label": "Reading Comprehension",
        "description": "Ability to understand written passages",
        "cefr_range": ["A1", "A2", "B1", "B2", "C1"],
        "deferred": False,
    },
    "listening_comprehension": {
        "label": "Listening Comprehension",
        "description": "Ability to understand spoken language",
        "cefr_range": ["A1", "A2", "B1", "B2"],
        "deferred": False,
    },
    "visual_comprehension": {
        "label": "Visual Comprehension",
        "description": "Ability to interpret visual scenes and describe them",
        "cefr_range": ["A1", "A2", "B1"],
        "deferred": False,
    },
    "written_production": {
        "label": "Written Production",
        "description": "Ability to produce written language",
        "cefr_range": ["A1", "A2", "B1", "B2"],
        "deferred": False,
    },
    "narrative_coherence": {
        "label": "Narrative Coherence",
        "description": "Ability to structure events in a logical order",
        "cefr_range": ["A1", "A2", "B1", "B2"],
        "deferred": False,
    },
    "mediation": {
        "label": "Mediation",
        "description": "Ability to explain or rephrase information for others",
        "cefr_range": ["A1", "A2", "B1", "B2"],
        "deferred": False,
    },
    "communication_strategies": {
        "label": "Communication Strategies",
        "description": "Ability to use strategies to maintain communication",
        "cefr_range": ["A1", "A2", "B1", "B2"],
        "deferred": False,
    },
    "confidence_and_anxiety": {
        "label": "Confidence & Anxiety",
        "description": "Self-reported confidence and language anxiety levels",
        "cefr_range": ["A1", "A2", "B1"],
        "deferred": False,
    },
    "spoken_production": {
        "label": "Spoken Production",
        "description": "Ability to produce spoken language (not assessed here)",
        "cefr_range": ["A1", "A2", "B1", "B2", "C1", "C2"],
        "deferred": True,
    },
    "spoken_interaction": {
        "label": "Spoken Interaction",
        "description": "Ability to engage in dialogue (not assessed here)",
        "cefr_range": ["A1", "A2", "B1", "B2", "C1", "C2"],
        "deferred": True,
    },
    "pronunciation": {
        "label": "Pronunciation",
        "description": "Pronunciation accuracy (not assessed here)",
        "cefr_range": ["A1", "A2", "B1", "B2"],
        "deferred": True,
    },
}


# ---------------------------------------------------------------------------
# Item catalog — each diagnostic item's metadata and scoring rules
# ---------------------------------------------------------------------------

CATALOG_ITEM = {
    "key": "",
    "type": "",          # multiple_choice | matching | writing | ordering | passage | transcript | visual | sentence_rewrite | mediation | self_assessment
    "prompt": "",
    "estimated_seconds": 0,
    "dimension_weights": {},  # dimension_name -> weight (1.0 = primary, 0.3-0.5 = secondary)
}

ITEM_CATALOG: list[dict] = [
    {
        "key": "grammar_recognition",
        "type": "multiple_choice",
        "prompt": "Which sentence is correct?",
        "estimated_seconds": 90,
        "dimension_weights": {"grammar_recognition": 1.0, "productive_grammar": 0.3},
    },
    {
        "key": "active_vocabulary",
        "type": "matching",
        "prompt": "Select the correct meaning for each word.",
        "estimated_seconds": 150,
        "dimension_weights": {"active_vocabulary": 1.0, "passive_vocabulary": 0.5},
    },
    {
        "key": "written_production",
        "type": "writing",
        "prompt": "Write 2-3 sentences about your morning routine.",
        "estimated_seconds": 180,
        "dimension_weights": {"written_production": 1.0, "productive_grammar": 0.4},
    },
    {
        "key": "narrative_coherence",
        "type": "ordering",
        "prompt": "Tap each event in the correct order.",
        "estimated_seconds": 120,
        "dimension_weights": {"narrative_coherence": 1.0},
    },
    {
        "key": "reading_comprehension",
        "type": "passage",
        "prompt": "Read the passage and answer the questions.",
        "estimated_seconds": 180,
        "dimension_weights": {
            "reading_comprehension": 1.0,
            "passive_vocabulary": 0.4,
            "grammar_recognition": 0.3,
        },
    },
    {
        "key": "listening_fallback",
        "type": "transcript",
        "prompt": "Read the conversation below and answer the questions.",
        "estimated_seconds": 90,
        "dimension_weights": {"listening_comprehension": 1.0},
    },
    {
        "key": "visual_comprehension",
        "type": "visual",
        "prompt": "Read the scene description and choose the best answer.",
        "estimated_seconds": 90,
        "dimension_weights": {"visual_comprehension": 1.0},
    },
    {
        "key": "productive_grammar",
        "type": "sentence_rewrite",
        "prompt": "Rewrite the full sentence correctly.",
        "estimated_seconds": 120,
        "dimension_weights": {"productive_grammar": 1.0, "grammar_recognition": 0.4},
    },
    {
        "key": "mediation",
        "type": "mediation",
        "prompt": "Read the message and explain it simply.",
        "estimated_seconds": 120,
        "dimension_weights": {"mediation": 1.0, "communication_strategies": 0.5},
    },
    {
        "key": "confidence_anxiety",
        "type": "self_assessment",
        "prompt": "Rate your confidence in these language situations.",
        "estimated_seconds": 60,
        "dimension_weights": {"confidence_and_anxiety": 1.0},
    },
]

# Fast lookup
ITEM_CATALOG_BY_KEY = {item["key"]: item for item in ITEM_CATALOG}


# ---------------------------------------------------------------------------
# CEFR calculation
# ---------------------------------------------------------------------------


def _calculate_cefr(score: float) -> str:
    """Original 3-band CEFR mapping for backward compatibility."""
    if score >= 85:
        return "B1"
    if score >= 65:
        return "A2"
    return "A1"


def _calculate_cefr_extended(score: float | None) -> str:
    """Full 6-band CEFR mapping.

    Used for the new multidimensional profile.  None → not_measured_yet.
    """
    if score is None:
        return "not_measured_yet"
    if score >= 96:
        return "C2"
    if score >= 86:
        return "C1"
    if score >= 71:
        return "B2"
    if score >= 51:
        return "B1"
    if score >= 31:
        return "A2"
    return "A1"


CEFR_LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2", "not_measured_yet"]


# ---------------------------------------------------------------------------
# Item scorer functions
# Each returns list[EvidenceContribution] for the dimensions it measures.
# ---------------------------------------------------------------------------


def _score_grammar_recognition(response_data: dict) -> list[EvidenceContribution]:
    correct = response_data.get("is_correct", False)
    score = 80.0 if correct else 45.0
    conf = 0.75
    return [
        EvidenceContribution(dimension="grammar_recognition", raw_score=score, confidence=conf, source_key="grammar_recognition"),
        EvidenceContribution(dimension="productive_grammar", raw_score=score * 0.6, confidence=conf * 0.8, source_key="grammar_recognition"),
    ]


def _score_active_vocabulary(response_data: dict) -> list[EvidenceContribution]:
    correct_count = response_data.get("correct_count", 0)
    total_words = response_data.get("total_words", 5)
    ratio = correct_count / max(total_words, 1)
    score = ratio * 100
    conf = 0.8
    return [
        EvidenceContribution(dimension="active_vocabulary", raw_score=score, confidence=conf, source_key="active_vocabulary"),
        EvidenceContribution(dimension="passive_vocabulary", raw_score=score * 0.85, confidence=conf * 0.85, source_key="active_vocabulary"),
    ]


def _score_written_production(response_data: dict) -> list[EvidenceContribution]:
    word_count = response_data.get("word_count", 0)
    has_structure = response_data.get("has_structure", False)
    score = 50.0
    if word_count >= 20:
        score += 20.0
    if has_structure:
        score += 15.0
    score = min(score, 100)
    conf = 0.65
    return [
        EvidenceContribution(dimension="written_production", raw_score=score, confidence=conf, source_key="written_production"),
        EvidenceContribution(dimension="productive_grammar", raw_score=score * 0.7, confidence=conf * 0.8, source_key="written_production"),
    ]


def _score_narrative_coherence(response_data: dict) -> list[EvidenceContribution]:
    correct_order = response_data.get("correct_order", False)
    score = 85.0 if correct_order else 40.0
    conf = 0.7
    return [
        EvidenceContribution(dimension="narrative_coherence", raw_score=score, confidence=conf, source_key="narrative_coherence"),
    ]


def _score_reading_comprehension(response_data: dict) -> list[EvidenceContribution]:
    mc_correct = response_data.get("mc_correct", 0)
    mc_total = response_data.get("mc_total", 3)
    ratio = mc_correct / max(mc_total, 1)
    score = ratio * 100
    conf = 0.7
    return [
        EvidenceContribution(dimension="reading_comprehension", raw_score=score, confidence=conf, source_key="reading_comprehension"),
        EvidenceContribution(dimension="passive_vocabulary", raw_score=score * 0.8, confidence=conf * 0.75, source_key="reading_comprehension"),
        EvidenceContribution(dimension="grammar_recognition", raw_score=score * 0.7, confidence=conf * 0.7, source_key="reading_comprehension"),
    ]


def _score_listening_fallback(response_data: dict) -> list[EvidenceContribution]:
    q1_correct = response_data.get("q1_correct", False)
    q2_correct = response_data.get("q2_correct", False)
    correct_count = (1 if q1_correct else 0) + (1 if q2_correct else 0)
    if correct_count == 2:
        score = 75.0
    elif correct_count == 1:
        score = 50.0
    else:
        score = 30.0
    conf = 0.5  # Reduced due to text fallback
    return [
        EvidenceContribution(dimension="listening_comprehension", raw_score=score, confidence=conf, source_key="listening_fallback"),
    ]


def _score_visual_comprehension(response_data: dict) -> list[EvidenceContribution]:
    selected = response_data.get("selected_description", "")
    expected = response_data.get("expected_key", "")
    has_detail = response_data.get("has_detail", False)
    correct = bool(selected) and (not expected or selected == expected)
    score = 75.0 if correct else 45.0
    if has_detail:
        score = min(score + 10, 100)
    conf = 0.6
    return [
        EvidenceContribution(dimension="visual_comprehension", raw_score=score, confidence=conf, source_key="visual_comprehension"),
    ]


def _score_productive_grammar(response_data: dict) -> list[EvidenceContribution]:
    correct_count = response_data.get("correct_count", 0)
    total = response_data.get("total", 3)
    ratio = correct_count / max(total, 1)
    score = ratio * 100
    conf = 0.7
    return [
        EvidenceContribution(dimension="productive_grammar", raw_score=score, confidence=conf, source_key="productive_grammar"),
        EvidenceContribution(dimension="grammar_recognition", raw_score=score * 0.8, confidence=conf * 0.85, source_key="productive_grammar"),
    ]


def _score_mediation(response_data: dict) -> list[EvidenceContribution]:
    has_key_points = response_data.get("has_key_points", False)
    word_count = response_data.get("word_count", 0)
    # Composite: key_points (50 points) + word_count contribution (50 points)
    key_score = 50.0 if has_key_points else 15.0
    word_ratio = min(word_count / 30, 1.0)
    word_score = word_ratio * 50
    score = min(key_score + word_score, 100)
    conf = 0.6
    return [
        EvidenceContribution(dimension="mediation", raw_score=score, confidence=conf, source_key="mediation"),
        EvidenceContribution(dimension="communication_strategies", raw_score=score * 0.8, confidence=conf * 0.8, source_key="mediation"),
    ]


def _score_confidence_anxiety(response_data: dict) -> list[EvidenceContribution]:
    ratings = response_data.get("ratings", [3, 3, 3, 3])
    if not ratings:
        ratings = [3, 3, 3, 3]
    average = sum(ratings) / len(ratings)
    # Invert Likert: 5 (most confident) → 100, 1 (least confident) → 0
    score = ((average - 1) / 4) * 100
    conf = 0.5  # Self-assessment — inherently limited
    return [
        EvidenceContribution(dimension="confidence_and_anxiety", raw_score=score, confidence=conf, source_key="confidence_anxiety"),
    ]


# Registry of all scorer functions
ITEM_SCORERS: dict[str, callable] = {
    "grammar_recognition": _score_grammar_recognition,
    "active_vocabulary": _score_active_vocabulary,
    "written_production": _score_written_production,
    "narrative_coherence": _score_narrative_coherence,
    "reading_comprehension": _score_reading_comprehension,
    "listening_fallback": _score_listening_fallback,
    "visual_comprehension": _score_visual_comprehension,
    "productive_grammar": _score_productive_grammar,
    "mediation": _score_mediation,
    "confidence_anxiety": _score_confidence_anxiety,
}


# ---------------------------------------------------------------------------
# Evidence aggregation
# ---------------------------------------------------------------------------


def _aggregate_confidence(confidences: list[float]) -> float:
    """Combined probability at least one estimate is reliable.

    Uses: 1 - product(1 - c_i), capped at 0.95.
    """
    if not confidences:
        return 0.0
    combined = 1.0
    for c in confidences:
        combined *= 1.0 - min(max(c, 0.0), 1.0)
    return min(1.0 - combined, 0.95)


def _detect_contradictions(contributions: list[EvidenceContribution]) -> list[str]:
    """Check if evidence sources disagree by more than 20 points."""
    if len(contributions) < 2:
        return []
    scores = [c.raw_score for c in contributions]
    contradictions = []
    for i in range(len(scores)):
        for j in range(i + 1, len(scores)):
            if abs(scores[i] - scores[j]) > 20:
                contradictions.append(
                    f"{contributions[i].source_key}({scores[i]:.0f}) vs "
                    f"{contributions[j].source_key}({scores[j]:.0f})"
                )
    return contradictions


def aggregate_dimension_scores(
    contributions: list[EvidenceContribution],
    dimension_name: str,
) -> DimensionResult:
    """Aggregate all evidence contributions for a single dimension."""
    registry = DIMENSION_REGISTRY.get(dimension_name, {})
    deferred = registry.get("deferred", False)

    if not contributions:
        return DimensionResult(
            estimated_level="not_measured_yet",
            status="not_measured_yet",
            needs_follow_up=not deferred,
            deferred=deferred,
        )

    # Weighted average using evidence weights from the item catalog
    total_weight = 0.0
    weighted_sum = 0.0
    confidences: list[float] = []
    for c in contributions:
        item = ITEM_CATALOG_BY_KEY.get(c.source_key, {})
        weights = item.get("dimension_weights", {})
        weight = weights.get(dimension_name, 0.5)
        weighted_sum += c.raw_score * c.confidence * weight
        total_weight += c.confidence * weight
        confidences.append(c.confidence)

    raw_score = weighted_sum / total_weight if total_weight > 0 else 0.0
    confidence = _aggregate_confidence(confidences)
    contradictions = _detect_contradictions(contributions)

    # Determine status
    if contradictions:
        status = "uncertain"
        needs_follow_up = True
    elif confidence >= 0.5:
        status = "measured"
        needs_follow_up = False
    else:
        status = "estimated"
        needs_follow_up = confidence < 0.5

    return DimensionResult(
        raw_score=round(raw_score, 1),
        estimated_level=_calculate_cefr_extended(raw_score),
        confidence=round(confidence, 3),
        evidence_count=len(contributions),
        contradictions=contradictions,
        needs_follow_up=needs_follow_up,
        status=status,
        deferred=deferred,
    )


def compute_dimension_results(
    all_contributions: list[EvidenceContribution],
) -> dict[str, DimensionResult]:
    """Produce a complete multidimensional profile.

    Every dimension in DIMENSION_REGISTRY appears in the result.
    Dimensions with no evidence get status="not_measured_yet".
    """
    # Group contributions by dimension
    grouped: dict[str, list[EvidenceContribution]] = {}
    for c in all_contributions:
        grouped.setdefault(c.dimension, []).append(c)

    # Compute result for each registered dimension
    results: dict[str, DimensionResult] = {}
    for dim_name in DIMENSION_REGISTRY:
        contributions = grouped.get(dim_name, [])
        results[dim_name] = aggregate_dimension_scores(contributions, dim_name)

    return results


def compute_legacy_assessments(
    dimension_results: dict[str, DimensionResult],
) -> list[dict]:
    """Build the backward-compatible 'assessments' array.

    Only includes dimensions with status in (measured, estimated).
    Uses the original 3-band CEFR for compatibility.
    """
    assessments = []
    for dim_name, result in dimension_results.items():
        if result.status in ("measured", "estimated"):
            assessments.append({
                "skill": dim_name,
                "cefr": _calculate_cefr(result.raw_score) if result.raw_score is not None else "A1",
                "confidence": result.confidence,
                "status": result.status,
                "needs_follow_up": result.needs_follow_up,
            })
    return assessments
