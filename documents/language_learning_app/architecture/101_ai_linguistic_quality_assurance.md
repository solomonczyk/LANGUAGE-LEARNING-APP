# AI Linguistic Quality Assurance

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Validation pipeline for all LLM outputs to ensure quality, accuracy, and safety.

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

## Pipeline stages

1. **Schema validation** — Output matches expected JSON Schema
2. **Linguistic validation** — Language is accurate (grammar, vocabulary, naturalness)
3. **Pedagogical validation** — Content is level-appropriate, scaffolding is correct
4. **Policy validation** — No rule violations (no XP awards, no state changes)
5. **Safety validation** — No harmful, offensive, or inappropriate content

## What is validated

- Lesson content (explanations, examples, activities)
- Feedback messages
- Quiz items
- Assessment responses
- Dialogue responses
- Narrative analysis

## Quality metrics

- Linguistic accuracy: <1% error rate target
- Pedagogical appropriateness: >95% appropriate for target level
- Schema compliance: 100% required
- Safety: 100% no harmful content
- Engagement: >80% learner satisfaction (from feedback)

## Rejection and retry

If validation fails:
- Schema error: Reject, log, retry up to 2 times with clearer schema
- Linguistic error: Reject, log, flag for human review (sampling)
- Pedagogical error: Reject, log, adjust context, retry once
- Safety error: Reject, log, escalate immediately
- After max retries: Fall back to template content, flag for review
