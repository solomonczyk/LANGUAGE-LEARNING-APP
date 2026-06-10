# User Journeys

**Status:** Draft  
**Version:** 1.0.0  
**Last updated:** 2026-06-10

---

## Journey 1: First-Time Onboarding and Diagnostic

**Trigger:** User downloads app and opens it for the first time

**Preconditions:**
- App installed on mobile device
- Internet connection active
- No existing account

### Steps

| Step | Actor | Action | System Decision | Data Writes |
|------|-------|--------|----------------|-------------|
| 1 | User | Opens app for first time | Display welcome screen | — |
| 2 | User | Selects "Create Account" | — | — |
| 3 | User | Enters email, password, selects target language (English) and native language (Italian) | Validate email format, password strength; check language support | User, AuthIdentity, LearnerProfile (created) |
| 4 | User | Completes onboarding questionnaire (goals, experience, interests) | Store preferences in profile | LearnerProfile (updated) |
| 5 | User | Selects "Start Diagnostic" | **Deterministic**: Create diagnostic session with adaptive engine | DiagnosticSession (created) |
| 6 | User | Answers reading comprehension question (text + multiple choice) | Score response; select next question based on adaptive algorithm | DiagnosticResponse (created) |
| 7 | User | Answers writing prompt (short text) | Store response | DiagnosticResponse (created) |
| 8 | User | Answers listening comprehension (audio + multiple choice) | Score response | DiagnosticResponse (created) |
| 9 | User | Answers grammar/vocabulary questions (mixed format) | Score response; determine if sufficient evidence collected | DiagnosticResponse (created) |
| 10 | System | Diagnostic complete | **Deterministic**: Compute skill assessments per dimension | SkillAssessment (created), DiagnosticSession (completed) |
| 11 | User | Views diagnostic results (CEFR levels per dimension, strengths/weaknesses) | | |
| 12 | User | Creates Learning Entry Contract (sets goal: B1 in 6 months, 4 sessions/week) | **Deterministic**: Validate and store contract | LearningEntryContract (created) |
| 13 | System | Presents personalized lesson recommendations | **LLM Proposal**: Suggest first lesson based on profile + interests | — |
| 14 | User | Selects personal narrative lesson | | LessonSession (created) |

**System Decisions:** 5 deterministic decisions, 1 LLM proposal point  
**Deterministic Validation Points:** Email validation, language support check, diagnostic scoring algorithm  
**Reward Events:** None (onboarding)  
**Audit Events:** User.created, DiagnosticSession.completed, LearningContract.created  
**Failure Branches:** Email already registered, network timeout during diagnostic, diagnostic interrupted mid-way  
**Recovery Branches:** Resume diagnostic from last answered question, retry registration with different email  
**Completion Criteria:** User has created account, completed diagnostic, signed learning contract, and selected first lesson

---

## Journey 2: Returning Learner After Long Break

**Trigger:** User opens app after 3+ months of inactivity

**Preconditions:**
- Existing account with prior learning data
- Prior skill levels recorded
- Learning contract expired or stale

### Steps

| Step | Actor | Action | System Decision | Data Writes |
|------|-------|--------|----------------|-------------|
| 1 | User | Logs in with email and password | Auth verification; detect inactivity period > 90 days | — |
| 2 | System | Detects long absence | **Deterministic**: Flag profile as "stale", recommend reassessment | LearnerProfile (flagged) |
| 3 | User | Views prompt: "It's been a while! Take a quick check-in to update your level?" | | |
| 4 | User | Accepts reassessment | | DiagnosticSession (created) |
| 5 | User | Completes shortened diagnostic (2 questions per dimension vs 5 for new users) | **Deterministic**: Adaptive diagnostic weighted against prior profile | DiagnosticResponse (created) |
| 6 | System | Computes updated skill assessments (prior data decayed + new evidence) | **Deterministic**: Skill assessment with decay function | SkillAssessment (updated) |
| 7 | User | Reviews updated profile (notes skill regression in speaking, stable reading) | | |
| 8 | User | Updates Learning Entry Contract (reduced frequency: 3 sessions/week) | **Deterministic**: Validate contract | LearningEntryContract (updated) |
| 9 | System | Recommends reviewing prior mastered items that may be forgotten | **Deterministic**: Identify review items due from SRS schedule | — |
| 10 | User | Starts review session for forgotten items | | LessonSession (created) |

