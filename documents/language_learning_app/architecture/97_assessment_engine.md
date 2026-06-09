# Assessment Engine

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Service that evaluates learner responses against criteria and generates evidence records.

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

The Assessment Engine evaluates learner performance across all task types, producing structured evidence for the learner model and mastery engine.

## Assessment types

1. **Formative** — In-lesson assessment, informs immediate feedback
2. **Quiz** — Controlled checkpoint, informs learner model
3. **Performance** — Task-based assessment, informs mastery
4. **Diagnostic** — Initial or periodic reassessment

## Evaluation pipeline

1. Receive learner response
2. Identify target criteria (from lesson contract or assessment spec)
3. Analyze response against criteria
4. Generate evidence record with confidence
5. Send evidence to Learner Model Service and Mastery Engine

## Scoring

- Binary (correct/incorrect) for objective items
- Rubric-based for production tasks
- Partial credit where appropriate
- Confidence score accompanies every assessment

## Anti-cheating measures

- Response time analysis (too fast = suspicious)
- Copy detection (identical responses across learners)
- Pattern analysis (unlikely perfect sequences)
- Session verification (same session as activity)
