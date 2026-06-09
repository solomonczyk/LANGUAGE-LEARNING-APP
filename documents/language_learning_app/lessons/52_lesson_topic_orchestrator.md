# Lesson Topic Orchestrator

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

How topics are selected for each lesson, balancing learner interest, curriculum requirements, and variety.

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

## Topic selection factors

1. **Learner interest** (weight: high) — Topics the learner has expressed interest in or engaged with previously
2. **Curriculum requirements** (weight: high) — Topics needed for comprehensive coverage
3. **Weak dimension support** (weight: medium) — Topics that provide practice in weak areas
4. **Variety** (weight: medium) — Avoid repeating the same topic type
5. **Seasonal/timely** (weight: low) — Current events, seasons, holidays
6. **Spiral review** (weight: medium) — Topics from earlier levels at higher complexity

## Topic bank

Topics are organized by domain:
- Self and identity — Personal background, personality, values, life story
- Daily life — Routines, home, food, health, transport
- Work and study — Jobs, careers, education, business
- Society and culture — Current events, traditions, arts, media
- Relationships — Family, friends, romance, community
- Abstract ideas — Opinions, arguments, hypotheticals

## Topic recycling

Topics are recycled at higher CEFR levels with increasing complexity:
- A1: Concrete, here-and-now, personal
- A2: Simple narratives, basic descriptions
- B1: Detailed accounts, opinions, plans
- B2: Abstract topics, arguments, complex narratives
- C1+: Nuanced discussion, cultural analysis, professional discourse
