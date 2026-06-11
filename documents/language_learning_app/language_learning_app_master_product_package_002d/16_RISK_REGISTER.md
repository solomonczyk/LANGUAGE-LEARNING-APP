# Master Risk Register

**Status:** CANONICAL  
**Version:** 1.0.0  
**Effective date:** 2026-06-10  
**Owner:** Product Owner  
**Change control:** Changes require a documented change request or ADR where specified.

## Priority risks

| ID | Risk | Probability | Impact | Owner | Mitigation | Trigger |
|---|---|---|---|---|---|---|
| R-01 | Endless scope expansion | High | Critical | Product Owner | MVP cut line, stage gates | deadline/budget >125% |
| R-02 | Weak paid demand | Medium | Critical | Product | early payment test | no payments after 2 offers |
| R-03 | Low Day-7 retention | High | High | Product/Learning | onboarding and lesson iteration | <40% in alpha |
| R-04 | AI feedback quality | Medium | Critical | AI/Learning | schemas, validators, human review | unsafe/incorrect feedback |
| R-05 | User data leakage | Low | Critical | Security | isolation tests, audit | any confirmed leak |
| R-06 | Support workload too high | Medium | High | Operations | guided scripts, self-service improvements | >30 min/user/week |
| R-07 | AI cost too high | Medium | High | Technical | budgets, caching, model policy | >€3/user/month alpha |
| R-08 | Product feels like generic chatbot | Medium | High | Product | structured journey, progress evidence | interview feedback |
| R-09 | Overclaiming learning outcomes | Medium | High | Marketing/Learning | claim review, measured evidence | unsupported promise |
| R-10 | Legal/payment readiness delay | Medium | High | Product | review before paid pilot | processor/legal blocker |
| R-11 | Mobile visual/accessibility failure | Medium | High | Mobile/QA | device matrix, operator review | critical layout defect |
| R-12 | Founder capacity bottleneck | High | High | Product Owner | timebox, scope reduction | repeated missed stages |

## Risk response rule

A critical risk becoming actual creates an immediate HOLD unless the relevant stage contract explicitly provides a safe recovery path.
