# Adaptive Learning Load

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Managing the total learning burden across lessons and review to prevent burnout.

## In scope

- Spaced repetition system design
- Adaptive review scheduling
- Review task variation policy
- Adaptive learning load specifications
- Gamification and engagement system
- Reward economy and streaks
- Content personalization and notifications

## Out of scope

- Implementation of SRS algorithm
- UI for review sessions
- Push notification infrastructure
- Leaderboard implementation

## Core decisions

1. SRS covers vocabulary, collocations, constructions, errors, stories, functions
2. Reward engine is fully deterministic, no LLM involvement
3. Learning load increases one dimension at a time
4. Streaks have recovery paths, not hard punishment

## Acceptance criteria

1. SRS interval chain is specified
2. Review task types match item types
3. Reward catalog is complete with deterministic rules
4. Notification policy includes frequency caps and opt-out

---

## Per-CEFR load limits

### A0-A1
- Daily lesson time: max 15 min
- Daily review time: max 5 min
- New words per day: max 5
- New constructions per day: max 1

### A1-A2
- Daily lesson time: max 20 min
- Daily review time: max 10 min
- New words per day: max 7
- New constructions per day: max 2

### A2-B1
- Daily lesson time: max 30 min
- Daily review time: max 15 min
- New words per day: max 9
- New constructions per day: max 2

### B1-B2
- Daily lesson time: max 40 min
- Daily review time: max 20 min
- New words per day: max 12
- New constructions per day: max 3

## Single-dimension increase rule

When the system determines the learner can handle more load, it increases only one dimension at a time. This prevents cognitive overload from simultaneous increases.

## Load monitoring

The system tracks:
- Actual vs planned load
- Learner completion rate
- Signs of fatigue (increased errors, longer response times)
- Learner-reported energy (optional)

## Adjustment triggers

Load is decreased when:
- Learner fails to complete 3 consecutive lessons
- Error rate increases sharply (50%+ above baseline)
- Learner requests lighter load
- Break in learning (3+ days inactive)

Load is increased when:
- Learner completes all lessons with >80% success for 5 consecutive sessions
- Learner requests more challenge
- Confidence on current items is high
