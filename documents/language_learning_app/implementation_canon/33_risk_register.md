# Risk Register

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  

---

## 1. Risks

| # | Risk | Likelihood | Impact | Mitigation | Contingency | Owner |
|---|------|-----------|--------|------------|-------------|-------|
| 1 | Expo SDK limitation prevents native feature (audio) | Medium | High | Use expo-av; eject to bare workflow if needed | Eject to bare React Native | Mobile |
| 2 | Supabase Auth outage blocks login | Low | High | Cache session; implement stale token grace period | Fallback to local auth session for 5 min | Backend |
| 3 | AI provider outage blocks submission analysis | Medium | High | AI Gateway with fallback provider; mock mode as safety net | Queue submissions; process when provider available | AI Gateway |
| 4 | Python GIL limits AI Gateway throughput | Low | Medium | Async I/O avoids GIL for network-bound operations | Extract AI Gateway to separate service | Backend |
| 5 | Module boundary erosion over time | Medium | Medium | Interface contracts; CI module dependency check | Extract into service if boundary violated | Architecture |
| 6 | Offline submission queue conflicts | Medium | Low | Idempotency keys prevent duplicates | Manual reconciliation by operator | Backend |
| 7 | Mobile state persistence corruption | Low | Medium | State versioning; migration on read | Clear and re-initialize; user re-auth | Mobile |
| 8 | Prompt injection via learner submission | Medium | High | Input sanitization; content wrapping; output scanning | Reject submission; flag user for review | Security |
| 9 | Reward duplicate/fraud attempt | Medium | High | Idempotency keys; UNIQUE constraints; server-side validation | IntegrityRiskSignal; operator review | Backend |
| 10 | Migration error in staging | Medium | Medium | Test migration in CI; automatic downgrade on failure | Manual DB restore from backup | Backend |
| 11 | Flaky tests degrade CI reliability | Medium | Medium | Flaky test quarantine; 48h root cause deadline | Revert change if cause not found | QA |
| 12 | Small team knowledge silos | Medium | High | Code review; documentation; pair programming | Cross-training sessions | Team |
| 13 | Real device testing gaps | Medium | Medium | Minimum device matrix (1 Android + 1 iOS + 1 tablet) | Cloud device farm for additional coverage | Mobile |
| 14 | Large text/a11y breaks layout | Low | Medium | Responsive design; test at 200% font scale in CI | Manual layout adjustment per device | Mobile |
| 15 | Scope creep beyond vertical slice | Medium | Medium | Fixed sprint scope; change control via ADR | Reject non-critical additions | PM |
| 16 | Third-party dependency vulnerability | Medium | High | Dependency scanning in CI; pinned versions | Urgent update; security release | Security |
| 17 | Learner data privacy compliance gap | Medium | High | Privacy controls defined; pseudonymization; data minimization | Legal review before production | Legal |
| 18 | Audit event loss | Low | Critical | Append-only table; queued async write; periodic reconciliation | Alert on loss; full audit replay | Backend |

---

## 2. Risk Acceptance

| Risk | Accepted? | Rationale |
|------|-----------|-----------|
| R1 (Expo limitation) | Yes | expo-av covers MVP; ejection possible but costly |
| R8 (Prompt injection) | Yes | Defense in depth: input sanitization + output scanning + rejection |
| R11 (Flaky tests) | Yes | Quarantine mechanism limits impact |
| R12 (Knowledge silos) | Yes | Mitigations in place (code review, documentation) |
| R13 (Device gaps) | Yes | Minimum device coverage accepted for MVP |

Risks not accepted (must be actively mitigated): R2, R3, R5, R9, R10, R14, R15, R16, R17, R18.

---

## 3. Risk Review Cadence

| Frequency | Activity |
|-----------|----------|
| Weekly (during active development) | Review open risks; update likelihood/impact |
| Sprint review | Review resolved risks; identify new risks |
| Milestone | Full risk register review and update |
