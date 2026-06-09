# Review Scheduler Service

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Service managing spaced repetition scheduling for all item types.

## In scope

- Overall system architecture
- AI agent architecture and validation pipeline
- Narrative, Visual, Audio scenario engines
- Curriculum, Learner Model, Assessment, Mastery, Reward engines
- Review scheduler and LQA services
- Model provider fallback and observability

## Out of scope

- Implementation code
- Infrastructure configuration
- CI/CD pipeline
- Third-party service integrations

## Core decisions

1. LLM cannot directly change mastery, XP, curriculum, or LKB
2. Required pipeline: LLM -> schema validation -> linguistic validation -> pedagogical validation -> policy engine -> state transition -> audit
3. Deterministic engines hold state authority
4. All state changes are auditable

## Acceptance criteria

1. All 14 architecture documents exist
2. LLM boundaries are clearly defined
3. Pipeline specification is complete
4. Each engine has defined responsibilities and interfaces

---

## Overview

The Review Scheduler determines when each item should be reviewed, composes daily review sessions, and tracks review performance.

## Scheduling algorithm

For each item:
1. Maintain current_interval and ease_factor
2. After each review, update based on performance
3. Perfect: ease_factor += 0.1, interval = interval * ease_factor
4. Good: ease_factor unchanged, interval = interval * ease_factor
5. Hint: ease_factor -= 0.1, interval = interval * ease_factor * 0.5
6. Fail: ease_factor -= 0.2, interval = 1 day

## Daily session composition

1. Collect items where scheduled_date <= today
2. Sort by priority (overdue first, then due today, then weak items)
3. Apply daily limits (per CEFR level)
4. Ensure variety (mix of item types)
5. Limit repeated same-item-type in a session

## Performance tracking

- Per-item recall history
- Per-session statistics (items reviewed, success rate, time spent)
- Weekly/monthly trends
- Item-level and category-level reports
