# Selected Technology Stack

**Status:** Draft  
**Version:** 1.0.0  
**Last updated:** 2026-06-10

---

## Introduction

This document defines the definitive technology stack for the Language Learning App MVP. Each selection is based on the comparison matrix in [07_technology_stack_comparison.md](07_technology_stack_comparison.md) and documented in the Architecture Decision Log (ADR-001 through ADR-012).

---

## Mobile Client

### Selected: React Native + Expo + TypeScript

| Component | Technology |
|-----------|-----------|
| Framework | React Native |
| Build Tool | Expo SDK 52+ |
| Language | TypeScript 5.x |
| Routing | Expo Router v4 |
| State Management | TanStack Query (server) + Zustand (client) |
| Forms | React Hook Form |
| Validation | Zod |
| Audio | expo-av |
| HTTP Client | TanStack Query / fetch |

**Justification:** React Native + Expo provides the fastest path to a production-quality mobile app on both iOS and Android from a single TypeScript codebase. TypeScript consistency with backend (Pydantic validation mirrors Zod on frontend) reduces cognitive overhead. Expo's EAS Build handles native builds without requiring native development environments.

**Version Requirements:**
- React Native: 0.76+
- Expo SDK: 52+
- TypeScript: 5.4+
- Zod: 3.23+

---

## Backend

### Selected: FastAPI + Python 3.12+

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI |
| Language | Python 3.12+ |
| Validation | Pydantic v2 |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Background Jobs | Arq (Redis-backed) |
| Testing | pytest, pytest-asyncio |

**Justification:** FastAPI's automatic OpenAPI generation, Pydantic v2 validation, and async-first architecture align with the requirements for structured APIs, validation pipelines, and async LLM calls. Python's ML ecosystem positions the project for future AI enhancements. The modular monolith pattern maps naturally to FastAPI's APIRouter and dependency injection.

**Version Requirements:**
- Python: 3.12+
- FastAPI: 0.111+
- Pydantic: 2.7+
- SQLAlchemy: 2.0+
- Alembic: 1.13+
- Arq: 0.26+

---

## Data Layer

### Selected: PostgreSQL + S3-Compatible Object Storage

| Component | Technology |
|-----------|-----------|
| Primary Database | PostgreSQL 16 |
| Object Storage (Local) | MinIO |
| Object Storage (Staging) | Cloudflare R2 |
| Cache | Redis 7+ (via Arq dependency) |

**Justification:** PostgreSQL provides ACID transactions essential for reward integrity, JSONB for flexible learner profiles, and row-level security for data isolation. S3-compatible storage provides a standard interface for audio recordings and lesson assets. MinIO enables zero-dependency local development; Cloudflare R2 eliminates egress fees for staging.

**Version Requirements:**
- PostgreSQL: 16+
- MinIO: latest (Docker)
- Redis: 7+

---

## AI Integration

### Selected: Provider-Independent AI Gateway

| Component | Technology |
|-----------|-----------|
| Gateway Pattern | AI Gateway abstraction layer |
| Provider SDK | Provider-independent interface |
| Output Format | Structured output only (JSON Schema) |
| Validation | Pydantic v2 (backend) |
| Fallback | Primary + fallback provider |
| Prompt Versioning | Git-based, version hash in audit |
| Cost Tracking | Per-request cost attribution |

**Justification:** A provider-independent gateway prevents vendor lock-in, enables structured output enforcement, and provides a single point for validation, cost tracking, and audit. All LLM responses are validated against schemas before any state change occurs.

---

## DevOps & Infrastructure

| Component | Technology |
|-----------|-----------|
| Containerization | Docker |
| Local Dev | Docker Compose |
| CI | GitHub Actions |
| Observability | OpenTelemetry + Grafana + Prometheus + Loki |
| Error Tracking | Sentry |
| Secrets | Environment variables (local), secrets manager (staging) |

---

## Validation & Testing

| Component | Technology |
|-----------|-----------|
| Backend Testing | pytest, pytest-asyncio |
| Contract Tests | PACT or built-in schema validation |
| Mobile Unit Tests | Jest + React Native Testing Library |
| E2E Tests | Detox (mobile) or Playwright (web) |
| Security Tests | OWASP ZAP, custom prompt injection test suite |
| Load Tests | Locust |
| Schema Validation | JSON Schema + Pydantic |

---

## Architecture Style

### Selected: Modular Monolith

**Justification:** A modular monolith provides the simplicity of a single deployment unit with clear bounded module boundaries. This avoids the operational complexity of microservices (service discovery, inter-service communication, distributed transactions) while maintaining the option to extract modules into separate services if needed post-MVP. The 20 bounded modules enforce separation of concerns through interface contracts rather than network calls.

See ADR-003 and [11_module_architecture.md](11_module_architecture.md) for detailed module boundaries.

---

## Stack Diagram

```
┌─────────────────────────────────────────┐
│           Mobile App (React Native)     │
│  Expo Router · TanStack Query · Zustand │
│  React Hook Form · Zod · expo-av       │
└──────────────────┬──────────────────────┘
                   │ HTTPS / JSON / JWT
                   ▼
┌─────────────────────────────────────────┐
│      Backend (FastAPI / Python 3.12+)   │
│  Pydantic v2 · SQLAlchemy 2 · Alembic  │
│  Arq Workers · OpenTelemetry            │
│  ┌───────────────────────────────────┐  │
│  │   20 Bounded Modules              │  │
│  │   (identity, diagnostics, ...)    │  │
│  └───────────────────────────────────┘  │
└───────┬────────────┬──────────┬─────────┘
        │            │          │
        ▼            ▼          ▼
   PostgreSQL     Redis     AI Gateway
        │            │          │
        ▼            ▼          ▼
    AWS R2/     (queue,     LLM Provider
    MinIO        cache)      (API)
```

---

## Risk Summary

| Risk | Impact | Mitigation |
|------|--------|------------|
| Python async ecosystem maturity | Lower than Node.js, but FastAPI + SQLAlchemy async is production-ready | Thorough testing; monitor connection pooling |
| Expo SDK limitations for native features | Audio recording may need native modules | expo-av covers MVP; eject available if needed |
| Arq community smaller than Celery | Fewer resources and integrations | MVP scale doesn't need Celery complexity |
| Supabase Auth dependency | Third-party auth dependency with migration cost | User export supported; can migrate to self-hosted auth |
