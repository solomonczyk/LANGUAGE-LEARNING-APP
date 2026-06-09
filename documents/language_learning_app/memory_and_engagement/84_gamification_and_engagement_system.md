# Gamification and Engagement System

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Meaningful gamification that supports learning goals without resorting to manipulative engagement tactics.

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

## Gamification philosophy

Game elements serve learning goals. They motivate through: competence (mastery feedback), autonomy (meaningful choices), and relatedness (social connection where appropriate).

## Game elements

### Points (XP)
Awarded for completed lessons, correct reviews, streak milestones, and retention achievements. XP reflects learning progress, not time spent.

### Levels
Learner levels based on cumulative XP. Each level unlocks cosmetic rewards (themes, badges). No content gated behind levels — all learning content is accessible based on ability alone.

### Achievements
Specific accomplishments: first story, 7-day streak, 10 perfect quizzes, first transfer task, 30-day retention of first item, first repair lesson completion.

### Streaks
Consecutive days of learning activity. Streaks have soft consequences (see streaks document).

### Leaderboards
Optional, privacy-preserving (pseudonyms only). Compare by XP, streak, or skill area progress. Default opt-out with learner opt-in.

## What is NOT gamified

- Content unlocking (based on ability, not gamification)
- Lesson selection (based on need, not points)
- Feedback quality (based on pedagogical criteria, not engagement)

## Engagement metrics vs learning metrics

The system tracks both but prioritizes learning:
- Engagement: DAU, session length, retention
- Learning: mastery progression, quiz scores, CEFR level advancement

Gamification is adjusted if engagement metrics improve but learning metrics do not.
