# Lesson Type Taxonomy

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Classification of the 14 lesson modes with definitions, primary skill focus, typical duration, and scaffolding pattern.

## In scope

- Lesson type taxonomy (14 modes)
- Runtime contract structure
- Topic orchestration and format selection
- Scaffolding, cognitive load, and feedback policies
- Completion and mastery criteria

## Out of scope

- Specific lesson content
- UI/UX implementation
- Teacher-facing tools
- Real-time execution logic

## Core decisions

1. Communicative goal drives every lesson
2. Scaffolding is per-skill and per-construction
3. Cognitive load increases one dimension at a time
4. Feedback is selective and prioritized

## Acceptance criteria

1. All 14 lesson modes are defined with purpose and structure
2. Lesson contract has all required fields
3. Scaffolding policy covers 6 levels with fading rules
4. Cognitive load limits are specified per CEFR level

---

## The 14 lesson modes

| # | Mode | Primary skill focus | Typical duration | Scaffolding pattern |
|---|------|-------------------|------------------|-------------------|
| 1 | personal_narrative | Integrated (speaking/writing) | 12-25 min | Full cycle |
| 2 | suggested_situation | Functional communication | 10-20 min | Guided -> independent |
| 3 | visual_single_scene | Description, vocabulary | 8-15 min | Fragments -> output |
| 4 | visual_sequence | Narrative, coherence | 12-20 min | Guided -> independent |
| 5 | illustrated_emotion_and_perspective | Pragmatics, inferencing | 10-18 min | Mixed -> output |
| 6 | audio_narrative | Listening, retelling | 10-25 min | Comprehension -> production |
| 7 | audio_dialogue | Listening, interaction | 12-20 min | Gist -> detail -> role-play |
| 8 | reading_based | Reading, vocabulary | 15-25 min | Pre -> during -> post |
| 9 | functional_communication | Pragmatics, speaking | 10-15 min | Model -> practice -> transfer |
| 10 | repair_lesson | Targeted grammar/vocab | 8-12 min | Error -> focus -> practice |
| 11 | mediation_lesson | Information transfer | 12-20 min | Reception -> mediation |
| 12 | review_lesson | Spaced repetition | 5-15 min | Retrieval -> application |
| 13 | progress_checkpoint | Assessment | 10-15 min | Independent performance |
| 14 | assessment_lesson | Comprehensive eval | 20-30 min | Independent with rubric |

## Mode selection factors

- Learner's weak dimensions (prioritized)
- Energy/time of day
- Recent lesson history (avoid repetition)
- Curriculum requirements
- Learner preference

## Mode combination rules

A single session may combine multiple modes:
- Primary mode + quiz (always, except assessment lessons)
- Review lesson precedes new content
- Repair lesson follows error pattern detection
