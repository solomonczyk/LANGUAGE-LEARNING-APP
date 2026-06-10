# Architecture Decision Log

**Status:** Draft  
**Version:** 1.0.0  
**Last updated:** 2026-06-10

---

## ADR-001: Mobile Framework

**Status:** Accepted  
**Context:** The mobile client is the primary interface for learners. Options included React Native + Expo, Flutter, native Android/iOS, and PWA. The framework must support rapid MVP development while providing access to native device features (audio recording, push notifications, biometrics). The team's strongest skill alignment is with TypeScript/React ecosystem.  
**Decision:** Use React Native with Expo SDK for mobile development, with TypeScript as the language, Expo Router for navigation, TanStack Query for server state, and Zustand for client state.  
**Alternatives Considered:** Flutter (strong widget system but adds Dart to the stack), native Android/iOS (too slow for MVP), PWA (insufficient native API access).  
**Consequences:** Positive — fast development, TypeScript consistency with backend validation patterns, large ecosystem. Negative — Expo abstraction may limit some native capabilities; ejection from Expo is possible but costly.  
**Risks:** Expo SDK release cycle may lag behind React Native; native module requirements may exceed Expo capabilities.  
**Reversal Strategy:** Eject from Expo to bare React Native workflow; or migrate specific screens to native modules.

---

## ADR-002: Backend Framework

**Status:** Accepted  
**Context:** The backend handles REST API, business logic, AI gateway, and data persistence. Options included FastAPI (Python), NestJS (Node), and Django/DRF. Key requirements: async support for LLM calls, strong validation for structured data, automatic OpenAPI generation, and ML/AI ecosystem compatibility.  
**Decision:** Use FastAPI with Python 3.12+, Pydantic v2 for validation, SQLAlchemy 2.0 for ORM, and Alembic for migrations.  
**Alternatives Considered:** NestJS (TypeScript consistency but Node.js ecosystem weaker for ML), Django/DRF (heavy framework, synchronous by default).  
**Consequences:** Positive — automatic OpenAPI, excellent async support, strong validation, ML ecosystem. Negative — Python async ecosystem less mature than Node.js; type safety weaker than TypeScript.  
**Risks:** Python GIL may limit CPU-bound operations; async SQLAlchemy has learning curve.  
**Reversal Strategy:** Extract AI Gateway to separate service if Python becomes a bottleneck; migrate individual modules to microservices.

---

## ADR-003: Modular Monolith

**Status:** Accepted  
**Context:** The architecture must support clear module boundaries while maintaining development velocity for a small MVP team. Microservices introduce operational complexity (service discovery, distributed transactions, inter-service communication) that is not justified for MVP scale.  
**Decision:** Use a modular monolith architecture with 20 bounded modules, each with defined interfaces, owned entities, and forbidden responsibilities. Modules communicate via Python function calls through interface contracts.  
**Alternatives Considered:** Microservices (premature complexity), traditional monolithic (no module boundaries).  
**Consequences:** Positive — simpler deployment, single database transaction, faster development, clear module boundaries. Negative — modules can become coupled if boundaries are not enforced; extraction to services requires effort if needed.  
**Risks:** Boundary erosion over time; deployment coupling (all modules deployed together).  
**Reversal Strategy:** Extract high-cohesion modules into separate services when justified by scaling or team structure.

---

## ADR-004: PostgreSQL as Source of Truth

**Status:** Accepted  
**Context:** The data model requires ACID transactions for reward integrity, relational integrity for learning data, flexible fields for learner profiles, and strong query capabilities for analytics.  
**Decision:** Use PostgreSQL 16 as the primary and sole source of truth. All business data stored in PostgreSQL with no secondary authoritative stores.  
**Alternatives Considered:** MongoDB (flexible schema but weak joins), Firebase/Supabase (vendor lock-in for core data).  
**Consequences:** Positive — ACID compliance, JSONB for flexible fields, strong query capabilities, mature tooling. Negative — schema migrations required; vertical scaling limit for single primary.  
**Risks:** Connection pool exhaustion under load; migration errors in production.  
**Reversal Strategy:** Add read replicas for scaling; migrate specific document-oriented data to document store if needed.

---

## ADR-005: Background Job Mechanism

**Status:** Accepted  
**Context:** The system needs background processing for AI analysis, notification delivery, and async audit writes. Options included Celery, Dramatiq, Arq, and PostgreSQL-based job queue.  
**Decision:** Use Arq with Redis as the background job queue. Arq's async-native design fits FastAPI's async model without the complexity of Celery.  
**Alternatives Considered:** Celery (battle-tested but heavy configuration), Dramatiq (simpler but less async-native), PostgreSQL job queue (simpler but limited scalability).  
**Consequences:** Positive — async-native, minimal configuration, Redis-backed. Negative — smaller community than Celery; Redis dependency for job processing.  
**Risks:** Redis outage stops job processing; Arq community issues may lack support.  
**Reversal Strategy:** Replace Arq with Celery if advanced scheduling or monitoring needed.

---

## ADR-006: Object Storage

**Status:** Accepted  
**Context:** The system requires object storage for audio recordings, lesson images, and content assets. Must work in local development and staging without external dependencies.  
**Decision:** Use S3-compatible object storage: MinIO for local development, Cloudflare R2 for staging. The S3 API standard provides portability.  
**Alternatives Considered:** AWS S3 (vendor lock-in, egress costs), Google Cloud Storage (vendor lock-in).  
**Consequences:** Positive — vendor-independent S3 API, free local development, no egress fees on R2. Negative — R2 has fewer features than S3.  
**Risks:** R2 compatibility gaps with S3 API.  
**Reversal Strategy:** Switch to AWS S3 or any S3-compatible provider by changing endpoint configuration.

