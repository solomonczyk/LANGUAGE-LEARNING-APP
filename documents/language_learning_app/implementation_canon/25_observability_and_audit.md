# Observability and Audit

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  
**ADR:** ADR-012, ADR-024

---

## 1. Logging

### Format
- Structured JSON
- Each log line is a single JSON object
- Never multi-line log messages

### Required Fields

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `timestamp` | ISO 8601 | `2026-06-10T14:30:00.000Z` | UTC |
| `level` | string | `INFO` | DEBUG, INFO, WARN, ERROR |
| `logger` | string | `app.modules.lesson_engine` | Module path |
| `message` | string | `Lesson session created` | Human-readable |
| `trace_id` | string (UUID) | `550e8400-...` | Correlates across modules |
| `request_id` | string (UUID) | — | HTTP request identifier |
| `user_id` | string (UUID, pseudonymized) | — | Nil if unauthenticated |
| `lesson_session_id` | string | — | Where applicable |
| `submission_id` | string | — | Where applicable |
| `provider_request_id` | string | — | AI provider request ID |
| `validation_result` | string | `passed` / `failed` | Validation outcomes |
| `policy_result` | string | `approved` / `rejected` | Policy decisions |
| `reward_transaction_id` | string | — | Reward events |
| `duration_ms` | number | — | Request latency |

### Redaction
- Fields containing `password`, `secret`, `token`, `key`, `authorization` are redacted: `[REDACTED]`
- PII (email, name) is never written to logs (use pseudonymized user_id)
- User submission content is logged only in audit (not in general application logs)

---

## 2. Metrics

| Metric | Type | Source | Notes |
|--------|------|--------|-------|
| `api.latency` | Histogram | FastAPI middleware | By endpoint, method, status |
| `api.requests_total` | Counter | FastAPI middleware | By endpoint, method |
| `api.errors_total` | Counter | FastAPI middleware | By error code |
| `mobile.errors_total` | Counter | Mobile telemetry | By screen, error type |
| `mobile.crash_count` | Counter | Sentry | — |
| `backend.errors_total` | Counter | Application | By module, error type |
| `submission.failures_total` | Counter | submission module | By failure reason |
| `ai.latency` | Histogram | AI Gateway | By operation, model |
| `ai.tokens_total` | Counter | AI Gateway | By model |
| `ai.cost_total` | Counter | AI Gateway | By model (USD) |
| `ai.failures_total` | Counter | AI Gateway | By failure cause |
| `ai.retries_total` | Counter | AI Gateway | By retry cause |
| `validation.schema_failures` | Counter | Validators | By module |
| `validation.linguistic_failures` | Counter | Linguistic validator | By reason |
| `validation.pedagogical_failures` | Counter | Pedagogical validator | By reason |
| `policy.rejection_total` | Counter | Policy engine | By policy type |
| `reward.conflicts_total` | Counter | Reward engine | Duplicate attempts |
| `reward.xp_awarded_total` | Counter | Reward engine | By activity type |
| `audit.write_failures` | Counter | Audit | — |
| `review.completion_total` | Counter | Review scheduler | — |
| `cost.per_lesson` | Gauge | Analytics | Average cost per lesson |

---

## 3. Tracing

- **Standard:** OpenTelemetry distributed tracing
- **Traced operations:**
  - Mobile HTTP request → backend → database → AI Gateway → response
  - AI Gateway call chain: provider request → schema validation → linguistic validation → pedagogical validation
  - Policy engine decision → state transition → audit write → reward computation
  - Background job execution (Arq worker → module → database)
- **Trace context propagation:**
  - Mobile: `X-Trace-Id` header on HTTP requests
  - Backend: OpenTelemetry context propagation across async calls
  - Job queue: Trace context passed to Arq jobs

---

## 4. Audit System

### Architecture
- Append-only `audit_events` table (no UPDATE, no DELETE)
- PRIMARY KEY: `event_id` (BIGSERIAL) for ordering
- WRITE: `INSERT` only (application user has no UPDATE/DELETE privilege)
- RETENTION: Partitioned by month, 2-year retention

### Audit Event Schema

```json
{
  "event_id": 12345,
  "trace_id": "550e8400-...",
  "user_id": "uuid (pseudonymized)",
  "action": "lesson_session.completed",
  "module": "lesson_engine",
  "resource_type": "lesson_session",
  "resource_id": "uuid",
  "result": "success",
  "details": {},
  "timestamp": "2026-06-10T14:30:00Z"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `event_id` | Auto | BIGSERIAL, append-only |
| `trace_id` | Yes | Correlation ID |
| `user_id` | Yes | Pseudonymized UUID |
| `action` | Yes | `{module}.{action}` (e.g., `mastery.level_up`) |
| `module` | Yes | Module name |
| `resource_type` | Yes | Entity type |
| `resource_id` | Yes | Entity UUID |
| `result` | Yes | `success`, `failure`, `blocked` |
| `details` | Conditional | Additional context (PII excluded) |
| `timestamp` | Auto | UTC |

### Audit Events (Required)

Every state transition defined in [state machines](../mvp_architecture/16_state_machines.md) must emit an audit event. Additionally:

| Action | Module | When |
|--------|--------|------|
| `auth.login` | identity | User logged in |
| `auth.logout` | identity | User logged out |
| `auth.refresh` | identity | Token refreshed |
| `gate.*` | policy_engine | Any dangerous action gate pass/fail |
| `reward.*` | reward_engine | Any reward transaction |
| `security.*` | integrity | Any security event |
| `settings.*` | learner_profile | Any setting change |
| `action.production_gate_violation` | integrity | Attempt to open production gate |

### Audit Write Failure Tolerance

```text
Audit event loss tolerance: 0
```

Audit write failure must:
1. Log the error to stdout as critical
2. Trigger an alert
3. NOT block the main operation (system proceeds but with elevated risk)
4. Queue for retry (Arq job)
5. Be reconciled in the next periodic audit completeness check

---

## 5. Observability Stack

| Component | Tool | Hosting |
|-----------|------|---------|
| Metrics collection | OpenTelemetry Collector | Sidecar / DaemonSet |
| Metrics storage | Prometheus | Self-hosted (Docker) |
| Visualization | Grafana | Self-hosted |
| Log aggregation | Loki | Self-hosted (Docker) |
| Tracing | Tempo | Self-hosted (Docker) |
| Error tracking | Sentry | Cloud (free tier) |
| Cost tracking | Custom (AI Gateway) | Application |
