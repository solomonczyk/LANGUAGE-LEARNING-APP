# Technology Stack Comparison

**Status:** Draft  
**Version:** 1.0.0  
**Last updated:** 2026-06-10

---

## 1. Mobile Client

### Options

| Criterion | React Native + Expo | Flutter | Native Android/iOS | PWA |
|-----------|--------------------|---------|-------------------|-----|
| **Fit to user stories** | Excellent — routing, forms, state management all well-supported | Good — widget system maps well to custom UI | Excellent — full platform capability | Poor — limited access to native APIs (audio, push, biometrics) |
| **Development speed** | Fast — Expo tooling, hot reload, EAS Build | Fast — hot reload, strong widget library | Slow — separate codebases for iOS/Android | Fast — web technology reuse |
| **Mobile support** | iOS + Android from one codebase | iOS + Android from one codebase | Native performance, full API access | Limited — no native modules |
| **Typing** | TypeScript — excellent | Dart — good, smaller ecosystem | Kotlin/Swift — excellent native typing | TypeScript — excellent |
| **Ecosystem** | Very large — npm ecosystem, React Native community | Growing — pub.dev, Google-backed | Mature — platform SDKs | Universal — web standards |
| **Security** | Good — depends on Expo security updates | Good — depends on Flutter security updates | Excellent — platform security model | Limited — browser security model |
| **Scalability** | Good — code organization patterns well-established | Good — widget composition | Excellent — platform-optimized | Limited — performance ceiling |
| **Cost** | Free, EAS Build has free tier | Free | Higher — separate iOS/Android dev | Free |
| **Self-hosting** | N/A (client-side) | N/A | N/A | N/A |
| **Operational complexity** | Low-moderate — Expo manages native builds | Moderate — Flutter build tooling | High — two platform build pipelines | Low |
| **Vendor lock-in** | Low — can eject from Expo | Moderate — Google-maintained | Low — platform standard | Low — web standard |
| **Team fit** | Strong — TypeScript throughout stack | Good — but adds Dart to polyglot | Fair — requires iOS + Android expertise | Fair — but limited capability |

**Decision:** React Native + Expo  
**Rationale:** Best fit for MVP speed while maintaining native capability. TypeScript shared with backend (if Node) or similar typing to Python Pydantic. Strong ecosystem for forms, state management, and navigation.

---

## 2. Backend

### Options

| Criterion | FastAPI (Python) | NestJS (Node) | Django/DRF |
|-----------|-----------------|---------------|------------|
| **Fit to user stories** | Excellent — async, Pydantic validation, OpenAPI generation | Excellent — structured, decorators, DI | Good — batteries included but heavy |
| **Development speed** | Fast — automatic OpenAPI, auto-validation | Fast — CLI generators, modular | Moderate — convention-over-configuration overhead |
| **Mobile support** | Excellent — REST API, JSON responses | Excellent — REST + GraphQL | Excellent — REST via DRF |
| **Typing** | Python + Pydantic v2 — good, runtime validation | TypeScript — excellent, compile-time safety | Python + DRF Serializers — minimal typing |
| **Ecosystem** | Rich — ML/AI native ecosystem | Rich — Node.js ecosystem | Very rich — Django packages |
| **Security** | Good — Pydantic validation, dependency injection | Good — middleware, guards, interceptors | Excellent — mature auth, CSRF, XSS protection |
| **Scalability** | Good — async, background tasks, horizontal scaling | Excellent — async, microservice-ready | Moderate — synchronous by default |
| **Cost** | Free | Free | Free |
| **Self-hosting** | Excellent — single process, Docker-friendly | Excellent | Excellent |
| **Operational complexity** | Low — simple deployment | Moderate — Node.js process management | Low-moderate |
| **Vendor lock-in** | Low — open standard | Low — open standard | Low |
| **Team fit** | Strong — Python widely known; ML ecosystem synergy | Good — if team has TypeScript expertise | Fair — but heavy for MVP |

**Decision:** FastAPI (Python)  
**Rationale:** FastAPI's automatic OpenAPI generation, Pydantic v2 validation, and async-first design match the requirements perfectly. Python ecosystem is ideal for eventual AI/ML integration. The framework supports modular monolith structure naturally through APIRouter and dependency injection.

---

## 3. Database

### Options

| Criterion | PostgreSQL | MongoDB | Managed (Supabase/Firebase) |
|-----------|-----------|---------|---------------------------|
| **Fit to user stories** | Excellent — relational data, transactions, JSONB for flexible fields | Good — flexible schema but weak joins | Good — rapid setup but vendor coupling |
| **Development speed** | Good — Alembic migrations, SQLAlchemy ORM | Fast — schema-less | Fastest — minimal setup |
| **Mobile support** | Excellent — any backend framework works | Good | Good — SDK available |
| **Typing** | Excellent — schema-enforced types | Fair — document validation | Good — typed SDKs |
| **Ecosystem** | Very mature — extensions, tooling | Mature | Growing |
| **Security** | Excellent — row-level security, encryption | Good | Provider-dependent |
| **Scalability** | Excellent — read replicas, partitioning | Excellent — horizontal sharding | Provider-dependent |
| **Cost** | Free (self-hosted) / Managed available | Free / Managed available | Scales with usage |
| **Self-hosting** | Excellent | Good | Not possible |
| **Operational complexity** | Moderate — requires DBA knowledge | Low-moderate | Low |
| **Vendor lock-in** | None — open standard | Minimal | High — provider-specific features |
| **Team fit** | Strong — widely known | Fair | Fair |

