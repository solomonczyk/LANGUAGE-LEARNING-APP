# User Story Catalog

**Status:** Draft  
**Version:** 1.0.0  
**Last updated:** 2026-06-10

---

## EPIC-01: Onboarding

### US-001: User Registration
**Title:** User Registration with Language Selection  
**As a** new learner, **I want** to register using email or social login and select my target language and native language, **so that** I can start my learning journey with content tailored to my language pair.  
**Priority:** Critical | **MVP:** Yes | **Persona:** P-02 | **FR:** FR-001 | **API:** POST /api/v1/auth/register | **Entity:** User, AuthIdentity  
**Acceptance Criteria:**
- [ ] User can register with email + password or social login (Google, Apple)
- [ ] User selects target language from a list of supported languages
- [ ] User selects native/support language
- [ ] Onboarding progress is saved if interrupted
- [ ] Registration completes within 5 seconds under normal conditions
**Failure States:** Email already registered, invalid email, unsupported language, network timeout  
**Security Notes:** Email and auth identity stored securely via external auth provider

### US-002: Onboarding Questionnaire
**Title:** Complete Onboarding Questionnaire  
**As a** new learner, **I want** to answer a brief questionnaire about my goals, experience level, and interests, **so that** my initial learning experience is personalized.  
**Priority:** High | **MVP:** Yes | **Persona:** P-03 | **FR:** FR-002 | **API:** POST /api/v1/learner-profile | **Entity:** LearnerProfile  
**Acceptance Criteria:**
- [ ] User answers 5-8 questions about goals, experience, and interests
- [ ] Questionnaire can be skipped and revisited
- [ ] Responses are saved to learner profile
**Failure States:** Partial completion, skipped questions  
**Security Notes:** Interest data is personal but not sensitive

### US-003: First-Session Tutorial
**Title:** Interactive First-Session Tutorial  
**As a** new learner, **I want** to receive a brief interactive tutorial on how to use the app, **so that** I understand the key features and interface.  
**Priority:** Medium | **MVP:** Yes | **Persona:** P-02 | **FR:** FR-003 | **API:** GET /api/v1/lessons | **Entity:** LessonDefinition  
**Acceptance Criteria:**
- [ ] Tutorial covers: creating a lesson, submitting work, reviewing feedback, tracking progress
- [ ] Tutorial is skippable
- [ ] Tutorial can be replayed from settings
**Failure States:** User skips tutorial and later reports confusion

---

## EPIC-02: Authentication

### US-004: Email and Password Login
**Title:** Login with Email and Password  
**As a** registered learner, **I want** to log in using my email and password, **so that** I can access my learning account.  
**Priority:** Critical | **MVP:** Yes | **Persona:** P-01 | **FR:** FR-004 | **API:** POST /api/v1/auth/login | **Entity:** AuthIdentity  
**Acceptance Criteria:**
- [ ] Login with valid credentials returns JWT access and refresh tokens
- [ ] Invalid credentials return clear error without revealing which field is wrong
- [ ] Rate limiting after 5 failed attempts
**Failure States:** Wrong credentials, account locked, network error

### US-005: Social Login
**Title:** Login with Social Provider  
**As a** registered learner, **I want** to log in using Google or Apple, **so that** I don't need to remember another password.  
**Priority:** High | **MVP:** Yes | **Persona:** P-03 | **FR:** FR-005 | **API:** POST /api/v1/auth/login (social) | **Entity:** AuthIdentity  
**Acceptance Criteria:**
- [ ] Login with Google returns valid session
- [ ] Login with Apple returns valid session
- [ ] Account linking works if same email exists

### US-006: Token Refresh
**Title:** Automatic Token Refresh  
**As a** logged-in learner, **I want** my session to be automatically refreshed, **so that** I stay logged in during a lesson session.  
**Priority:** High | **MVP:** Yes | **Persona:** P-01 | **FR:** FR-006 | **API:** POST /api/v1/auth/refresh | **Entity:** AuthIdentity

---

## EPIC-03: Diagnostic

### US-007: Start Diagnostic Session
**Title:** Start Multidimensional Diagnostic  
**As a** new learner, **I want** to start a comprehensive diagnostic session that tests multiple skill dimensions, **so that** the app understands my current proficiency.  
**Priority:** Critical | **MVP:** Yes | **Persona:** P-02 | **FR:** FR-007 | **API:** POST /api/v1/diagnostics/sessions | **Entity:** DiagnosticSession  
**Acceptance Criteria:**
- [ ] Session covers reading, writing, listening, grammar dimensions
- [ ] Session starts with adaptive questions based on persona onboarding data
- [ ] Estimated duration is shown before starting