**System Decisions:** 4 deterministic decisions, 0 LLM proposals  
**Deterministic Validation Points:** Inactivity threshold, diagnostic decay function, contract validation  
**Reward Events:** XP for completing reassessment  
**Audit Events:** User.login_after_absence, DiagnosticSession.completed, Contract.updated  
**Failure Branches:** User declines reassessment (continue with stale profile), user doesn't remember password  
**Recovery Branches:** Password reset, skip reassessment and go directly to lessons  
**Completion Criteria:** User has updated profile, signed new contract, and started a review session

---

## Journey 3: Personal Narrative Lesson

**Trigger:** User selects "Personal Narrative" lesson mode

**Preconditions:**
- Learner has active profile and learning contract
- At least one lesson slot available for today

### Steps

| Step | Actor | Action | System Decision | Data Writes |
|------|-------|--------|----------------|-------------|
| 1 | User | Selects "Personal Narrative" from lesson modes | | |
| 2 | System | Generates personalized prompt based on learner interests and level | **LLM Proposal**: Generate prompt (e.g., "Tell me about a memorable trip") | LessonSession (created, state: active) |
| 3 | User | Views prompt and writes 5-10 sentences in target language | | |
| 4 | User | Submits narrative text | **Deterministic**: Input normalization, security/injection scan, schema validation | Submission (created, state: submitted) |
| 5 | System | Binds lesson context to submission | | AIAnalysisRequest (created) |
| 6 | System | Sends to AI Gateway for analysis | **LLM Proposal**: Analyze text for grammar, vocabulary, coherence, fluency | AIAnalysisResult (created) |
| 7 | System | **Validation Gate**: Validate AI output schema | **Deterministic**: Schema validation | ValidationResult (created) |
| 8 | System | **Validation Gate**: Linguistic validation | **Deterministic**: Check AI analysis for linguistic accuracy | ValidationResult (updated) |
| 9 | System | **Validation Gate**: Pedagogical validation | **Deterministic**: Check feedback appropriateness for learner level | ValidationResult (updated) |
| 10 | System | **Policy Gate**: Policy engine checks all validations passed | **Deterministic**: If all pass, proceed; if not, escalate | — |
| 11 | System | **Mastery Gate**: Compute mastery evidence | **Deterministic**: Update mastery based on performance | MasteryEvidence (created) |
| 12 | System | **Review Gate**: Create SRS review items from errors | **Deterministic**: Schedule review items | ReviewItem (created), ReviewSchedule (created) |
| 13 | System | **Reward Gate**: Calculate and award XP | **Deterministic**: Reward Engine calculates XP | RewardTransaction (created) |
| 14 | System | Records audit event | | AuditEvent (created) |
| 15 | User | Views analysis: corrected text, error explanations, suggestions, XP earned | | |
| 16 | User | Reads feedback and marks as understood | | LessonSession (state: completed) |

**System Decisions:** 7 deterministic decisions, 2 LLM proposal points  
**Deterministic Validation Points:** Input security scan, schema validation, linguistic validation, pedagogical validation, policy engine, mastery calculation, reward calculation  
**Data Writes:** LessonSession, Submission, AIAnalysisRequest, AIAnalysisResult, ValidationResult, MasteryEvidence, ReviewItem, ReviewSchedule, RewardTransaction, AuditEvent  
**Failure Branches:** AI timeout, schema validation failure, pedagogical rejection, duplicate submission detected  
**Recovery Branches:** Retry AI call with fallback provider (up to 2 retries), inform user of temporary issue, allow resubmission after cooling period  
**Reward Events:** XP for completing lesson; bonus XP if all validations pass first try  
**Audit Events:** LessonSession.created, LessonSession.completed, Submission.accepted, AIAnalysis.completed, Reward.awarded  
**Completion Criteria:** User has received analysis, reviewed feedback, lesson session is marked completed, XP has been awarded, review items scheduled

