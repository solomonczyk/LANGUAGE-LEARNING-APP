# Observability

**Status:** Draft  
**Version:** 1.0.0  
**Last updated:** 2026-06-10

---

## Strategy Overview

Observability is built on three pillars: **structured logging**, **metrics**, and **distributed tracing**, using OpenTelemetry as the unified data collection standard. The stack is self-hosted for staging (Grafana + Prometheus + Loki + Tempo) with Sentry for error tracking.

---

## 1. Logging

### Log Format (Structured JSON)

Every log entry MUST include these fields:

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| timestamp | ISO8601 | Event time | Always |
| level | string | debug, info, warn, error, fatal | Always |
| trace_id | UUID | OpenTelemetry trace ID | Always |
| span_id | UUID | OpenTelemetry span ID | Always |
| service | string | "backend-api" | Always |
| module | string | Module name (e.g., "lesson_engine") | Always |
| user_id | string | Pseudonymized user ID (NOT email) | When available |
| request_id | UUID | HTTP request ID | When available |
| lesson_session_id | UUID | Current lesson session | When available |
| provider_request_id | string | AI provider request ID | LLM calls |
| validation_result | string | pass/fail | Validation steps |
| policy_result | string | approved/rejected/retry | Policy decisions |
| reward_transaction_id | UUID | Reward transaction ID | Reward events |
| message | string | Human-readable message | Always |
| error | object | Error details | On error |

### Log Levels

| Level | When to Use |
|-------|-------------|
| DEBUG | Detailed diagnostic information (development only in staging) |
| INFO | Normal operation events (lesson started, completed, reward) |
| WARN | Unexpected but handled situations (retry, fallback used) |
| ERROR | Error that requires investigation (provider failure, validation failure) |
| FATAL | System cannot continue (database connection lost) |

### Log Retention
- **Local**: 7 days
- **Staging**: 30 days in Loki
- **Production (future)**: 90 days hot, 1 year cold

---

## 2. Metrics

### API Metrics

| Metric | Type | Description |
|--------|------|-------------|
| api_requests_total | Counter | Total API requests by endpoint, method, status |
| api_request_duration_seconds | Histogram | Request latency (p50, p95, p99) by endpoint |
| api_requests_active | Gauge | Currently active requests |

### AI/Latency Metrics

| Metric | Type | Description |
|--------|------|-------------|
| llm_request_duration_seconds | Histogram | LLM call latency by provider, model, operation |
| llm_requests_total | Counter | LLM call count by provider, model, result |
| llm_errors_total | Counter | LLM errors by provider, error type |
| llm_tokens_total | Counter | Token usage by provider, model |
| llm_cost_total | Counter | Cost by provider (from token count) |

### Validation Metrics

| Metric | Type | Description |
|--------|------|-------------|
| validation_results_total | Counter | Validation results by validator type, result |
| validation_duration_seconds | Histogram | Validation latency by validator type |

### Pipeline Metrics

| Metric | Type | Description |
|--------|------|-------------|
| pipeline_duration_seconds | Histogram | Full pipeline duration |
| pipeline_step_duration | Histogram | Per-step duration |
| pipeline_results_total | Counter | Pipeline result (accepted, rejected, failed) |

### Business Metrics

| Metric | Type | Description |
|--------|------|-------------|
| lesson_completions_total | Counter | Lesson completions by type |
| lesson_completion_rate | Gauge | Ratio of started vs completed |
| review_completions_total | Counter | Review completions |
| duplicate_attempts_total | Counter | Duplicate reward/submission attempts |
| security_events_total | Counter | Security events by type, severity |
| xp_awarded_total | Counter | Total XP awarded |
| active_users | Gauge | Daily/weekly active users |

### Cost Metrics

| Metric | Type | Description |
|--------|------|-------------|
| cost_per_lesson | Gauge | Average AI cost per completed lesson |
| cost_per_user | Gauge | AI cost per user (daily) |
| provider_cost_total | Counter | Cost by provider |
| storage_bytes_total | Gauge | Object storage usage by bucket |

