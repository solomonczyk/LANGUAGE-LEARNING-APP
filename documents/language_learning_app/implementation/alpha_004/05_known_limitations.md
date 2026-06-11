# 05 — Known Limitations

## Runtime Limitations

| # | Limitation | Impact | Status |
|---|-----------|--------|--------|
| L1 | Home screen loading state persists indefinitely when API data unavailable (no timeout → error fallback) | Loading spinner shows forever instead of error state | Minor |
| L2 | Result screen loading state similarly hangs without timeout | Loading spinner shows forever | Minor |
| L3 | Offline state not visually distinct from initial loading | Both show the same LoadingScreen component | Minor |
| L4 | Diagnostic writing step has hardcoded responses (is_correct: true, etc.) | No real interaction for grammar/vocab/coherence steps | Expected (MVP) |
| L5 | No lesson timeout — lesson session can stay ACTIVE indefinitely | Orphaned sessions possible | Minor |
| L6 | `lesson_duration_minutes` is a suggestion, not enforced | Lesson doesn't enforce time limit | Expected (MVP) |

## Mobile/Platform Limitations

| # | Limitation | Impact | Status |
|---|-----------|--------|--------|
| M1 | iOS native validation blocked on environment (no macOS) | Cannot test VoiceOver, iOS Safari, iPad | Environment blocker |
| M2 | Android native screenshots blocked (no emulator/ADB) | Cannot test TalkBack, physical device UX | Environment blocker |
| M3 | Screen reader compatibility not verified | VoiceOver/TalkBack untested | Environment blocker |
| M4 | Color contrast not measured with automated tools | Manual contrast check only | Environment blocker |
| M5 | Focus order on native platforms unchecked | Tab navigation ordering unverified | Environment blocker |

## Alpha Limitations

| # | Limitation | Impact | Status |
|---|-----------|--------|--------|
| A1 | Only mock AI available — no real LLM analysis | Analysis is predetermined, not adaptive | By design |
| A2 | Only one lesson type (personal narrative) | No variety in lesson types | By design (MVP) |
| A3 | Only CEFR assessment with mock scoring | Diagnosis uses simplified mock logic | By design |
| A4 | No session persistence across browser restart | Local state lost on browser close | Known (MVP) |
| A5 | No user authentication beyond stub | All users are "local_learner" by default | Known (MVP) |
| A6 | No production deployment | alpha is local-only | By design |
| A7 | 3–5 testers only | Limited feedback coverage | By design (closed alpha) |

## Trust/Safety Limitations

| # | Limitation | Impact | Status |
|---|-----------|--------|--------|
| S1 | Mastery evidence is automatically created on COMPLETE — no separate learner confirmation | Learner may not be aware of evidence recording | Minor |
| S2 | No data deletion endpoint | Cannot delete learner data via API | Minor (MVP) |
| S3 | No explicit consent collection beyond "Start Learning!" | Consent is implicit | Minor (MVP) |
| S4 | Reward authority uses mock values | No meaningful reward calculation | By design |

## Technical Debt

| # | Item | Impact | Status |
|---|------|--------|--------|
| T1 | `process_lesson_session` is a single large function doing orchestration + validation + recording | Hard to test, maintain, or extend | Accepted |
| T2 | Diagnostic responses bypass user interaction (hardcoded correct answers) | Diagnostic is a simulation, not real assessment | Accepted (MVP) |
| T3 | No E2E test for mobile app (only backend integration tests) | Mobile UX bugs may not be caught | Accepted |

---

*Created: 2026-06-11*
