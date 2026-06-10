# Environment and Configuration Canon

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  

---

## 1. Environment Definitions

| Environment | Purpose | Users | Production? |
|-------------|---------|-------|-------------|
| `local` | Developer machine | Developer | No |
| `test` | Automated tests | CI pipeline | No |
| `staging` | Pre-release validation | Internal team, testers | No (planned) |
| `production` | Live users | Learners | **FORBIDDEN (locked)** |

---

## 2. Local Environment

| Component | Configuration | Access |
|-----------|--------------|--------|
| Mobile | Expo dev client, local API URL | `http://localhost:8000` |
| Backend | `uvicorn --reload`, local config | `http://localhost:8000` |
| Database | PostgreSQL 16 Docker container | `localhost:5432` |
| Redis | Redis 7 Docker container | `localhost:6379` |
| Object storage | MinIO Docker container | `localhost:9000` (API) |
| Auth | Supabase Auth (mock or local) | Local Supabase or cloud project |
| AI mode | `MOCK` (always) | — |
| Telemetry | Console output, local Prometheus+Grafana | Optional |

**Start command:** `docker compose up` (all services)

---

## 3. Test Environment

| Component | Configuration | Notes |
|-----------|--------------|-------|
| Database | `test_ll_app` PostgreSQL | Created/managed by pytest fixture |
| Redis | Separate Redis instance (test) | — |
| Object storage | MinIO test bucket | New bucket per test run |
| AI mode | `MOCK` | All test environments |
| Auth | Mock Supabase Auth | No external calls |
| Telemetry | Disabled | — |

---

## 4. Staging Environment (Planned)

| Component | Configuration | Notes |
|-----------|--------------|-------|
| Mobile | Expo staging build, staging API URL | `https://api-staging.llapp.com` |
| Backend | Docker container, staging config | Staging server |
| Database | PostgreSQL 16 (staging cluster) | Separate server |
| Redis | Redis 7 (staging) | Separate instance |
| Object storage | Cloudflare R2 | Dedicated bucket |
| Auth | Supabase Auth (staging project) | Separate Supabase project |
| AI mode | Real provider (mock fallback) | — |
| Telemetry | Full stack (Prometheus + Grafana + Loki + Tempo) | — |

---

## 5. Production Environment (Planned, FORBIDDEN)

Not defined until `production_accepted=true` is set by a future authorized task.

---

## 6. Environment Isolation Rules

| Rule | Enforcement |
|------|-------------|
| Separate databases per environment | CI + manual verification |
| No shared credentials across environments | Separate secrets per environment |
| No staging data from real users | Synthetic/test data only |
| No production credentials in local | .env files excluded from git |
| No secrets in repository | CI secret scan |
| No cross-environment API calls | Config validation |

---

## 7. Configuration Management

| Config Type | Local | Test | Staging |
|-------------|-------|------|---------|
| API URLs | `.env.local` | Hardcoded test config | `.env.staging` |
| Database URL | `.env.local` | Pytest fixture | CI/CD secret |
| Auth keys | `.env.local` (mock) | Mock | CI/CD secret |
| AI provider keys | Not needed (mock) | Mock | CI/CD secret |
| Storage keys | `.env.local` (MinIO) | MinIO | CI/CD secret |
| Feature flags | `.env.local` | `.env.test` | `.env.staging` |

---

## 8. Secrets Management

| Secret | Storage |
|--------|---------|
| Auth JWT secret | Environment variable (local: `.env`, staging: CI/CD secrets) |
| Supabase keys | Environment variable |
| AI provider key | Environment variable (staging only) |
| Sentry DSN | Environment variable (staging, optional) |
| Database password | Environment variable (local: `.env`, staging: CI/CD secrets) |

**Rules:**
- `.env` files are in `.gitignore` (never committed)
- `.env.example` is committed with placeholder values
- CI/CD secrets stored in GitHub Actions secrets, not repository
- Secrets rotated immediately on suspected exposure

---

## 9. Migration Policy by Environment

| Environment | Migration Strategy |
|-------------|-------------------|
| Local | Auto-apply on container start (alembic upgrade head) |
| Test | Apply in pytest session fixture; rollback on teardown |
| Staging | Manual trigger via deployment pipeline; tested in CI first |
| Production | Not applicable (FORBIDDEN) |