---

## ADR-007: Authentication Strategy

**Status:** Accepted  
**Context:** Authentication must support email/password and social login (Google, Apple), with JWT token management and reasonable MVP effort.  
**Decision:** Use Supabase Auth as the authentication provider. Provides email/password auth, OAuth social login, JWT management, and row-level security integration with PostgreSQL.  
**Alternatives Considered:** Clerk (rich features but more expensive), Firebase Auth (vendor lock-in, Google ecosystem), self-hosted JWT (full control but high implementation effort).  
**Consequences:** Positive — quick setup, social login built-in, PostgreSQL RLS integration, generous free tier. Negative — third-party dependency; user data stored with Supabase.  
**Risks:** Supabase pricing changes; service outage prevents login.  
**Reversal Strategy:** Export users and migrate to self-hosted auth or alternative provider.

---

## ADR-008: AI Gateway Abstraction

**Status:** Accepted  
**Context:** The system relies on LLM providers for analysis and feedback. Provider independence avoids vendor lock-in and enables fallback. Structured output enforcement is critical for safety.  
**Decision:** Build a provider-independent AI Gateway abstraction layer within the backend. All LLM calls go through the gateway, which enforces structured output, manages provider failover, tracks costs, and records audit events.  
**Alternatives Considered:** Direct provider SDK integration (simple but tight coupling), third-party AI gateway (additional dependency).  
**Consequences:** Positive — provider independence, centralized validation, cost tracking, audit. Negative — additional abstraction layer; must maintain provider SDK adapters.  
**Risks:** Provider API changes require adapter updates; gateway becomes a bottleneck.  
**Reversal Strategy:** Split gateway into separate service if latency or scaling becomes an issue.

---

## ADR-009: Structured Output Validation

**Status:** Accepted  
**Context:** LLM outputs must be validated before any state change. Schema, linguistic, and pedagogical validation ensure quality and safety.  
**Decision:** Three-stage validation pipeline: (1) schema validation (Pydantic/JSON Schema), (2) linguistic validation (grammar, accuracy), (3) pedagogical validation (level-appropriateness, learning value). All three must pass before state transitions occur.  
**Alternatives Considered:** Single validation stage (insufficient), no validation (unsafe), LLM self-validation (unreliable).  
**Consequences:** Positive — defense in depth, clear failure points, audit trail for each stage. Negative — increased pipeline latency; more complex error handling.  
**Risks:** Over-validation may reject acceptable outputs; false positives frustrate learners.  
**Reversal Strategy:** Adjust validation thresholds per stage; add override capability for operator review (post-MVP).

---

## ADR-010: Deterministic Mastery and Rewards

**Status:** Accepted  
**Context:** Mastery transitions and reward decisions must be completely deterministic. LLM must not influence state transitions or reward amounts. This protects system integrity and prevents gaming.  
**Decision:** Mastery engine and reward engine are 100% deterministic. LLM analysis provides evidence for mastery but cannot cause state transitions. Reward amounts are pre-defined per activity type with no LLM input.  
**Alternatives Considered:** LLM-influenced rewards (risk of gaming and inconsistency), hybrid approach (blurs accountability).  
**Consequences:** Positive — system integrity, predictable behavior, testable logic. Negative — less flexibility; cannot reward nuanced performance.  
**Risks:** Deterministic system may not capture all learning dimensions.  
**Reversal Strategy:** Add performance modifiers to reward calculation if needed, but keep LLM out of reward logic.

---

## ADR-011: Audit Architecture

**Status:** Accepted  
**Context:** Complete auditability is required for all state-changing operations. Audit events must be immutable, traceable, and queryable.  
**Decision:** Implement an append-only audit event table (no UPDATE or DELETE allowed by application role). Each event includes trace_id for correlation, user_id (pseudonymized), action, module, details, and result. Concurrent writes are handled via BIGSERIAL primary key.  
**Alternatives Considered:** File-based audit logs (harder to query), external audit service (additional dependency), blockchain-based audit (over-engineered for MVP).  
**Consequences:** Positive — immutable, queryable, correlated via trace_id. Negative — audit table grows quickly; partitioning strategy needed.  
**Risks:** Audit write failure must not block main operation; buffer and async write strategy needed.  
**Reversal Strategy:** Add audit log archival to object storage for long-term retention.

---

## ADR-012: Observability Stack

**Status:** Accepted  
**Context:** The system requires metrics, structured logging, and distributed tracing for debugging, monitoring, and cost tracking.  
**Decision:** Use OpenTelemetry for instrumentation and data collection, with Grafana + Prometheus (metrics), Loki (logs), and Tempo (traces) for storage and visualization. Sentry provides error tracking. The stack is self-hosted for staging to control costs.  
**Alternatives Considered:** Datadog (expensive for MVP), New Relic (expensive), AWS X-Ray (vendor lock-in).  
**Consequences:** Positive — open standard, self-hostable, no vendor lock-in, covers all three pillars. Negative — requires infrastructure to host the observability stack.  
**Risks:** Self-hosting complexity; scaling the observability stack for larger deployments.  
**Reversal Strategy:** Migrate to managed OpenTelemetry-compatible services (Grafana Cloud, Datadog) as scale requires.
