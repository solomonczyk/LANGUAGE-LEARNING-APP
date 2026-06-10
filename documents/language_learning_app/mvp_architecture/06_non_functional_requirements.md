# Non-Functional Requirements

**Status:** Draft  
**Version:** 1.0.0  
**Last updated:** 2026-06-10

---

## Required Initial Targets

The following targets are mandatory and must be met for MVP acceptance:

```json
{
  "api_p95_latency_non_ai_ms": 500,
  "lesson_state_transition_p95_ms": 300,
  "llm_analysis_target_p95_seconds": 12,
  "availability_target": "99.5%",
  "audit_event_loss_tolerance": 0,
  "reward_double_credit_tolerance": 0,
  "cross_user_data_leak_tolerance": 0
}
```

---

## NFR Catalog

### NFR-001: API Response Time (Non-AI)
**Category:** Performance | **Priority:** Critical  
**Description:** All API endpoints that do not involve LLM calls must respond within defined latency targets.  
**Target:** p95 < 500ms, p99 < 1500ms  
**Measurement:** Request tracing via OpenTelemetry; percentile aggregation over 5-minute windows  
**Source:** Product requirement for responsive UX

### NFR-002: Lesson State Transition Latency
**Category:** Performance | **Priority:** Critical  
**Description:** Deterministic state transitions (validation, scoring, mastery update) must complete within latency target.  
**Target:** p95 < 300ms  
**Measurement:** Span timing for state transition operations  
**Source:** User journey step timing requirements

### NFR-003: LLM Analysis Completion Time
**Category:** Performance | **Priority:** High  
**Description:** AI analysis of learner submissions must complete within acceptable time to maintain flow.  
**Target:** p95 < 12 seconds (provisional — may be adjusted based on provider performance)  
**Measurement:** AI Gateway span timing from request to validated response  
**Source:** User journey requiring real-time feedback

### NFR-004: API Availability
**Category:** Availability | **Priority:** Critical  
**Description:** The backend API must maintain high availability during operating hours.  
**Target:** 99.5% availability measured monthly (excluding planned maintenance)  
**Measurement:** Uptime checks every 60 seconds; successful response rate  
**Source:** Product reliability requirement

### NFR-005: Audit Event Durability
**Category:** Auditability | **Priority:** Critical  
**Description:** No audit event may be lost under any circumstances.  
**Target:** 0 events lost (audit_event_loss_tolerance = 0)  
**Measurement:** Sequential audit event ID monitoring; reconciliation checks  
**Source:** Regulatory and security requirement

### NFR-006: Reward Transaction Integrity
**Category:** Security | **Priority:** Critical  
**Description:** No learner may receive double credit for the same action.  
**Target:** 0 duplicate credit events (reward_double_credit_tolerance = 0)  
**Measurement:** Idempotency key monitoring; duplicate detection alerts  
**Source:** Reward economy integrity

### NFR-007: Data Isolation
**Category:** Security | **Priority:** Critical  
**Description:** No learner data may be accessible to another learner under any circumstances.  
**Target:** 0 cross-user data leak events (cross_user_data_leak_tolerance = 0)  
**Measurement:** Penetration testing; automated IDOR detection in CI  
**Source:** Privacy and security requirement

### NFR-008: Mobile Responsiveness
**Category:** Mobile | **Priority:** High  
**Description:** The mobile app UI must respond to user interactions within defined time.  
**Target:** UI response < 100ms for navigation and local operations; loading states for network operations  
**Measurement:** React Native interaction tracking; Firebase Performance Monitoring  
**Source:** UX requirement for mobile learning

### NFR-009: Accessibility Compliance
**Category:** Accessibility | **Priority:** Medium  
**Description:** The mobile app must meet accessibility standards for learners with disabilities.  
**Target:** WCAG 2.1 AA compliance for all learner-facing screens  
**Measurement:** Automated accessibility audit in CI; manual review per sprint  
**Source:** Inclusive learning requirement

### NFR-010: Localization Support
**Category:** Localization | **Priority:** High  
**Description:** The app must support the native language UI for at least one language pair in MVP. Architecture must support extension.  
**Target:** Full UI localization for 1 support language; i18n framework in place  
**Measurement:** i18n coverage report; string extraction audit  
**Source:** Persona P-02 requirement

### NFR-011: API Idempotency
**Category:** Reliability | **Priority:** Critical  
**Description:** All mutating API endpoints must support idempotent operations via idempotency keys.  
**Target:** 100% of POST/PUT/PATCH endpoints support idempotency-key header  
**Measurement:** Contract test per endpoint; idempotency audit  
**Source:** Duplicate submission prevention (FR-054)

### NFR-012: Data Consistency
**Category:** Reliability | **Priority:** High  
**Description:** The system must maintain data consistency across entities within the modular monolith.  
**Target:** PostgreSQL transaction isolation (READ COMMITTED minimum); no eventual consistency for critical paths  
**Measurement:** Consistency validation tests; no dirty reads in audit trail  
**Source:** Trust in learning data

