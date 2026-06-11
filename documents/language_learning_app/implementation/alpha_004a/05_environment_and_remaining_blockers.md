# Environment and Remaining Blockers — Alpha 004A

## Infrastructure

| Component | Status | Notes |
|-----------|--------|-------|
| PostgreSQL 16 | ✓ Running (Docker) | Container healthy |
| Backend API | ✓ Running (Docker) | Port 8000 |
| Expo Web | ✓ Running | Port 8081 |
| Mock AI Gateway | ✓ Active | Valid fixture mode |
| Real AI Provider | ✗ NOT connected | By design |
| Staging | ✗ NOT deployed | By design |
| Production | ✗ NOT deployed | By design |

## Remaining Blockers

### Native Mobile Platforms (Environment Blockers)

These are environment limitations, not code issues:

- **iOS Simulator**: Not available on Windows. Cannot verify native iOS rendering or gesture handling.
- **Android Emulator**: Not available. Cannot verify native Android rendering.
- **Physical Devices**: Cannot be tested from this environment.
- **Screen Reader / Accessibility**: Not tested. Relies on Expo/React Native defaults.
- **Color Contrast**: Not measured with automation tools.

### Known Limitations (from Layer 003/004)

- Auth is entirely stub-based (X-User-Id header). No JWT, no real auth.
- All AI analysis uses mock fixtures. No real LLM calls.
- Single user flow (local_learner). No multi-user data isolation testing.
- No offline support. Requires network connectivity.

## Closed Learner Alpha Readiness

All runtime blockers fixed. The full learner journey works end-to-end in Expo Web:

1. ✅ Root route → onboarding
2. ✅ Onboarding → register + profile
3. ✅ Profile → diagnostic
4. ✅ Diagnostic assessments → completed
5. ✅ Diagnostic → learning contract (auto-created)
6. ✅ Contract → home dashboard
7. ✅ Home → lesson session
8. ✅ Lesson → submit text
9. ✅ Submission → processing pipeline
10. ✅ Processing → validation + completion
11. ✅ Completion → result + mastery evidence

The app is ready for closed learner alpha **on Expo Web**.
Native mobile platforms require additional environment setup.
