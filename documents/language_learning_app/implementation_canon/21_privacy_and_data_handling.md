# Privacy and Data Handling

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  

---

## 1. Data Classification

| Classification | Examples | Storage | Handling |
|---------------|----------|---------|----------|
| Personal data | Email, name, Supabase Auth identity | Supabase Auth + `users` table (minimal) | Pseudonymized in logs, encrypted at rest |
| Learner data | Skill dimensions, learner profile, diagnostic results | PostgreSQL (`learner_profiles`, `skill_dimensions`) | Associated with pseudonymized ID |
| Lesson submissions | Text responses, audio recordings | PostgreSQL (text) + Object storage (audio) | Transcript stored with submission |
| AI payloads | Prompt templates, AI analysis results | PostgreSQL | Prompts versioned in git, analysis stored with submission |
| Analytics | Aggregated usage metrics | PostgreSQL (analytics module) | Aggregated, not individually identifiable |
| Audit | Immutable event log | PostgreSQL (audit events) | Pseudonymized user ID, no PII |
| Security events | Threat detection, rate limit hits | PostgreSQL (security events) | User ID + IP logged |

---

## 2. Data Retention

| Data Type | Retention | Deletion Method |
|-----------|-----------|-----------------|
| User account (active) | Until deletion request | Soft delete + anonymize |
| User account (deleted) | 90 days after deletion request | Hard delete after 90 days |
| Lesson submissions | Duration of account + 90 days | Deleted with account |
| Audio recordings | Duration of account + 90 days | Delete from object storage |
| AI analysis results | Duration of account + 90 days | Deleted with account |
| Audit events | 2 years | Partitioned, old partitions dropped |
| Security events | 1 year | Partitioned, old partitions dropped |
| Analytics aggregates | Indefinite (no PII) | Retained |
| Session data | 30 days after session expiry | Deleted |
| Drafts (local device) | Until submission or 7 days | Cleared on submission or expiry |

---

## 3. Data Deletion

| Request | Process | Max Timeframe |
|---------|---------|---------------|
| Account deletion (self-service) | User triggers in settings → confirmation → soft delete → 90d purge | Immediate (soft), 90 days (hard) |
| Account deletion (operator) | Operator initiates → same process | Immediate |
| Data export | User requests → backend compiles JSON → downloadable link | 48 hours |

---

## 4. Data Export

Export format: JSON file containing:
- Learner profile (skill dimensions, goals)
- Lesson history (lesson types, completion status, dates)
- Submission history (text only, not audio)
- Reward ledger (transactions, XP)

NOT included in export:
- Other users' data
- Audit events
- Security events
- Raw AI prompts

---

## 5. Data Minimization

| Principle | Implementation |
|-----------|---------------|
| Collect only what's needed | No unnecessary fields in signup form (email + password only) |
| Store only what's needed | No PII beyond email and name |
| Use pseudonyms | Logs use `user_id` (UUID), not email or name |
| Don't log PII | All logs are structured JSON with PII fields excluded |
| No tracking cookies | No analytics cookies on mobile; telemetry is code-level |

---

## 6. Pseudonymization

| Context | Identifier Used | Original |
|---------|----------------|----------|
| Logs | `user_id` (UUID) | Email, name |
| Audit | `user_id` (UUID) | Personal data |
| Telemetry | `user_id` (UUID) | Personal data |
| Analytics | `user_id` (UUID) or anonymous | Personal data |
| Third-party (AI provider) | Random request ID (not user UUID) | User UUID stored in audit linkage |

---

## 7. Provider Data Boundaries

| Data | Sent to AI Provider? | Rationale |
|------|---------------------|-----------|
| Learner submission text | Yes (required for analysis) | Core feature |
| Learner profile (level, goals) | Yes (in prompt context) | Required for level-appropriate feedback |
| Learner name | No | Not needed |
| User email | No | Not needed |
| Other users' data | No | Privacy |
| API keys | No | Security |

---

## 8. Child User Assumption

- Age verification is out of MVP scope
- App is designed for general audiences
- No data collection from known children under 13 without parental consent (if US-based)
- **Legal review needed** for GDPR (16), COPPA (13), or equivalent compliance
- This canon does NOT assert GDPR or COPPA compliance without legal review

---

## 9. Consent

| Consent Type | Obtained When | Withdrawal |
|-------------|---------------|------------|
| Terms of service acceptance | On signup | Account deletion |
| Privacy policy acceptance | On signup | Account deletion |
| Notification permission | After first lesson | Settings → Notifications |
| Data processing (AI analysis) | On signup (ToS) | Account deletion |

---

## 10. Legal-Review Boundary

This canon defines privacy controls that lay the foundation for compliance, but does NOT assert:
- GDPR compliance
- COPPA compliance
- CCPA compliance
- Any other regulatory compliance

Legal review is required before any such assertion. The controls defined here are designed to be compatible with these frameworks but require legal verification.

---

## 11. Privacy Requirements Traceability

| Requirement | Canon Document | Verification |
|-------------|----------------|--------------|
| Data classification defined | §1 above | Document review |
| Retention periods defined | §2 above | Document review |
| Deletion process defined | §3 above | Integration test |
| Export process defined | §4 above | Integration test |
| Minimization enforced | §5 above | Code review |
| Pseudonymized logs | §6 above | Log inspection |
| Provider boundaries | §7 above | Code review |
