# Risk Register

**Status:** Draft  
**Version:** 1.0.0  
**Last updated:** 2026-06-10

---

| ID | Category | Description | Likelihood (1-5) | Impact (1-5) | Score | Mitigation | Contingency | Owner | Status |
|----|----------|-------------|-------------------|---------------|-------|------------|-------------|-------|--------|
| R-01 | Technical | AI provider outage or degraded performance affecting all LLM-dependent features | 3 | 5 | 15 | Provider fallback strategy; degrade gracefully with cached responses | Switch to fallback provider; non-AI features remain functional | ai_gateway | Mitigated |
| R-02 | Technical | LLM latency exceeding p95 target of 12s, degrading user experience | 3 | 4 | 12 | Optimize prompt length; use faster model class where possible; streaming responses | Increase timeout target; inform users of longer processing | ai_gateway | Mitigated |
| R-03 | Technical | Mobile compatibility issues across Android versions and device types | 3 | 3 | 9 | Extensive device testing; Expo handles most compatibility | Issue-specific workarounds; target latest 2 Android versions | mobile | Mitigated |
| R-04 | Product | Low lesson completion rate indicating poor engagement or difficulty mismatch | 4 | 4 | 16 | Adaptive difficulty; persona-based content; feedback loops | A/B test lesson formats; adjust difficulty calibration | curriculum | Open |
| R-05 | Product | Diagnostic accuracy insufficient for meaningful skill assessment | 2 | 4 | 8 | Evidence-based assessment design; confidence scoring | Adaptive follow-up questions; manual override for edge cases | diagnostics | Mitigated |
| R-06 | Security | Prompt injection attack bypasses input sanitization | 3 | 5 | 15 | Defense in depth (input scan + output validation + content wrapping) | Emergency prompt update; affected data review | integrity | Mitigated |
| R-07 | Security | Data leakage via AI provider processing of learner submissions | 2 | 5 | 10 | Data minimization; no PII sent to provider; DPA with provider | Rotate provider; notify affected users | ai_gateway | Mitigated |
| R-08 | Security | Account takeover via credential stuffing or weak passwords | 3 | 4 | 12 | Rate limiting on auth; strong password policy; Supabase Auth security | Force password reset; monitor for unusual activity | identity | Mitigated |
| R-09 | Security | Reward economy exploited via duplicate submissions or race conditions | 3 | 5 | 15 | Idempotency keys + unique constraints + transactional writes | Reverse duplicate rewards; alert operator | reward_engine | Mitigated |
| R-10 | Operational | AI cost overruns due to unexpected usage spikes or inefficient prompts | 3 | 4 | 12 | Cost tracking per lesson; budget alerts; prompt optimization | Reduce model tier; increase caching; rate limit AI calls | ai_gateway | Mitigated |
| R-11 | Operational | Database performance degradation under load | 2 | 4 | 8 | Connection pooling; query optimization; indexing strategy | Read replicas; query tuning; vertical scaling | backend | Mitigated |
| R-12 | AI | LLM produces linguistically inaccurate feedback that misleads learners | 3 | 4 | 12 | Linguistic validation gate; schema constraints; limited analysis scope | Human review (post-MVP); flag for correction | linguistic_validation | Mitigated |
| R-13 | AI | LLM output bias (gender, cultural, regional) in examples and feedback | 2 | 3 | 6 | Prompt design with bias mitigation; diverse content | Content review; feedback reporting mechanism | ai_gateway | Open |
| R-14 | Regulatory | GDPR/CCPA compliance gaps in data processing or retention | 2 | 5 | 10 | Privacy by design; data minimization; retention policies | Legal review before production launch | operator | Open |
| R-15 | Technical | Redis outage stops background job processing and caching | 2 | 4 | 8 | Redis replication; graceful degradation without cache | Restart Redis; reprocess queued jobs | backend | Mitigated |
| R-16 | Product | Low retention after first session (users don't return after onboarding) | 4 | 5 | 20 | Strong onboarding experience; immediate value in first lesson; notification strategy | Analyze drop-off; improve first session experience | product | Open |
| R-17 | Technical | Schema migration conflict during concurrent development | 3 | 3 | 9 | Alembic migration review in PR; sequential migration application | Roll back and recreate migration | backend | Mitigated |
| R-18 | Security | Audit log tampering (modification or deletion of audit events) | 1 | 5 | 5 | Append-only table; separate DB user; integrity checking | Restore from backup; investigate breach | audit | Mitigated |
