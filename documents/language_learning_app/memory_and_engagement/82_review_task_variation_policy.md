# Review Task Variation Policy

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Ensuring review tasks remain engaging through variation by item type and format.

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

## Why variation matters

Repeated exposure to the same item in the same format leads to:
- Format familiarity rather than true recall
- Boredom and reduced engagement
- Overconfidence (recognizing the format, not the content)

## Task rotation

Each item type has 3-5 possible task formats. The system rotates through them:

### Vocabulary
1. Multiple choice (L2 definition -> L2 word)
2. Gap-fill in sentence
3. Translation (L1 -> L2)
4. Write a sentence using the word
5. Choose the correct collocation

### Grammar constructions
1. Complete the sentence
2. Error identification and correction
3. Transformation (change tense, negate, etc.)
4. Combine sentences using the construction
5. Produce original sentence

## Difficulty layering

Review tasks can be layered by difficulty:
- Easy (recognition): 70% confidence needed
- Medium (cued production): 50% confidence needed
- Hard (free production): 30% confidence needed

The system increases difficulty layer after successful recall at current layer.
