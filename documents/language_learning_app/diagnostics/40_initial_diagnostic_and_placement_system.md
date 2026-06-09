# Initial Diagnostic and Placement System

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

The multidimensional initial assessment that evaluates learners across 14+ separate dimensions with confidence intervals.

## In scope

- Initial diagnostic design and placement
- Multidimensional learner profiling
- Entry contract and onboarding
- Continuous recalibration and assessment confidence
- Error evidence tracking

## Out of scope

- Individual diagnostic items
- Norm-referenced scoring
- Certification decision logic
- Third-party assessment integration

## Core decisions

1. Diagnostic must evaluate 14+ separate dimensions
2. No single-level placement is allowed
3. Confidence intervals accompany every estimate
4. Continuous recalibration updates the profile

## Acceptance criteria

1. All diagnostic dimensions are defined with assessment methods
2. Confidence model is mathematically specified
3. Error evidence model is structured and actionable
4. Recalibration policy is defined

---

## Purpose of the initial diagnostic

To create a detailed, multi-dimensional profile of the learner's current language abilities — not a single level. This profile drives lesson personalization, curriculum starting point, and scaffolding level.

## Dimensions assessed

| Dimension | Assessment method | What is measured |
|-----------|------------------|-----------------|
| Reading | Text comprehension questions | Understanding written texts |
| Listening | Audio comprehension | Understanding spoken language |
| Passive vocabulary | Recognition tasks | Vocabulary breadth |
| Active vocabulary | Production tasks | Vocabulary available for use |
| Grammar recognition | Grammaticality judgments | Explicit grammar knowledge |
| Productive grammar | Error analysis in production | Grammar in use |
| Spoken production | Monologue task | Extended speech |
| Spoken interaction | Dialogue task | Interactive communication |
| Pronunciation intelligibility | Reading aloud, free speech | Sound production |
| Narrative coherence | Story retelling | Discourse organization |
| Writing | Written prompt response | Written production |
| Mediation | Information transfer task | Relaying information |
| Communication strategies | Problem-solving scenario | Strategy use |

## Adaptive diagnostic flow

The diagnostic uses adaptive difficulty within each dimension to efficiently find the learner's level:
1. Start at estimated level (or A1 if unknown)
2. Present task at that level
3. If correct, move up; if incorrect, move down
4. Converge on level estimate after 3-5 items per dimension

## Confidence intervals

Each dimension estimate includes a confidence interval. The system requires minimum confidence before making placement decisions. Low-confidence dimensions are flagged for early reassessment.

## Duration

Estimated 30-45 minutes for full diagnostic. Learners can pause and resume. If full diagnostic is too long, a short-form version (15 min) provides initial estimates with wider confidence intervals.
