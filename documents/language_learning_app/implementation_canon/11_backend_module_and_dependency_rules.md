# Backend Module and Dependency Rules

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  
**Schema:** `schemas/backend_module.schema.json`  
**Example:** `examples/backend_module.example.json`

---

## 1. Module Definitions

### 1.1 identity
| Field | Value |
|-------|-------|
| Responsibility | User registration, auth, identity management |
| Owned entities | User, AuthIdentity |
| Public interfaces | `register_user()`, `authenticate()`, `verify_token()`, `refresh_token()` |
| Consumed interfaces | None (external: Supabase Auth SDK) |
| Forbidden | Access learner profile data, manage rewards |
| Events emitted | `user.registered`, `user.deleted`, `user.suspended` |

### 1.2 learner_profile
| Field | Value |
|-------|-------|
| Responsibility | Multidimensional learner profile, skill dimensions, goals, progression |
| Owned entities | LearnerProfile, SkillDimension, XPBalance |
| Public interfaces | `get_profile()`, `update_profile()`, `get_skill_dimensions()` |
| Consumed interfaces | `identity.verify_token()`, `diagnostics.get_assessment()`, `mastery.get_mastery_records()` |
| Forbidden | Award rewards or XP, modify lesson content |

### 1.3 diagnostics
| Field | Value |
|-------|-------|
| Responsibility | Diagnostic sessions, question delivery, response collection, assessment |
| Owned entities | DiagnosticSession, DiagnosticResponse, SkillAssessment |
| Public interfaces | `create_session()`, `submit_response()`, `complete_session()`, `get_assessment()` |
| Forbidden | Modify mastery directly, award rewards |

### 1.4 learning_contract
| Field | Value |
|-------|-------|
| Responsibility | Learning Entry Contract lifecycle |
| Owned entities | LearningEntryContract |
| Public interfaces | `create_contract()`, `get_current_contract()`, `update_contract()` |
| Forbidden | Modify lesson content or progress |

### 1.5 curriculum
| Field | Value |
|-------|-------|
| Responsibility | Lesson selection, recommendation, curriculum progression |
| Owned entities | LessonDefinition |
| Forbidden | Generate lesson content (delegates to content module), modify learner profile |

### 1.6 lesson_engine
| Field | Value |
|-------|-------|
| Responsibility | Lesson session lifecycle (create → submit → complete) |
| Owned entities | LessonSession, LessonAttempt |
| Forbidden | Direct AI Gateway calls, award rewards |

### 1.7 content
| Field | Value |
|-------|-------|
| Responsibility | Lesson content, prompts, media assets |
| Owned entities | ContentVersion |
| Forbidden | Modify lesson sessions or learner data |

### 1.8 submission
| Field | Value |
|-------|-------|
| Responsibility | Accept, validate, process learner submissions |
| Owned entities | Submission |
| Consumed interfaces | `integrity.scan_input()`, `ai_gateway.analyze_text()` |
| Forbidden | Modify mastery, rewards, or review schedule |

### 1.9 ai_gateway
| Field | Value |
|-------|-------|
| Responsibility | Provider-independent LLM interface, structured output, validation, audit |
| Owned entities | AIAnalysisRequest, AIAnalysisResult, PromptTemplateVersion |
| Forbidden | LLM output must not directly modify any system state |

### 1.10 linguistic_validation
| Field | Value |
|-------|-------|
| Responsibility | Validate AI analysis for linguistic accuracy |
| Owned entities | ValidationResult |
| Forbidden | Modify AI output (pass/fail only) |

### 1.11 pedagogical_validation
| Field | Value |
|-------|-------|
| Responsibility | Validate AI feedback for level-appropriateness and learning value |
| Owned entities | ValidationResult |
| Forbidden | Modify AI output (pass/fail only) |

### 1.12 policy_engine
| Field | Value |
|-------|-------|
| Responsibility | Central policy decisions — lesson completion, retry eligibility, reward eligibility |
| Owned entities | None (stateless) |
| Forbidden | Modify any state directly (decisions only) |

### 1.13 mastery
| Field | Value |
|-------|-------|
| Responsibility | Mastery records, evidence, deterministic state transitions |
| Owned entities | MasteryRecord, MasteryEvidence |
| Forbidden | LLM influence on mastery transitions; rewards modifying mastery |

### 1.14 review_scheduler
| Field | Value |
|-------|-------|
| Responsibility | Spaced repetition scheduling, review items |
| Owned entities | ReviewItem, ReviewSchedule |
| Forbidden | Award rewards, modify mastery |

