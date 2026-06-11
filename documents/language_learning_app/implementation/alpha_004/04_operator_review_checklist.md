# 04 — Operator Review Checklist

## Overview

This checklist is completed by the operator (project maintainer) for each alpha platform before accepting the alpha candidate. The operator review is mandatory.

## Visual Review

| # | Check | Result | Notes |
|---|-------|--------|-------|
| V1 | Onboarding screen renders correctly | [ ] PASS [ ] FAIL | |
| V2 | Diagnostic screen renders correctly | [ ] PASS [ ] FAIL | |
| V3 | Learning Contract screen renders correctly | [ ] PASS [ ] FAIL | |
| V4 | Home/Dashboard screen renders correctly | [ ] PASS [ ] FAIL | |
| V5 | Lesson screen renders correctly | [ ] PASS [ ] FAIL | |
| V6 | Processing/Lesson Session screen renders correctly | [ ] PASS [ ] FAIL | |
| V7 | Result screen renders correctly | [ ] PASS [ ] FAIL | |
| V8 | All CTA buttons visible and labeled | [ ] PASS [ ] FAIL | |
| V9 | Text input areas visible and usable | [ ] PASS [ ] FAIL | |
| V10 | No text clipping or overflow | [ ] PASS [ ] FAIL | |

## Flow Review

| # | Check | Result | Notes |
|---|-------|--------|-------|
| F1 | Onboarding → Profile → Diagnostic flow works | [ ] PASS [ ] FAIL | |
| F2 | Diagnostic → Contract → Home flow works | [ ] PASS [ ] FAIL | |
| F3 | Home → Lesson → Processing → Result flow works | [ ] PASS [ ] FAIL | |
| F4 | Result → Back to Home navigation works | [ ] PASS [ ] FAIL | |
| F5 | Lesson submission creates submission in backend | [ ] PASS [ ] FAIL | |
| F6 | Processing completes with COMPLETED status | [ ] PASS [ ] FAIL | |
| F7 | Mastery evidence recorded after completion | [ ] PASS [ ] FAIL | |
| F8 | Audit events recorded for key transitions | [ ] PASS [ ] FAIL | |

## Learning Clarity Review

| # | Check | Result | Notes |
|---|-------|--------|-------|
| L1 | Learner understands what to do on onboarding | [ ] PASS [ ] FAIL | |
| L2 | Learner understands diagnostic is a test | [ ] PASS [ ] FAIL | |
| L3 | Learner understands what Learning Contract means | [ ] PASS [ ] FAIL | |
| L4 | Learner understands the lesson task | [ ] PASS [ ] FAIL | |
| L5 | Learner understands processing is happening | [ ] PASS [ ] FAIL | |
| L6 | Learner understands their result/corrections | [ ] PASS [ ] FAIL | |
| L7 | No confusing terminology used | [ ] PASS [ ] FAIL | |

## Error Clarity Review

| # | Check | Result | Notes |
|---|-------|--------|-------|
| E1 | Loading state has meaningful message | [ ] PASS [ ] FAIL | |
| E2 | Error state has understandable message | [ ] PASS [ ] FAIL | |
| E3 | Error state has retry action | [ ] PASS [ ] FAIL | |
| E4 | Offline/unavailable state handled gracefully | [ ] PASS [ ] FAIL | |
| E5 | Validation failure does NOT look like success | [ ] PASS [ ] FAIL | |

## Trust/Safety Review

| # | Check | Result | Notes |
|---|-------|--------|-------|
| T1 | No fake completion state | [ ] PASS [ ] FAIL | |
| T2 | Completion requires all validations to pass | [ ] PASS [ ] FAIL | |
| T3 | Result screen shows actual status, not assumed PASS | [ ] PASS [ ] FAIL | |
| T4 | No misleading "congratulations" without evidence | [ ] PASS [ ] FAIL | |
| T5 | Incomplete lesson shows warning | [ ] PASS [ ] FAIL | |

## Anti-Cheat Sanity

| # | Check | Result | Notes |
|---|-------|--------|-------|
| A1 | Cross-user data access blocked | [ ] PASS [ ] FAIL | |
| A2 | Request body user ID ignored | [ ] PASS [ ] FAIL | |
| A3 | Malformed payload rejected | [ ] PASS [ ] FAIL | |
| A4 | Unknown resources return 404 | [ ] PASS [ ] FAIL | |
| A5 | Operator routes require operator role | [ ] PASS [ ] FAIL | |

## Audit Evidence

| # | Check | Result | Notes |
|---|-------|--------|-------|
| AD1 | Audit events recorded in DB | [ ] PASS [ ] FAIL | |
| AD2 | DIAGNOSTIC_STARTED events present | [ ] PASS [ ] FAIL | |
| AD3 | DIAGNOSTIC_COMPLETED events present | [ ] PASS [ ] FAIL | |
| AD4 | LESSON_COMPLETED events present | [ ] PASS [ ] FAIL | |
| AD5 | Audit events are append-only (no delete) | [ ] PASS [ ] FAIL | |

## Proof Consistency

| # | Check | Result | Notes |
|---|-------|--------|-------|
| P1 | Proof JSON matches actual state | [ ] PASS [ ] FAIL | |
| P2 | Proof fields are consistent with report | [ ] PASS [ ] FAIL | |
| P3 | No contradictions between evidence and proof | [ ] PASS [ ] FAIL | |

## Git Consistency

| # | Check | Result | Notes |
|---|-------|--------|-------|
| G1 | Git is clean | [ ] PASS [ ] FAIL | |
| G2 | HEAD matches origin/master | [ ] PASS [ ] FAIL | |
| G3 | No secrets committed | [ ] PASS [ ] FAIL | |
| G4 | No real AI provider configs committed | [ ] PASS [ ] FAIL | |

## Verdict

**Operator verdict:** `[ ] PASS  [ ] FAIL  [ ] BLOCKED`

- **PASS**: All checks passed or non-blocking warnings documented
- **FAIL**: One or more critical checks failed — alpha cannot proceed
- **BLOCKED**: Platform/environment blockers prevent full review

**Cannot pass if:**
- ❌ Broken navigation
- ❌ Hidden or non-functional CTA
- ❌ Fake success state
- ❌ Keyboard overlaps input
- ❌ Unreadable layout
- ❌ Missing error/loading state
- ❌ Completion without validation
- ❌ Reward/mastery inconsistency
- ❌ Audit gap

**Operator signature:** _________________ **Date:** _____________

---

*Created: 2026-06-11*
