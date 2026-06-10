# Testing Canon

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  
**Schema:** `schemas/test_requirement.schema.json`  
**Example:** `examples/test_requirement.example.json`

---

## 1. Test Types

| # | Test Type | Scope | Tool | Owner | Blocking |
|---|-----------|-------|------|-------|----------|
| 1 | Unit | Pure functions, utilities, validators | pytest (backend), Jest (frontend) | Developer | Yes |
| 2 | Schema | JSON Schema / Pydantic / Zod validation | pytest + jsonschema | Developer | Yes |
| 3 | Contract | API endpoint existence, status codes, error shapes | pytest + httpx (backend) | Backend | Yes |
| 4 | Integration | Multi-step flows across modules | pytest + test DB | Backend | Yes |
| 5 | State machine | Entity state transitions, forbidden transitions | pytest + state machine tests | Backend | Yes |
| 6 | Database | Migration apply/rollback, seed data | pytest + alembic | Backend | Yes |
| 7 | Migration | Upgrade + downgrade, data integrity | pytest + test DB | Backend | Yes |
| 8 | Security | IDOR, prompt injection, duplicate reward, rate limit | pytest + custom test suite | Security | Yes |
| 9 | Prompt evaluation | Mock AI output schema compliance | pytest + fixture-based | AI Gateway | Yes |
| 10 | Frontend component | UI component rendering, states, interactions | Jest + React Native Testing Library | Mobile | Yes |
| 11 | Mobile E2E | Critical user journeys on device | Detox (or Maestro) | Mobile | Yes |
| 12 | Accessibility | Screen reader, contrast, touch targets | Jest + aXe (RNL), manual | Mobile | Yes |
| 13 | Device | Layout rendering at breakpoint widths | Visual regression (emulator) | Mobile | Yes |
| 14 | Recovery | App crash, network loss, interruption | pytest + mobile E2E | Both | Yes |
| 15 | Load | API latency under concurrent users | Locust | Backend | No (informational) |
| 16 | Visual regression | Screen snapshots at breakpoints | Storybook + chromatic (post-MVP) | Mobile | Post-MVP |
| 17 | Audit completeness | Every state transition has audit event | pytest | Backend | Yes |

---

## 2. Required Test Scenarios

| Scenario | Test Type | Description |
|----------|-----------|-------------|
| Onboarding completion | Integration | User completes onboarding → profile created |
| Diagnostic completion | Integration | User completes diagnostic → skill assessment created |
| Lesson creation | Integration | Lesson session created with valid data |
| Valid submission | Integration | Text submission → pipeline → completion |
| Invalid submission (empty) | Integration | Empty submission rejected with validation error |
| Invalid submission (malicious) | Security | XSS/script injection rejected |
| Malformed mock AI output | Prompt eval | Invalid JSON from mock AI → rejected |
| Pedagogical rejection | Integration | Output valid but level-inappropriate → rejected |
| Duplicate attempt | State machine | Same idempotency key → 409 |
| Duplicate reward | Security | Same lesson rewarded twice → blocked |
| Cross-user access | Security | User A tries to access User B's session → 404 |
| Retry denied | State machine | Retry exceeds max → failure |
| Offline interruption | Recovery | Network dropped during submission → draft saved |
| App restart recovery | Recovery | App killed → session restored |
| Keyboard overlap | Device | Form input visible with keyboard open |
| Small screen (<360dp) | Device | All screens render without horizontal scroll |
| Large text (200%) | Accessibility | All text readable, no truncation |
| Tablet layout | Device | Two-column layout renders correctly |
| Android back | Platform | Back exits lesson with confirmation |
| iOS swipe back | Platform | Swipe disabled during submission |
| Audit completeness | Audit | Every state transition logs audit event |

---

## 3. Test Requirements by Module

| Module | Unit | Integration | Contract | State Machine |
|--------|------|-------------|----------|---------------|
| identity | ✓ | ✓ | ✓ | — |
| learner_profile | ✓ | ✓ | ✓ | — |
| diagnostics | ✓ | ✓ | ✓ | ✓ |
| learning_contract | ✓ | ✓ | ✓ | — |
| curriculum | ✓ | ✓ | ✓ | — |
| lesson_engine | ✓ | ✓ | ✓ | ✓ |
| content | ✓ | — | ✓ | — |
| submission | ✓ | ✓ | ✓ | ✓ |
| ai_gateway | ✓ | — | ✓ | ✓ |
| linguistic_validation | ✓ | ✓ | — | — |
| pedagogical_validation | ✓ | ✓ | — | — |
| policy_engine | ✓ | ✓ | — | — |
| mastery | ✓ | ✓ | — | ✓ |
| review_scheduler | ✓ | ✓ | — | ✓ |
| reward_engine | ✓ | ✓ | — | ✓ |
| notifications | ✓ | — | ✓ | — |
| analytics | ✓ | — | — | — |
| audit | ✓ | ✓ | ✓ | — |
| integrity | ✓ | ✓ | — | — |
| operator | — | ✓ | ✓ | — |

---

## 4. Test Coverage Targets

| Metric | Target | Tool |
|--------|--------|------|
| Backend line coverage | ≥85% | pytest-cov |
| Backend branch coverage | ≥75% | pytest-cov |
| Frontend line coverage | ≥80% | Jest coverage |
| Module interface coverage | 100% (contract tests) | pytest |
| State machine transition coverage | 100% | pytest |
| Security scenario coverage | 100% | pytest |
| Migration reversibility | 100% | pytest |

---

## 5. Test Environment

| Aspect | Configuration |
|--------|---------------|
| Database | Separate PostgreSQL database (test_ll_app) |
| Redis | Separate Redis instance (test) |
| Object storage | MinIO test bucket |
| AI mode | `MOCK` (always in test) |
| Auth | Mock Supabase Auth (no external calls) |
| Reset | Database reset before each test module |

---

## 6. Forbidden Test Patterns

| Pattern | Reason |
|---------|--------|
| Disabled test without issue reference | Untracked regression risk |
| Placeholder test (`pass` / empty) | False sense of coverage |
| Testing real provider calls | Cost + flakiness + external dependency |
| Testing client with real backend | Requires network, slow |
| Ignoring test failures in CI | Silent regression |
| `sleep()` in tests | Flaky; use await/event pattern |
