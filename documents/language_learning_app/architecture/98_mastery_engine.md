# Mastery Engine

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Deterministic state machine managing mastery state transitions for all LKB items.

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

The Mastery Engine is a fully deterministic service that manages the mastery lifecycle of every LKB item for every learner. No LLM involvement.

## Mastery states

```
introduced -> recognized -> reconstructed -> guided_use -> independent_use -> interactive_use -> transferred -> retained
```

## State transitions

Each transition requires specific evidence:

| Transition | Required evidence |
|------------|------------------|
| -> introduced | Item presented in a lesson |
| -> recognized | Correct recognition in quiz (1+ evidence) |
| -> reconstructed | Correct production with scaffolding (2+ evidence) |
| -> guided_use | Correct production with prompts (3+ evidence) |
| -> independent_use | Correct production without support (3+ evidence across contexts) |
| -> interactive_use | Correct use in dialogue/ interaction (2+ evidence) |
| -> transferred | Correct use in new context (2+ evidence) |
| -> retained | Successful recall after 7+ day delay (1+ evidence) |

## Retention requirement

The retained state can ONLY be achieved after a delayed review (minimum 7 days after last practice). This ensures retained represents true long-term knowledge, not short-term recall.

## Regressions

If a learner consistently fails at a higher mastery state, they regress to the previous state. Evidence of failure must be: 3 consecutive failures at current state, or 5 failures within 10 attempts.