---

## 3. Tracing

### Required Trace Coverage

Every span must include:
- `trace_id` — shared across all spans in a request
- `span_id` — unique span identifier
- `parent_span_id` — parent span for hierarchy
- `service.name` — "backend-api"
- `module` — owning module name

### Trace: Full Lesson Submission Pipeline

```
POST /lesson-sessions/{id}/attempts
  ├── input_normalization
  ├── security_scan
  ├── schema_validation
  ├── context_binding
  ├── llm_proposal
  │   ├── http.request (to LLM provider)
  │   └── response_parsing
  ├── output_validation
  ├── linguistic_validation
  ├── pedagogical_validation
  ├── policy_engine
  ├── state_transition
  ├── mastery_evidence
  ├── review_scheduling
  ├── reward_transaction
  ├── audit_event
  └── response_assembly
```

### Trace: AI Provider Call (Detailed)

```
llm_proposal
  ├── prompt_assembly (template + context)
  ├── provider_router (primary or fallback)
  ├── http.request (LLM API call)
  │   ├── request_tokens
  │   ├── response_tokens
  │   └── latency
  ├── response_validation (schema check)
  └── cost_tracking
```

---

## 4. Alerting

### Critical Alerts (Pager)

| Alert | Condition | Threshold | Response |
|-------|-----------|-----------|----------|
| API Down | Health check fails | 2 consecutive failures | Investigate immediately |
| High Error Rate | 5xx rate > 5% | 5-minute window | Investigate immediately |
| Audit Write Failure | Audit event write fails | Any occurrence | Investigate immediately |
| Reward Duplicate Spike | Duplicate attempts > 5/min | 5-minute window | Investigate reward integrity |

### Warning Alerts (Ticket)

| Alert | Condition | Threshold |
|-------|-----------|-----------|
| High AI Latency | LLM p95 > 15s | 5-minute window |
| Provider Failure Rate | LLM errors > 10% | 5-minute window |
| Schema Validation Failure | Validation failure rate > 5% | 15-minute window |
| High Retry Rate | Pipeline retry rate > 10% | 15-minute window |
| Pedagogical Rejection Spike | Rejection rate > 15% | 30-minute window |
| Security Event Rate | Security events > 10/hour | 1-hour window |
| Cost Anomaly | Daily cost > 2x normal | Daily check |

---

## 5. Dashboards

### Suggested Grafana Dashboards

| Dashboard | Panels |
|-----------|--------|
| **API Overview** | Request rate, latency (p50/p95/p99), error rate, active requests |
| **AI Performance** | LLM latency by provider, token usage, cost rate, provider error rate |
| **Pipeline Health** | Pipeline duration, step breakdown, pass/fail rate, retry rate |
| **Business KPIs** | Lesson completion rate, review completion rate, active users, XP awarded |
| **Security** | Security events by type, rate limit hits, duplicate attempts, auth failures |
| **Cost** | Cost per lesson, cost per user, provider cost breakdown, daily cost trend |

---

## 6. Cost Tracking

### Per-Lesson Cost Calculation

```
lesson_cost = SUM(
  text_analysis_cost +
  feedback_cost +
  (dialogue_turns × dialogue_turn_cost) +
  (retries × retry_cost)
)
```

Cost data is:
- Captured per AI request (tokens × provider rate)
- Aggregated per lesson session
- Stored in audit event metadata
- Available via analytics API

### Budget Alerts

| Scope | Threshold | Action |
|-------|-----------|--------|
| Daily AI cost | $X (configured) | Warning alert |
| Weekly AI cost | $X × 7 | Critical alert |
| Per-user daily cost | $X (anomaly threshold) | Warning alert |
| Provider budget | $X (configured per provider) | Critical alert — failover |
