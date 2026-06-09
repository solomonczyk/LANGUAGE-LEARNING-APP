# Risk Register

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Comprehensive risk register for the language learning app project.

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

## Technical risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| LLM quality insufficient for pedagogical use | Medium | High | Fallback templates, human review sampling, multiple providers |
| LLM cost exceeds projections | Medium | High | Model tier routing, cost caps, usage optimization |
| Prompt injection bypasses defenses | Low | Critical | Defense-in-depth, regular red team testing, incident response plan |
| Validation pipeline latency too high | Medium | Medium | Async validation, caching, performance optimization |
| SRS algorithm ineffective | Low | Medium | A/B testing, literature-based algorithm selection, iterative tuning |

## Market risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Competitor launches similar feature | Medium | Medium | Speed to market, unique methodology, privacy differentiation |
| User acquisition cost too high | Medium | High | Organic growth through quality, referral program, content marketing |
| Target audience too narrow | Low | Medium | Expand to adjacent segments (corporate, academic) |

## Pedagogical risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Personal narrative approach doesn't scale | Low | High | Hybrid approach with suggested situations, scenario library |
| Learning outcomes not measurable | Low | High | CEFR-aligned assessment, controlled validation study |
| Learners resistant to personal sharing | Medium | Medium | Opt-in sharing, strong privacy, alternative modes available |

## Operational risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| LLM provider goes down | Medium | High | Multi-provider, graceful degradation, template fallback |
| Data breach | Low | Critical | Encryption, isolation, audit, incident response plan |
| Regulatory changes for AI in education | Medium | Medium | Compliance monitoring, legal review, adaptable architecture |
