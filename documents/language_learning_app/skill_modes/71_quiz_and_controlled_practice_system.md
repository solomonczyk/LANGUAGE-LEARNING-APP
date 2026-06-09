# Quiz and Controlled Practice System

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Short, frequent checkpoints (4-7 items, 2-4 min) that provide immediate feedback without serving as mastery assessment.

## In scope

- Personal narrative lesson system
- Suggested situation lesson system
- Visual narrative and emotion/perspective systems
- Audio narrative and listening comprehension
- Reading, writing, and spoken dialogue systems
- Quiz and controlled practice system

## Out of scope

- Implementation code
- UI specifications
- Third-party integration details
- Production deployment configuration

## Core decisions

1. Each skill mode has a defined pedagogical purpose
2. Writing follows scaffolded self-correction cycle
3. Visual scenes accept multiple emotional interpretations
4. Quiz is a checkpoint, not mastery assessment

## Acceptance criteria

1. All 13 skill mode documents exist with substantive content
2. Writing cycle is specified (draft through transfer)
3. Visual narrative includes all required task types
4. Quiz specifications include length and item types

---

## Purpose

Quizzes are short controlled-practice checkpoints that:
- Provide immediate feedback to the learner
- Inform the learner model
- Identify areas needing more practice
- Do NOT change mastery state alone

## Quiz design

| Aspect | Specification |
|--------|--------------|
| Length | 4-7 items |
| Duration | 2-4 minutes |
| Frequency | At end of every lesson (except assessment lessons) |
| Difficulty | Matched to lesson content |
| Item types | Multiple choice, gap-fill, matching, ordering, short answer |

## Item types

- **Multiple choice** — Recognition (grammar, vocabulary)
- **Gap-fill** — Production within context
- **Matching** — Connections (word-definition, collocation)
- **Ordering** — Sequence (narrative, dialogue)
- **Short answer** — Controlled production

## Scoring

- Binary (correct/incorrect) for objective items
- Partial credit possible for production items
- Score recorded as percentage
- Score > 80% signals readiness for next level
- Score < 60% triggers review

## Quiz vs mastery

| Feature | Quiz | Mastery assessment |
|---------|------|-------------------|
| Length | 4-7 items | Multiple evidence points |
| Context | Single lesson | Multiple contexts |
| Delayed testing | No | Yes (7+ day delay) |
| State change | Evidence only | State transition |
| Purpose | Immediate feedback | Long-term verification |
