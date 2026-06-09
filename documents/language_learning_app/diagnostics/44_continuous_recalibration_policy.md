# Continuous Recalibration Policy

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

How the learner model is updated based on ongoing performance evidence, not just the initial diagnostic.

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

## Why continuous recalibration?

Language ability changes with learning. The initial diagnostic is a snapshot. Ongoing performance provides richer, more current evidence.

## Evidence sources

| Source | Evidence value | Update frequency |
|--------|---------------|-----------------|
| Lesson performance | High — direct observation | Per lesson |
| Quiz results | High — controlled condition | Per quiz |
| Review sessions | Medium — recall under schedule | Per review |
| Spontaneous production | High — naturalistic use | Per occurrence |
| Error correction patterns | Medium — indirect evidence | Per correction |

## Recalibration algorithm

Bayesian updating approach:
1. Prior: current estimate with confidence
2. Evidence: new observation with reliability weight
3. Posterior: updated estimate with adjusted confidence

Confidence increases with consistent evidence and decreases with contradictory evidence.

## Reassessment triggers

Full reassessment is triggered when:
- Confidence drops below threshold for any key dimension
- Significant time gap (3+ months with low activity)
- Learner reports feeling overplaced or underplaced
- Major change in learning context (new job, new country)
- Performance patterns strongly contradict current profile

## Handling contradictions

When new evidence contradicts current estimates:
1. Log the contradiction
2. Lower confidence in affected dimension(s)
3. Request additional evidence (specific tasks)
4. Update estimate only after sufficient contradictory evidence
