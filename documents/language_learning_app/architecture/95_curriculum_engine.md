# Curriculum Engine

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Service managing curriculum progression, item sequencing, and adaptive content selection.

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

The Curriculum Engine determines what the learner should study next based on their profile, history, and curriculum requirements.

## Responsibilities

1. **Item selection** — Choose next items for introduction based on prerequisites and learner readiness
2. **Sequencing** — Order items for optimal learning (spiral, blocked, interleaved)
3. **Adaptation** — Adjust sequence based on learner performance
4. **Coverage tracking** — Ensure all required items are eventually covered
5. **Prerequisite management** — Enforce prerequisite completion

## Selection algorithm

Item priority score = (curriculum_requirement * 0.3) + (weakness_weight * 0.3) + (interest_weight * 0.2) + (review_need * 0.1) + (variety_bonus * 0.1)

## Curriculum structure

The curriculum is organized as a directed acyclic graph (DAG) where:
- Nodes are LKB items
- Edges are prerequisite relationships
- Paths represent learning sequences
- Multiple paths exist for different learner profiles
