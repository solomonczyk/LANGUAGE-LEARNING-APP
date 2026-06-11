# 08 — Mock AI Gateway (Vertical Slice 003)

## Overview
Deterministic mock AI analysis for local development. No real LLM calls.

## Configuration
- `MOCK_AI_ENABLED=true` — enables mock gateway
- `MOCK_AI_FIXTURE_MODE=valid` — returns well-formed analysis
- `MOCK_AI_FIXTURE_MODE=malformed` — returns intentionally invalid output

## Deterministic Fixtures
Three fixtures selected by text content:
1. **cat_pet** — triggered by "cat", "pet", "dog"
2. **morning_routine** — triggered by "morning", "wake", "breakfast"
3. **generic** — fallback for all other text

## Fixture Structure
```json
{
  "analysis_version": "mock-v1",
  "meaning_preserved": true,
  "detected_issues": [
    {
      "code": "VERB_FORM",
      "severity": "major",
      "span": "...",
      "suggestion": "..."
    }
  ],
  "strengths": ["..."],
  "recommended_focus": ["..."],
  "confidence": 0.91
}
```

## Malformed Output
```json
{
  "analysis_version": "mock-v1",
  "detected_issues": "malformed",  // Should be list
  "strengths": null,               // Should not be null
  "confidence": "high"             // Should be float
}
```

## Flow
1. Submission text received
2. AIAnalysisRequest created (status: RUNNING)
3. Fixture selected deterministically
4. AIAnalysisResult stored (schema_valid: true/false)
5. If malformed → schema_valid=false → downstream blocked
6. If valid → linguistic validation → pedagogical validation → policy

## Verified
- Deterministic fixture selection: PASSED (7 unit tests)
- All fixture fields valid: PASSED
- Malformed output detected: PASSED
- No randomness: PASSED
- DB persistence of requests/results: PASSED