**Decision:** PostgreSQL  
**Rationale:** PostgreSQL provides relational integrity for learning data, JSONB for flexible profiles, excellent transaction support for reward integrity, and mature tooling (Alembic, SQLAlchemy). The ACID guarantees are essential for reward and audit requirements.

---

## 4. Queue / Background Processing

| Criterion | Celery | Dramatiq | Arq | PostgreSQL Job Queue |
|-----------|--------|----------|-----|---------------------|
| **Fit to user stories** | Good — battle-tested | Good — simpler than Celery | Good — async-native | Fair — no separate infra |
| **Development speed** | Moderate — configuration-heavy | Good | Good — Redis-native async | Fast — no new dependencies |
| **Typing** | Python — fair | Python — fair | Python + Redis — fair | Python — fair |
| **Ecosystem** | Very mature | Maturing | Growing | Minimal |
| **Security** | Good — Redis ACL | Good | Good | Good — DB-level |
| **Scalability** | Excellent | Good | Good | Limited — DB bottleneck |
| **Cost** | Free | Free | Free | Free |
| **Self-hosting** | Excellent | Excellent | Excellent | Excellent |
| **Operational complexity** | High — broker, result backend, monitoring | Moderate | Low — Redis only | Low — no additional infra |
| **Vendor lock-in** | Low | Low | Low | None |
| **Team fit** | Good — widely known | Fair | Fair — growing adoption | Fair |

**Decision:** Arq  
**Rationale:** Arq provides async-native Redis-backed job queuing that fits naturally with FastAPI's async model. Simpler than Celery (no separate worker configuration complexity), while providing sufficient reliability for MVP async tasks (AI analysis, notifications).

---

## 5. Object Storage

| Criterion | MinIO (self-hosted) | AWS S3 | Cloudflare R2 |
|-----------|-------------------|--------|---------------|
| **Fit to user stories** | Excellent — S3-compatible | Excellent | Excellent |
| **Development speed** | Fast — Docker container | Fast — SDK | Fast — SDK |
| **Security** | Good — identity-based | Excellent — IAM | Good |
| **Cost** | Free | Pay-per-use | Free egress, pay-per-use |
| **Self-hosting** | Excellent | Not possible | Not possible |
| **Vendor lock-in** | Low — S3 API standard | High | Moderate |
| **Team fit** | Strong | Strong | Strong |

**Decision:** S3-compatible (MinIO local, R2 staging)  
**Rationale:** S3 API is the industry standard. MinIO enables fully local development without external dependencies. Cloudflare R2 provides cost-effective staging without egress fees.

---

## 6. Authentication

| Criterion | Supabase Auth | Clerk | Firebase Auth | Self-hosted JWT |
|-----------|--------------|-------|--------------|-----------------|
| **Fit to user stories** | Excellent — social login, email/password, RLS | Excellent — rich features | Excellent | Good — full control |
| **Development speed** | Fast — drop-in client SDK | Fast | Fast | Slow — implement from scratch |
| **Security** | Excellent — SOC 2 compliant | Excellent | Excellent | Depends on implementation |
| **Cost** | Free tier generous | Free tier limited | Free tier generous | Free |
| **Vendor lock-in** | Moderate — can migrate users | Moderate | High — Firebase-specific | None |
| **Operational complexity** | Low | Low | Low | High |

**Decision:** Supabase Auth  
**Rationale:** Supabase provides managed auth with social login support, row-level security integration with PostgreSQL, and generous free tier. Can be self-hosted if needed. Provides OAuth support out of the box.

---

## 7. Observability

| Criterion | OpenTelemetry | Datadog | Grafana Stack | Sentry |
|-----------|--------------|---------|---------------|--------|
| **Fit to user stories** | Excellent — traces, metrics, logs | Excellent | Excellent | Good — error tracking |
| **Development speed** | Moderate — instrumentation setup | Fast | Moderate | Fast |
| **Cost** | Free | Expensive | Free (self-hosted) / Grafana Cloud | Free tier |
| **Vendor lock-in** | Low — open standard | High | Low — open source | Moderate |
| **Self-hosting** | Excellent | Not possible | Excellent | Not possible |
| **Team fit** | Strong — industry standard | Fair — budget concern | Strong | Strong |

**Decision:** OpenTelemetry + Grafana stack + Sentry  
**Rationale:** OpenTelemetry is the open standard for observability data. Self-hosted Grafana + Prometheus + Loki provide cost-effective metrics and logs. Sentry provides specialized error tracking with rich context.

---

## Summary Decision Table

| Category | Selected Option | Runner-Up | Key Differentiator |
|----------|----------------|-----------|-------------------|
| Mobile | React Native + Expo | Flutter | TypeScript consistency, ecosystem |
| Backend | FastAPI (Python) | NestJS | Auto OpenAPI, Pydantic, ML-ready |
| Database | PostgreSQL | — | ACID, JSONB, maturity |
| Queue | Arq | PostgreSQL Job Queue | Async-native, Redis simplicity |
| Object Storage | MinIO (local) / R2 (staging) | AWS S3 | S3-compatible, cost-effective |
| Auth | Supabase Auth | Clerk | PostgreSQL RLS integration |
| Observability | OpenTelemetry + Grafana + Sentry | Datadog | Open standard, self-hostable |
