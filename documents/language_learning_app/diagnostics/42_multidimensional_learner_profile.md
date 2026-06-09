# Multidimensional Learner Profile

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

The structured representation of a learner's abilities across all assessed dimensions.

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

## Profile structure

The learner profile captures ability estimates across all 14+ dimensions, plus metadata, preferences, and history.

## Per-dimension data

For each dimension:
- CEFR level estimate (A1-C2 with sub-level)
- Confidence interval
- Number of observations
- Date of last assessment
- Trend (improving, stable, declining)

## Profile sections

### Ability estimates
Per-dimension CEFR levels with confidence. This is the core data driving personalization.

### Skill asymmetry visualization
Visual comparison of strongest and weakest dimensions. Example: Reading B1 vs Speaking A2. This helps learners understand their profile and motivates targeted practice.

### Learning style indicators
Preferences for: inductive vs deductive, visual vs auditory, individual vs interactive, fast vs thorough.

### Interest inventory
Topics the learner has engaged with: personal stories, suggested preferences, content engagement history.

### Error profile
Most common error types, persistent patterns, L1-specific issues.

### Versioning

The profile is versioned. Each update creates a new version. Previous versions are retained for analysis. Major updates (e.g., new diagnostic) create a new baseline.
