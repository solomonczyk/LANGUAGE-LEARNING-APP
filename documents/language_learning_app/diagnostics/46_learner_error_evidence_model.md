# Learner Error Evidence Model

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Structured tracking of learner errors for remediation, SRS, and profile refinement.

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

1. Diagnostic must evaluate 13 separate dimensions
2. No single-level placement is allowed
3. Confidence intervals accompany every estimate
4. Continuous recalibration updates the profile

## Acceptance criteria

1. All diagnostic dimensions are defined with assessment methods
2. Confidence model is mathematically specified
3. Error evidence model is structured and actionable
4. Recalibration policy is defined

---

## Purpose

To systematically track, categorize, and act on learner errors. Errors are valuable data points for personalization, not just failures to be corrected.

## Error type taxonomy

### Grammatical errors
- Article misuse
- Tense/aspect errors
- Agreement errors
- Word order
- Preposition errors
- Pronoun errors

### Lexical errors
- Wrong word choice
- False cognate
- Collocation error
- Overgeneralization

### Phonological errors
- Segment substitution
- Stress shift
- Intonation pattern

### Pragmatic errors
- Register mismatch
- Inappropriate directness
- Speech act error

### Discourse errors
- Coherence breakdown
- Reference ambiguity
- Missing discourse markers

## Error tracking per event

Each recorded error includes:
- Error type (from taxonomy)
- Target form (correct version)
- Learner form (what was produced)
- Context (the utterance/sentence)
- L1 influence flag
- Frequency count
- Pattern detection (isolated error or systematic?)
- Remediation attempts and outcomes

## Error to mastery link

Persistent errors indicate items that are introduced but not mastered. The error evidence model feeds into:
1. Mastery engine — errors block mastery advancement
2. SRS — error items scheduled for focused review
3. Lesson selection — repair lessons built around error patterns
4. Scaffolding level — errors may indicate need for more support

## Privacy consideration

Error data is personally identifiable (reveals specific learner weaknesses). Protected accordingly. Aggregate error data (anonymized) used for improving LKB and pedagogy.
