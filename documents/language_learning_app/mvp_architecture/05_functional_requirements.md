# Functional Requirements

**Status:** Draft  
**Version:** 1.0.0  
**Last updated:** 2026-06-10

---

## Identity Domain

### FR-001: User Registration
**Description:** System shall allow user registration with email + password or social login (Google, Apple). Must collect email, password (strength validated), target language, and native language.  
**Priority:** Critical | **Source US:** US-001 | **Service Owner:** identity | **Data Owner:** User  
**Acceptance Criteria:**
- [ ] Registration accepts email and password meeting strength requirements
- [ ] Registration accepts Google and Apple OAuth
- [ ] Required fields: email, target_language, native_language
- [ ] Duplicate email returns clear error
**Failure Behaviour:** Return 409 for duplicate email, 422 for validation failure  
**Security Impact:** Account creation vector; rate limit to 3 registrations/IP/hour  
**Observability:** registration_count, registration_failure_rate

### FR-002: Onboarding Questionnaire
**Description:** System shall present a 5-8 question onboarding questionnaire covering goals, experience level, and interests. Responses stored in learner profile.  
**Priority:** High | **Source US:** US-002 | **Service Owner:** identity | **Data Owner:** LearnerProfile  
**Acceptance Criteria:** Questions saved, profile updated, questionnaire skippable  
**Failure Behaviour:** Allow empty responses for optional questions  
**Security Impact:** Minimal

### FR-003: Tutorial Delivery
**Description:** System shall deliver an interactive tutorial covering key features. Must be skippable and replayable.  
**Priority:** Medium | **Source US:** US-003 | **Service Owner:** identity | **Data Owner:** LessonDefinition  
**Failure Behaviour:** Graceful if tutorial content fails to load; show fallback text  
**Security Impact:** None

## Authentication Domain

### FR-004: Email Login
**Description:** System shall authenticate users via email + password, returning JWT access token (15 min expiry) and refresh token (7 day expiry).  
**Priority:** Critical | **Source US:** US-004 | **Service Owner:** identity | **Data Owner:** AuthIdentity  
**Failure Behaviour:** Rate limit after 5 failures, 5-minute lockout  
**Security Impact:** CRITICAL — authentication gateway

### FR-005: Social Login
**Description:** System shall support OAuth login via Google and Apple, creating or linking accounts on first use.  
**Priority:** High | **Source US:** US-005 | **Service Owner:** identity | **Data Owner:** AuthIdentity  
**Failure Behaviour:** OAuth provider errors returned to user  
**Security Impact:** CRITICAL — depends on provider security

### FR-006: Token Refresh
**Description:** System shall accept refresh tokens to issue new access tokens without re-authentication.  
**Priority:** High | **Source US:** US-006 | **Service Owner:** identity | **Data Owner:** AuthIdentity  
**Failure Behaviour:** Invalid/expired refresh token returns 401  
**Security Impact:** Critical — refresh token rotation required

### FR-007: Start Diagnostic Session
**Description:** System shall create a multidimensional diagnostic session covering reading, writing, listening, and grammar. Session adaptively selects questions based on learner responses.  
**Priority:** Critical | **Source US:** US-007, US-010 | **Service Owner:** diagnostics | **Data Owner:** DiagnosticSession  
**Failure Behaviour:** Session creation fails gracefully with retry  
**Security Impact:** None  
**Observability:** diagnostic_session_count

### FR-008: Record Diagnostic Response
**Description:** System shall accept and validate diagnostic question responses, scoring them against answer keys.  
**Priority:** Critical | **Source US:** US-008 | **Service Owner:** diagnostics | **Data Owner:** DiagnosticResponse  
**Failure Behaviour:** Reject malformed responses, preserve partial progress

### FR-009: Complete Diagnostic
**Description:** System shall compute skill assessments per dimension upon diagnostic completion, using deterministic scoring algorithm.  
**Priority:** Critical | **Source US:** US-009 | **Service Owner:** diagnostics | **Data Owner:** SkillAssessment  
**Failure Behaviour:** If insufficient evidence, prompt for more responses

### FR-010: Return User Reassessment
**Description:** System shall detect returning users after >90 days inactivity and offer shortened reassessment.  
**Priority:** High | **Source US:** US-010 | **Service Owner:** diagnostics | **Data Owner:** DiagnosticSession  
**Failure Behaviour:** If user declines, continue with decayed profile

### FR-011: View Learner Profile
**Description:** System shall display the learner profile including skill dimensions, XP balance, streak count, and recent activity.  
**Priority:** High | **Source US:** US-011 | **Service Owner:** learner_profile | **Data Owner:** LearnerProfile

