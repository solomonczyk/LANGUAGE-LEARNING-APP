# Streaks, Soft Consequences and Recovery

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Streak system design focused on motivation without punitive mechanics.

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

## Streak definition

A streak is the count of consecutive days where the learner completes at least one learning activity (lesson, review, quiz, or assessment). Minimum engagement: 3 minutes or 70% of a lesson.

## Freeze mechanisms

- Learners get 1 free streak freeze per week
- Freezes are automatically applied when a day is missed
- Unused freezes expire at end of week (use it or lose it)
- Additional freezes earnable through achievements

## Recovery paths

After a streak break:
- Day 1-3 missed: streak preserved with freeze, no notification
- Day 4-7 missed: streak resets but XP from streak milestones is kept
- Day 8+ missed: streak resets, milestones kept, recovery lesson offered

## No hard punishment

Streaks have only positive consequences:
- Streak milestones reward XP
- Long streaks unlock cosmetic achievements
- No content is locked behind streak length
- No punitive mechanics for breaking streaks

## Motivational design

- Streak count displayed prominently
- Streak milestones at 7, 14, 30, 60, 90, 180, 365 days
- Each milestone has unique achievement
- Streak recovery encouragement: 'You had a 14-day streak last month! Let's start a new one.'
- No shame or guilt messaging
