# 01 — Closed Alpha Scope

## Purpose

Define the exact scope of the controlled closed learner alpha for the Language Learning App. This scope is deliberately narrow — it is NOT an open beta, NOT a public release, and NOT production-ready.

## Explicitly In Scope

- **Controlled closed alpha only**: 3–5 invited synthetic testers (no real users at scale)
- **Mock AI only**: All AI analysis is deterministic mock fixtures, no real LLM
- **Local / controlled environment**: Docker + Expo Web on localhost only
- **Full learner journey**: onboarding → profile → diagnostic → contract → lesson → submission → analysis → validation → completion → mastery → audit
- **Expo Web (Chromium)**: Primary test platform
- **Android emulator / physical device**: If available to tester (optional)
- **UX hardening review**: Loading, error, offline, keyboard, viewport testing
- **Deterministic state verification**: All state transitions must be reproducible

## Explicitly Out of Scope

| Feature | Status |
|---------|--------|
| Real AI provider (OpenAI, DeepSeek, Claude, etc.) | NOT ALLOWED |
| Real LLM calls | NOT ALLOWED |
| Staging deployment | NOT ALLOWED |
| Production deployment | NOT ALLOWED |
| Real users at scale | NOT ALLOWED |
| Payments / subscriptions | NOT ALLOWED |
| Social features | NOT ALLOWED |
| Unrestricted AI chat | NOT ALLOWED |
| Push notifications | NOT ALLOWED |
| New lesson modes beyond personal narrative | NOT ALLOWED |
| Database schema changes | NOT ALLOWED unless blocker |
| Production acceptance | NOT ALLOWED (production_accepted=false) |
| Cosmetic redesign | NOT ALLOWED (hardening only) |
| New MVP features | NOT ALLOWED |

## Test Data

- **No real personal data allowed**
- All testers use synthetic learner profiles (see test script)
- Synthetic learner usernames: `alpha_tester_01` through `alpha_tester_05`
- Synthetic credentials only (no email/phone collection)

## Platforms

| Platform | Status |
|----------|--------|
| Expo Web (Chromium) | ✅ Primary |
| Expo Web (Firefox) | ⚠️ If available |
| Android emulator | ❓ Tester-dependent |
| Android physical device | ❓ Tester-dependent |
| iOS simulator | ❌ Blocked (no macOS) |
| iOS physical device | ❌ Blocked (no macOS) |
| iPad | ❌ Blocked (no macOS) |

## Duration

- **Alpha window**: 1 week from start
- **Expected tester commitment**: 1–2 hours total
- **Bug reporting window**: During alpha window

## Environment

- Backend: Docker (PostgreSQL 16.14 + FastAPI on port 8000)
- Mobile: Expo Web on port 8081
- Mock AI: `mock_ai_fixture_mode=valid`

---

*Created: 2026-06-11*