### FR-012: Update Learner Profile
**Description:** System shall allow learners to update language preferences, goals, and notification settings.  
**Priority:** Medium | **Source US:** US-012 | **Service Owner:** learner_profile | **Data Owner:** LearnerProfile

### FR-013: Skill Dimension Display
**Description:** System shall display skill levels broken down by dimension with CEFR labels and progress bars.  
**Priority:** High | **Source US:** US-013 | **Service Owner:** learner_profile | **Data Owner:** SkillDimension

### FR-014: Create Learning Entry Contract
**Description:** System shall allow creation of a learning contract with target CEFR level, weekly session count, and focus areas.  
**Priority:** Critical | **Source US:** US-014 | **Service Owner:** learning_contract | **Data Owner:** LearningEntryContract

### FR-015: Review Contract
**Description:** System shall display current contract terms with progress against goals.  
**Priority:** High | **Source US:** US-015 | **Service Owner:** learning_contract | **Data Owner:** LearningEntryContract

### FR-016: Update Contract
**Description:** System shall allow contract modification with re-validation of goals.  
**Priority:** Medium | **Source US:** US-016 | **Service Owner:** learning_contract | **Data Owner:** LearningEntryContract

### FR-017: Browse Lessons
**Description:** System shall display available lesson modes with descriptions, estimated duration, and recommended level.  
**Priority:** High | **Source US:** US-017 | **Service Owner:** curriculum | **Data Owner:** LessonDefinition

### FR-018: Recommend Lesson
**Description:** System shall recommend a lesson based on learner profile, skill gaps, and learning contract priorities.  
**Priority:** High | **Source US:** US-018 | **Service Owner:** curriculum | **Data Owner:** LessonDefinition  
**LLM Boundary:** Recommendation may use LLM to generate personalized prompt, but selection algorithm is deterministic

### FR-019: Start Lesson Session
**Description:** System shall create a new lesson session with appropriate content, prompt, and configuration.  
**Priority:** Critical | **Source US:** US-019 | **Service Owner:** lesson_engine | **Data Owner:** LessonSession

### FR-020: Generate Narrative Prompt
**Description:** System shall generate a personalized narrative prompt based on learner interests and level. May use LLM.  
**Priority:** High | **Source US:** US-020 | **Service Owner:** content | **Data Owner:** LessonDefinition  
**LLM Boundary:** LLM proposes prompt; approved if passes content policy

### FR-021: Accept Text Submission
**Description:** System shall accept text submissions with input normalization, security scanning, and schema validation.  
**Priority:** Critical | **Source US:** US-021, US-024, US-033 | **Service Owner:** submission | **Data Owner:** Submission

### FR-022: Generate Text Analysis
**Description:** System shall generate AI analysis of text submissions including grammar, vocabulary, coherence, and fluency feedback.  
**Priority:** High | **Source US:** US-022, US-025, US-034 | **Service Owner:** ai_gateway | **Data Owner:** AIAnalysisResult  
**LLM Boundary:** LLM proposes analysis; must pass validation gates before presentation

### FR-023: Present Visual Scene
**Description:** System shall present an image scene as lesson content with description prompt.  
**Priority:** High | **Source US:** US-023 | **Service Owner:** content | **Data Owner:** LessonDefinition

### FR-024: Accept Audio Recording
**Description:** System shall accept audio submissions with format validation (MP4/WAV), size limits (max 10MB), and duration limits (max 5 min).  
**Priority:** High | **Source US:** US-024, US-027 | **Service Owner:** submission | **Data Owner:** Submission

### FR-025: Generate Visual Description Feedback
**Description:** System shall generate targeted feedback on visual description focusing on vocabulary range, descriptive accuracy, and sentence structure.  
**Priority:** High | **Source US:** US-025 | **Service Owner:** ai_gateway | **Data Owner:** AIAnalysisResult

### FR-026: Audio Playback
**Description:** System shall play audio narratives with playback controls (play, pause, rewind 10s).  
**Priority:** High | **Source US:** US-026 | **Service Owner:** content | **Data Owner:** LessonDefinition

### FR-027: Audio Retelling Analysis
**Description:** System shall analyze audio retelling via STT → AI analysis pipeline for comprehension accuracy and language quality.  
**Priority:** High | **Source US:** US-027, US-028 | **Service Owner:** ai_gateway | **Data Owner:** AIAnalysisResult

### FR-028: Generate Audio Feedback
**Description:** System shall present audio retelling analysis including comprehension score, accuracy, and pronunciation notes.  
**Priority:** High | **Source US:** US-028 | **Service Owner:** ai_gateway | **Data Owner:** AIAnalysisResult

