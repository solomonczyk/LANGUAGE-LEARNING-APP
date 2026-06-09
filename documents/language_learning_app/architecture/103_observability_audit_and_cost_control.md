# Observability, Audit and Cost Control

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Logging, monitoring, audit trail, and cost management across all services.

## In scope

- Overall system architecture
- AI agent architecture and validation pipeline
- Narrative, Visual, Audio scenario engines
- Curriculum, Learner Model, Assessment, Mastery, Reward engines
- Review scheduler and LQA services
- Model provider fallback and observability

## Out of scope

- Implementation code
- Infrastructure configuration
- CI/CD pipeline
- Third-party service integrations

## Core decisions

1. LLM cannot directly change mastery, XP, curriculum, or LKB
2. Required pipeline: LLM -> schema validation -> linguistic validation -> pedagogical validation -> policy engine -> state transition -> audit
3. Deterministic engines hold state authority
4. All state changes are auditable

## Acceptance criteria

1. All 14 architecture documents exist
2. LLM boundaries are clearly defined
3. Pipeline specification is complete
4. Each engine has defined responsibilities and interfaces

---

## Logging structure

Each service logs:
- All requests and responses (service health)
- All state mutations (learner model changes, mastery updates, reward transactions)
- All LLM calls (prompt, response, cost, latency)
- All validation results (pass/fail by stage)
- All errors and exceptions

## Audit trail requirements

The following operations require full audit trails:
- Mastery state changes
- Reward transactions
- Curriculum progression changes
- Profile changes
- Diagnostic results
- Content changes (LKB updates)
- Security events

## Observability metrics

- Service health: uptime, response time, error rate
- LLM usage: calls per user, tokens, cost, latency
- Learning metrics: lessons completed, items mastered, time spent
- Engagement: DAU, retention, session length
- Validation: pass/fail rates per pipeline stage

## Cost control

- Per-user daily cost cap (configurable)
- Per-session cost tracking
- Model tier routing for cost optimization
- Anomaly detection for unusual cost patterns
- Monthly cost reports by service, user, and activity type

## Alerting thresholds

- Error rate > 5% for any service
- P95 latency > 5s for lesson generation
- Cost > 2x daily average
- Any security event logged