### US-008: Answer Diagnostic Question
**Title:** Answer Diagnostic Questions  
**As a** learner in a diagnostic session, **I want** to answer questions across different skill dimensions, **so that** my proficiency can be accurately assessed.  
**Priority:** Critical | **MVP:** Yes | **Persona:** P-01 | **FR:** FR-008 | **API:** POST /api/v1/diagnostics/{id}/responses | **Entity:** DiagnosticResponse

### US-009: Complete Diagnostic
**Title:** Complete Diagnostic and Receive Assessment  
**As a** learner, **I want** to complete the diagnostic and receive my skill assessment results, **so that** I understand my strengths and areas for improvement.  
**Priority:** Critical | **MVP:** Yes | **Persona:** P-04 | **FR:** FR-009 | **API:** POST /api/v1/diagnostics/{id}/complete | **Entity:** SkillAssessment

### US-010: Return User Diagnostic
**Title:** Returning User Reassessment  
**As a** returning learner, **I want** to take a shorter reassessment diagnostic, **so that** my profile reflects my current level after a long break.  
**Priority:** High | **MVP:** Yes | **Persona:** P-01 | **FR:** FR-010 | **API:** POST /api/v1/diagnostics/sessions | **Entity:** DiagnosticSession

---

## EPIC-04: Learner Profile

### US-011: View Profile
**Title:** View Learner Profile  
**As a** learner, **I want** to view my profile showing skill dimensions, XP, and progress, **so that** I can track my learning journey.  
**Priority:** High | **MVP:** Yes | **Persona:** P-01 | **FR:** FR-011 | **API:** GET /api/v1/learner-profile | **Entity:** LearnerProfile

### US-012: Update Profile
**Title:** Update Profile Settings  
**As a** learner, **I want** to update my profile settings including language preferences and goals, **so that** my learning experience stays relevant.  
**Priority:** Medium | **MVP:** Yes | **Persona:** P-03 | **FR:** FR-012 | **API:** PUT /api/v1/learner-profile | **Entity:** LearnerProfile

### US-013: View Skill Dimensions
**Title:** View Skill Dimension Breakdown  
**As a** learner, **I want** to see my skill levels broken down by dimension (reading, writing, listening, speaking, grammar, vocabulary), **so that** I know which areas need focus.  
**Priority:** High | **MVP:** Yes | **Persona:** P-04 | **FR:** FR-013 | **API:** GET /api/v1/mastery/profile | **Entity:** SkillDimension

---

## EPIC-05: Learning Entry Contract

### US-014: Create Learning Contract
**Title:** Create Learning Entry Contract  
**As a** learner after completing diagnostics, **I want** to create a Learning Entry Contract that sets my goals and commitments, **so that** I have a clear learning plan.  
**Priority:** Critical | **MVP:** Yes | **Persona:** P-01 | **FR:** FR-014 | **API:** POST /api/v1/learning-contract/current | **Entity:** LearningEntryContract

### US-015: Review Contract Terms
**Title:** Review and Accept Contract Terms  
**As a** learner, **I want** to review my learning contract terms including frequency, duration, and focus areas, **so that** I commit to a realistic plan.  
**Priority:** High | **MVP:** Yes | **Persona:** P-03 | **FR:** FR-015 | **API:** GET /api/v1/learning-contract/current | **Entity:** LearningEntryContract

### US-016: Update Contract
**Title:** Update Learning Contract  
**As a** learner, **I want** to update my learning contract as my circumstances change, **so that** the plan remains realistic.  
**Priority:** Medium | **MVP:** Yes | **Persona:** P-03 | **FR:** FR-016 | **API:** PUT /api/v1/learning-contract/current | **Entity:** LearningEntryContract

---

## EPIC-06: Lesson Selection

### US-017: Browse Available Lessons
**Title:** Browse Available Lesson Modes  
**As a** learner, **I want** to see available lesson modes (narrative, visual, audio, functional, writing), **so that** I can choose the type of practice I want.  
**Priority:** High | **MVP:** Yes | **Persona:** P-01 | **FR:** FR-017 | **API:** GET /api/v1/lessons | **Entity:** LessonDefinition

