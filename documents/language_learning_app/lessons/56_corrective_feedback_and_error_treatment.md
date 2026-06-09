# Corrective Feedback and Error Treatment

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Types of corrective feedback, when to use each, and how errors are selected for treatment.

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

## Feedback types

| Type | Description | Best for | Example |
|------|-------------|----------|---------|
| Explicit correction | Direct error indication with correct form | Persistent errors, teachable moments | 'You should say: I went, not I goed' |
| Recast | Rephrase error in correct form without flagging | Slips, fluency-focused tasks | 'Yesterday I go to store' -> 'Ah, yesterday you went to the store' |
| Clarification request | Indicate non-understanding | Communication breakdowns | 'Sorry, could you repeat that?' |
| Metalinguistic clue | Provide grammatical hint | Self-correction capable learners | 'What tense should you use for yesterday?' |
| Elicitation | Prompt to self-correct | Ready-for-self-correction | 'How do we say that in past tense?' |
| Repetition | Repeat error with questioning intonation | Noticing errors | 'I goed to the store?' |

## Error selection for treatment

Not all errors are treated. Selection criteria:
1. **Global vs local** — Global errors (affecting meaning) treated first
2. **Persistent vs sporadic** — Persistent errors need treatment; sporadic slips may be ignored
3. **Teachable moment** — Is the learner ready for this specific correction?
4. **Cognitive load** — Don't overload with too many corrections per session
5. **Focus of lesson** — Prioritize errors related to the lesson's communicative goal

## Feedback within the lesson

1. During free production: minimal interruption (note errors)
2. During practice phase: targeted correction on focus items
3. After task: summary of key errors with explanation
4. In repair lessons: systematic treatment of identified error patterns

## Error tracking

All treated errors are recorded in the error evidence model for SRS scheduling and future repair lessons.
