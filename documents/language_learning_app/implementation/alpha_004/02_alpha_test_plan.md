# 02 — Alpha Test Plan

## Overview

Controlled closed alpha test plan for the Language Learning App's first vertical slice. The test covers the full learner journey with deterministic mock AI.

## Test Objectives

1. Verify the complete learner journey works end-to-end
2. Identify UX blockers and usability issues
3. Validate deterministic state transitions
4. Verify audit trail completeness
5. Confirm duplicate submission protection
6. Verify mastery/reward evidence recording
7. Confirm error/loading/offline states are understandable

## Test Environments

### Primary
- Backend: http://localhost:8000 (Docker)
- Mobile: http://localhost:8081 (Expo Web)
- Mock AI: Valid mode (deterministic fixtures)
- Browser: Chromium (Chrome/Edge) responsive mode

### Secondary (if available)
- Android emulator or physical device via Expo Go
- Firefox or other Chromium-based browser

## Test Data

All testers use synthetic profiles:

| Tester | Username | Target Language | Native Language | Self-Reported Level |
|--------|----------|-----------------|-----------------|---------------------|
| T1 | `alpha_tester_01` | Spanish | English | A1 |
| T2 | `alpha_tester_02` | French | English | A2 |
| T3 | `alpha_tester_03` | Japanese | English | B1 |
| T4 | `alpha_tester_04` | German | English | A1 |
| T5 | `alpha_tester_05` | Korean | English | A2 |

## Test Cycles

### Cycle 1: Baseline verification (T1–T2)
- Full learner journey with valid mock AI
- Verify all states are reachable
- Verify completion and mastery evidence

### Cycle 2: Validation paths (T3)
- Submission with minimum text (10 chars)
- Submission with very long text (5000 chars)
- Observation of loading states

### Cycle 3: Error/edge cases (T4)
- Malformed AI processing path
- Network error simulation (stop Docker)
- Idempotency verification

### Cycle 4: UX review (T5)
- Viewport testing (small phone, regular phone, tablet, zoomed)
- Keyboard behavior
- Visual polish review

## Test Execution

Each tester follows the [learner test script](03_learner_test_script.md).

Results recorded in:
- `evidence/e2e_journey_matrix.json`
- `evidence/ux_acceptance_matrix.json`
- `evidence/operator_review_report.md`

---

*Created: 2026-06-11*