---

## Journey 4: Visual Description Lesson

**Trigger:** User selects "Visual Scene" lesson mode

**Preconditions:** User has active profile and available lesson slot

### Steps

| Step | Actor | Action | System Decision | Data Writes |
|------|-------|--------|----------------|-------------|
| 1 | User | Selects "Visual Scene" lesson | | |
| 2 | System | Loads image scene and generates description prompt | **Deterministic**: Select image from content library based on level + interests | LessonSession (created) |
| 3 | User | Views image and writes description in target language (50-100 words) | | |
| 4 | User | Submits text | **Deterministic**: Normalize, scan, validate | Submission (created) |
| 5 | System | AI analysis of description (vocabulary range, descriptive accuracy, grammar) | **LLM Proposal**: Analyze | AIAnalysisResult |
| 6 | System | Validation pipeline (schema → linguistic → pedagogical → policy) | **Deterministic**: Chain of validators | ValidationResult |
| 7 | System | Lesson completion: mastery, review, reward, audit | **Deterministic**: All gates | Multiple entities |
| 8 | User | Views feedback with highlighted corrections and lexical suggestions | | |

**Failure Branches:** Image fails to load, AI analysis timeout  
**Reward Events:** XP + potential "Visual Descriptor" badge on 5th visual lesson  
**Audit Events:** Full pipeline audit

---

## Journey 5: Audio Retelling Lesson

**Trigger:** User selects "Audio Narrative" lesson mode

**Preconditions:** Device has audio playback capability; microphone permissions granted

### Steps

| Step | Actor | Action | System Decision | Data Writes |
|------|-------|--------|----------------|-------------|
| 1 | User | Selects "Audio Narrative" lesson | | |
| 2 | System | Loads audio narrative (short story at target level) | **Deterministic**: Select from content library | LessonSession (created) |
| 3 | User | Listens to audio (can replay up to 3 times) | | |
| 4 | User | Records retelling of the story in target language | | |
| 5 | User | Submits audio recording | **Deterministic**: Validate audio format, duration, size | Submission (created, type: audio) |
| 6 | System | Audio processing: speech-to-text conversion | **Boundary**: STT service | Transcript generated |
| 7 | System | AI analysis: compare retelling to original for comprehension accuracy | **LLM Proposal**: Analyze transcript | AIAnalysisResult |
| 8 | System | Validation pipeline | **Deterministic**: All gates | ValidationResult |
| 9 | System | Lesson completion | **Deterministic**: All gates | Multiple entities |
| 10 | User | Views analysis: comprehension score, language accuracy, pronunciation notes | | |

**Failure Branches:** Microphone not available, audio too quiet, STT failure, recording too long (>5 min)  
**Reward Events:** XP + bonus for comprehensive retelling  
**Audit Events:** Audio submission received, STT completed, analysis completed

---

## Journey 6: Functional Communication Lesson

**Trigger:** User selects "Functional Communication" lesson mode

**Preconditions:** User has A1+ level in target language

### Steps

| Step | Actor | Action | System Decision | Data Writes |
|------|-------|--------|----------------|-------------|
| 1 | User | Selects "Functional Communication" | | |
| 2 | System | Loads scenario: "Ordering food at a restaurant" | **Deterministic**: Scenario from content library matched to level | LessonSession (created) |
| 3 | User | Views scenario context and role (customer) | | |
| 4 | System | AI dialogue partner initiates conversation | **LLM Proposal**: Generate first dialogue turn | |
| 5 | User | Responds as customer (text or audio) | | LessonAttempt |
| 6 | System | AI partner responds based on user's input | **LLM Proposal**: Generate next turn | |
| 7 | User | Continues dialogue (minimum 3 exchanges) | | |
| 8 | User | Completes dialogue | | |
| 9 | System | Full dialogue analysis | **LLM Proposal**: Analyze conversational effectiveness | AIAnalysisResult |
| 10 | System | Validation pipeline → lesson completion | **Deterministic**: All gates | Multiple entities |
| 11 | User | Views dialogue transcript with corrections and communication tips | | |