### US-018: Get Recommended Lesson
**Title:** Receive Recommended Lesson  
**As a** learner, **I want** to receive a lesson recommendation based on my profile, skill gaps, and preferences, **so that** I practice what benefits me most.  
**Priority:** High | **MVP:** Yes | **Persona:** P-04 | **FR:** FR-018 | **API:** GET /api/v1/lessons/recommended | **Entity:** LessonDefinition

### US-019: Start Lesson Session
**Title:** Start a Lesson Session  
**As a** learner, **I want** to start a lesson session for a selected lesson type, **so that** I can begin practicing.  
**Priority:** Critical | **MVP:** Yes | **Persona:** P-02 | **FR:** FR-019 | **API:** POST /api/v1/lesson-sessions | **Entity:** LessonSession

---

## EPIC-07: Personal Narrative

### US-020: Receive Narrative Prompt
**Title:** Receive Personal Narrative Prompt  
**As a** learner, **I want** to receive a prompt asking me to describe a personal experience in the target language, **so that** I practice authentic self-expression.  
**Priority:** High | **MVP:** Yes | **Persona:** P-04 | **FR:** FR-020 | **API:** POST /api/v1/lesson-sessions | **Entity:** LessonSession

### US-021: Submit Narrative Text
**Title:** Submit Personal Narrative  
**As a** learner, **I want** to write my personal narrative in the target language, **so that** I practice written production.  
**Priority:** High | **MVP:** Yes | **Persona:** P-01 | **FR:** FR-021 | **API:** POST /api/v1/submissions/text | **Entity:** Submission

### US-022: Receive Narrative Analysis
**Title:** Receive Narrative Analysis and Feedback  
**As a** learner, **I want** to receive AI analysis of my narrative with corrections and suggestions, **so that** I learn from my mistakes.  
**Priority:** High | **MVP:** Yes | **Persona:** P-04 | **FR:** FR-022 | **API:** GET /api/v1/submissions/{id}/analysis | **Entity:** AIAnalysisResult

---

## EPIC-08: Visual Lesson

### US-023: View Visual Scene
**Title:** View Single Image Scene for Description  
**As a** learner, **I want** to see an image scene and receive a prompt to describe it in the target language, **so that** I practice vocabulary and descriptive language.  
**Priority:** High | **MVP:** Yes | **Persona:** P-02 | **FR:** FR-023 | **API:** POST /api/v1/lesson-sessions | **Entity:** LessonDefinition

### US-024: Submit Visual Description  
**Title:** Submit Description of Visual Scene  
**As a** learner, **I want** to write or record a description of the visual scene, **so that** I practice production skills.  
**Priority:** High | **MVP:** Yes | **Persona:** P-04 | **FR:** FR-024 | **API:** POST /api/v1/submissions/text | **Entity:** Submission

### US-025: Receive Visual Feedback
**Title:** Receive Feedback on Visual Description  
**As a** learner, **I want** to receive targeted feedback on my description, **so that** I improve my descriptive vocabulary and sentence structure.  
**Priority:** High | **MVP:** Yes | **Persona:** P-02 | **FR:** FR-025 | **API:** GET /api/v1/submissions/{id}/analysis | **Entity:** AIAnalysisResult

---

## EPIC-09: Audio Narrative

### US-026: Listen to Audio Clip
**Title:** Listen to Target Language Audio  
**As a** learner, **I want** to listen to a short audio narrative in the target language, **so that** I practice listening comprehension.  
**Priority:** High | **MVP:** Yes | **Persona:** P-04 | **FR:** FR-026 | **API:** POST /api/v1/lesson-sessions | **Entity:** LessonSession

### US-027: Retell Audio Story
**Title:** Retell the Audio Story  
**As a** learner, **I want** to retell the audio story in my own words (text or audio), **so that** I practice both comprehension and production.  
**Priority:** High | **MVP:** Yes | **Persona:** P-01 | **FR:** FR-027 | **API:** POST /api/v1/submissions/audio | **Entity:** Submission

### US-028: Receive Audio Analysis
**Title:** Receive Audio Retelling Analysis  
**As a** learner, **I want** to receive analysis of my retelling including comprehension accuracy and language quality, **so that** I improve my listening and production.  
**Priority:** High | **MVP:** Yes | **Persona:** P-04 | **FR:** FR-028 | **API:** GET /api/v1/submissions/{id}/analysis | **Entity:** AIAnalysisResult

---

## EPIC-10: Functional Communication

