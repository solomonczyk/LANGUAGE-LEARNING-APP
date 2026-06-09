# Lesson Completion and Mastery Policy

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Criteria for lesson completion, partial completion rules, and how lesson performance affects mastery.

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

## Lesson completion criteria

A lesson is considered complete when:
1. The communicative goal has been attempted
2. Minimum engagement threshold met (70% of cognitive budget)
3. At least one practice activity completed for each focus item
4. Quiz completed (for non-assessment lessons)

## Partial completion

Learners may exit a lesson before full completion:
- Partial progress is saved
- System notes which stages were completed
- Partial completion gives partial credit (proportional XP)
- Option to resume from where left off (within 24 hours)

## Mastery update on completion

Lesson performance triggers mastery state changes:
- Quiz score >80% on focus items: evidence for independent_use
- Quiz score 60-80%: evidence for guided_use
- Quiz score <60%: no advancement, flagged for review
- In-lesson production success: per-item evidence recorded

## Minimum engagement threshold

If learner exits before minimum engagement (70% of cognitive budget or less than 50% of activities):
- Lesson marked as abandoned
- No mastery updates
- No XP awarded
- Abandonment noted in learner model (for pattern detection)

## Mastery delay

Even after successful lesson completion, retained status requires delayed verification (minimum 7 days, via spaced repetition).
