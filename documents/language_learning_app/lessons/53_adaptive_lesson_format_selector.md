# Adaptive Lesson Format Selector

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Algorithm for selecting the optimal lesson mode based on learner state and context.

## In scope

- Lesson type taxonomy (14 modes)
- Runtime contract structure
- Topic orchestration and format selection
- Scaffolding, cognitive load, and feedback policies
- Completion and mastery criteria

## Out of scope

- Specific lesson content
- UI/UX implementation
- Teacher-facing tools
- Real-time execution logic

## Core decisions

1. Communicative goal drives every lesson
2. Scaffolding is per-skill and per-construction
3. Cognitive load increases one dimension at a time
4. Feedback is selective and prioritized

## Acceptance criteria

1. All 14 lesson modes are defined with purpose and structure
2. Lesson contract has all required fields
3. Scaffolding policy covers 6 levels with fading rules
4. Cognitive load limits are specified per CEFR level

---

## Selection factors

### Learner state
- **Energy level** — High energy: dialogue, role-play. Low energy: reading, listening.
- **Time available** — Short (5-10 min): review, quiz. Medium (10-20 min): single mode. Long (20-30 min): multi-mode.
- **Recent performance** — Poor performance: repair lesson, more scaffolding. Good performance: challenge mode.
- **Weak dimensions** — Prioritize modes that target weak areas.

### Context
- **Time of day** — Morning: production-heavy. Evening: receptive-heavy.
- **Day of week** — Weekdays: shorter sessions. Weekends: longer sessions.
- **Streak status** — At risk: easy win lesson. Active: normal selection.

### Curriculum
- **Required items** — Items due for introduction or review
- **Spiral schedule** — Topics due for re-engagement
- **Checkpoint due** — Progress checkpoint if interval elapsed

## Selection algorithm

1. Filter available modes by curriculum requirements
2. Score each mode by learner state fit
3. Apply variety penalty (reduce score of recently used modes)
4. Select highest-scoring mode
5. If multiple modes score equally, prefer learner-preferred mode
