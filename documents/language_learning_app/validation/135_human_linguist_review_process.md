# Human Linguist Review Process

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Process for human linguists to review AI-generated content and provide feedback.

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

## Review scope

Human linguists review a sample of AI-generated content:
- Lesson content: 10% sample
- Feedback messages: 5% sample
- Quiz items: 15% sample
- Narrative analyses: 5% sample

Sample rate increases if quality metrics decline.

## Review criteria

| Criterion | What is checked |
|-----------|-----------------|
| Accuracy | Is the language correct? |
| Naturalness | Does it sound natural? |
| Level-appropriateness | Is it right for the CEFR level? |
| Pedagogical value | Does it support learning? |
| Cultural sensitivity | Is it culturally appropriate? |
| Safety | No harmful content |

## Feedback loop

1. Linguist reviews sampled content
2. Issues recorded with severity
3. Issues categorized (linguistic, pedagogical, safety)
4. Feedback sent to ML/engineering team
5. Root cause identified (prompt issue, LKB gap, model issue)
6. Fix implemented
7. Fix verified

## Linguist qualifications

- Native or near-native proficiency in target language
- Training in language teaching (MA in applied linguistics or equivalent)
- Experience with CEFR framework
- Familiarity with the product's methodology
