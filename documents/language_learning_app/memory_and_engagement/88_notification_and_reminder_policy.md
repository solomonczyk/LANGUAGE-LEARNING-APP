# Notification and Reminder Policy

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

When and how to notify learners, with frequency caps, content guidelines, and opt-out controls.

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

## Notification types

| Type | Trigger | Frequency cap |
|------|---------|---------------|
| Review reminder | Items due for review | 1x per day |
| Lesson suggestion | No activity for 24h | 1x per day |
| Streak at risk | No activity by evening | 1x per day |
| Achievement unlocked | Event occurs | Per achievement |
| Progress report | Weekly | 1x per week |
| New content available | Content update | 1x per week |

## Content guidelines

- Action-oriented: 'You have 3 items to review.'
- Personal: 'Yesterday you talked about your trip. Ready to continue?'
- Encouraging: 'You're on a 7-day streak! Keep going.'
- Informative: 'You've learned 50 new words this week.'
- NOT manipulative: no false urgency, no shame, no guilt.

## Opt-out and quiet hours

- Learners can disable notification types individually
- Quiet hours: learner-set time when no notifications are sent
- Default quiet hours: 22:00 - 08:00
- No notifications during consecutive learner inactivity (paused learning)

## Behavioral design

- Notifications are sent at the learner's preferred time (from learning entry contract)
- Content varies to avoid habituation
- A/B testing on notification copy and timing
- Learners can request more/less frequent notifications
- No notification spam — max 3 per day regardless of triggers
