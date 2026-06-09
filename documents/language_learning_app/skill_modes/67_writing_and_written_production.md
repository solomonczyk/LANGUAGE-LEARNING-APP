# Writing and Written Production

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

The scaffolded writing cycle that develops written production skills without premature AI correction.

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

## The writing cycle

1. **Draft** — Learner writes freely without interruption
2. **Problem identification** — AI identifies specific problems (not all errors)
3. **Hint** — Targeted hint for each identified problem
4. **Self-correction** — Learner attempts to fix the problem
5. **Recheck** — AI checks the correction
6. **Natural model** — AI provides a natural version (after learner's attempt)
7. **Transfer** — Learner applies learning to a new writing task

## Key principle

AI does NOT immediately rewrite the learner's text. The learner must attempt self-correction first. Full model is only provided after the learner has tried.

## Text types by level

| Level | Text types |
|-------|-----------|
| A1 | Single sentences, short descriptions |
| A2 | Short paragraphs, simple narratives |
| B1 | Connected paragraphs, emails, stories |
| B2 | Structured texts, arguments, reports |
| C1+ | Extended essays, professional documents, creative writing |

## Assessment dimensions

- Content (relevance, completeness)
- Organization (coherence, cohesion)
- Vocabulary (range, appropriateness)
- Grammar (accuracy, complexity)
- Mechanics (spelling, punctuation)
