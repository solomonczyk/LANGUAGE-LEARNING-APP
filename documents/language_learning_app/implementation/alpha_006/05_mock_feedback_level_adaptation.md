# Mock Feedback Level Adaptation

## Purpose

Make mock AI feedback level-adaptive so A1 learners receive simple, supportive feedback while B2 learners receive nuanced, style-focused feedback.

## Backend Changes

### AI Gateway (`backend/app/modules/ai_gateway/services.py`)

**New function**: `_adapt_fixture_by_level(fixture, learner_level)`

This function modifies the base fixture output based on the learner's CEFR level:

#### A1 Adaptation
- Reduces to 1 correction maximum
- All corrections marked as "minor" severity
- Single supportive strength ("Good job! You are sharing your ideas.")
- 1 recommended focus item
- Confidence adjusted to 0.85 (supportive)

#### A2 Adaptation
- Up to 2 corrections
- Encouraging strengths
- Short, clear correction suggestions
- Confidence at 0.82

#### B1 Adaptation
- All original corrections preserved
- More precise feedback phrasing with "Consider using:" prefix
- Grammar + vocabulary specific strengths
- Full recommended focus items

#### B2 Adaptation
- All original corrections preserved with "For more natural phrasing, try:" prefix
- Stylistic precision strengths
- Additional recommended focus: "Natural collocation", "Stylistic precision"
- Higher confidence at 0.92

**Updated function**: `_select_fixture(text, learner_level)`

Now accepts a `learner_level` parameter (default "A2") and calls `_adapt_fixture_by_level()` after selecting the base fixture.

### Lesson Engine (`backend/app/modules/lesson_engine/services.py`)

**Changed**: The `process_lesson_session()` function now reads the learner's `self_reported_level` from the `LearnerProfile` model and passes it to `analyze_submission()`. Previously this was hardcoded as `"A2"`.

## Frontend Changes

### Result Screen (`mobile/app/result/[id].tsx`)

**Added**: Fetching the learning contract to determine learner level. Added `getLevelFeedback(level)` function that returns level-appropriate feedback content:

- **A1**: "Good effort!" intro, 1 strength, 1 correction ("Small suggestion"), simplified improvement text
- **A2**: "You did well!" intro, 2 strengths, 1-2 corrections, standard improvement text
- **B1**: "Good progress." intro, detailed strengths, 2+ corrections with precise language
- **B2**: "Refinements" section title, nuanced corrections with naturalness focus, style observation

**Level-appropriate labels**:
- "Great work!" vs "Lesson Complete!"
- "What you did well" vs "Strengths"  
- "Check results" vs "Validation Result"
- "Language check" vs "Linguistic Check"

## Version

- Analysis version bumped from "mock-v1" to "mock-v2-level-aware" to distinguish level-aware fixtures
- All existing tests updated for new version string
- Added 4 new tests for level-awareness behavior

## Verification

| Criterion | Status |
|-----------|--------|
| A1 feedback not overwhelming | True — 1 correction max, all minor |
| A2 feedback clear and short | True — 2 corrections max, encouraging |
| B1 feedback more precise | True — grammar + vocabulary detail |
| B2 feedback nuanced | True — natural collocation, style focus |
| Feedback remains supportive | True — strengths shown first at all levels |
