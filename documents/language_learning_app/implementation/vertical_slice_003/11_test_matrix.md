# 11 — Test Matrix (Vertical Slice 003)

## Test Totals
| Group | Tests | Passed | Failed |
|-------|-------|--------|--------|
| Backend Unit | 70 | 70 | 0 |
| Backend Integration | 39 | 39 | 0 |
| State Machine | 8 | 8 | 0 |
| API Contract | 39 | 39 | 0 |
| Database | 39 | 39 | 0 |
| E2E | 39 | 39 | 0 |
| Security | 4 | 4 | 0 |
| Mobile | 0 | 0 | 0 |
| **TOTAL** | **109** | **109** | **0** |

## Unit Test Coverage by Module
| Module | Tests | Scope |
|--------|-------|-------|
| audit | 3 | CRUD, field validation, write failure |
| diagnostics | 9 | CEFR calc, assessment, boundary |
| learning_contract | 6 | Level-based params, determinism |
| mastery | 4 | Evidence types, profile |
| mock_ai | 12 | Fixture selection, structure, determinism |
| policy_engine | 2 | COMPLETE decision |
| state_machine | 8 | Transitions, guards, resets |
| validation | 24 | Linguistic (11) + pedagogical (13) |

## Integration Test Coverage
| Flow | Tests | Status |
|------|-------|--------|
| Health | 2 | PASSED |
| Identity (register, login, me, duplicates) | 5 | PASSED |
| Learner Profile (create, read, persistence, dedup) | 4 | PASSED |
| Diagnostic (full flow, state guards, cross-user) | 3 | PASSED |
| Lesson (create, get, submit, process, cross-user) | 5 | PASSED |
| Learning Contract | 1 | PASSED |
| Mastery | 1 | PASSED |
| Audit (operator access, non-op blocked) | 2 | PASSED |
| Idempotency (submission, response, completion) | 3 | PASSED |
| Security (spoofing, injection, malformed, 404) | 4 | PASSED |
| State Machine (diagnostic + lesson via API) | 2 | PASSED |
| Error Contract (canonical error structure) | 2 | PASSED |
| Persistence (lesson data, audit events) | 2 | PASSED |
| Duplicate Processing | 1 | PASSED |
| Retryable Flag | 1 | PASSED |

## Android Device Matrix
| Device | Size | OS | Status |
|--------|------|----|--------|
| Small phone | <4.7" | Android 12+ | BLOCKED_ENVIRONMENT |
| Regular phone | 5.0-6.0" | Android 12+ | BLOCKED_ENVIRONMENT |
| Large phone | 6.5"+ | Android 12+ | BLOCKED_ENVIRONMENT |
| Tablet | 10"+ | Android 12+ | BLOCKED_ENVIRONMENT |

## iOS Device Matrix
| Device | Status |
|--------|--------|
| Small iPhone | BLOCKED_ENVIRONMENT |
| Regular iPhone | BLOCKED_ENVIRONMENT |
| Large iPhone | BLOCKED_ENVIRONMENT |
| iPad | BLOCKED_ENVIRONMENT |

> Note: Full device QA requires Expo Go or dedicated emulator/simulator which is unavailable in current CLI-only environment.
