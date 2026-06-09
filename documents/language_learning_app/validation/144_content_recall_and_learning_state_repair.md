# Content Recall and Learning State Repair

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Handling of content that needs to be recalled or updated, and repair of inconsistent learning state.

## In scope

- MVP scope and roadmap
- Validation and experiment plan
- Product and learning metrics
- Accessibility and inclusive learning
- Content authoring and editorial workflow
- Human linguist review and AI calibration
- Risk register, traceability matrix, acceptance criteria
- Language variants, licensing, offline learning, state repair

## Out of scope

- Implementation of validation infrastructure
- Specific A/B test configurations
- Marketing collateral
- User research recruitment

## Core decisions

1. MVP scope is clearly defined with phased rollout
2. Validation plan includes A/B testing and user studies
3. Traceability matrix covers all requirements
4. Risk register is comprehensive with mitigations

## Acceptance criteria

1. All 15 validation documents exist
2. MVP scope is specific and actionable
3. Risk register has probability, impact, and mitigation for each risk
4. Acceptance criteria are testable

---

## Content recall scenarios

1. **LKB update** — A grammar rule is corrected. Learners who engaged with the previous version need notification and re-instruction.
2. **Content error** — A specific lesson contained an error. Affected learners are identified and offered repair.
3. **Pedagogical improvement** — A teaching approach is improved. Learners who went through the old approach are offered updated content.

## State repair scenarios

1. **Profile inconsistency** — Diagnostic and ongoing performance don't match. Recalibration triggered.
2. **Mastery/performance mismatch** — Quiz shows mastery but free production shows errors. Regression triggered.
3. **Evidence contradiction** — Two evidence sources conflict. Confidence reduced, new evidence requested.

## Repair mechanisms

| Issue | Detection | Repair action |
|-------|-----------|--------------|
| LKB update | Version change notification | Flag affected items for re-introduction |
| Content error | Error report | Push repair lesson to affected learners |
| Profile mismatch | Anomaly detection | Recalibration or partial reassessment |
| Mastery mismatch | Performance monitoring | Mastery regression to previous state |
| Evidence conflict | Cross-validation | Request additional evidence |

## Learner notification

When state repair is needed, the learner is informed:
- What happened (if visible)
- What changed (transparent explanation)
- What to expect (repair lesson, recalibration)
- No penalty for system errors

## Graceful degradation

If state cannot be perfectly repaired:
1. Best-effort reconstruction
2. Wider confidence intervals
3. Additional observation period
4. Human review if automated repair fails
