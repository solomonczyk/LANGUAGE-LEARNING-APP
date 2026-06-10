# CI/CD and Quality Gates

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  
**Schema:** `schemas/quality_gate.schema.json`  
**Example:** `examples/quality_gate.example.json`

---

## 1. CI Pipeline (GitHub Actions)

```
Trigger: push to any branch, PR to master
├── lint (ruff, ESLint, prettier — all 0 warnings required)
├── type-check (mypy for backend, tsc for frontend — 0 errors required)
├── unit-tests (pytest for backend, Jest for frontend — all pass)
├── schema-validation (all schemas valid against meta-schema)
├── contract-tests (API endpoints match OpenAPI spec)
├── integration-tests (pytest with test database)
├── migration-tests (alembic upgrade + downgrade)
├── openapi-drift (OpenAPI spec matches implementation)
├── artifact-validation (artifact index entries exist, paths valid)
├── traceability-validation (traceability matrix requirements met)
├── secret-scan (trufflehog or git leaks — 0 secrets found)
├── dependency-scan (pip audit + npm audit — 0 vulnerabilities)
├── mobile-build (expo build — iOS and Android SDK compile)
├── backend-container (Docker build check)
└── proof-validation (proof JSON schema + field completeness)
```

---

## 2. Required Checks

| Check | Tool | Warnings Allowed | Fail on |
|-------|------|-----------------|---------|
| Format | ruff format (backend), prettier (frontend) | 0 | Any formatting diff |
| Lint | ruff (backend), ESLint (frontend) | 0 | Any error or warning |
| Type check | mypy (backend, strict), tsc (frontend, strict) | 0 | Any type error |
| Unit tests | pytest / Jest | 0 | Any test failure |
| Schema validation | pytest + JSON Schema validators | 0 | Any schema mismatch |
| Contract tests | pytest + httpx | 0 | Any contract violation |
| Integration tests | pytest + test DB | 0 | Any test failure |
| Migration tests | pytest + alembic | 0 | Migration apply/rollback failure |
| OpenAPI drift | OpenAPI spec vs routes | 0 | Undocumented endpoint or response |
| Artifact validation | Custom script | 0 | Missing artifact |
| Traceability | Custom script | 0 | Untraced requirement |
| Secret scan | trufflehog/gitleaks | 0 | Any secret detected |
| Dependency scan | pip audit / npm audit | 0 | Any vulnerability |
| Mobile build | EAS Build / expo run | 0 | Compilation error |
| Docker build | docker build | 0 | Build failure |
| Proof validation | JSON Schema validation | 0 | Invalid proof |

---

## 3. Branch Rules

| Rule | Implementation |
|------|---------------|
| Protected branch | `master` — cannot push directly |
| PR required | All changes must go through PR |
| PR checks | All CI checks must pass before merge |
| PR approvals | Minimum 1 review (MVP); 2 for production |
| Linear history | Rebase-only merge (no merge commits) |
| Commit signing | GPG commit signing recommended |

---

## 4. Pre-Commit Hooks

| Hook | Action |
|------|--------|
| `pre-commit` | Format check (ruff/prettier), lint, secret scan |
| `pre-push` | Type check, unit tests, schema validation |

---

## 5. Staging Gate

| Check | Requirement |
|-------|-------------|
| CI passes | All checks must pass |
| Migration forward/backward | Alembic upgrade + downgrade verified |
| E2E tests pass | Mobile E2E on staging API |
| Manual QA sign-off | Tester confirms basic flows |
| Documentation sync | Artifact index up to date |

---

## 6. Production Gate

| Status | **FORBIDDEN** (MVP phase) |
|--------|--------------------------|

Production deployment opens only when: `production_accepted=true` — which is FORBIDDEN in the current phase. Future task will define the production gate.

---

## 7. Rollback

| Scenario | Rollback Procedure |
|----------|-------------------|
| Failed migration | Alembic downgrade, then fix forward |
| Failed deployment | Revert to previous CI artifact |
| Data corruption | Restore from last backup |
| Security incident | Revoke tokens, rollback, alert |

---

## 8. Migration Failure Behaviour

| Failure | Action |
|---------|--------|
| Upgrade fails on test | Block CI; developer fixes migration |
| Upgrade fails on staging | Auto-downgrade; block staging deploy; alert |
| Downgrade fails | Manual intervention by DB admin |

---

## 9. Flaky Test Policy

| Rule | Detail |
|------|--------|
| Quarantine | Flaky tests moved to separate CI job (informational) |
| Root cause | 48h to identify root cause or revert |
| Re-integration | Fixed tests re-join main CI on next pass |
| Maximum | No more than 3 flaky tests quarantined at once |

---

## 10. Warning Policy

| Scope | Allowed |
|-------|---------|
| CI pipeline | 0 warnings across all checks |
| Lint | 0 warnings |
| Type check | 0 warnings |
| Build output | 0 warnings |
| Deprecation warnings | 0 (resolve before merge) |
