# Short Alpha Recheck Plan

## Purpose

Run a controlled recheck with 3 synthetic profiles to verify that:
1. Diagnostic demo confusion is fixed
2. A1 contract wording is simplified
3. Lesson wording is level-aware
4. Mock feedback is level-aware
5. Full learner flow completes without blockers

## Synthetic Profiles

| ID | Level | Type | Self-Reported |
|----|-------|------|---------------|
| ALPHA-006-A1 | A1 | beginner | A1 |
| ALPHA-006-A2 | A2 | returning_low | A2 |
| ALPHA-006-B1 | B1 | work_focused | B1 |

## Flow Steps

Each profile must complete:
1. Root (health check)
2. Onboarding (register + create profile)
3. Diagnostic (4-step flow)
4. Learning contract (create + display)
5. Home (display + lesson card)
6. Lesson (open + level-aware content)
7. Submission (write + submit)
8. Mock feedback (analysis + feedback)
9. Result (display level-aware feedback)
10. Home return

## Acceptance Criteria

| Metric | Target |
|--------|--------|
| Profiles total | 3 |
| Profiles completed | 3 |
| Critical issues | 0 |
| Major blocking issues | 0 |
| Minor issues | 0 |
| Diagnostic confusion | false (all profiles) |
| Contract understood | true (all profiles) |
| Lesson understood | true (all profiles) |
| Feedback understood | true (all profiles) |

## Data Collection

For each profile:
- Full flow timestamps
- API responses at each step
- Assessment CEFR results
- Lesson analysis results
- Audit events
- Operator notes
