# Memory Review Reward Economy

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Deterministic reward system for spaced repetition and review activities.

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

## Rewarded actions

| Action | XP | Rate limit |
|--------|----|------------|
| Completed review session | 10 XP | Once per session |
| Recall without hint | 5 XP per item | Per item per review |
| Recall with hint | 3 XP per item | Per item per review |
| Use in sentence | 8 XP | Per item per review |
| Dialogue use | 10 XP | Per item per review |
| Transfer task | 15 XP | Per task |
| 7-day retention | 25 XP bonus | Once per item |
| 30-day retention | 100 XP bonus | Once per item |
| 90-day retention | 500 XP bonus | Once per item |

## Deterministic rule

LLM NEVER awards XP or any reward. All reward calculations are performed by the Reward Engine based on verifiable events.

## Transaction integrity

- Each reward is an atomic transaction with idempotency key
- Duplicate events (same idempotency key) are silently ignored
- Failed transactions roll back completely
- All transactions are logged in the audit trail

## Anti-farming

- Per-action rate limits enforced
- Suspicious patterns (same action too quickly, unlikely consistency) flagged
- Review rewards require actual engagement duration (min 3s per item)
- Transfer rewards require novel production (detected via similarity checking)
