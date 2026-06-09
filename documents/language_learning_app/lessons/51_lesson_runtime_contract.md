# Lesson Runtime Contract

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

The full lesson contract structure that governs every lesson session.

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

## Lesson contract fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| communicative_goal | string | The real-world purpose of the lesson | Yes |
| grammar_focus | list[LKB ID] | Grammar items addressed | Yes |
| vocabulary_focus | list[LKB ID] | Vocabulary/collocation items | Yes |
| narrative_focus | string | Discourse type (narrative, descriptive, argumentative) | Yes |
| receptive_skill_focus | string | Primary receptive skill | Yes |
| productive_skill_focus | string | Primary productive skill | Yes |
| interaction_focus | string | Interaction type (if any) | No |
| strategy_focus | string | Communication strategy addressed | No |
| scaffolding_mode | string | Initial scaffolding level | Yes |
| cognitive_budget | object | Time, items, complexity limits | Yes |
| assessment_criteria | object | Criteria for success | Yes |

## Contract lifecycle

1. **Proposal** — Curriculum Engine proposes a contract based on learner state
2. **Validation** — Contract validated against learner profile, curriculum, and policies
3. **Acceptance** — Contract accepted and lesson begins
4. **Execution** — Lesson is delivered with real-time adaptation
5. **Completion** — Results recorded, contract closed

## Cognitive budget structure

```json
{
  "max_duration_minutes": 15,
  "max_new_vocabulary": 5,
  "max_new_constructions": 1,
  "max_corrections": 3,
  "audio_max_seconds": 40,
  "interaction_turns": 6
}
```
