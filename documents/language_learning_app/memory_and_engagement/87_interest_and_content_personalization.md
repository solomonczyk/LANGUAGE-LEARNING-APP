# Interest and Content Personalization

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

How the system captures, maintains, and uses knowledge of the learner's interests.

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

## Interest sources

1. **Explicit** — Learner states interests during onboarding and contract updates
2. **Behavioral** — Topics the learner engages with, stories they tell, time spent on content
3. **Inferred** — Related topics based on stated interests and demographics
4. **Imported** — Connected accounts (optional), calendar events, location data (with permission)

## Interest categories

- Hobbies and activities
- Professional domains
- Life situations (parent, student, commuter)
- Cultural interests (films, music, books)
- Travel destinations and experiences
- Current events and topics

## Content personalization

Interests influence:
- Topic selection for suggested situations
- Example sentences in grammar instruction
- Vocabulary selection
- Reading text topics
- Audio narrative themes
- Scenario contexts

## Interest decay and refresh

Interests naturally change over time. The system:
- Tracks engagement with interest areas (declining engagement = waning interest)
- Periodically asks: 'Are you still interested in X?'
- Suggests new topics: 'We noticed you've been talking about cooking a lot.'
- Removes stale interests after 3 months of no engagement

## Privacy control

Learners can view, edit, and delete interest data at any time. Interest data is not shared with third parties.
