# Security Implementation Canon

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  

---

## 1. Threat Coverage

| Threat | Preventive Control | Detective Control | Recovery |
|--------|-------------------|-------------------|----------|
| Prompt injection | Input sanitization, content wrapping, role isolation | Detection on output | Reject, log SecurityEvent |
| Indirect prompt injection | Input validation before prompt construction | AI output scanning | Reject, log |
| Malicious transcript | Input sanitization, length limits, content checks | Checksum verification | Reject, flag user |
| Malicious image metadata (post-MVP) | MIME validation, strip metadata | — | Reject |
| Replay attack | Idempotency keys, JWT short expiry | Duplicate detection | 409 response |
| Forged completion | Server-side session state machine | State validation | Reject, log IntegrityRiskSignal |
| Duplicate reward | UNIQUE constraint on (user, activity_type, id) | Reward transaction gate | 409 + IntegrityRiskSignal |
| IDOR | User ID check on every resource query | Audit log cross-check | 404 (hide existence) |
| Account takeover | Strong auth (Supabase), rate limiting | Suspicious login detection | Password reset |
| Token leakage | Secure storage, no logging of tokens | — | Revoke all sessions |
| Provider leakage | No provider API keys in client | — | Rotate keys |
| Upload abuse | MIME validation, size limits, checksums | Rate limiting | Reject, rate limit |
| Rate abuse | Per-user + per-IP rate limiting | Rate limit monitoring | 429 response |
| Audit tampering | Append-only audit tables, no DELETE/UPDATE | Periodic hash checks | Alert |
| Dependency vulns | Regular `pip audit` + `npm audit` | CI dependency scan | Update dependency |
| Log leakage | No secrets/PII in logs, structured logging | Periodic log review | Redact, rotate |
| Secrets leakage | .env not in repo, secrets manager | CI secret scan | Rotate secrets |
| Client tampering | No business rules on client | Server-side validation | Reject, log |

---

## 2. Preventive Controls

| Control | Implementation | Owner |
|---------|---------------|-------|
| Input sanitization | Strip control characters, limit length, escape HTML | integrity module |
| Auth verification | JWT verification on every request | identity module |
| Rate limiting | Redis-based per-user and per-IP counters | integrity module |
| Idempotency | Idempotency-Key with 24h storage | API middleware |
| MIME validation | Check Content-Type and magic bytes on upload | integrity module |
| CORS | Staging/Production: restrict to known origins | API middleware |
| Content security | Prompt wrapping isolation for AI Gateway | ai_gateway module |

---

## 3. Detective Controls

| Control | Implementation | Owner |
|---------|---------------|-------|
| Duplicate attempt detection | Database UNIQUE constraints + idempotency | integrity module |
| Anomaly detection | Rate limit threshold alerts | integrity module |
| Prompt injection detection | Output scanning for prompt leakage patterns | ai_gateway module |
| Audit completeness | Periodic cron: audit event count vs expected | integrity module |
| Dependency scanning | CI: `pip audit` and `npm audit` weekly | CI/CD |

---

## 4. Security Incident Recovery

| Incident | Response |
|----------|---------|
| Confirmed attack | Revoke affected tokens, suspend user, log SecurityEvent |
| Rate limit breach | Block IP/user, alert operator, review patterns |
| Audit discrepancy | Full audit replay, identify gap, fix root cause |
| Secrets exposed | Rotate immediately, revoke all tokens, audit access logs |
| Provider breach | Rotate provider keys, fail-over to fallback provider |

---

## 5. Security Test Requirements

| Test | Tool | When | Blocking |
|------|------|------|----------|
| Prompt injection suite | Custom test prompts | CI (prompt evaluation) | Yes |
| IDOR check | Automated: attempt cross-user access | CI (security tests) | Yes |
| Rate limit check | Load test: exceed limits | CI | Yes |
| Duplicate reward | State-machine: same reward twice | CI | Yes |
| Dependency scan | `pip audit` / `npm audit` | CI | Yes |
| Secret scan | `trufflehog` or `git leaks` | CI (pre-commit + CI) | Yes |
| Token leakage | Lint: no token vars in log calls | CI | Yes |

---

## 6. Security Audit Events

Every security-relevant operation emits an audit event:

| Event | Fields |
|-------|--------|
| `security.threat_detected` | `type`, `severity`, `details`, `user_id`, `ip`, `trace_id` |
| `security.rate_limit_hit` | `user_id`, `ip`, `endpoint`, `count` |
| `security.duplicate_attempt` | `user_id`, `activity_type`, `activity_id` |
| `security.forged_completion` | `user_id`, `lesson_session_id`, `method` |
| `security.auth_anomaly` | `user_id`, `ip`, `action`, `reason` |
| `integrity.signal` | `user_id`, `signal_type`, `details` |

---

## 7. Forbidden Security Patterns

| Pattern | Reason |
|---------|--------|
| Client-side security decisions | Defeated by client tampering |
| Trusting user-provided user_id | IDOR vulnerability |
| Secrets in mobile bundle | Extracted via decompilation |
| SQL query string concatenation | SQL injection |
| Disabled security tests | Undocumented risk |
| Mutable audit logs | Undetectable tampering |
