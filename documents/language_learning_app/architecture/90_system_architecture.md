# System Architecture

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Overall system architecture including services, communication patterns, and data flow.

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

## Architecture overview

The system follows a microservices architecture with clear service boundaries and a central API gateway.

## Services

### Core services
- **API Gateway** — Single entry point, authentication, routing
- **Curriculum Engine** — Manages progression, item selection, sequencing
- **Narrative Learning Engine (NLE)** — Personal narrative lessons
- **Visual Scenario Engine** — Image-based lesson generation
- **Audio Scenario Engine** — Audio-based lesson generation
- **Learner Model Service** — Per-dimension ability estimates
- **Assessment Engine** — Response evaluation and evidence generation
- **Mastery Engine** — Deterministic mastery state machine
- **Reward Engine** — Deterministic XP and reward calculation
- **Review Scheduler** — Spaced repetition scheduling

### Supporting services
- **AI Provider Abstraction** — Multi-LLM support with fallback
- **Linguistic Quality Assurance** — Schema + linguistic + pedagogical validation
- **Observability Service** — Logging, audit, cost tracking
- **Content Service** — LKB management, content delivery

## Communication

- Synchronous: REST/gRPC between services for request-response
- Asynchronous: Message queue for event-driven updates (lesson completion -> mastery update -> review scheduling)

## Data stores
- Learner profiles: Document DB
- LKB: Relational DB with versioning
- Session data: Cache (Redis)
- Audit log: Append-only log
- Event store: Message queue persistence

## System diagram

```
[Mobile App] <-> [API Gateway] <-> [Services] <-> [AI Provider]
                    |
              [Auth Service]
                    |
              [Event Bus] -> [Observability/Audit]
```