### NFR-013: Model Fallback
**Category:** Reliability | **Priority:** High  
**Description:** AI Gateway must support provider fallback in case of primary provider failure.  
**Target:** Configured primary + fallback provider; automatic fallback within 30s of primary failure detection  
**Measurement:** Provider health monitoring; fallback trigger count  
**Source:** AI dependency risk mitigation

### NFR-014: Rate Limiting
**Category:** Security | **Priority:** Critical  
**Description:** API rate limits must prevent abuse while allowing legitimate usage.  
**Target:** 100 req/min authenticated, 10 req/min unauthenticated, 5 auth attempts/min/IP  
**Measurement:** Rate limit hit count; abuse incident tracking  
**Source:** Abuse prevention (FR-055)

### NFR-015: Disaster Recovery
**Category:** Reliability | **Priority:** Medium  
**Description:** The system must support recovery from data loss scenarios.  
**Target:** RPO < 1 hour (database), RTO < 4 hours  
**Measurement:** Restore drill results  
**Source:** Operational reliability

### NFR-016: Maintainability
**Category:** Quality | **Priority:** Medium  
**Description:** The codebase must maintain testability and clarity standards.  
**Target:** Test coverage > 80% (backend), > 60% (mobile), linting without errors  
**Measurement:** CI pipeline coverage reports, linting results  
**Source:** Development velocity requirement

### NFR-017: Testability
**Category:** Quality | **Priority:** Medium  
**Description:** The system architecture must support automated testing at all levels of the test pyramid.  
**Target:** All state machines testable without LLM; all validators testable in isolation  
**Measurement:** Test architecture review; validation pipeline unit tests  
**Source:** Quality assurance requirement

### NFR-018: LLM Cost Control
**Category:** Cost | **Priority:** High  
**Description:** AI provider costs must be controlled and predictable per lesson.  
**Target:** Cost per lesson < $0.10 (provisional); total monthly AI cost budget with alerting  
**Measurement:** Cost tracking per user, per lesson, per provider  
**Source:** Operational cost management

### NFR-019: Observability Coverage
**Category:** Observability | **Priority:** High  
**Description:** All system components must emit structured logs, metrics, and traces.  
**Target:** 100% of endpoints traced; all validation failures logged; all policy decisions logged  
**Measurement:** Trace coverage report; log completeness audit  
**Source:** Operational visibility requirement

### NFR-020: Graceful Degradation
**Category:** Reliability | **Priority:** High  
**Description:** System must degrade gracefully when AI provider is unavailable; non-AI features remain functional.  
**Target:** Non-AI endpoints functional during AI provider outage; clear user messaging about AI feature unavailability  
**Measurement:** Chaos engineering tests  
**Source:** User experience during provider issues

### NFR-021: Mobile Battery Impact
**Category:** Performance | **Priority:** Medium  
**Description:** The mobile app must not excessively drain device battery.  
**Target:** < 5% battery usage per 30-minute lesson session (provisional)  
**Measurement:** Battery usage profiling  
**Source:** Mobile UX requirement

### NFR-022: Audio Quality
**Category:** Performance | **Priority:** Medium  
**Description:** Audio recording and playback quality must support effective language learning.  
**Target:** Sampling rate >= 16kHz for recordings; clear playback at normal volume  
**Measurement:** Audio quality assessment  
**Source:** Audio lesson requirement

### NFR-023: Schema Validation Performance
**Category:** Performance | **Priority:** Medium  
**Description:** Schema validation for LLM outputs must not become a bottleneck.  
**Target:** Validation complete < 100ms for typical LLM response payload  
**Measurement:** Validation gate span timing  
**Source:** Pipeline latency requirement

### NFR-024: Database Connection Pooling
**Category:** Scalability | **Priority:** Medium  
**Description:** Database connections must be pooled and reused efficiently.  
**Target:** Max 20 simultaneous connections per API instance; connection wait < 50ms  
**Measurement:** Connection pool metrics  
**Source:** Scalability requirement

### NFR-025: CI Pipeline Duration
**Category:** Development | **Priority:** Low  
**Description:** CI pipeline must complete within acceptable time for developer iteration.  
**Target:** Full CI pipeline < 15 minutes  
**Measurement:** CI workflow duration tracking  
**Source:** Development velocity

### NFR-026: Security Event Response
**Category:** Security | **Priority:** Critical  
**Description:** Security events must be detected and alert operators promptly.  
**Target:** Security event alert within 5 minutes of occurrence  
**Measurement:** Event-to-alert latency  
**Source:** Security monitoring requirement

### NFR-027: Content Delivery Latency
**Category:** Performance | **Priority:** Medium  
**Description:** Lesson content (text, images, audio) must load within acceptable time.  
**Target:** Content load p95 < 2 seconds (cached), < 5 seconds (cold)  
**Measurement:** Content delivery timing  
**Source:** Lesson experience quality

### NFR-028: Scheduler Accuracy
**Category:** Reliability | **Priority:** High  
**Description:** Review scheduling calculations must be deterministic and reproducible.  
**Target:** Same inputs always produce same schedule output; no floating-point drift  
**Measurement:** Schedule computation comparison tests  
**Source:** SRS reliability requirement
