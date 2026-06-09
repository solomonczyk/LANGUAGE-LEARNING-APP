# Product Principles and Non-Goals — Language Learning App

**Status:** Approved  
**Version:** 1.0.0  
**Last updated:** 2026-06-09

---

## Purpose

This document defines the core product principles that guide all design and development decisions, plus explicit non-goals to prevent scope creep and maintain product focus.

## In scope

- Defining the 7 core product principles
- Establishing non-goals to maintain focus
- Providing guidance for trade-off decisions
- Setting team-wide design philosophy

## Out of scope

- Implementation-specific rules
- UI design guidelines
- Monetization strategy details
- Marketing positioning

## Core decisions

1. Principles rank above features — a feature that violates a principle will not be built
2. Non-goals are as important as goals for maintaining focus
3. Principles inform architectural decisions (privacy by design, LLM constraints)
4. Principles are stable; non-goals may evolve over product phases

## Acceptance criteria

1. Each principle has a clear definition and rationale
2. Non-goals are explicit, not implied
3. Principles can guide concrete trade-off decisions
4. No principle contradicts another

---

## Core principles

### Principle 1: Personal meaning first

Every lesson connects to the learner's life, interests, or needs. Content that matters is content that sticks. This is the primary differentiator from all competitors.

**Trade-off guidance:** When choosing between a pedagogically "optimal" generic example and a slightly messier personal example, choose the personal one.

### Principle 2: Communication over grammar

Grammar is taught in service of communication, never as an end in itself. A lesson's primary goal is always a communicative task. Grammar explanations are brief, contextualized, and immediately applicable.

**Trade-off guidance:** When a grammar point would take significant time but only marginally improves communication, defer or omit it.

### Principle 3: Authentic tasks

Practice activities mirror real-world language use. Learners prepare for actual situations they will encounter. Tasks are evaluated on communicative effectiveness, not just formal correctness.

**Trade-off guidance:** Prefer a task that is slightly harder but authentic over one that is easier but artificial.

### Principle 4: Adaptive scaffolding

Support adjusts per skill and per construction, not per global level. The learner receives help where needed and independence where ready. Scaffolding fades as competence grows.

**Trade-off guidance:** When uncertain about scaffolding level, start higher (more support) and fade quickly rather than starting too low.

### Principle 5: Learner agency

Learners make meaningful choices: topics, goals, pace, practice focus. The app guides but does not control. Learners can skip, repeat, or dive deeper.

**Trade-off guidance:** When the optimal learning path conflicts with learner choice, respect the choice and adapt.

### Principle 6: Privacy by design

Personal stories and data are protected. No unnecessary data collection. User control over information. Data minimization is a design requirement, not an afterthought.

**Trade-off guidance:** When a feature requires data collection that cannot be fully justified, the feature is redesigned or dropped.

### Principle 7: Evidence-based progression

All advancement is grounded in demonstrated ability, not time spent or lessons completed. Mastery requires evidence across multiple contexts. The system is honest about what the learner knows and does not know.

**Trade-off guidance:** When a learner wants to advance but lacks evidence, the system explains what is needed rather than allowing premature progression.

## Non-goals

| Non-goal | Rationale |
|----------|-----------|
| Exam preparation tool | Tests measure different skills; exam focus distorts communicative approach. We build communication ability; exams are a secondary benefit. |
| Children's app | Cognitive development, attention span, and motivation differ fundamentally from adult learners. Our methodology is designed for adult cognition. |
| Social network | Adding social features creates moderation, safety, and privacy burdens that distract from core learning value. |
| Human teacher replacement | The app complements human instruction. It does not replace expert teachers. Learners are encouraged to seek human interaction. |
| Free-form AI chat | Unstructured conversation lacks pedagogical scaffolding, learning objectives, and progress tracking. Communication is structured toward goals. |
| Translation service | Translation is a different cognitive skill from communicative language use. We teach expression, not conversion between languages. |
| Gamification-first | Game elements serve learning goals, not engagement metrics alone. We gamify meaningfully or not at all. |
| One-size-fits-all curriculum | Every learner has a unique path based on their profile, goals, and interests. There is no single "course." |

## Principle hierarchy

When principles conflict, higher-ranked principles take precedence:

1. Privacy by design
2. Personal meaning first
3. Learner agency
4. Evidence-based progression
5. Communication over grammar
6. Adaptive scaffolding
7. Authentic tasks
