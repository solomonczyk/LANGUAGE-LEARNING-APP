# Requirements Traceability Matrix

**Status:** Draft  
**Version:** 1.0.0  
**Last updated:** 2026-06-10

---

## Table 1: User Story to Requirement Traceability

| US ID | Title | FR IDs | Persona | API Endpoint | Data Entity |
|-------|-------|--------|---------|-------------|-------------|
| US-001 | User Registration with Language Selection | FR-001 | P-02 | POST /api/v1/auth/register | User, AuthIdentity, LearnerProfile |
| US-002 | Onboarding Questionnaire | FR-002 | P-03 | POST /api/v1/learner-profile | LearnerProfile |
| US-003 | First-Session Tutorial | FR-003 | P-02 | GET /api/v1/lessons | LessonDefinition |
| US-004 | Login with Email and Password | FR-004 | P-01 | POST /api/v1/auth/login | AuthIdentity |
| US-005 | Social Login | FR-005 | P-03 | POST /api/v1/auth/login/social | AuthIdentity |
| US-006 | Token Refresh | FR-006 | P-01 | POST /api/v1/auth/refresh | AuthIdentity |
| US-007 | Start Diagnostic Session | FR-007 | P-02 | POST /api/v1/diagnostics/sessions | DiagnosticSession |
| US-008 | Answer Diagnostic Question | FR-008 | P-01 | POST /api/v1/diagnostics/{id}/responses | DiagnosticResponse |
| US-009 | Complete Diagnostic | FR-009 | P-04 | POST /api/v1/diagnostics/{id}/complete | SkillAssessment |
| US-010 | Return User Reassessment | FR-010 | P-01 | POST /api/v1/diagnostics/sessions | DiagnosticSession |
| US-011 | View Learner Profile | FR-011 | P-01 | GET /api/v1/learner-profile | LearnerProfile |
| US-012 | Update Profile Settings | FR-012 | P-03 | PUT /api/v1/learner-profile | LearnerProfile |
| US-013 | View Skill Dimension Breakdown | FR-013 | P-04 | GET /api/v1/mastery/profile | SkillDimension |
| US-014 | Create Learning Entry Contract | FR-014 | P-01 | POST /api/v1/learning-contract/current | LearningEntryContract |
| US-015 | Review Contract Terms | FR-015 | P-03 | GET /api/v1/learning-contract/current | LearningEntryContract |
| US-016 | Update Learning Contract | FR-016 | P-03 | PUT /api/v1/learning-contract/current | LearningEntryContract |
| US-017 | Browse Available Lesson Modes | FR-017 | P-01 | GET /api/v1/lessons | LessonDefinition |
| US-018 | Receive Recommended Lesson | FR-018 | P-04 | GET /api/v1/lessons/recommended | LessonDefinition |
| US-019 | Start a Lesson Session | FR-019 | P-02 | POST /api/v1/lesson-sessions | LessonSession |
| US-020 | Receive Personal Narrative Prompt | FR-020 | P-04 | POST /api/v1/lesson-sessions | LessonSession |
| US-021 | Submit Personal Narrative | FR-021 | P-01 | POST /api/v1/submissions/text | Submission |
| US-022 | Receive Narrative Analysis | FR-022 | P-04 | GET /api/v1/submissions/{id}/analysis | AIAnalysisResult |
| US-023 | View Image Scene for Description | FR-023 | P-02 | POST /api/v1/lesson-sessions | LessonDefinition |
| US-024 | Submit Description of Visual Scene | FR-024 | P-04 | POST /api/v1/submissions/text | Submission |
| US-025 | Receive Feedback on Visual Description | FR-025 | P-02 | GET /api/v1/submissions/{id}/analysis | AIAnalysisResult |
| US-026 | Listen to Target Language Audio | FR-026 | P-04 | POST /api/v1/lesson-sessions | LessonSession |
| US-027 | Retell the Audio Story | FR-027 | P-01 | POST /api/v1/submissions/audio | Submission |
| US-028 | Receive Audio Retelling Analysis | FR-028 | P-04 | GET /api/v1/submissions/{id}/analysis | AIAnalysisResult |
| US-029 | Start Functional Communication Scenario | FR-029 | P-03 | POST /api/v1/lesson-sessions | LessonSession |
| US-030 | Complete a Functional Communication Task | FR-030 | P-03 | POST /api/v1/lesson-sessions/{id}/attempts | LessonAttempt |
| US-031 | Receive Functional Communication Feedback | FR-031 | P-03 | GET /api/v1/submissions/{id}/analysis | AIAnalysisResult |
| US-032 | Start Guided Writing Task | FR-032 | P-04 | POST /api/v1/lesson-sessions | LessonSession |
| US-033 | Submit Writing for AI Correction | FR-033 | P-01 | POST /api/v1/submissions/text | Submission |
| US-034 | Receive Detailed Writing Analysis | FR-034 | P-04 | GET /api/v1/submissions/{id}/analysis | AIAnalysisResult |
| US-035 | Revise Writing Based on Feedback | FR-035 | P-01 | POST /api/v1/submissions/text | Submission |
| US-036 | Start AI Dialogue Simulation | FR-036 | P-04 | POST /api/v1/lesson-sessions | LessonSession |
| US-037 | Exchange Dialogue Turns | FR-037 | P-04 | POST /api/v1/lesson-sessions/{id}/attempts | LessonAttempt |
| US-038 | Complete Dialogue and Receive Assessment | FR-038 | P-03 | POST /api/v1/lesson-sessions/{id}/complete | PerformanceAssessment |
| US-039 | Take a Short Content Quiz | FR-039 | P-01 | POST /api/v1/assessments | PerformanceAssessment |
| US-040 | Complete Performance-Based Assessment | FR-040 | P-03 | POST /api/v1/assessments/performance | PerformanceAssessment |
| US-041 | View Assessment Results | FR-041 | P-04 | GET /api/v1/assessments/{id} | SkillAssessment |
| US-042 | Track Mastery Progress per Skill | FR-042 | P-01 | GET /api/v1/mastery/profile | MasteryRecord |
| US-043 | Receive Mastery Evidence After Lesson | FR-043 | P-04 | POST /api/v1/lesson-sessions/{id}/complete | MasteryEvidence |
| US-044 | Receive Mastery Level-Up Notification | FR-044 | P-01 | GET /api/v1/mastery/profile | MasteryRecord |
| US-045 | View Due Review Items | FR-045 | P-01 | GET /api/v1/reviews/due | ReviewItem |
| US-046 | Complete a Review Attempt | FR-046 | P-03 | POST /api/v1/reviews/{id}/attempt | ReviewSchedule |
| US-047 | View Upcoming Review Schedule | FR-047 | P-01 | GET /api/v1/reviews | ReviewSchedule |
| US-048 | Earn XP for Completing Lessons | FR-048 | P-01 | POST /api/v1/lesson-sessions/{id}/complete | RewardTransaction |
| US-049 | View XP Transaction History | FR-049 | P-03 | GET /api/v1/rewards/ledger | XPBalance |
| US-050 | Earn Achievement Badge | FR-050 | P-04 | POST /api/v1/lesson-sessions/{id}/complete | RewardTransaction |
| US-051 | Receive Review Reminder Notification | FR-051 | P-03 | POST /api/v1/notifications | Notification |
| US-052 | Streak Reminder | FR-052 | P-01 | POST /api/v1/notifications | Notification |
| US-053 | Malicious Input Detection | FR-053 | System | All | SecurityEvent |
| US-054 | Prevent Duplicate Submissions | FR-054 | System | POST /api/v1/submissions/text | IntegrityRiskSignal |
| US-055 | Rate Limit API Requests | FR-055 | System | All | IntegrityRiskSignal |
| US-056 | View Personal Learning Analytics | FR-056 | P-01 | GET /api/v1/analytics | AuditEvent |
| US-057 | Audit Event Logging | FR-057 | System | All | AuditEvent |
| US-058 | Track and Report Errors | FR-058 | Operator | Internal | AuditEvent |
| US-059 | View System Health Dashboard | FR-059 | Operator | GET /api/v1/health | None |
| US-060 | Access Read-Only User Diagnostics | FR-060 | Operator | GET /api/v1/operator/diagnostics | DiagnosticSession |
| US-061 | View System Audit Log | FR-061 | Operator | GET /api/v1/operator/audit | AuditEvent |