**Failure Branches:** User cannot produce any response (scaffolding prompt offered), dialogue goes off-topic  
**Reward Events:** XP for completion + bonus for completing scenario without scaffolding  
**Audit Events:** Dialogue session, each turn logged

---

## Journey 7: Scheduled Review Session

**Trigger:** User receives push notification: "You have 5 review items due!"

**Preconditions:** User has completed past lessons; SRS has generated review items

### Steps

| Step | Actor | Action | System Decision | Data Writes |
|------|-------|--------|----------------|-------------|
| 1 | User | Opens notification → review screen | | |
| 2 | System | Loads due review items ordered by priority | **Deterministic**: Review due calculation | — |
| 3 | User | Views first review item (vocabulary card: word + sentence) | | |
| 4 | User | Recalls meaning and types answer | | |
| 5 | System | Checks answer against expected | **Deterministic**: Exact/close match scoring | ReviewItem (updated) |
| 6 | User | Rates recall difficulty (easy/medium/hard) | | |
| 7 | System | Updates SRS schedule based on performance + difficulty rating | **Deterministic**: SRS algorithm (interval recalculation) | ReviewSchedule (updated) |
| 8 | User | Repeats for remaining items | | |
| 9 | System | After all items: compute XP for review session | **Deterministic**: Reward Engine | RewardTransaction |
| 10 | User | Views session summary: items reviewed, accuracy, XP earned | | |

**Failure Branches:** No due items, user rates inconsistently  
**Reward Events:** XP per item reviewed correctly  
**Audit Events:** ReviewSession.completed, SRS.schedule.updated

---

## Journey 8: Failed Attempt and Repair Lesson

**Trigger:** User's submission fails pedagogical validation (sufficient for lesson completion but below quality threshold)

**Preconditions:** User has an active lesson session

### Steps

| Step | Actor | Action | System Decision | Data Writes |
|------|-------|--------|----------------|-------------|
| 1 | System | Pedagogical validation fails (e.g., submission too short, too many errors) | **Deterministic**: Below quality threshold | ValidationResult (failed) |
| 2 | System | **Retry Gate**: Checks retry eligibility (retry count < 3, classified cause) | **Deterministic**: Retry gate decision | — |
| 3 | User | Views message: "Your response needs more work. Here's what to improve." | | |
| 4 | User | Receives guided hints (vocabulary suggestions, structure tips) | **LLM Proposal**: Generate scaffolding hints | |
| 5 | User | Revises and resubmits (attempt 2) | | Submission (attempt 2) |
| 6 | System | Validation pipeline re-run | **Deterministic**: Full pipeline | ValidationResult |
| 7 | System | Still below threshold → retry gate allows one more attempt with more scaffolding | **Deterministic**: Retry gate | — |
| 8 | User | Receives more explicit scaffolding (model sentence, key vocabulary) | **LLM Proposal**: Generate focused scaffolding | |
| 9 | User | Revises and resubmits (attempt 3) | | Submission (attempt 3) |
| 10 | System | Validation pipeline passes (acceptable quality achieved) | **Deterministic**: Pipeline pass | ValidationResult |
| 11 | System | **Retry Gate**: Reset retry counter on success | **Deterministic**: Reset | — |
| 12 | System | Lesson completion flow (mastery, review, reward - reduced XP for retries) | **Deterministic**: Reduced reward for retries | Multiple entities |
| 13 | User | Views feedback showing improvement trajectory across attempts | | |

**Failure Branches:** Max retries exceeded (lesson failed, no XP, item added to review as error case)  
**Recovery Branches:** User can abandon and try different lesson mode, or retry next day  
**Reward Events:** Reduced XP for retry-based completion (70% of base), bonus for improvement shown  
**Audit Events:** Submission.rejected, Retry.granted, Submission.accepted_after_retry, Reward.reduced
