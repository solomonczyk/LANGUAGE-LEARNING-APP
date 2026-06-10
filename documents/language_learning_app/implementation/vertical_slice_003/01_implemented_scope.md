# Implemented Scope

## Mobile Application

- Expo Router app with TypeScript
- Routes: /onboarding, /diagnostic, /learning-contract, /home, /lesson/:id, /lesson-session/:id, /result/:id
- Onboarding screen with 4-step form (language, native language, goals, level)
- Diagnostic screen with 4-step assessment (grammar, vocabulary, writing, coherence)
- Learning Contract confirmation screen
- Home dashboard with lesson card
- Lesson screen with communicative goal, task, text input
- Processing screen with progress indicator
- Result screen with strengths, corrections, validation results
- Shared components: Button, LoadingScreen, ErrorScreen, StepIndicator, ProgressBar
- Zustand stores for onboarding draft, diagnostic draft, lesson text draft, route intent
- TanStack Query for server state management
- API client module with auth headers and idempotency support

## Backend Application

- FastAPI modular monolith with 13 modules
- SQLAlchemy 2.0 async with PostgreSQL
- Alembic migrations

### Backend Modules
1. **identity** — Local auth stub with user registration and login
2. **learner_profile** — Profile CRUD with language preferences
3. **diagnostics** — 4-dimension diagnostic with deterministic scoring
4. **learning_contract** — Deterministic contract creation from diagnostic results
5. **lesson_engine** — Lesson session management with full state machine
6. **submission** — Text reception, normalization, storage, deduplication
7. **ai_gateway** — Provider-independent mock AI analysis
8. **linguistic_validation** — Deterministic analysis quality checks
9. **pedagogical_validation** — Deterministic lesson-fit checks
10. **policy_engine** — Authoritative completion decision
11. **mastery** — Evidence creation and profile (limited types only)
12. **audit** — Append-only event storage
13. **operator** — Read-only diagnostic endpoints

## Database
- 17 tables: users, learner_profiles, diagnostic_sessions, diagnostic_responses, skill_assessments, learning_entry_contracts, lesson_definitions, lesson_sessions, lesson_attempts, submissions, ai_analysis_requests, ai_analysis_results, validation_results, mastery_records, mastery_evidence, audit_events
- UUID primary keys, timestamps, foreign keys, indexes, unique constraints
- Alembic migration with full upgrade and downgrade

## Infrastructure
- Docker Compose with PostgreSQL 16 and backend service
- Dockerfile for backend
- GitHub Actions CI with 7 job groups
- .env.example without credentials
