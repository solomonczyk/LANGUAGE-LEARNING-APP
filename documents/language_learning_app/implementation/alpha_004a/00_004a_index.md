# Alpha 004A — Visual/Runtime Blocker Fix and Evidence Recheck

## Overview

- **Task**: LANGUAGE-LEARNING-APP-004A-VISUAL-RUNTIME-BLOCKER-FIX-AND-EVIDENCE-RECHECK
- **Parent Task**: LANGUAGE-LEARNING-APP-S1-ACCEPTANCE-HARDENING-AND-CLOSED-LEARNER-ALPHA-PREP-004
- **Date**: 2026-06-11
- **Verdict**: ACCEPTED_WITH_ENVIRONMENT_BLOCKERS

## Purpose

Fix real visual/runtime blockers found during manual local review of Layer 004, and re-prove that the accepted vertical slice can be a candidate for closed learner alpha.

## Blocker Reconciliation

| Blocker | Before | After | Fix |
|---------|--------|-------|-----|
| Root route unmatched | FAIL | PASS | Created mobile/app/index.tsx redirecting to /onboarding |
| Database health pending | FAIL | PASS | Added real DB connectivity check to health endpoint |
| Frontend API 404s | FAIL | PASS | Learning contract 404 was resource-not-found; fixed with auto-creation |
| Diagnostic → contract | FAIL | PASS | Learning-contract screen auto-creates on 404 |
| Lesson route API errors | FAIL | PASS | Lesson loads properly with valid data; invalid ID shows safe error |
| Screenshots missing | FAIL | PASS | 12 screenshots created for full flow |

## Artifacts

- [01_blocker_reconciliation_report.md](01_blocker_reconciliation_report.md)
- [02_visual_recheck_report.md](02_visual_recheck_report.md)
- [03_api_contract_recheck.md](03_api_contract_recheck.md)
- [04_learning_contract_flow_recheck.md](04_learning_contract_flow_recheck.md)
- [05_environment_and_remaining_blockers.md](05_environment_and_remaining_blockers.md)
- [proof_language_learning_app_alpha_004a.json](proof_language_learning_app_alpha_004a.json)
- [alpha_004a_artifact_index.json](alpha_004a_artifact_index.json)

## Evidence

- [evidence/screenshots/](evidence/screenshots/) — 12 screenshots of fixed flow
- [evidence/logs/](evidence/logs/) — backend health, console, OpenAPI, test output
- [evidence/environment_blockers.md](evidence/environment_blockers.md)
