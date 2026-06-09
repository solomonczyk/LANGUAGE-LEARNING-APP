# Narrative Learning Engine

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

The service responsible for managing personal narrative lessons from elicitation through transfer.

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

The NLE manages the complete lifecycle of personal narrative lessons. It orchestrates elicitation, analysis, activity generation, and transfer.

## Components

### Narrative Elicitor
Prompts the learner to share stories. Uses topic, emotion, and time-based prompts. Manages the elicitation dialogue flow.

### Narrative Analyzer
Processes learner narratives to extract linguistic features:
- Grammatical patterns (tense, aspect, modality)
- Vocabulary range and appropriateness
- Narrative coherence (sequence markers, reference)
- Pragmatic features (register, speech acts)
- Error patterns

### Activity Generator
Creates practice activities based on analysis results:
- Targets identified weak areas
- Uses learner's own content for personalization
- Selects appropriate scaffolding level
- Generates varied task formats

### Transfer Builder
Creates transfer tasks that apply new language to different but related contexts.

## Data flow

1. Learner shares story (text/speech)
2. NLE analyzes narrative
3. Activity Generator creates practice activities
4. Learner completes activities
5. NLE updates learner model and mastery state