---

## Table 2: Functional Requirement to Module Traceability

| FR ID | Title | Module/Service | Priority |
|-------|-------|---------------|----------|
| FR-001 | User Registration | identity | Critical |
| FR-002 | Onboarding Questionnaire | identity | High |
| FR-003 | Tutorial Delivery | identity | Medium |
| FR-004 | Email Login | identity | Critical |
| FR-005 | Social Login | identity | High |
| FR-006 | Token Refresh | identity | High |
| FR-007 | Start Diagnostic Session | diagnostics | Critical |
| FR-008 | Record Diagnostic Response | diagnostics | Critical |
| FR-009 | Complete Diagnostic | diagnostics | Critical |
| FR-010 | Return User Reassessment | diagnostics | High |
| FR-011 | View Learner Profile | learner_profile | High |
| FR-012 | Update Learner Profile | learner_profile | Medium |
| FR-013 | Skill Dimension Display | learner_profile | High |
| FR-014 | Create Learning Entry Contract | learning_contract | Critical |
| FR-015 | Review Contract | learning_contract | High |
| FR-016 | Update Contract | learning_contract | Medium |
| FR-017 | Browse Lessons | curriculum | High |
| FR-018 | Recommend Lesson | curriculum | High |
| FR-019 | Start Lesson Session | lesson_engine | Critical |
| FR-020 | Generate Narrative Prompt | content | High |
| FR-021 | Accept Text Submission | submission | Critical |
| FR-022 | Generate Text Analysis | ai_gateway | High |
| FR-023 | Present Visual Scene | content | High |
| FR-024 | Accept Audio Recording | submission | High |
| FR-025 | Generate Visual Description Feedback | ai_gateway | High |
| FR-026 | Audio Playback | content | High |
| FR-027 | Audio Retelling Analysis | ai_gateway | High |
| FR-028 | Generate Audio Feedback | ai_gateway | High |
| FR-029 | Functional Scenario Delivery | content | High |
| FR-030 | Functional Task Acceptance | lesson_engine | High |
| FR-031 | Functional Feedback Generation | ai_gateway | Medium |
| FR-032 | Guided Writing Task | content | Medium |
| FR-033 | Writing Correction | ai_gateway | High |
| FR-034 | Detailed Writing Analysis | ai_gateway | High |
| FR-035 | Revision Cycle | lesson_engine | Medium |
| FR-036 | Dialogue Initiation | lesson_engine | High |
| FR-037 | Dialogue Turn Exchange | ai_gateway | High |
| FR-038 | Dialogue Completion Assessment | assessment | Medium |
| FR-039 | Quiz Delivery | assessment | Medium |
| FR-040 | Performance Task Assessment | assessment | Medium |
| FR-041 | Assessment Results Display | assessment | High |
| FR-042 | Mastery Profile Display | mastery | High |
| FR-043 | Mastery Evidence Generation | mastery | High |
| FR-044 | Mastery Level-Up Event | mastery | Medium |
| FR-045 | Due Review Display | review_scheduler | High |
| FR-046 | Review Attempt Processing | review_scheduler | High |
| FR-047 | Review Schedule Display | review_scheduler | Low |
| FR-048 | XP Reward | reward_engine | High |
| FR-049 | XP Ledger | reward_engine | Medium |
| FR-050 | Achievement Badges | reward_engine | Low |
| FR-051 | Review Notification | notifications | Medium |
| FR-052 | Streak Notification | notifications | Low |
| FR-053 | Input Security Scan | integrity | Critical |
| FR-054 | Duplicate Detection | integrity | Critical |
| FR-055 | Rate Limiting | integrity | Critical |
| FR-056 | Learning Analytics | analytics | Low |
| FR-057 | Audit Logging | audit | Critical |
| FR-058 | Error Tracking | operator | High |
| FR-059 | Health Check | operator | High |
| FR-060 | Operator User Lookup | operator | Medium |
| FR-061 | Operator Audit View | operator | Medium |
| FR-062 | AI Gateway Structured Output | ai_gateway | Critical |
| FR-063 | Assessment Confidence Scoring | diagnostics | Medium |
| FR-064 | Content Version Tracking | content | Low |
| FR-065 | Prompt Template Versioning | ai_gateway | Medium |

