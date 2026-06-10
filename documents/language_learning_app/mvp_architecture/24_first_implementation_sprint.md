# First Implementation Sprint

**Status:** Draft  
**Version:** 1.0.0  
**Last updated:** 2026-06-10

---

## Sprint Overview

**Goal:** Build the first vertical slice through the entire learning system: from onboarding through lesson completion, with mock AI analysis, deterministic validation, and audit.

**Duration:** 2 weeks (recommended)  
**Team:** 1-2 backend, 1 mobile, 1 QA (or equivalent cross-functional capacity)

---

## Sprint Scope (One Vertical Slice)

```
Onboarding → Learner Profile → Diagnostic Session → Learning Entry Contract 
→ Text-Based Personal Narrative Lesson → Submission → Mock AI Analysis 
→ Schema Validation → Deterministic Lesson Completion → Mastery Evidence → Audit
```

This is a **feature-level** slice, not a collection of micro-tasks. The slice demonstrates the complete data flow from user registration through lesson completion with audit and reward.

---

## Deliverables

### 1. Mobile Shell (React Native/Expo)
**Description:** Navigation shell with basic screens for the vertical slice
- Registration/login screen
- Home/dashboard screen (basic)
- Lesson screen (text input)
- Profile screen (read-only)
- Navigation between screens (Expo Router)

**Definition of Done:**
- [ ] App boots on iOS simulator and Android emulator
- [ ] Registration screen renders and accepts input
- [ ] Navigation between screens works
- [ ] Lesson screen displays prompt and accepts text input
- [ ] Profile screen displays basic user info

### 2. Backend Modular Monolith (FastAPI)
**Description:** FastAPI project with initial module structure
- Project scaffold (FastAPI app, dependency injection, config)
- 5 initial modules: identity, learner_profile, diagnostics, lesson_engine, audit
- Module registration and dependency wiring
- Health check endpoint

**Definition of Done:**
- [ ] FastAPI app starts and responds to health check
- [ ] Module routing works (APIRouter per module)
- [ ] Dependency injection loads module dependencies
- [ ] Configuration loads from environment

### 3. PostgreSQL Schema (Initial Migration)
**Description:** Alembic migration with core tables
- Tables: User, AuthIdentity, LearnerProfile, SkillDimension, DiagnosticSession, DiagnosticResponse, SkillAssessment, LearningEntryContract, LessonDefinition, LessonSession, LessonAttempt, Submission, ValidationResult, MasteryRecord, MasteryEvidence, RewardTransaction, AuditEvent
- Foreign keys and indexes
- UUID primary keys
- Created_at/updated_at conventions

**Definition of Done:**
- [ ] Migration applies cleanly
- [ ] Migration rolls back cleanly
- [ ] All required tables present
- [ ] Foreign key constraints defined
- [ ] Indexes for query patterns defined

### 4. Auth Stub (Supabase Auth)
**Description:** Basic authentication integration
- Supabase Auth client setup
- Registration endpoint (POST /auth/register)
- Login endpoint (POST /auth/login)
- Token verification middleware
- Basic user record creation

**Definition of Done:**
- [ ] User can register with email + password
- [ ] User can log in and receive JWT
- [ ] Authenticated endpoints validate token
- [ ] User record created in database on registration

### 5. Diagnostic Flow
**Description:** Initial diagnostic session creation and completion
- Diagnostic session creation
- Predefined diagnostic questions (static for sprint 1)
- Response recording
- Simple scoring algorithm (deterministic)
- Skill assessment output

**Definition of Done:**
- [ ] Diagnostic session created on request
- [ ] Questions returned to client
- [ ] Responses stored and scored
- [ ] Skill assessment computed on completion

### 6. One Lesson Flow (Personal Narrative)
**Description:** Complete personal narrative lesson end-to-end
- Lesson prompt generation (static template for sprint 1)
- Lesson session lifecycle (created → active → submitting → completed)
- Text submission handling
- Mock AI analysis pipeline

**Definition of Done:**
- [ ] Lesson session created with prompt
- [ ] Learner submits text response
- [ ] Text flows through pipeline steps
- [ ] Lesson completes and returns analysis

