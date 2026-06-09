# Language Scaffolding Policy

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

The six-level scaffolding system that provides appropriate support for each skill and construction combination.

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

## Six scaffolding levels

| Level | Description | Example |
|-------|-------------|---------|
| native_formulation | Learner uses L1, system provides target form | L1: I'm hungry -> L2: J'ai faim |
| target_fragments | Learner completes fragments in L2 | I am ___ (hungry) |
| mixed_construction | Learner uses mixed L1/L2, system guides to full L2 | I am have hunger -> I am hungry |
| guided_target_output | Learner produces with prompts and cues | Tell me how you feel using I am + adjective |
| independent_target_output | Learner produces independently | Describe how you feel |
| interactive_target_use | Learner uses in dialogue without preparation | Respond naturally in conversation |

## Application rules

Scaffolding level is determined per (skill, construction) pair, not globally. Example:
- Learner A: Speaking/Past tense = guided_target_output, but Speaking/Present tense = independent_target_output
- Learner B: Writing/Formal register = mixed_construction, but Speaking/Formal register = native_formulation

## Fading rules

Scaffolding fades when:
1. Learner achieves 3 consecutive correct uses at current level
2. Learner self-corrects without prompting
3. Learner expresses confidence

Scaffolding increases when:
1. Learner makes 2 consecutive errors at current level
2. Learner expresses frustration
3. Task complexity increases (new topic, longer text, etc.)

## Scaffolding within a lesson

A single lesson may move through multiple levels:
- Start at one level below independent (ensuring success)
- Move to independent as soon as possible
- Return to support if errors appear
- End at highest achieved level
