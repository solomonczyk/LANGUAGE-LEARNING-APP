# Closed Learner Alpha Execution Plan

## 1. Objective

Execute a controlled closed learner alpha against the accepted Layer 004A baseline. The goal is to validate the complete learner journey through the app with 3–5 synthetic testers, verifying that each step works as expected in a controlled environment.

## 2. Scope

### In scope

- Onboarding flow
- Diagnostic flow
- Learning Contract creation and display
- Home dashboard
- Lesson flow (create session, submit, process, result)
- Mock AI analysis pipeline
- Mastery evidence creation
- Audit event recording
- Feedback collection
- Operator observations

### Out of scope

- Real AI provider integration
- Real LLM calls
- Staging deployment
- Production deployment
- New features or lesson modes
- Social features
- Payments
- Real personal data

## 3. Environment

| Component | Configuration |
|-----------|--------------|
| Backend | Docker Compose on localhost:8000 |
| Database | PostgreSQL 16 (Docker) |
| Frontend | Expo Web (ready) |
| AI Gateway | Mock mode (valid fixtures) |
| Auth | Stub mode (X-User-Id header) |
| Network | Localhost only |

## 4. Participant Profiles

Five synthetic testers:

| ID | Type | Profile |
|----|------|---------|
| ALPHA-001 | returning_learner | Already familiar with the app flow |
| ALPHA-002 | beginner | First time using the app |
| ALPHA-003 | work_focused | Focused on efficiency and getting through quickly |
| ALPHA-004 | low_confidence | Needs clear instructions and reassurance |
| ALPHA-005 | returning_learner (advanced) | Higher level, wants to see advanced features |

## 5. Test Flow

Each tester must complete:

1. Root → redirected to onboarding
2. Onboarding: select target language, native language, learning goal, level
3. Diagnostic: complete all 4 steps (grammar, vocabulary, writing, coherence)
4. Learning Contract: view contract with personalized parameters
5. Home: see dashboard with lesson plan and mastery progress
6. Lesson: read communicative goal, write response, submit
7. Lesson Session: watch processing pipeline
8. Result: see feedback, corrections, validation results
9. Mastery: verify mastery records created
10. Audit: verify audit events recorded

## 6. Success Criteria

- 3–5 testers complete the full flow
- Critical issues: 0
- Major blocking issues: 0
- Runtime blockers: 0
- Happy path API 404: 0
- Audit completion present: true
- Real AI calls: false
- Feedback collected from all testers
