# AI Assessment Calibration and Human Agreement

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Process for calibrating AI assessments against human expert judgments.

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

## Purpose

AI assessments of learner language must be calibrated against human expert judgments to ensure validity and reliability.

## Calibration process

1. Sample of learner responses (minimum 100 per skill area per CEFR level)
2. Both AI and human linguists assess the same responses
3. Agreement metrics calculated
4. Thresholds set for acceptable agreement
5. Regular calibration cycles

## Agreement metrics

| Metric | What it measures | Target |
|--------|-----------------|--------|
| Cohen's kappa | Inter-rater agreement (beyond chance) | > 0.7 |
| Exact agreement | Same rating assigned | > 80% |
| Adjacent agreement | Within one level | > 95% |
| Spearman correlation | Ranking consistency | > 0.8 |

## Calibration frequency

- Initial calibration: Before any production use
- Ongoing: Monthly recalibration on new sample
- Event-driven: After any significant model or prompt change

## Handling disagreements

When AI and human disagree:
1. Log the disagreement
2. Third expert adjudicates
3. Update AI assessment criteria if systematic error found
4. Track disagreement rate over time

## Human rater qualifications

- Native/near-native proficiency
- Training on assessment rubrics
- Calibration before each rating session
- Inter-rater reliability check among human raters