---

## Table 3: API Endpoint to User Story Traceability

| Endpoint | Method | US IDs | Module |
|----------|--------|--------|--------|
| /api/v1/auth/register | POST | US-001 | identity |
| /api/v1/auth/login | POST | US-004 | identity |
| /api/v1/auth/login/social | POST | US-005 | identity |
| /api/v1/auth/refresh | POST | US-006 | identity |
| /api/v1/users/me | GET, PATCH | US-001 | identity |
| /api/v1/learner-profile | GET, PUT | US-011, US-012 | learner_profile |
| /api/v1/diagnostics/sessions | POST | US-007, US-010 | diagnostics |
| /api/v1/diagnostics/{id}/responses | POST | US-008 | diagnostics |
| /api/v1/diagnostics/{id}/complete | POST | US-009 | diagnostics |
| /api/v1/learning-contract/current | GET, POST, PUT | US-014, US-015, US-016 | learning_contract |
| /api/v1/lessons | GET | US-017 | curriculum |
| /api/v1/lessons/recommended | GET | US-018 | curriculum |
| /api/v1/lesson-sessions | POST | US-019, US-020, US-023, US-026, US-029, US-032, US-036 | lesson_engine |
| /api/v1/lesson-sessions/{id} | GET | US-019 | lesson_engine |
| /api/v1/lesson-sessions/{id}/attempts | POST | US-030, US-037 | lesson_engine |
| /api/v1/lesson-sessions/{id}/complete | POST | US-038, US-043, US-048, US-050 | lesson_engine |
| /api/v1/submissions/text | POST | US-021, US-024, US-033, US-035, US-054 | submission |
| /api/v1/submissions/audio | POST | US-027, US-054 | submission |
| /api/v1/submissions/{id}/analysis | GET | US-022, US-025, US-028, US-031, US-034 | submission |
| /api/v1/reviews/due | GET | US-045 | review_scheduler |
| /api/v1/reviews/{id}/attempt | POST | US-046 | review_scheduler |
| /api/v1/reviews | GET | US-047 | review_scheduler |
| /api/v1/mastery/profile | GET, PUT | US-013, US-042, US-044 | mastery |
| /api/v1/rewards/ledger | GET | US-049 | reward_engine |
| /api/v1/notifications | GET | US-051, US-052 | notifications |
| /api/v1/assessments | POST | US-039 | assessment |
| /api/v1/assessments/performance | POST | US-040 | assessment |
| /api/v1/assessments/{id} | GET | US-041 | assessment |
| /api/v1/analytics | GET | US-056 | analytics |
| /api/v1/operator/diagnostics | GET | US-060 | operator |
| /api/v1/operator/audit | GET | US-061 | operator |
| /api/v1/health | GET | US-059 | operator |

