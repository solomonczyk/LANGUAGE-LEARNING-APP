# Dangerous Action Gates

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  

---

## 1. Gate System Rules

| # | Rule | Description |
|---|------|-------------|
| 1 | Generation ≠ Acceptance | LLM may propose; only deterministic validation may accept |
| 2 | Parse success ≠ Linguistic acceptance | Schema-valid output may still fail linguistic checks |
| 3 | Linguistic pass ≠ Pedagogical pass | Linguistically correct output may be inappropriate for learner level |
| 4 | Retry only by classified cause | Every retry must have a documented reason category |
| 5 | Mastery changes via deterministic engine only | LLM may not influence mastery transitions |
| 6 | Rewards only from Reward Engine | LLM may not award or suggest rewards |
| 7 | Validation failure blocks downstream | No state change until all prerequisite gates pass |
| 8 | Production gate FORBIDDEN | `production_accepted=true` is not permitted |

---

## 2. Gate: AI Generation Gate

| Aspect | Value |
|--------|-------|
| **Protects** | System from accepting unvalidated LLM output |
| **Trigger** | LLM response received |
| **Pass criteria** | Schema valid AND content policy compliant |
| **On pass** | Analysis proceeds to linguistic validation |
| **On fail** | Output rejected; retry gate evaluated (if retryable) |
| **Audit** | `gate.ai_generation.{passed,failed}` |
| **Bypass** | No bypass permitted |

---

## 3. Gate: Retry Gate

| Aspect | Value |
|--------|-------|
| **Protects** | System from infinite or unnecessary retries |
| **Trigger** | Step failure (validation error, timeout, provider error) |
| **Pass criteria** | Retry count < max_retries AND cause is classified retryable |
| **On pass** | Pipeline resumes from failed step |
| **On fail** | Pipeline terminates with final failure |
| **Audit** | `gate.retry.{granted,denied}` |
| **Blind retry** | FORBIDDEN — every retry must have classified cause |

| Cause | Max Retries | Fallback Behaviour |
|-------|-------------|-------------------|
| Timeout | 2 | Fallback provider on 2nd failure |
| Provider 5xx | 2 | Fallback provider immediately |
| Network error | 2 | Retry same provider |
| Schema validation failure | 2 | Regenerate with same provider (no schema change) |
| Linguistic rejection | 0 | Must provide feedback to user |
| Pedagogical rejection | 0 | Must provide feedback to user |

---

## 4. Gate: Schema Acceptance Gate

| Aspect | Value |
|--------|-------|
| **Protects** | System from malformed or schema-invalid data |
| **Trigger** | Data received (AI output or submission) |
| **Pass criteria** | JSON Schema / Pydantic validation passes |
| **On pass** | Data proceeds to next validation stage |
| **On fail** | Data rejected with validation errors |
| **Audit** | `gate.schema.{passed,failed}` |

---

## 5. Gate: Linguistic Acceptance Gate

| Aspect | Value |
|--------|-------|
| **Protects** | System from linguistically incorrect analysis/feedback |
| **Trigger** | AI analysis output after schema validation |
| **Pass criteria** | Linguistic validation passes |
| **On pass** | Proceeds to pedagogical validation |
| **On fail** | Rejected; retry gate evaluated (0 retries for linguistic) |
| **Audit** | `gate.linguistic.{passed,failed}` |

---

## 6. Gate: Pedagogical Acceptance Gate

| Aspect | Value |
|--------|-------|
| **Protects** | System from pedagogically inappropriate content |
| **Trigger** | After linguistic validation passes |
| **Pass criteria** | Content appropriate for learner level, learning objectives met |
| **On pass** | Proceeds to policy engine for state transition decision |
| **On fail** | Rejected; 0 retries; learner receives improvement guidance |
| **Audit** | `gate.pedagogical.{passed,failed}` |

---

## 7. Gate: Lesson Completion Gate

| Aspect | Value |
|--------|-------|
| **Protects** | Lesson state from unauthorized completion |
| **Trigger** | All validations pass, policy engine evaluates |
| **Pass criteria** | Policy engine approves completion (submission + validation + gates all pass) |
| **On pass** | `lesson_engine.complete_session()` — deterministic state transition |
| **On fail** | Session remains active; learner receives guidance |
| **Audit** | `gate.lesson_completion.{passed,failed}` |
| **Authority** | **Only deterministic engine can complete a lesson** |

---

## 8. Gate: Mastery Transition Gate

| Aspect | Value |
|--------|-------|
| **Protects** | Mastery state from unauthorized changes |
| **Trigger** | Lesson completion with passing assessment |
| **Pass criteria** | Mastery evidence threshold met (deterministic) |
| **On pass** | `mastery` module updates level (deterministic algorithm) |
| **On fail** | Evidence accumulated but no level change |
| **Audit** | `gate.mastery.{level_up,evidence_accumulated}` |
| **Authority** | **LLM MUST NOT influence mastery** |

---

## 9. Gate: Reward Transaction Gate

| Aspect | Value |
|--------|-------|
| **Protects** | Reward economy from fraud, duplicates, unauthorized credit |
| **Trigger** | Lesson or review completion |
| **Pass criteria** | Idempotency check + duplicate detection + legitimate completion verified |
| **On pass** | XP awarded, ledger updated |
| **On fail** | Transaction rejected; IntegrityRiskSignal logged |
| **Audit** | `gate.reward.{committed,rejected,duplicate_attempt}` |
| **Authority** | **Only Reward Engine can award rewards. LLM NEVER.** |

---

## 10. Gate: Review Scheduling Gate

| Aspect | Value |
|--------|-------|
| **Protects** | Review schedule from incorrect item creation |
| **Trigger** | Lesson completion with error items identified |
| **Pass criteria** | Items identified, priority calculated, schedule computed |
| **On pass** | Review items created with SRS schedule |
| **On fail** | Items deferred to next pipeline run |
| **Audit** | `gate.review_schedule.{scheduled,deferred}` |

---

## 11. Gate: Notification Dispatch Gate

| Aspect | Value |
|--------|-------|
| **Protects** | Users from excessive or mistimed notifications |
| **Trigger** | Scheduled notification time reached |
| **Pass criteria** | Learner opted in, within quiet hours, notification type enabled |
| **On pass** | Notification dispatched |
| **On fail** | Notification suppressed; logged |
| **Audit** | `gate.notification.{dispatched,suppressed}` |
| **LLM direct dispatch** | **FORBIDDEN** — only notification module can dispatch |

---

## 12. Gate: Downstream Action Gate

| Aspect | Value |
|--------|-------|
| **Protects** | System from cascading actions without validation |
| **Trigger** | Any state change that triggers secondary effects |
| **Pass criteria** | All upstream gates passed + policy engine approves downstream |
| **On pass** | Downstream actions queued (notifications, scheduling) |
| **On fail** | All downstream blocked; only primary state change committed |
| **Audit** | `gate.downstream.{approved,blocked}` |

---

## 13. Gate: Production Gate

| Aspect | Value |
|--------|-------|
| **Protects** | Production environment from premature release |
| **Status** | **FOREVER BLOCKED in MVP** |
| **Pass criteria** | `production_accepted=true` — which is FORBIDDEN |
| **Audit** | Any attempt to open logs as `security.violation.production_gate_violation` |

This gate exists as a marker. In the current phase, the production gate is permanently locked. It may only be opened by a separate future task with appropriate authority.
