# Assessment Confidence and Evidence Model

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

How the system determines confidence in its ability estimates and what constitutes sufficient evidence.

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

## Confidence model

Every ability estimate includes a confidence level: Low, Medium, High, or Very High.

| Confidence | Meaning | Evidence required |
|------------|---------|------------------|
| Low | Preliminary estimate, may be inaccurate | 1-3 observations |
| Medium | Reasonably confident, may shift | 4-8 observations across contexts |
| High | Stable estimate, unlikely to change | 9-15 observations across multiple contexts |
| Very High | Highly reliable estimate | 15+ observations, confirmed by delayed testing |

## Evidence weighting

Not all observations are equal. Weight factors:

| Factor | Weight adjustment |
|--------|-----------------|
| Task type (production > recognition) | Production: 1.5x, Recognition: 1.0x |
| Context variety (multiple contexts > single) | Per new context: +0.2x |
| Time span (distributed > massed) | Per day apart: +0.05x |
| Spontaneity (spontaneous > rehearsed) | Spontaneous: 1.3x |
| Delayed performance (1+ week) | 2.0x |

## Minimum evidence requirements

- Lesson placement: Minimum Medium confidence in relevant dimensions
- Mastery transition: Minimum 3 observations at target level
- Level advancement: Minimum High confidence across production dimensions
- Certificate readiness: Minimum Very High confidence in all relevant dimensions

## Handling insufficient evidence

When confidence is too low for a decision:
- The system transparently explains what additional evidence is needed
- Suggests specific tasks or activities to gather evidence
- Does not make premature advancement decisions
