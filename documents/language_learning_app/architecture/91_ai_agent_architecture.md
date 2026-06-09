# AI Agent Architecture

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Multi-agent AI architecture with clearly defined roles, boundaries, and communication.

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

## Agent roles

### Lesson Orchestrator Agent
Coordinates the overall lesson flow. Receives the lesson contract, delegates to specialized agents, manages time and scaffolding.

### Narrative Analyst Agent
Analyzes learner narratives for grammar, vocabulary, coherence, and pragmatics. Produces structured analysis.

### Content Generator Agent
Generates practice activities, examples, and explanations based on LKB items and learner profile.

### Feedback Agent
Provides corrective feedback according to the feedback policy. Selects feedback type based on error, learner, and context.

### Dialogue Manager Agent
Manages interactive dialogue turns, maintains context, selects appropriate responses.

## Agent communication

Agents communicate via structured messages with schema validation. No agent can directly mutate state — all outputs go through the validation pipeline.

## Agent boundaries

Each agent:
- Has a defined system prompt (version-controlled)
- Has access to specific context (learner profile, LKB items, lesson contract)
- Cannot access other learners' data
- Cannot perform state mutations
- Must produce structured output (JSON Schema validated)

## Pipeline for all agent outputs

```
Agent output -> Schema validation -> Linguistic validation -> Pedagogical validation -> Policy engine -> Deterministic state transition -> Audit log
```
