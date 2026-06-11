# Stage Gates and Acceptance System

**Status:** CANONICAL  
**Version:** 1.0.0  
**Effective date:** 2026-06-10  
**Owner:** Product Owner  
**Change control:** Changes require a documented change request or ADR where specified.

## Decision vocabulary

- **GO:** all blocking criteria passed; next stage allowed.
- **HOLD:** stage remains open; bounded corrective work only.
- **PIVOT:** hypothesis, segment, offer, or implementation approach changes through approved change control.
- **STOP:** work on the current direction ends.

## Universal blocking criteria

Every stage requires:

- defined goal;
- scope and forbidden scope;
- owner;
- deadline and maximum timebox;
- budget limit;
- deliverables;
- tests;
- evidence;
- zero unresolved critical contradiction;
- proof artifact;
- commit/push/clean Git for repository stages.

## Zero-tolerance criteria

- cross-user data leak: 0;
- unauthorized mastery transition: 0;
- duplicate reward credit: 0;
- audit loss for authoritative events: 0;
- critical security vulnerability open at release: 0;
- fake learner completion: 0;
- production gate bypass: 0.

## Stage-specific summaries

### S0 Master canon closure

PASS when this package is complete, traceable, internally consistent, and accepted.

### S1 Vertical slice

PASS when mobile, backend, PostgreSQL, mock AI, validation, deterministic transitions, audit, tests, visual evidence, and Git proof are complete.

### S2 Evidence/usability acceptance

PASS when critical paths work on the device matrix, accessibility baseline passes, recovery works, and operator visual review is PASS.

### S3 Real-AI integration

PASS when one provider is isolated behind the gateway, output quality is validated, cost is bounded, no blind retry exists, and human review passes.

### S4 Internal alpha

PASS when critical runtime defects are zero, instrumentation is complete, and at least 80% of invited testers complete first value.

### S5 Learner alpha

PASS when at least 10 real learners participate, ≥70% complete first value, and Day-7 return is ≥40%.

### S6 Closed beta

PASS when product reliability and learning evidence are stable across at least 30 qualified learners and no safety gate fails.

### S7 Paid pilot

PASS when at least 10 learners pay, ≥80% activate, week-one return is ≥50%, and support/AI costs remain within limits.

### S8 Public MVP decision

GO only when learning, retention, commercial, safety, operational, and financial evidence jointly pass.

## Stop triggers

Stop or fundamentally pivot when two consecutive bounded experiments fail the same core hypothesis and no materially different test remains justified.
