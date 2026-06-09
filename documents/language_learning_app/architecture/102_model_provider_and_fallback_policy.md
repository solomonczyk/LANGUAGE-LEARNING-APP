# Model Provider and Fallback Policy

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Strategy for supporting multiple LLM providers with graceful degradation.

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

## Provider support

The system supports multiple LLM providers for redundancy, cost optimization, and capability matching.

## Provider tiers

| Tier | Provider | Use case | Cost |
|------|----------|----------|------|
| Primary | High-quality | Lesson generation, analysis | Higher |
| Secondary | Mid-quality | Quiz generation, simple feedback | Medium |
| Fallback | Any available | When primary unavailable | Varies |
| Local/Template | No LLM | Graceful degradation | Zero |

## Model capability registry

Each task type has minimum capability requirements:
- Narrative analysis: High linguistic understanding
- Content generation: Creative, level-appropriate output
- Feedback: Pedogogically appropriate responses
- Dialogue: Natural conversation maintenance
- Simple tasks: Basic language processing

## Fallback chain

For each request:
1. Try primary provider
2. If unavailable or error -> try secondary
3. If unavailable or error -> try fallback
4. If all providers fail -> use template content
5. Log all failures and escalations

## Cost optimization

- Simple tasks routed to cheaper models
- Complex tasks routed to capable models
- Token usage tracked per task, per provider
- Monthly provider cost analysis
- Automatic rebalancing based on cost/quality data