### US-029: Start Functional Scenario
**Title:** Start Functional Communication Scenario  
**As a** learner, **I want** to start a practical scenario (ordering food, asking directions, making a request), **so that** I practice real-world communication.  
**Priority:** High | **MVP:** Yes | **Persona:** P-03 | **FR:** FR-029 | **API:** POST /api/v1/lesson-sessions | **Entity:** LessonSession

### US-030: Complete Functional Task
**Title:** Complete a Functional Communication Task  
**As a** learner, **I want** to complete the task by producing appropriate target language responses, **so that** I practice practical communication.  
**Priority:** High | **MVP:** Yes | **Persona:** P-03 | **FR:** FR-030 | **API:** POST /api/v1/lesson-sessions/{id}/attempts | **Entity:** LessonAttempt

### US-031: Receive Functional Feedback
**Title:** Receive Functional Communication Feedback  
**As a** learner, **I want** feedback on how effectively I communicated in the scenario, **so that** I improve my practical language use.  
**Priority:** Medium | **MVP:** Yes | **Persona:** P-03 | **FR:** FR-031 | **API:** GET /api/v1/submissions/{id}/analysis | **Entity:** AIAnalysisResult

---

## EPIC-11: Writing Cycle

### US-032: Start Writing Task
**Title:** Start Guided Writing Task  
**As a** learner, **I want** to start a writing task with a prompt and word count guidance, **so that** I practice extended written production.  
**Priority:** Medium | **MVP:** Yes | **Persona:** P-04 | **FR:** FR-032 | **API:** POST /api/v1/lesson-sessions | **Entity:** LessonSession

### US-033: Submit Writing for Correction
**Title:** Submit Writing for AI Correction  
**As a** learner, **I want** to submit my writing for AI-powered correction and analysis, **so that** I identify errors and improve.  
**Priority:** High | **MVP:** Yes | **Persona:** P-01 | **FR:** FR-033 | **API:** POST /api/v1/submissions/text | **Entity:** Submission

### US-034: Receive Writing Analysis
**Title:** Receive Detailed Writing Analysis  
**As a** learner, **I want** a detailed analysis of my writing including grammar, vocabulary, and organization, **so that** I understand my specific areas for improvement.  
**Priority:** High | **MVP:** Yes | **Persona:** P-04 | **FR:** FR-034 | **API:** GET /api/v1/submissions/{id}/analysis | **Entity:** AIAnalysisResult

### US-035: Revise and Resubmit
**Title:** Revise Writing Based on Feedback  
**As a** learner, **I want** to revise my writing based on feedback and resubmit, **so that** I practice the correction cycle.  
**Priority:** Medium | **MVP:** Yes | **Persona:** P-01 | **FR:** FR-035 | **API:** POST /api/v1/submissions/text | **Entity:** Submission

---

## EPIC-12: Dialogue Simulation

### US-036: Start Dialogue Simulation
**Title:** Start AI Dialogue Simulation  
**As a** learner, **I want** to start a dialogue simulation with an AI conversation partner, **so that** I practice interactive communication.  
**Priority:** High | **MVP:** Yes | **Persona:** P-04 | **FR:** FR-036 | **API:** POST /api/v1/lesson-sessions | **Entity:** LessonSession

### US-037: Exchange Dialogue Turns
**Title:** Exchange Dialogue Turns  
**As a** learner, **I want** to exchange turns in a simulated dialogue, **so that** I practice conversational flow.  
**Priority:** High | **MVP:** Yes | **Persona:** P-04 | **FR:** FR-037 | **API:** POST /api/v1/lesson-sessions/{id}/attempts | **Entity:** LessonAttempt

### US-038: Complete Dialogue and Receive Assessment
**Title:** Complete Dialogue and Receive Assessment  
**As a** learner, **I want** to complete the dialogue and receive an assessment of my conversational performance, **so that** I improve my interactive skills.  
**Priority:** Medium | **MVP:** Yes | **Persona:** P-03 | **FR:** FR-038 | **API:** POST /api/v1/lesson-sessions/{id}/complete | **Entity:** PerformanceAssessment

---

## EPIC-13: Assessment

### US-039: Take Short Quiz
**Title:** Take a Short Content Quiz  
**As a** learner, **I want** to take a short quiz covering vocabulary and grammar from my recent lessons, **so that** I reinforce learning.  
**Priority:** Medium | **MVP:** Yes | **Persona:** P-01 | **FR:** FR-039 | **API:** POST /api/v1/assessments | **Entity:** PerformanceAssessment