### 7. Mock AI Gateway
**Description:** Simulated AI analysis returning pre-defined structured responses
- Mock implementation of `analyze_text()` returning structured analysis
- Schema validation of mock output
- Simulated latency (500ms-2000ms)
- Configurable success/failure for testing

**Definition of Done:**
- [ ] Mock returns structured analysis matching expected schema
- [ ] Configurable response delay
- [ ] Configurable failure mode (timeout, invalid JSON)
- [ ] Schema validation on output

### 8. Validation Pipeline
**Description:** Three-stage validation pipeline
- Input schema validation (Pydantic)
- Output schema validation (mock AI output validated)
- Basic linguistic validation (word count, language detection)
- Basic pedagogical validation (minimum length, level match)

**Definition of Done:**
- [ ] Invalid input rejected
- [ ] Invalid mock output rejected
- [ ] Too-short submission flagged
- [ ] Validation results stored

### 9. Audit System
**Description:** Structured audit event logging
- Audit event model (event_id, trace_id, user_id, action, module, details, result, timestamp)
- Audit middleware/logging hook
- All pipeline steps emit audit events
- Read-only audit query endpoint (operator)

**Definition of Done:**
- [ ] Every state-changing operation creates audit event
- [ ] Audit events contain required fields
- [ ] Trace ID correlates events from single request
- [ ] Operator can query audit events

### 10. Tests
**Description:** Initial test suite for sprint 1 deliverables
- Unit tests for all business logic
- Integration tests for diagnostic and lesson flows
- Contract tests for API endpoints
- Schema validation tests
- State machine tests for LessonSession

**Definition of Done:**
- [ ] All unit tests pass
- [ ] Integration tests for diagnostic and lesson flows pass
- [ ] Contract tests pass for all implemented endpoints
- [ ] State machine transitions tested

### 11. Local Docker Environment
**Description:** Docker Compose setup for local development
- API container (hot-reload)
- PostgreSQL container
- Redis container
- MinIO container
- Docker network configuration
- Docker health checks

**Definition of Done:**
- [ ] `docker compose up` starts all services
- [ ] API accessible on localhost:8000
- [ ] Database migrations auto-run on API start
- [ ] All services report healthy

### 12. CI (GitHub Actions)
**Description:** Basic CI pipeline
- Lint (ruff, ESLint)
- Backend tests (pytest)
- Schema validation
- Build check

**Definition of Done:**
- [ ] CI runs on PR to main
- [ ] All jobs pass on clean code
- [ ] Pipeline completes in < 15 minutes

---

## What is NOT in Sprint 1

| Feature | Reason | Planned Sprint |
|---------|--------|----------------|
| Audio recording/upload | Dependency on audio pipeline | Sprint 2 |
| Real AI provider integration | Mock AI sufficient for validation | Sprint 2 |
| Spaced repetition scheduling | Requires lesson data | Sprint 2 |
| Full reward engine | Requires lesson completion flow | Sprint 2 |
| Push notifications | Requires notification infrastructure | Sprint 3 |
| All 5 lesson modes | Sprint 1 covers 1 lesson mode | Sprint 2-3 |
| Anti-cheat (full) | Basic duplicate detection in sprint 1 | Sprint 2 |
| Operator dashboard | Read-only audit available | Sprint 3 |
| Image/visual lessons | Requires asset pipeline | Sprint 3 |
| Dialogue simulation | Requires multi-turn flow | Sprint 3 |

---

## Sprint Acceptance Criteria

The sprint is successful when:
- [ ] A learner can register → complete diagnostic → sign learning contract → take personal narrative lesson → submit text → receive mock analysis → see XP earned
- [ ] All pipeline steps execute in order
- [ ] Audit events exist for every operation
- [ ] All tests pass
- [ ] Local Docker environment works on a fresh checkout
- [ ] CI pipeline passes
- [ ] Proof JSON generated and committed
- [ ] No security vulnerabilities introduced
- [ ] All forbidden actions respected (no production code, no real LLM calls)
