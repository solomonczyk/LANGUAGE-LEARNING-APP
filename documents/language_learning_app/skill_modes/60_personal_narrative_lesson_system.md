# Personal Narrative Lesson System

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

The core lesson mode where learners tell their own stories as the basis for language learning.

## In scope

- Personal narrative lesson system
- Suggested situation lesson system
- Visual narrative and emotion/perspective systems
- Audio narrative and listening comprehension
- Reading, writing, and spoken dialogue systems
- Quiz and controlled practice system

## Out of scope

- Implementation code
- UI specifications
- Third-party integration details
- Production deployment configuration

## Core decisions

1. Each skill mode has a defined pedagogical purpose
2. Writing follows scaffolded self-correction cycle
3. Visual scenes accept multiple emotional interpretations
4. Quiz is a checkpoint, not mastery assessment

## Acceptance criteria

1. All 13 skill mode documents exist with substantive content
2. Writing cycle is specified (draft through transfer)
3. Visual narrative includes all required task types
4. Quiz specifications include length and item types

---

## Overview

Personal narrative is the flagship lesson mode. The learner shares a real story from their life, and the system builds a complete lesson around it.

## Lesson flow

1. **Elicitation** — System prompts the learner to share a story (guided by topic, emotion, time frame)
2. **Narrative** — Learner tells/writes their story
3. **Analysis** — System analyzes language: grammar, vocabulary, coherence, pragmatics
4. **Focus on form** — Key items extracted from the narrative for practice
5. **Practice activities** — Scaffolded activities using the learner's own content
6. **Retelling** — Learner retells the same story with improvements
7. **Dialogue extension** — System asks follow-up questions as a dialogue partner
8. **Transfer** — Learner applies new language to a similar but different story

## Elicitation techniques

- Open prompt: 'Tell me about something that happened this week'
- Guided prompt: 'Describe a time you felt frustrated'
- Image stimulus: 'This image reminds me of... what about you?'
- Emotion prompt: 'When did you last feel proud?'

## Analysis dimensions

- Grammatical accuracy and range
- Lexical richness
- Narrative coherence (temporal sequence, reference maintenance)
- Pragmatic appropriateness
- Fluency indicators
