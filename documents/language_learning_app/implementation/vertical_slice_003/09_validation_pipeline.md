# 09 — Validation Pipeline (Vertical Slice 003)

## Pipeline Stages

```
Submission Text
    │
    ▼
Mock AI Analysis (deterministic)
    │
    ├── schema_valid=false ──► FAILED (downstream blocked)
    │
    ▼ schema_valid=true
Linguistic Validation
    │
    ├── failed ──► REJECTED
    │
    ▼ passed
Pedagogical Validation
    │
    ├── failed ──► REJECTED
    │
    ▼ passed
Policy Decision → COMPLETE / REJECT
```

## Linguistic Validation (6 checks)
1. output_consistency — all required fields present
2. issue_structure — each issue has code, severity, span, suggestion
3. severity_validity — severity is major/minor/info
4. span_validity — span is non-empty string
5. allowed_codes — issue code in allowed set
6. confidence_range — confidence between 0.0 and 1.0

## Pedagogical Validation (5 checks)
1. feedback_matches_goal — recommended_focus aligns with lesson goals
2. corrections_within_budget — major corrections ≤ contract limit
3. no_unsupported_mastery_claim — no "mastery" or "independent_use" in raw output
4. no_reward_command — no "reward" or "xp" in raw output
5. no_curriculum_mutation — no "curriculum" or "syllabus" in raw output

## Policy Decision
- Both validations pass → COMPLETE
- Linguistic fails → RETRY (if attempts remain)
- Pedagogical fails → REJECT
- Both fail → FAIL

## Verified
- All linguistic validation checks: PASSED
- All pedagogical validation checks: PASSED
- Malformed output handled: PASSED
- Failure audit events created: PASSED
- No false positives from "expansion" (XP substring): FIXED