### FR-029: Functional Scenario Delivery
**Description:** System shall deliver practical communication scenarios with role context and objectives.  
**Priority:** High | **Source US:** US-029 | **Service Owner:** content | **Data Owner:** LessonDefinition

### FR-030: Functional Task Acceptance
**Description:** System shall accept multiple types of functional communication attempts (text, audio) within a scenario.  
**Priority:** High | **Source US:** US-030 | **Service Owner:** lesson_engine | **Data Owner:** LessonAttempt

### FR-031: Functional Feedback Generation
**Description:** System shall provide feedback on communicative effectiveness in functional scenarios.  
**Priority:** Medium | **Source US:** US-031 | **Service Owner:** ai_gateway | **Data Owner:** AIAnalysisResult

### FR-032: Guided Writing Task
**Description:** System shall present writing tasks with prompt, word count guidance, and structure suggestions.  
**Priority:** Medium | **Source US:** US-032 | **Service Owner:** content | **Data Owner:** LessonDefinition

### FR-033: Writing Correction
**Description:** System shall perform AI-powered writing correction with error categorization and suggestions.  
**Priority:** High | **Source US:** US-033 | **Service Owner:** ai_gateway | **Data Owner:** AIAnalysisResult

### FR-034: Detailed Writing Analysis
**Description:** System shall provide detailed writing analysis covering grammar, vocabulary, organization, and register.  
**Priority:** High | **Source US:** US-034 | **Service Owner:** ai_gateway | **Data Owner:** AIAnalysisResult

### FR-035: Revision Cycle
**Description:** System shall allow learners to revise and resubmit work, tracking improvement across attempts.  
**Priority:** Medium | **Source US:** US-035 | **Service Owner:** lesson_engine | **Data Owner:** Submission

### FR-036: Dialogue Initiation
**Description:** System shall initiate AI-powered dialogue simulation with scenario context and role assignment.  
**Priority:** High | **Source US:** US-036 | **Service Owner:** lesson_engine | **Data Owner:** LessonSession

### FR-037: Dialogue Turn Exchange
**Description:** System shall manage turn-by-turn dialogue exchange with AI partner responding contextually.  
**Priority:** High | **Source US:** US-037 | **Service Owner:** ai_gateway | **Data Owner:** LessonAttempt

### FR-038: Dialogue Completion Assessment
**Description:** System shall assess dialogue performance based on turn appropriateness, language quality, and task completion.  
**Priority:** Medium | **Source US:** US-038 | **Service Owner:** assessment | **Data Owner:** PerformanceAssessment

### FR-039: Quiz Delivery
**Description:** System shall deliver short quizzes (vocabulary, grammar, comprehension) with immediate scoring.  
**Priority:** Medium | **Source US:** US-039 | **Service Owner:** assessment | **Data Owner:** PerformanceAssessment

### FR-040: Performance Task Assessment
**Description:** System shall provide performance-based assessments that demonstrate integrated skill ability.  
**Priority:** Medium | **Source US:** US-040 | **Service Owner:** assessment | **Data Owner:** PerformanceAssessment

### FR-041: Assessment Results Display
**Description:** System shall display assessment results with score, feedback, and improvement suggestions.  
**Priority:** High | **Source US:** US-041 | **Service Owner:** assessment | **Data Owner:** SkillAssessment

### FR-042: Mastery Profile Display
**Description:** System shall display mastery progress per skill dimension with level, XP to next level, and recent evidence.  
**Priority:** High | **Source US:** US-042 | **Service Owner:** mastery | **Data Owner:** MasteryRecord

### FR-043: Mastery Evidence Generation
**Description:** System shall generate mastery evidence upon lesson completion, recording performance data.  
**Priority:** High | **Source US:** US-043 | **Service Owner:** mastery | **Data Owner:** MasteryEvidence  
**LLM Boundary:** LLM may propose evidence, but mastery state transition is deterministic

### FR-044: Mastery Level-Up Event
**Description:** System shall detect mastery level-up conditions and trigger notification and reward events.  
**Priority:** Medium | **Source US:** US-044 | **Service Owner:** mastery | **Data Owner:** MasteryRecord

### FR-045: Due Review Display
**Description:** System shall display review items due for practice, ordered by priority (overdue > due today > due this week).  
**Priority:** High | **Source US:** US-045 | **Service Owner:** review_scheduler | **Data Owner:** ReviewItem

### FR-046: Review Attempt Processing
**Description:** System shall accept review attempts, score them, and update SRS schedule based on performance.  
**Priority:** High | **Source US:** US-046 | **Service Owner:** review_scheduler | **Data Owner:** ReviewSchedule

### FR-047: Review Schedule Display
**Description:** System shall display upcoming review schedule with estimated workload.  
**Priority:** Low | **Source US:** US-047 | **Service Owner:** review_scheduler | **Data Owner:** ReviewSchedule

