# Visual Scenario Engine

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Service for processing images and generating language learning activities from visual content.

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

The Visual Scenario Engine processes images to create descriptive, narrative, emotional, and interactive language tasks.

## Input processing

- Image format: JPEG, PNG, WebP
- Size limit: 10 MB per image
- Sequence: up to 6 images per lesson
- OCR: Text within images extracted for vocabulary tasks

## Scene analysis pipeline

1. Image classification (indoor/outdoor, people/scene/object)
2. Object and person detection
3. Scene description generation
4. Emotion/expression recognition (for people)
5. Action/interaction identification
6. Story generation (for sequences)

## Activity generation

Based on analysis, engine generates:
- Description tasks (what do you see?)
- Narrative tasks (tell the story)
- Emotion interpretation tasks (how do they feel?)
- Prediction tasks (what happens next?)
- Perspective tasks (how does each person see it?)

## No forced interpretation

For emotion/perspective tasks, multiple interpretations are accepted. The engine checks for justification quality, not correctness of emotional reading.