### US-040: Complete Performance Task
**Title:** Complete Performance-Based Assessment  
**As a** learner, **I want** to complete a performance-based task that demonstrates my ability in a skill dimension, **so that** I can prove mastery.  
**Priority:** Medium | **MVP:** Yes | **Persona:** P-03 | **FR:** FR-040 | **API:** POST /api/v1/assessments/performance | **Entity:** PerformanceAssessment

### US-041: View Assessment Results
**Title:** View Assessment Results  
**As a** learner, **I want** to view my assessment results with detailed feedback, **so that** I understand my current level.  
**Priority:** High | **MVP:** Yes | **Persona:** P-04 | **FR:** FR-041 | **API:** GET /api/v1/assessments/{id} | **Entity:** SkillAssessment

---

## EPIC-14: Mastery

### US-042: Track Mastery Progress
**Title:** Track Mastery Progress per Skill  
**As a** learner, **I want** to see my mastery progress for each skill dimension, **so that** I know how close I am to the next level.  
**Priority:** High | **MVP:** Yes | **Persona:** P-01 | **FR:** FR-042 | **API:** GET /api/v1/mastery/profile | **Entity:** MasteryRecord

### US-043: Receive Mastery Evidence
**Title:** Receive Mastery Evidence After Lesson  
**As a** learner, **I want** to receive mastery evidence after completing a lesson, **so that** I see proof of my learning.  
**Priority:** High | **MVP:** Yes | **Persona:** P-04 | **FR:** FR-043 | **API:** POST /api/v1/lesson-sessions/{id}/complete | **Entity:** MasteryEvidence

### US-044: Mastery Level Up
**Title:** Receive Mastery Level-Up Notification  
**As a** learner, **I want** to be notified when I achieve a new mastery level in a skill dimension, **so that** I celebrate my progress.  
**Priority:** Medium | **MVP:** Yes | **Persona:** P-01 | **FR:** FR-044 | **API:** GET /api/v1/mastery/profile | **Entity:** MasteryRecord

---

## EPIC-15: Review/SRS

### US-045: View Due Reviews
**Title:** View Due Review Items  
**As a** learner, **I want** to see a list of review items that are due for practice, **so that** I can reinforce previously learned material.  
**Priority:** High | **MVP:** Yes | **Persona:** P-01 | **FR:** FR-045 | **API:** GET /api/v1/reviews/due | **Entity:** ReviewItem

### US-046: Complete Review Attempt
**Title:** Complete a Review Attempt  
**As a** learner, **I want** to attempt a review item and receive immediate feedback, **so that** I reinforce my memory.  
**Priority:** High | **MVP:** Yes | **Persona:** P-03 | **FR:** FR-046 | **API:** POST /api/v1/reviews/{id}/attempt | **Entity:** ReviewSchedule

### US-047: View Review Schedule
**Title:** View Upcoming Review Schedule  
**As a** learner, **I want** to see when my next reviews are scheduled, **so that** I can plan my practice sessions.  
**Priority:** Low | **MVP:** No | **Persona:** P-01 | **FR:** FR-047 | **API:** GET /api/v1/reviews | **Entity:** ReviewSchedule

---

## EPIC-16: Rewards

### US-048: Earn XP for Lesson Completion
**Title:** Earn XP for Completing Lessons  
**As a** learner, **I want** to earn XP when I complete lessons, **so that** I feel rewarded for my effort.  
**Priority:** High | **MVP:** Yes | **Persona:** P-01 | **FR:** FR-048 | **API:** POST /api/v1/lesson-sessions/{id}/complete | **Entity:** RewardTransaction

### US-049: View XP Ledger
**Title:** View XP Transaction History  
**As a** learner, **I want** to view my XP transaction history, **so that** I understand how I earned my rewards.  
**Priority:** Medium | **MVP:** Yes | **Persona:** P-03 | **FR:** FR-049 | **API:** GET /api/v1/rewards/ledger | **Entity:** XPBalance

### US-050: Earn Achievement Badge
**Title:** Earn Achievement Badge  
**As a** learner, **I want** to earn achievement badges for milestones (first lesson, streak, level up), **so that** I feel recognized for my accomplishments.  
**Priority:** Low | **MVP:** Yes | **Persona:** P-04 | **FR:** FR-050 | **API:** POST /api/v1/lesson-sessions/{id}/complete | **Entity:** RewardTransaction

---

## EPIC-17: Notifications

