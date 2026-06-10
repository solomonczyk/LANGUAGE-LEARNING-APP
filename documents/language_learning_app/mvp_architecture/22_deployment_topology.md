# Deployment Topology

**Status:** Draft  
**Version:** 1.0.0  
**Last updated:** 2026-06-10

---

## Environment Strategy

For MVP planning, only **local**, **test**, and **staging-planned** environments are defined. Production deployment is not performed.

| Environment | Purpose | Data | Access | External Deps |
|-------------|---------|------|--------|---------------|
| **Local** | Developer workstation development | Synthetic/test data | Developer only | None (Docker Compose) |
| **Test** | CI pipeline automated testing | Isolated per run | CI only | None (ephemeral) |
| **Staging-planned** | Integration testing, review | Anonymized test data | Dev team | Managed services |

---

## Local Development Environment

```yaml
# docker-compose.yml structure
services:
  api:
    build: ./backend
    ports: ["8000:8000"]
    depends_on: [db, redis, storage]
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:postgres@db:5432/llapp
      REDIS_URL: redis://redis:6379
      STORAGE_ENDPOINT: http://storage:9000
      AI_PROVIDER_KEY: "${AI_PROVIDER_KEY}"
    volumes: ["./backend:/app"]

  db:
    image: postgres:16-alpine
    ports: ["5432:5432"]
    environment:
      POSTGRES_DB: llapp
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes: ["pgdata:/var/lib/postgresql/data"]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  storage:
    image: minio/minio
    ports: ["9000:9000", "9001:9001"]
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    volumes: ["miniodata:/data"]
```

### Local Environment Setup
- **Mobile**: Expo development build connecting to `http://localhost:8000/api/v1`
- **Backend**: Hot-reload FastAPI with Uvicorn
- **Database**: PostgreSQL 16 with Alembic migrations auto-applied
- **Queue**: Arq worker started alongside API
- **Storage**: MinIO console at `http://localhost:9001`

---

## Test Environment (CI Pipeline)

| Component | Implementation |
|-----------|---------------|
| **Database** | Ephemeral PostgreSQL in CI container (service container) |
| **Redis** | Ephemeral Redis in CI container |
| **Storage** | MinIO in CI container |
| **Backend** | pytest with async test client |
| **Mobile** | Jest with React Native Testing Library |
| **Duration** | Full CI: < 15 minutes |

### CI Pipeline (GitHub Actions)

```yaml
# .github/workflows/ci.yml structure
jobs:
  lint:
    - ruff check backend/
    - eslint mobile/
  
  test-backend:
    - pytest backend/tests/ --cov --cov-report=term
    - pytest backend/tests/contract/
    - pytest backend/tests/state_machine/
  
  test-mobile:
    - npx jest mobile/
  
  schema-validation:
    - python scripts/validate_schemas.py
    - python scripts/validate_openapi.py
  
  security-scan:
    - bandit backend/ -r
    - npm audit mobile/
```

---

## Staging Environment (Planned)

### Architecture

```
                         ┌─────────────┐
                         │  Cloudflare │
                         │  (CDN/SSL)  │
                         └──────┬──────┘
                                │
                         ┌──────┴──────┐
                         │  Load       │
                         │  Balancer   │
                         └──────┬──────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
              ┌─────┴─────┐          ┌──────┴──────┐
              │  API       │          │  API        │
              │  Instance 1│          │  Instance 2 │
              └─────┬─────┘          └──────┬───────┘
                    │                       │
                    └───────────┬───────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
              ┌─────┴─────┐          ┌──────┴──────┐
              │ PostgreSQL│          │  Redis      │
              │ (Managed) │          │  (Managed)  │
              └───────────┘          └─────────────┘
```

### Staging Components

| Component | Technology | Configuration |
|-----------|-----------|---------------|
| **Backend** | Docker container | 2 instances, 4 vCPU, 8GB RAM each |
| **PostgreSQL** | Managed (Supabase/RDS) | 2 vCPU, 8GB RAM, 100GB storage |
| **Redis** | Managed (Upstash) | 250MB cache |
| **Object Storage** | Cloudflare R2 | Pay-as-you-go |
| **Auth** | Supabase Auth | Managed |
| **Observability** | Grafana Cloud (free tier) | Logs 7d, Metrics 30d |
| **Error Tracking** | Sentry | Free tier |
| **CI/CD** | GitHub Actions | Free tier |

### Health Checks

```
GET /api/v1/health
{
  "status": "ok",
  "version": "1.0.0",
  "uptime_seconds": 123456,
  "dependencies": {
    "database": { "status": "ok", "latency_ms": 3 },
    "redis": { "status": "ok", "latency_ms": 1 },
    "storage": { "status": "ok", "latency_ms": 15 },
    "auth_provider": { "status": "ok", "latency_ms": 45 }
  }
}
```

---

## Migration Strategy

### Database Migrations
- **Tool**: Alembic
- **Applied**: Automatically on container startup (dev), as CI step (test), as deployment step (staging)
- **Reversible**: All migrations must have `downgrade()` for rollback
- **Naming**: `{YYYYMMDD_HHMM}_{description}.py`

### Rollback Procedure
1. Detect issue via health check or alert
2. Roll back API container to previous version
3. Run Alembic downgrade if database migration was part of release
4. Verify health
5. Investigate root cause

---

## Secrets Management

| Environment | Method | Scope |
|-------------|--------|-------|
| **Local** | `.env` file | Not committed; documented in `.env.example` |
| **Test** | GitHub Actions secrets | Repository-level |
| **Staging** | Secrets manager | Service-level |

**Secrets Required:**
- `AI_PROVIDER_PRIMARY_KEY` — Primary LLM provider API key
- `AI_PROVIDER_FALLBACK_KEY` — Fallback LLM provider API key
- `SUPABASE_URL` — Supabase project URL
- `SUPABASE_SERVICE_KEY` — Supabase service role key
- `DATABASE_URL` — PostgreSQL connection string
- `REDIS_URL` — Redis connection string
- `SENTRY_DSN` — Sentry project DSN
- `STORAGE_ACCESS_KEY` — Object storage access key
- `STORAGE_SECRET_KEY` — Object storage secret key
