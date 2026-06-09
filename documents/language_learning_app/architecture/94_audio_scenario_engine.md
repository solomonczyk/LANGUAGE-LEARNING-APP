# Audio Scenario Engine

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Service for processing audio content and generating listening comprehension activities.

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

The Audio Scenario Engine processes audio narratives and dialogues for listening comprehension, retelling, and language production activities.

## Input processing

- Audio format: MP3, WAV, M4A
- Duration limits enforced by CEFR level
- Speech-to-text transcription (for analysis)
- Speaker diarization (for multi-speaker audio)

## Audio analysis pipeline

1. Transcription (ASR)
2. Duration verification (level-appropriate?)
3. Complexity analysis (vocabulary, grammar, speed)
4. Content segmentation (scenes, topics)
5. Question generation (gist, detail, inference)

## Activity generation

- Gist comprehension questions
- Detail comprehension questions
- Inference questions
- Vocabulary from audio
- Retelling prompts
- Dialogue role-play extension

## Duration compliance

Audio duration is checked against per-CEFR limits:
- A0-A1: 5-15 seconds
- A1-A2: 15-40 seconds
- A2-B1: 40-90 seconds
- B1-B2: 1-3 minutes
- B2+: 3-5 minutes
