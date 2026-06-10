# MVP Product Scope

**Status:** Draft  
**Version:** 1.0.0  
**Last updated:** 2026-06-10

---

## Primary MVP Goal

The learner must complete the following end-to-end journey:

```
Registration/onboarding
→ Multidimensional diagnostic
→ Learning Entry Contract
→ Personalized lesson
→ First attempt
→ Constrained AI analysis
→ Guided correction
→ Independent output
→ Mastery evidence
→ Review scheduling
→ Deterministic reward
→ Learner profile update
```

This goal defines the minimum viable product. Every lesson mode must support this complete cycle. The MVP is a **vertically integrated learning experience**, not a collection of disconnected features.

---

## Product Vision Statement

A mobile-first language learning application that combines AI-powered personalized content with deterministic pedagogical controls, enabling learners at any level to practice and improve their target language through realistic, context-rich interactions while maintaining system integrity, measurable progress, and complete auditability.

---

## MVP Must-Have Capabilities

### Onboarding and Identity
- User registration and authentication (email + social login)
- Target language selection
- Native/support language selection
- Basic onboarding questionnaire (goals, experience, interests)

### Learner Profile
- Multidimensional learner profile creation
- Skill dimension tracking (speaking, listening, reading, writing, grammar, vocabulary)
- Language preference management
- XP balance and progression display

### Diagnostic
- Multidimensional initial diagnostic (reading, writing, listening, grammar)
- Adaptive question selection based on learner responses
- Skill assessment with confidence scoring
- CEFR level estimation per dimension
- Diagnostic session persistence across interruptions

### Learning Entry Contract
- Personalized learning commitment based on diagnostic results
- Goal setting (target CEFR level, weekly practice target)
- Area-of-focus selection
- Learning plan preview

### Lesson Modes (5 required)
1. **Personal Narrative** — Learner describes a personal experience in target language
2. **Visual Single Scene** — Learner describes a single image scene
3. **Audio Narrative** — Learner listens to audio and retells the story
4. **Functional Communication** — Learner completes a practical communication task
5. **Writing Correction Cycle** — Learner writes, receives analysis, revises

### Submission and Analysis
- Text submission with input normalization
- Audio recording and upload
- Constrained AI analysis (structured output only)
- Writing correction with guided feedback
- Short quiz with automated scoring
- Performance-based task assessment

### Dialogue Simulation
- Structured dialogue with AI-powered conversation partner
- Scenario-driven interaction
- Turn-by-turn evaluation

### Mastery and Progress
- Mastery lifecycle per skill dimension
- Mastery evidence accumulation
- Deterministic mastery transitions
- Progress tracking across dimensions

### Spaced Repetition / Review Scheduling
- SRS-based review item creation from lesson errors and target items
- Due review calculation
- Review attempt scoring
- Adaptive scheduling based on performance

### Deterministic Rewards
- XP-based reward system
- XP ledger with complete transaction history
- Achievement badges for milestones
- Streak tracking with soft consequences and recovery
- Deterministic reward calculation (no AI involvement in reward decisions)

### Safety and Integrity
- Prompt injection defense (input sanitization, prompt isolation)
- Anti-cheat mechanisms (duplicate detection, timing analysis, pattern detection)
- Rate limiting per user and endpoint
- Audit trail for all state-changing operations

### System Capabilities
- Error recovery with grace degradation
- Idempotent API operations
- Basic analytics (lesson completion rates, retention, error patterns)
- Operator/admin read-only diagnostics

---

## MVP Out of Scope

The following are explicitly excluded from the MVP:

| Category | Exclusion |
|----------|-----------|
| Social | Full social network, friend connections, newsfeed |
| Marketplace | Teacher/tutor marketplace, tutor booking |
| Live Instruction | Live tutors, live classroom, real-time video lessons |
| Classroom | Classroom management, student groups, teacher dashboards |
| Multiplayer | Multiplayer games, competitive modes |
| Leaderboards | Public leaderboards (private/optional may be post-MVP) |
| Avatars | Advanced avatars, 3D characters, animated tutors |
| Media | Video generation, animated video lessons |
| AR/VR | Augmented reality, virtual reality features |
| Offline | Full offline model inference (basic offline browsing may be post-MVP) |
| AI Chat | Unrestricted AI chat, open-ended conversation |
| Curriculum | Autonomous AI-driven curriculum modification |
| Payments | Payments, subscriptions, in-app purchases (MVP is free/pre-funded) |
| Production | Production release, public app store listing |

---

## Success Criteria

The MVP is successful when:

1. **Completion**: A learner can complete the full journey from registration through lesson completion to mastery evidence and reward
2. **Lesson Modes**: At least 3 of the 5 lesson modes are functional end-to-end
3. **Diagnostic Accuracy**: Diagnostic assessment provides actionable skill profile within ±0.5 CEFR sub-level per dimension
4. **AI Safety**: No prompt injection bypasses reach the LLM, no AI output bypasses validation gates
5. **Deterministic Control**: All state transitions, mastery changes, and reward transactions are deterministic
6. **Audit**: Every state-changing operation is recorded in the audit trail
7. **Idempotency**: Duplicate submissions do not result in duplicate rewards or progress
8. **Recovery**: System recovers gracefully from provider timeouts, network failures, and invalid inputs

---

## Constraints and Assumptions

- **Mobile-first**: Primary client is iOS/Android via React Native; web PWA is secondary
- **Online required**: Active internet connection required for lessons; offline caching is post-MVP
- **AI provider assumed**: LLM provider assumed available; fallback strategy defined but graceful degradation preferred
- **User age 16+**: MVP assumes users are 16 or older; no child-specific data handling required
- **Single language pair**: MVP launches supporting one language pair; architecture supports extension
- **Free tier**: MVP operates without payment infrastructure; cost controls prevent runaway AI spend