### 1.15 reward_engine
| Field | Value |
|-------|-------|
| Responsibility | Deterministic reward calculation, XP ledger, achievements |
| Owned entities | RewardTransaction, XPBalance |
| Forbidden | **LLM MUST NEVER INFLUENCE REWARDS** — all reward logic is deterministic |

### 1.16 notifications
| Field | Value |
|-------|-------|
| Responsibility | Push notification scheduling, delivery, preferences |
| Owned entities | Notification |
| Forbidden | Send without user consent; exceed rate limits |

### 1.17 analytics
| Field | Value |
|-------|-------|
| Responsibility | Learning analytics, aggregation, reporting |
| Owned entities | None (reads from audit and other entities) |
| Forbidden | Modify any data (read-only module) |

### 1.18 audit
| Field | Value |
|-------|-------|
| Responsibility | Immutable audit event logging, query, retention |
| Owned entities | AuditEvent |
| Forbidden | Audit events must never be modified or deleted (append-only) |

### 1.19 integrity
| Field | Value |
|-------|-------|
| Responsibility | Security scanning, anti-cheat, duplicate detection, rate limiting |
| Owned entities | SecurityEvent, IntegrityRiskSignal |
| Forbidden | Modify learner state (read-only checks) |

### 1.20 operator
| Field | Value |
|-------|-------|
| Responsibility | Operator/admin read-only tools |
| Owned entities | None |
| Forbidden | Modify any data (read-only access) |

---

## 2. Dependency Matrix

Format: Row module → may import interfaces from column module

| Module | identity | learner_profile | diagnostics | learning_contract | curriculum | lesson_engine | content | submission | ai_gateway | linguistic_val | pedagogical_val | policy_engine | mastery | review_scheduler | reward_engine | notifications | analytics | audit | integrity | operator |
|--------|----------|----------------|-------------|-------------------|------------|---------------|---------|------------|------------|---------------|----------------|--------------|---------|-----------------|--------------|-------------|-----------|-------|-----------|----------|
| identity | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| learner_profile | ✓ | — | ✓ | — | — | — | — | — | — | — | — | — | ✓ | — | — | — | — | — | — | — |
| diagnostics | — | ✓ | — | — | — | — | — | — | — | — | — | — | ✓ | — | — | — | — | — | — | — |
| learning_contract | — | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| curriculum | — | ✓ | — | ✓ | — | — | — | — | — | — | — | — | ✓ | — | — | — | — | — | — | — |
| lesson_engine | — | ✓ | — | — | ✓ | — | ✓ | ✓ | — | — | — | ✓ | ✓ | — | — | — | — | ✓ | — | — |
| content | — | ✓ | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| submission | — | — | — | — | — | — | — | — | ✓ | — | — | — | — | — | — | — | — | ✓ | ✓ | — |
| ai_gateway | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | ✓ | — | — |
| linguistic_val | — | — | — | — | — | — | — | — | — | — | — | ✓ | — | — | — | — | — | ✓ | — | — |
| pedagogical_val | — | ✓ | — | — | — | — | — | — | — | — | — | ✓ | ✓ | — | — | — | — | ✓ | — | — |
| policy_engine | — | — | — | — | — | — | — | — | — | ✓ | ✓ | — | — | — | — | — | — | ✓ | ✓ | — |
| mastery | — | ✓ | — | — | — | — | — | — | — | — | — | ✓ | — | — | — | — | — | ✓ | — | — |
| review_scheduler | — | — | — | — | — | — | — | — | — | — | — | — | ✓ | — | — | — | — | ✓ | — | — |
| reward_engine | — | ✓ | — | — | — | — | — | — | — | — | — | ✓ | ✓ | — | — | — | — | ✓ | — | — |
| notifications | — | ✓ | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | ✓ | — | — |
| analytics | — | ✓ | — | — | — | — | — | — | — | — | — | — | ✓ | — | — | — | — | ✓ | — | — |
| audit | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| integrity | — | — | — | — | — | — | — | ✓ | ✓ | — | — | — | — | — | — | — | — | ✓ | — | — |
| operator | — | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | — | — | — | ✓ | — | — |

---

## 3. Forbidden Cross-Module Operations

| Violation | Example | Enforcement |
|-----------|---------|-------------|
| Direct table access across modules | `lesson_engine` reads `User` table directly | CI check: module only queries its own entities |
| Mastery updates outside Mastery | `reward_engine` calls `db.execute("UPDATE mastery...")` | Code review + module authority check |
| Reward writes outside Reward Engine | `lesson_engine` inserts into `reward_transactions` | Code review + module authority check |
| Audit bypass | Module writes state without calling `audit.record_event()` | Code review + test requirement |
| Circular import | `identity → learner_profile → identity` | CI circular import detection |
