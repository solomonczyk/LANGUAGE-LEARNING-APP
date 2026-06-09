# Reward Engine

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Deterministic service that calculates and distributes all XP and rewards.

## In scope

- Overall system architecture
- AI agent architecture and validation pipeline
- Narrative, Visual, Audio scenario engines
- Curriculum, Learner Model, Assessment, Mastery, Reward engines
- Review scheduler and LQA services
- Model provider fallback and observability

## Out of scope

- Implementation code
- Infrastructure configuration
- CI/CD pipeline
- Third-party service integrations

## Core decisions

1. LLM cannot directly change mastery, XP, curriculum, or LKB
2. Required pipeline: LLM -> schema validation -> linguistic validation -> pedagogical validation -> policy engine -> state transition -> audit
3. Deterministic engines hold state authority
4. All state changes are auditable

## Acceptance criteria

1. All 14 architecture documents exist
2. LLM boundaries are clearly defined
3. Pipeline specification is complete
4. Each engine has defined responsibilities and interfaces

---

## Overview

The Reward Engine is the sole authority for all reward calculations. It is fully deterministic with no LLM involvement.

## Reward rules

Each reward type has a deterministic rule:

| Event | XP | Condition |
|-------|----|-----------|
| Lesson completion | base_xp(lesson_type, duration) | >= 70% engagement |
| Review recall | item_value_xp(item) * recall_modifier | Correct response |
| Quiz pass | quiz_pass_xp(count) * score_modifier | >= 60% score |
| Streak milestone | streak_xp(streak_length) | Milestone reached |
| Retention achievement | retention_xp(days) | Item retained at check |

## Transaction processing

1. Receive reward event with idempotency key
2. Check idempotency (already processed? -> return cached result)
3. Validate event against rules
4. Check rate limits
5. Calculate XP
6. Record transaction (atomic)
7. Return result

## Audit trail

All reward transactions are logged with:
- Transaction ID
- Learner ID
- Event type
- XP amount
- Timestamp
- Idempotency key
- Source service
- Previous balance and new balance
