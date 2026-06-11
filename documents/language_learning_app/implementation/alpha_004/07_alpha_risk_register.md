# 07 — Alpha Risk Register

## Risk Assessment

| # | Risk | Likelihood | Impact | Mitigation | Status |
|---|------|-----------|--------|------------|--------|
| R1 | Tester closes browser mid-flow, loses state | Medium | Medium — learner must restart onboarding | Script warns about browser state; state machine handles new sessions | Open |
| R2 | Backend container crashes during test | Low | High — all test sessions blocked | `docker compose up -d` restarts; data persisted in PostgreSQL | Mitigated |
| R3 | Database migration conflict | Low | High — incompatible schema | Single migration (001); no schema changes planned | Mitigated |
| R4 | Tester enters real personal data | Low | Medium — data stored in local DB | Script explicitly forbids; no email validation in registration | Open |
| R5 | Expo Web bundle fails to load | Medium | High — cannot test mobile app | Known dependency warnings (react-native version mismatch); non-blocking if Metro bundler works | Accepted |
| R6 | Audit events not recorded | Low (was Medium — FIXED) | Medium — untraceable learner activity | FIXED: record_event calls added to lesson_engine and diagnostics services | Closed |
| R7 | Cross-user data leak due to auth stub | Low | Critical — data privacy violation | Auth stub uses x-user-id header; all endpoints enforce ownership | Mitigated |
| R8 | Tester cannot access localhost:8081 (port conflict) | Medium | Medium — cannot test | Script provides instructions to check port availability | Open |
| R9 | Mock AI malformed mode breaks pipeline unexpectedly | Low | Medium — processing fails | Expected behavior; pipeline returns FAILED state gracefully | Mitigated |
| R10 | Git dirty / unpushed commits at alpha end | Low | Low — blockers for next stage | Operator review enforces Git clean exit | Mitigated |
| R11 | Duplicate submission idempotency fails | Low (was tested) | Medium — duplicate data | Integration test covers idempotency key | Mitigated |
| R12 | Incomplete documentation for alpha testers | Low | Medium — testers don't know what to do | Script provided; operator available for questions | Open |

## Risk Response Plan

| Trigger | Response |
|---------|----------|
| Backend crash | `docker compose down && docker compose up -d` — data preserved in PostgreSQL volume |
| Database corruption | `docker compose down -v && docker compose up -d` — full reset (loss of all test data) |
| Expo Web unresponsive | `cd mobile && npx expo start --web` restart |
| Critical security issue | Stop all test sessions immediately; notify operator |
| Blocker bug found | Fix if within hardening scope; document if in staging scope |

## Risk Owner

All risks owned by the project maintainer (operator) during alpha execution.

---

*Created: 2026-06-11*