### US-051: Receive Review Reminder
**Title:** Receive Review Reminder Notification  
**As a** learner, **I want** to receive a notification when I have due review items, **so that** I don't forget to practice.  
**Priority:** Medium | **MVP:** Yes | **Persona:** P-03 | **FR:** FR-051 | **API:** POST /api/v1/notifications | **Entity:** Notification

### US-052: Streak Reminder
**Title:** Receive Streak Reminder  
**As a** learner, **I want** to receive a reminder if I haven't practiced today, **so that** I maintain my learning streak.  
**Priority:** Low | **MVP:** Yes | **Persona:** P-01 | **FR:** FR-052 | **API:** POST /api/v1/notifications | **Entity:** Notification

---

## EPIC-18: Safety and Integrity

### US-053: Input Sanitization
**Title:** Malicious Input Detection  
**As a** system, **I want** to detect and block malicious input (prompt injection, XSS, SQLi), **so that** the application and AI remain secure.  
**Priority:** Critical | **MVP:** Yes | **Persona:** System | **FR:** FR-053 | **API:** All | **Entity:** SecurityEvent  
**Acceptance Criteria:**
- [ ] Prompt injection patterns are detected in learner submissions
- [ ] Malicious input is rejected with appropriate error
- [ ] Security event is logged
**Security Notes:** CRITICAL — First line of defense against LLM attacks

### US-054: Duplicate Submission Prevention
**Title:** Prevent Duplicate Submissions  
**As a** system, **I want** to detect and reject duplicate submissions, **so that** learners cannot earn undeserved rewards.  
**Priority:** Critical | **MVP:** Yes | **Persona:** System | **FR:** FR-054 | **API:** POST /api/v1/submissions/text, POST /api/v1/submissions/audio | **Entity:** IntegrityRiskSignal

### US-055: Rate Limit Enforcement
**Title:** Rate Limit API Requests  
**As a** system, **I want** to limit API request rates per user and per IP, **so that** the system is protected from abuse.  
**Priority:** Critical | **MVP:** Yes | **Persona:** System | **FR:** FR-055 | **API:** All | **Entity:** IntegrityRiskSignal

---

## EPIC-19: Analytics and Audit

### US-056: View Learning Analytics
**Title:** View Personal Learning Analytics  
**As a** learner, **I want** to see my learning analytics (lessons completed, time spent, progress), **so that** I can reflect on my effort.  
**Priority:** Low | **MVP:** Yes | **Persona:** P-01 | **FR:** FR-056 | **API:** GET /api/v1/analytics | **Entity:** AuditEvent

### US-057: Audit Event Logging
**Title:** Complete Audit Event Logging  
**As a** system, **I want** to log every state-changing operation as an audit event, **so that** all system actions are traceable.  
**Priority:** Critical | **MVP:** Yes | **Persona:** System | **FR:** FR-057 | **API:** All | **Entity:** AuditEvent

### US-058: Error Tracking
**Title:** Track and Report Errors  
**As an** operator, **I want** to track application errors with context, **so that** I can diagnose and fix issues.  
**Priority:** High | **MVP:** Yes | **Persona:** Operator | **FR:** FR-058 | **API:** Internal | **Entity:** AuditEvent

---

## EPIC-20: Operator Support

### US-059: View System Health
**Title:** View System Health Dashboard  
**As an** operator, **I want** to view the system health status, **so that** I can monitor service availability.  
**Priority:** High | **MVP:** Yes | **Persona:** Operator | **FR:** FR-059 | **API:** GET /api/v1/health | **Entity:** None  
**Acceptance Criteria:**
- [ ] Health endpoint returns status of all dependent services
- [ ] Response includes database connectivity, queue status, storage status
- [ ] Response time under 100ms

### US-060: Read-Only User Diagnostics
**Title:** Access Read-Only User Diagnostics  
**As an** operator, **I want** to view a user's diagnostic results and learning data, **so that** I can help troubleshoot issues.  
**Priority:** Medium | **MVP:** Yes | **Persona:** Operator | **FR:** FR-060 | **API:** GET /api/v1/operator/diagnostics | **Entity:** DiagnosticSession

### US-061: View Audit Log
**Title:** View System Audit Log  
**As an** operator, **I want** to view and search the audit log, **so that** I can investigate unexpected behavior.  
**Priority:** Medium | **MVP:** Yes | **Persona:** Operator | **FR:** FR-061 | **API:** GET /api/v1/operator/audit | **Entity:** AuditEvent