---

## Table 4: Entity to Module Traceability

| Entity | Module |
|--------|--------|
| User | identity |
| AuthIdentity | identity |
| LearnerProfile | learner_profile |
| SkillDimension | learner_profile |
| XPBalance | learner_profile |
| DiagnosticSession | diagnostics |
| DiagnosticResponse | diagnostics |
| SkillAssessment | diagnostics |
| LearningEntryContract | learning_contract |
| LessonDefinition | curriculum |
| LessonSession | lesson_engine |
| LessonAttempt | lesson_engine |
| Submission | submission |
| AIAnalysisRequest | ai_gateway |
| AIAnalysisResult | ai_gateway |
| ValidationResult | linguistic_validation / pedagogical_validation |
| PerformanceAssessment | assessment |
| MasteryRecord | mastery |
| MasteryEvidence | mastery |
| ReviewItem | review_scheduler |
| ReviewSchedule | review_scheduler |
| RewardTransaction | reward_engine |
| Notification | notifications |
| SecurityEvent | integrity |
| IntegrityRiskSignal | integrity |
| AuditEvent | audit |
| PromptTemplateVersion | ai_gateway |
| ContentVersion | content |

---

## Table 5: NFR to ADR Traceability

| NFR ID | NFR Title | Related ADR |
|--------|-----------|-------------|
| NFR-001 | API Response Time (Non-AI) | ADR-002 (FastAPI), ADR-003 (Modular Monolith) |
| NFR-002 | Lesson State Transition Latency | ADR-003 (Modular Monolith) |
| NFR-003 | LLM Analysis Completion Time | ADR-008 (AI Gateway), ADR-009 (Structured Output Validation) |
| NFR-004 | API Availability | ADR-003 (Modular Monolith), ADR-012 (Observability) |
| NFR-005 | Audit Event Durability | ADR-011 (Audit Architecture) |
| NFR-006 | Reward Transaction Integrity | ADR-010 (Deterministic Mastery/Rewards), ADR-004 (PostgreSQL) |
| NFR-007 | Data Isolation | ADR-004 (PostgreSQL), ADR-007 (Supabase Auth) |
| NFR-008 | Mobile Responsiveness | ADR-001 (React Native/Expo) |
| NFR-009 | Accessibility Compliance | ADR-001 (React Native/Expo) |
| NFR-010 | Localization Support | ADR-001 (React Native/Expo) |
| NFR-011 | API Idempotency | ADR-002 (FastAPI), ADR-009 (Structured Output Validation) |
| NFR-012 | Data Consistency | ADR-004 (PostgreSQL) |
| NFR-013 | Model Fallback | ADR-008 (AI Gateway) |
| NFR-014 | Rate Limiting | ADR-007 (Supabase Auth) |
| NFR-015 | Disaster Recovery | ADR-004 (PostgreSQL), ADR-006 (Object Storage) |
| NFR-016 | Maintainability | ADR-002 (FastAPI), ADR-003 (Modular Monolith) |
| NFR-017 | Testability | ADR-003 (Modular Monolith), ADR-009 (Structured Output Validation) |
| NFR-018 | LLM Cost Control | ADR-008 (AI Gateway), ADR-012 (Observability) |
| NFR-019 | Observability Coverage | ADR-012 (Observability) |
| NFR-020 | Graceful Degradation | ADR-008 (AI Gateway), ADR-005 (Arq) |
| NFR-025 | CI Pipeline Duration | ADR-001, ADR-002 (Build tooling) |
| NFR-026 | Security Event Response | ADR-011 (Audit), ADR-012 (Observability) |
| NFR-028 | Scheduler Accuracy | ADR-010 (Deterministic Mastery) |
