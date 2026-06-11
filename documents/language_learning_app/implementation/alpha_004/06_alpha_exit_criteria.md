# 06 — Alpha Exit Criteria

## Definition

The closed alpha is considered complete when ALL of the following criteria are met. If ANY criterion is not met, the alpha must be extended or rejected.

## Mandatory Exit Criteria

### 1. Runtime Stability
- [ ] Backend starts and stays healthy for the duration of all test sessions
- [ ] PostgreSQL migrations are current and stable
- [ ] No database connection errors during test sessions
- [ ] Docker compose up/down cycle passes cleanly

### 2. Learner Journey Completeness
- [ ] T1 completes full journey: onboarding → result → home
- [ ] T2 completes full journey with different profile settings
- [ ] All 16 journey steps are reachable and functional
- [ ] No step produces an unhandled error

### 3. Test Results
- [ ] Backend unit tests: 109 passed, 0 failed
- [ ] Backend integration tests: all passed
- [ ] Mobile TypeScript typecheck: 0 errors
- [ ] OpenAPI contract valid

### 4. UX Quality
- [ ] No critical UX blockers (see classification below)
- [ ] All CTA buttons visible and functional
- [ ] Error states show understandable messages
- [ ] Loading states show meaningful indicators
- [ ] Keyboard does not hide text input
- [ ] Text readable at 200% browser zoom

### 5. Deterministic Correctness
- [ ] Same input produces same result (deterministic analysis)
- [ ] State machine transitions are reproducible
- [ ] No randomness in analysis or validation
- [ ] Mock AI fixtures return consistent output

### 6. Audit Integrity
- [ ] DIAGNOSTIC_STARTED events recorded
- [ ] DIAGNOSTIC_COMPLETED events recorded
- [ ] LESSON_COMPLETED events recorded
- [ ] No audit events can be deleted via API

### 7. Security Gates
- [ ] Cross-user data access blocked
- [ ] User ID in request body is ignored
- [ ] Malformed payload rejected
- [ ] Unknown resource returns 404

### 8. Anti-Cheat
- [ ] Duplicate submission with idempotency key is safe
- [ ] Cannot complete lesson without submission
- [ ] Cannot submit empty or too-short text (< 10 chars)

## Issue Classification

### Blocker (alpha fails)
- Cannot complete the full learner journey
- Test suite regression (new failures)
- Cross-user data leak
- Fake completion state
- Broken navigation between required screens
- Processing pipeline hangs indefinitely
- Data loss on normal operation

### Non-blocking (alpha passes with notes)
- Minor visual alignment issues
- Loading animation not perfectly smooth
- Incomplete (but not broken) error messages
- Missing transition animations
- Browser-specific minor rendering difference

## Pass/Fail Decision

| Criterion | Weight | Status |
|-----------|--------|--------|
| Runtime stability | BLOCKER | [ ] PASS [ ] FAIL |
| Learner journey | BLOCKER | [ ] PASS [ ] FAIL |
| Test results | BLOCKER | [ ] PASS [ ] FAIL |
| UX (no critical blockers) | BLOCKER | [ ] PASS [ ] FAIL |
| Deterministic correctness | BLOCKER | [ ] PASS [ ] FAIL |
| Audit integrity | BLOCKER | [ ] PASS [ ] FAIL |
| Security gates | BLOCKER | [ ] PASS [ ] FAIL |
| Anti-cheat | BLOCKER | [ ] PASS [ ] FAIL |

**Final verdict:**
- [ ] **PASS** — All blocker criteria met, non-blocking issues documented
- [ ] **FAIL** — One or more blocker criteria not met
- [ ] **EXTEND** — Most criteria met but additional testing needed

---

*Created: 2026-06-11*
