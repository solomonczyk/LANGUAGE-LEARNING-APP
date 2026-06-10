# Backend Architecture

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  
**ADR:** ADR-002, ADR-003

---

## 1. Backend Structure

```
backend/
├── app/
│   ├── main.py                  # FastAPI app creation, middleware, lifespan
│   ├── config.py                # Pydantic Settings (environment config)
│   ├── database.py              # SQLAlchemy engine, session factory
│   ├── dependencies.py          # FastAPI dependency injection (get_db, get_current_user)
│   ├── modules/                 # Bounded modules
│   │   ├── identity/
│   │   ├── learner_profile/
│   │   ├── diagnostics/
│   │   ├── learning_contract/
│   │   ├── curriculum/
│   │   ├── lesson_engine/
│   │   ├── content/
│   │   ├── submission/
│   │   ├── ai_gateway/
│   │   ├── linguistic_validation/
│   │   ├── pedagogical_validation/
│   │   ├── policy_engine/
│   │   ├── mastery/
│   │   ├── review_scheduler/
│   │   ├── reward_engine/
│   │   ├── notifications/
│   │   ├── analytics/
│   │   ├── audit/
│   │   ├── integrity/
│   │   └── operator/
│   ├── shared/                  # Shared logic across modules
│   │   ├── models/              # Base SQLAlchemy models, mixins
│   │   ├── schemas/             # Shared Pydantic schemas
│   │   ├── exceptions/          # Custom exception classes
│   │   ├── pagination/          # Pagination utilities
│   │   └── middleware/          # FastAPI middleware
│   └── telemetry/               # OpenTelemetry setup
├── alembic/                     # Alembic migrations
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── contract/
│   ├── schema/
│   └── fixtures/
├── alembic.ini
├── pyproject.toml
├── Dockerfile
└── docker-compose.yml
```

---

## 2. Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Framework | FastAPI | 0.111+ |
| Language | Python | 3.12+ |
| Validation | Pydantic v2 | 2.7+ |
| ORM | SQLAlchemy 2.0 | 2.0+ |
| Migrations | Alembic | 1.13+ |
| Background jobs | Arq | 0.26+ |
| Testing | pytest + pytest-asyncio | latest |
| Linting | ruff | latest |
| Formatting | ruff format | latest |
| Type checking | mypy | latest |

---

## 3. Modular Monolith Architecture

Style: **Modular monolith** — single deployment unit, 20 bounded modules, Python function calls through interface contracts.

### Rules:
- Modules communicate via Python function calls (not HTTP)
- Each module has a defined `public_interface.py` (what other modules may import)
- Internal modules (not in `public_interface.py`) are private and must not be imported cross-module
- Circular module dependencies are FORBIDDEN
- Module extraction to microservices is possible post-MVP but not planned

### Module interface pattern:
```python
# app/modules/identity/public_interface.py
from app.modules.identity.services import register_user, authenticate, verify_token

__all__ = ["register_user", "authenticate", "verify_token"]
```

---

## 4. Dependency Injection

- FastAPI `Depends()` for: `get_db` (session), `get_current_user` (auth), `get_config`
- Module-level dependencies: each module exposes its own dependency functions
- Services are instantiated per-request (no global singletons except config and engine)

---

## 5. Configuration

- Library: Pydantic `BaseSettings` (via `pydantic-settings`)
- Source: environment variables (local `.env` file for development)
- Environment variable prefix: `LL_APP_`
- Secrets: environment variables only (never in code)
- All config defined in `app/config.py`:

```python
class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="LL_APP_")
    
    database_url: str
    redis_url: str
    auth_jwt_secret: str
    supabase_url: str
    supabase_anon_key: str
    ai_mock_mode: bool = True  # MVP override
    ai_provider_api_key: str | None = None
    storage_endpoint: str
    storage_bucket: str
    sentry_dsn: str | None = None
    environment: str = "local"  # local, test, staging
```

---

## 6. Background Jobs

- Library: Arq (Redis-backed)
- Jobs defined in `app/jobs.py`
- All AI analysis dispatched as background jobs (non-blocking API)
- Job results polled or pushed via WebSocket post-MVP
- Job queue: Arq worker runs in separate container

---

## 7. Error Handling

- FastAPI exception handlers for: `RequestValidationError`, `HTTPException`, custom `AppException`
- All errors return the canonical error contract (see [API canon](12_api_design_canon.md))
- Module-level exceptions inherit from `AppException` with `code`, `message`, `http_status`, `retryable`
- Unhandled exceptions: caught by global handler, logged, return 500 with safe message

---

## 8. Middleware

| Middleware | Order | Purpose |
|------------|-------|---------|
| OpenTelemetry | 1 | Request tracing, metrics collection |
| Request ID | 2 | Add X-Request-Id to each request |
| CORS | 3 | CORS headers for mobile/web |
| Rate limiting | 4 | Per-user rate limiting |
| Auth | 5 | JWT verification (exception for /auth and /health) |
| Audit | 6 | Request-level audit logging |

---

## 9. Test Database

- Separate PostgreSQL database per environment
- Test database: created automatically by pytest fixture
- Migration strategy: Alembic `upgrade()` in test setup, `downgrade()` in teardown (or transactional rollback)
- Fixtures: pytest fixtures for all entities, sessions
