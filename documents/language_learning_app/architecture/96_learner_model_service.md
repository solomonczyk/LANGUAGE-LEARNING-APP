# Learner Model Service

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Service that stores, serves, and updates learner profiles across all dimensions.

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

The Learner Model Service maintains the system's representation of each learner's language abilities, preferences, and history.

## API

- GET /learner/{id}/profile — Full profile
- GET /learner/{id}/profile/{dimension} — Single dimension
- POST /learner/{id}/evidence — Add evidence
- POST /learner/{id}/recalibrate — Trigger recalibration
- GET /learner/{id}/history — Learning history

## Profile structure

- Identity: ID, language pair, L1, other languages
- Abilities: Per-dimension CEFR estimates with confidence
- Preferences: Learning style, mode preference, time preference
- Interests: Topic areas with engagement levels
- History: Lessons completed, items learned, error patterns
- State: Current scaffolding levels per (skill, construction)
- Schedule: Current SRS state for all items

## Evidence model

Evidence entries: timestamp, dimension, observation type, value, confidence_weight. Evidence is additive — old evidence is not deleted but may be deprecated by newer, higher-weight evidence.