### FR-048: XP Reward
**Description:** System shall award XP deterministically for lesson completions and review attempts.  
**Priority:** High | **Source US:** US-048 | **Service Owner:** reward_engine | **Data Owner:** RewardTransaction  
**LLM Boundary:** STRICTLY FORBIDDEN — rewards are 100% deterministic

### FR-049: XP Ledger
**Description:** System shall maintain a complete, immutable XP transaction ledger.  
**Priority:** Medium | **Source US:** US-049 | **Service Owner:** reward_engine | **Data Owner:** XPBalance

### FR-050: Achievement Badges
**Description:** System shall award deterministic achievement badges for milestones.  
**Priority:** Low | **Source US:** US-050 | **Service Owner:** reward_engine | **Data Owner:** RewardTransaction

### FR-051: Review Notification
**Description:** System shall send push notifications for due review items based on learner's preferred time.  
**Priority:** Medium | **Source US:** US-051 | **Service Owner:** notifications | **Data Owner:** Notification

### FR-052: Streak Notification
**Description:** System shall send reminder notifications if learner has not practiced by a defined threshold time.  
**Priority:** Low | **Source US:** US-052 | **Service Owner:** notifications | **Data Owner:** Notification

### FR-053: Input Security Scan
**Description:** System shall scan all user input for prompt injection patterns, XSS, SQLi, and other malicious content. Blocked input must be rejected with SecurityEvent logging.  
**Priority:** Critical | **Source US:** US-053 | **Service Owner:** integrity | **Data Owner:** SecurityEvent

### FR-054: Duplicate Detection
**Description:** System shall detect duplicate submissions via content hash and idempotency keys.  
**Priority:** Critical | **Source US:** US-054 | **Service Owner:** integrity | **Data Owner:** IntegrityRiskSignal

### FR-055: Rate Limiting
**Description:** System shall enforce rate limits: 100 req/min authenticated, 10 req/min unauthenticated, 5 auth attempts per minute.  
**Priority:** Critical | **Source US:** US-055 | **Service Owner:** integrity | **Data Owner:** IntegrityRiskSignal

### FR-056: Learning Analytics
**Description:** System shall provide analytics on completed lessons, time spent, skills improved, and streaks.  
**Priority:** Low | **Source US:** US-056 | **Service Owner:** analytics | **Data Owner:** AuditEvent

### FR-057: Audit Logging
**Description:** System shall log all state-changing operations as structured audit events with trace_id, user_id, action, timestamp, and result.  
**Priority:** Critical | **Source US:** US-057 | **Service Owner:** audit | **Data Owner:** AuditEvent

### FR-058: Error Tracking
**Description:** System shall capture and report application errors with full context for operator diagnosis.  
**Priority:** High | **Source US:** US-058 | **Service Owner:** operator | **Data Owner:** AuditEvent

### FR-059: Health Check
**Description:** System shall provide health check endpoint reporting status of all dependent services.  
**Priority:** High | **Source US:** US-059 | **Service Owner:** operator | **Data Owner:** None

### FR-060: Operator User Lookup
**Description:** System shall provide operator read-only access to user diagnostic data and learning profile.  
**Priority:** Medium | **Source US:** US-060 | **Service Owner:** operator | **Data Owner:** DiagnosticSession

### FR-061: Operator Audit View
**Description:** System shall provide operator search and view of audit log with filtering.  
**Priority:** Medium | **Source US:** US-061 | **Service Owner:** operator | **Data Owner:** AuditEvent

### FR-062: AI Gateway Structured Output
**Description:** AI Gateway shall enforce structured output only — all LLM responses must conform to a defined JSON schema.  
**Priority:** Critical | **Source US:** US-022, US-028, US-034 | **Service Owner:** ai_gateway | **Data Owner:** AIAnalysisResult

### FR-063: Assessment Confidence Scoring
**Description:** System shall compute confidence scores for diagnostic assessments based on response consistency and quantity.  
**Priority:** Medium | **Source US:** US-009 | **Service Owner:** diagnostics | **Data Owner:** SkillAssessment

### FR-064: Content Version Tracking
**Description:** System shall track versions of lesson content, prompts, and analysis templates.  
**Priority:** Low | **Source US:** None (system quality) | **Service Owner:** content | **Data Owner:** ContentVersion

### FR-065: Prompt Template Versioning
**Description:** System shall version all LLM prompt templates with hash, enabling audit trail of which prompt version was used for each analysis.  
**Priority:** Medium | **Source US:** US-053, US-057 | **Service Owner:** ai_gateway | **Data Owner:** PromptTemplateVersion
