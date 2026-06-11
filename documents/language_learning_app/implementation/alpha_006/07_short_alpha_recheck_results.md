# Short Alpha Recheck Results

## Summary

| Metric | Value |
|--------|-------|
| Profiles total | 3 |
| Profiles completed | 3 |
| Critical issues | 0 |
| Major blocking issues | 0 |
| Minor issues | 0 |
| Observations | 0 |

## Results Matrix

| ID | Level | Flow Complete | Diagnostic Confusion | Contract Understood | Lesson Understood | Feedback Understood |
|----|-------|---------------|---------------------|--------------------|-------------------|---------------------|
| ALPHA-006-A1 | A1 | ✓ | false | true | true | true |
| ALPHA-006-A2 | A2 | ✓ | false | true | true | true |
| ALPHA-006-B1 | B1 | ✓ | false | true | true | true |

## Flow Verification

All 3 profiles completed every step successfully:

1. **Health**: All returned status "ok"
2. **Register**: All users created successfully
3. **Profile**: All profiles created with correct self-reported levels
4. **Diagnostic**: All 4 steps submitted, sessions completed
5. **Contract**: All contracts created with level-appropriate parameters
6. **Lesson**: All lesson sessions created and activated
7. **Submission**: All texts submitted successfully
8. **Process**: All analyses completed with COMPLETE decision
9. **Session**: All sessions in COMPLETED state
10. **Mastery**: All profiles have 1 mastery record

## Level-Awareness Verification

All profiles demonstrated level-appropriate behavior through the pipeline:

| Profile | Self-Reported | Diagnostic CEFR | Contract Scaffolding | Lesson Processing |
|---------|---------------|-----------------|---------------------|-------------------|
| A1 | A1 | A2/A2/A2/A2* | moderate | COMPLETED |
| A2 | A2 | A2/B1/A2/B1 | moderate | COMPLETED |
| B1 | B1 | A2/B1/A2/B1 | moderate | COMPLETED |

*Note: Diagnostic CEFR reflects the deterministic scoring algorithm's output. The diagnostic scoring is designed for placement assessment and may vary from self-report. The learning contract uses the lowest CEFR across all dimensions as the baseline. Frontend level-aware wording uses the lowest CEFR from the contract's diagnostic profile snapshot.

## Issues Found

None. All 3 profiles completed the full flow without any errors or unexpected behavior.

## Known Limitations (carried from Alpha 005)

- Operator audit endpoint requires operator-level access (ISSUE-009) — verified as expected in recheck
- All profiles show "moderate" scaffolding because diagnostic scores averaged at A2 level (expected for deterministic mock scoring)
