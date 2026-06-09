# Adaptive Review Scheduler

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

The algorithm and service for scheduling optimal review times for each item.

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

## Scheduling algorithm

1. Each item has a current interval (time until next review)
2. After each review, interval is adjusted based on performance
3. Perfect recall: interval = current_interval * 2
4. Good recall: interval = current_interval * 1.5
5. Recall with hint: interval = current_interval * 1.2
6. Failed recall: interval = max(interval_before_fail / 2, 1 day)
7. Consecutive failure (3+): interval reset to 1 day, item flagged

## Daily review composition

Each review session selects items by priority:
1. Overdue items (past scheduled review time)
2. Items due today
3. Items due soon (within 2 days) — prefetch for upcoming busy days
4. Weak items (consecutive failures, low confidence)

## Session limits

Maximum review items per day:
- A1: 10 items
- A2: 15 items
- B1: 20 items
- B2: 25 items
- C1+: 30 items

Learner can request more or fewer. New items are introduced only after current review load permits.

## Priority scoring

Item priority = (days_overdue * 2) + (failure_count * 5) + (novelty_bonus if recent lesson)
