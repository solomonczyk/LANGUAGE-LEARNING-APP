# Audiovisual Comprehension System

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Comprehension skills development using combined audio and visual channels (video).

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

Audiovisual comprehension combines auditory and visual channels, providing richer context and more authentic input than audio alone.

## Video types

- Short clips — 15-60 seconds, single scene
- Scene from media — 1-3 minutes, multiple characters
- Interview — 2-5 minutes, natural speech
- Documentary excerpt — 3-8 minutes, narration + footage
- Instructional video — 1-5 minutes, step-by-step

## Comprehension levels

| Level | Focus | Task |
|-------|-------|------|
| Global | Main idea, setting, characters | Summary, multiple choice |
| Selective | Specific information | Details, fill-in |
| Detailed | Full understanding | Retelling, Q&A |
| Inferential | Implied meaning, subtext | Inference questions |
| Evaluative | Opinion, judgment | Critical response |

## Visual support

Visual cues in video support comprehension:
- Facial expressions aid emotional understanding
- Body language adds meaning to speech
- Visual context clarifies unfamiliar vocabulary
- On-screen text (when available) reinforces reading
