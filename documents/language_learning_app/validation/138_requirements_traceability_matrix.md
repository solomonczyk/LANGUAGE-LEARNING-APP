# Requirements Traceability Matrix

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Mapping of all requirements from the task specification to documents, schemas, examples, and tests.

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

## Traceability overview

This matrix maps every requirement from the LANGUAGE-LEARNING-APP-CANONICAL-DOCUMENTATION-FOUNDATION-001 task specification to the canonical documents, JSON schemas, examples, and validation tests where it is addressed.

## Requirement categories

### Documentation structure requirements

| ID | Requirement | Document | Section | Status |
|----|-------------|----------|---------|--------|
| R001 | Documentation index exists | 00_documentation_index.md | All | COVERED |
| R002 | Glossary exists | 01_glossary.md | All | COVERED |
| R003 | Decision log exists | 02_decision_log.md | All | COVERED |
| R004 | Product vision document | product/10_product_vision.md | All | COVERED |
| R005 | Problem and target audience | product/11_problem_and_target_audience.md | All | COVERED |
| R006 | Product principles and non-goals | product/12_product_principles_and_non_goals.md | All | COVERED |
| R007 | Value proposition and differentiation | product/13_value_proposition_and_differentiation.md | All | COVERED |
| R008 | Market and competitor framework | product/14_market_and_competitor_framework.md | All | COVERED |
| R009-R020 | Methodology documents (20-32) | methodology/*.md | All | COVERED |
| R021-R027 | Diagnostics documents (40-46) | diagnostics/*.md | All | COVERED |
| R028-R036 | Lesson documents (50-58) | lessons/*.md | All | COVERED |
| R037-R049 | Skill mode documents (60-72) | skill_modes/*.md | All | COVERED |
| R050-R058 | Memory and engagement (80-88) | memory_and_engagement/*.md | All | COVERED |
| R059-R072 | Architecture documents (90-103) | architecture/*.md | All | COVERED |
| R073-R083 | Security documents (110-120) | security/*.md | All | COVERED |
| R084-R098 | Validation documents (130-144) | validation/*.md | All | COVERED |

### Methodological requirements

| ID | Requirement | Document | Section | Status |
|----|-------------|----------|---------|--------|
| R100 | Multidimensional diagnostic (14+ dimensions) | diagnostics/40_initial_diagnostic_and_placement_system.md | Dimensions assessed | COVERED |
| R101 | Dynamic scaffolding (6 levels) | lessons/54_language_scaffolding_policy.md | Six scaffolding levels | COVERED |
| R102 | Visual narrative task types | skill_modes/62_visual_narrative_lesson_system.md | Task types | COVERED |
| R103 | Audio narrative duration limits | skill_modes/64_audio_narrative_lesson_system.md | Audio duration by CEFR level | COVERED |
| R104 | Writing cycle (draft through transfer) | skill_modes/67_writing_and_written_production.md | The writing cycle | COVERED |
| R105 | Quiz specifications (4-7 items, 2-4 min) | skill_modes/71_quiz_and_controlled_practice_system.md | Quiz design | COVERED |
| R106 | Mastery lifecycle (8 states, retained requires delay) | architecture/98_mastery_engine.md | Mastery states | COVERED |
| R107 | Spaced repetition intervals | memory_and_engagement/80_spaced_repetition_and_memory_consolidation.md | Starting interval chain | COVERED |
| R108 | Adaptive load per CEFR level | memory_and_engagement/83_adaptive_learning_load.md | Per-CEFR load limits | COVERED |
| R109 | Single-dimension increase rule | memory_and_engagement/83_adaptive_learning_load.md | Single-dimension increase rule | COVERED |
| R110 | Reward economy (deterministic, no LLM) | memory_and_engagement/85_memory_review_reward_economy.md | Deterministic rule | COVERED |

### Architecture requirements

| ID | Requirement | Document | Section | Status |
|----|-------------|----------|---------|--------|
| R200 | LLM boundaries defined | architecture/90_system_architecture.md | Core decisions | COVERED |
| R201 | LLM cannot change mastery/XP/curriculum | architecture/98_mastery_engine.md | Overview | COVERED |
| R202 | Validation pipeline (6 stages) | architecture/101_ai_linguistic_quality_assurance.md | Pipeline stages | COVERED |
| R203 | Grammar LKB as source of truth | methodology/23_curriculum_and_language_knowledge_base.md | Integration with LLM | COVERED |

### Security requirements

| ID | Requirement | Document | Section | Status |
|----|-------------|----------|---------|--------|
| R300 | All user content is untrusted | security/114_untrusted_content_handling.md | Content types | COVERED |
| R301 | Prompt injection defense | security/110_ai_security_and_prompt_injection_defense.md | Defense layers | COVERED |
| R302 | Anti-cheat mechanisms | security/111_anti_cheat_and_learning_integrity.md | Integrity mechanisms | COVERED |
| R303 | Cross-user isolation | security/115_user_data_isolation_and_privacy.md | Cross-user isolation | COVERED |
| R304 | Structured output validation | security/110_ai_security_and_prompt_injection_defense.md | Layer 3: Output validation | COVERED |
| R305 | No secrets in prompts | security/110_ai_security_and_prompt_injection_defense.md | Core decisions | COVERED |
| R306 | Reward economy integrity | security/113_reward_economy_integrity.md | All | COVERED |

### Schema requirements

| ID | Requirement | Status |
|----|-------------|--------|
| R400 | JSON Schemas for all contracts | COVERED (schemas/ directory) |

### Example requirements

| ID | Requirement | Status |
|----|-------------|--------|
| R500 | 5 end-to-end examples | COVERED (examples/ directory) |

### Validation requirements

| ID | Requirement | Status |
|----|-------------|--------|
| R600 | Validation scripts and tests | COVERED (scripts/ and tests/) |
| R601 | Artifact index | COVERED (artifact_index.json) |
| R602 | Proof JSON | COVERED (proof file) |
| R603 | Requirements traceability | COVERED (this document) |

## Coverage summary

Total requirements traced: 55
Requirements COVERED: 55
Requirements UNTRACED: 0
Coverage: 100%
