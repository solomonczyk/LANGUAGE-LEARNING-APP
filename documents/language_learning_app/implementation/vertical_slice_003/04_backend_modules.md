# Backend Modules

## Module Directory: `backend/app/modules/`

### 1. identity
- **Path:** `modules/identity/`
- **Files:** `__init__.py`, `schemas.py`, `services.py`, `router.py`, `public_interface.py`
- **Endpoints:** POST /identity/register, POST /identity/login, GET /identity/me
- **Models:** User
- **Purpose:** Local auth stub for development

### 2. learner_profile
- **Path:** `modules/learner_profile/`
- **Files:** `__init__.py`, `schemas.py`, `services.py`, `router.py`, `public_interface.py`
- **Endpoints:** POST /learner-profile, GET /learner-profile/me
- **Models:** LearnerProfile
- **Purpose:** Learner profile CRUD

### 3. diagnostics
- **Path:** `modules/diagnostics/`
- **Files:** `__init__.py`, `schemas.py`, `services.py`, `router.py`, `public_interface.py`
- **Endpoints:** POST /diagnostics/sessions, POST /diagnostics/sessions/{id}/responses, POST /diagnostics/sessions/{id}/complete, GET /diagnostics/sessions/{id}
- **Models:** DiagnosticSession, DiagnosticResponse, SkillAssessment
- **States:** CREATED, IN_PROGRESS, COMPLETED, FAILED

### 4. learning_contract
- **Path:** `modules/learning_contract/`
- **Files:** `__init__.py`, `schemas.py`, `services.py`, `router.py`, `public_interface.py`
- **Endpoints:** GET /learning-contract/current, POST /learning-contract/current
- **Models:** LearningEntryContract
- **Purpose:** Deterministic contract generation

### 5. lesson_engine
- **Path:** `modules/lesson_engine/`
- **Files:** `__init__.py`, `schemas.py`, `services.py`, `router.py`, `public_interface.py`
- **Endpoints:** POST /lesson-sessions, GET /lesson-sessions/{id}, POST /lesson-sessions/{id}/submissions, POST /lesson-sessions/{id}/process
- **Models:** LessonSession, LessonAttempt
- **States:** CREATED, ACTIVE, SUBMITTED, ANALYSIS_PENDING, ANALYSIS_VALIDATED, COMPLETED, REJECTED, FAILED

### 6. submission
- **Path:** `modules/submission/`
- **Files:** `__init__.py`, `schemas.py`, `services.py`, `router.py`, `public_interface.py`
- **Endpoints:** POST /submissions, GET /submissions/{id}
- **Models:** Submission
- **States:** RECEIVED, VALIDATED, ANALYSIS_PENDING, ANALYZED, ACCEPTED, REJECTED, FAILED

### 7. ai_gateway
- **Path:** `modules/ai_gateway/`
- **Files:** `__init__.py`, `schemas.py`, `services.py`, `router.py`, `public_interface.py`
- **Endpoints:** POST /ai-gateway/analyze, GET /ai-gateway/status
- **Models:** AIAnalysisRequest, AIAnalysisResult
- **Purpose:** Mock AI analysis with deterministic fixtures

### 8. linguistic_validation
- **Path:** `modules/linguistic_validation/`
- **Files:** `__init__.py`, `schemas.py`, `services.py`, `router.py`, `public_interface.py`
- **Endpoints:** POST /linguistic-validation/validate
- **Models:** ValidationResult
- **Checks:** output_consistency, issue_structure, severity_validity, span_validity, allowed_codes, confidence_range

### 9. pedagogical_validation
- **Path:** `modules/pedagogical_validation/`
- **Files:** `__init__.py`, `schemas.py`, `services.py`, `router.py`, `public_interface.py`
- **Endpoints:** POST /pedagogical-validation/validate
- **Models:** ValidationResult
- **Checks:** feedback_matches_goal, corrections_within_budget, no_unsupported_mastery_claim, no_reward_command, no_curriculum_mutation

### 10. policy_engine
- **Path:** `modules/policy_engine/`
- **Files:** `__init__.py`, `schemas.py`, `services.py`, `router.py`, `public_interface.py`
- **Endpoints:** POST /policy-engine/decide
- **Purpose:** Authoritative completion decision
- **Decisions:** COMPLETE, RETRY, REJECT, FAIL

### 11. mastery
- **Path:** `modules/mastery/`
- **Files:** `__init__.py`, `schemas.py`, `services.py`, `router.py`, `public_interface.py`
- **Endpoints:** POST /mastery/evidence, GET /mastery/profile
- **Models:** MasteryRecord, MasteryEvidence
- **States:** PENDING, RECORDED, REJECTED
- **Allowed types:** introduced, recognized, guided_use

### 12. audit
- **Path:** `modules/audit/`
- **Files:** `__init__.py`, `schemas.py`, `services.py`, `router.py`, `public_interface.py`
- **Endpoints:** POST /audit/events, GET /audit/events
- **Models:** AuditEvent
- **Purpose:** Append-only event storage

### 13. operator
- **Path:** `modules/operator/`
- **Files:** `__init__.py`, `router.py`
- **Endpoints:** GET /operator/health, GET /operator/audit-events
- **Purpose:** Read-only diagnostic endpoints
