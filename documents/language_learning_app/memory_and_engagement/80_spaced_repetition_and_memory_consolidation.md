# Spaced Repetition and Memory Consolidation

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

The spaced repetition system for long-term retention of all item types.

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

## Items reviewed

The SRS covers: vocabulary items, collocations, grammatical constructions, dialogue fragments, persistent error patterns, learner's own story segments, and communicative functions.

## Starting interval chain

1. Within lesson (immediate review)
2. 2 hours
3. 12 hours
4. 2 days
5. 7 days
6. 21-30 days
7. 60-90 days

## Adaptive intervals

Intervals adapt based on recall success:
- Perfect recall: interval doubles
- Recall with hint: interval increases by 50%
- Failed recall: interval resets to last successful interval (not to zero)
- Persistent failure: item moved to intensive review track

## Review task types by item type

| Item type | Review task |
|-----------|------------|
| Vocabulary | Recognition -> recall -> use in sentence |
| Collocation | Complete the collocation -> use in context |
| Construction | Complete the pattern -> produce independently |
| Dialogue fragment | Complete the line -> respond appropriately |
| Error pattern | Identify error -> correct it |
| Story segment | Continue the story -> retell |
| Communicative function | Identify situation -> produce appropriate response |
