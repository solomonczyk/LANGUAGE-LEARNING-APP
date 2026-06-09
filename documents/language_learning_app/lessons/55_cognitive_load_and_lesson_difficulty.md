# Cognitive Load and Lesson Difficulty

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Management of cognitive load within lessons and across sessions, with per-CEFR load limits.

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

## Cognitive load types

### Intrinsic load
The inherent complexity of the language task. Managed by controlling task parameters: topic familiarity, text length, grammatical complexity, number of new items.

### Extraneous load
Unnecessary cognitive demands from poor instruction. Minimized by clear instructions, consistent UI, familiar task formats, and no split attention.

### Germane load
Cognitive resources devoted to learning. Maximized through meaningful tasks, personal relevance, and active processing.

## Per-CEFR load limits

### A0-A1
- Duration: 8-12 minutes
- New constructions: 1
- Active vocabulary: 3-5 words
- Collocations: 1-2
- Sentences produced: 2-4
- Audio: 10-20 seconds
- Dialogue turns: 2-4
- Major corrections: max 2

### A1-A2
- Duration: 12-18 minutes
- New constructions: 1-2
- Active vocabulary: 5-7 words
- Collocations: 2-3
- Sentences produced: 4-7
- Audio: 20-45 seconds
- Dialogue turns: 4-6
- Major corrections: max 3

### A2-B1
- Duration: 15-25 minutes
- New constructions: 1-2
- Active vocabulary: 6-9 words
- Collocations: 3-4
- Sentences produced: 7-12
- Audio: 45-90 seconds
- Dialogue turns: 6-10
- Short writing: included
- Major corrections: max 3

## Single-dimension increase rule

When increasing difficulty, only one dimension changes per lesson. Others remain at current level. Valid dimensions for increase: time, vocabulary count, grammatical complexity, audio length, interaction turns, number of corrections.

## Break scheduling

Recommended: 5-minute break after every 25 minutes of learning. System prompts break after intensive sessions. Learner can dismiss or accept.
