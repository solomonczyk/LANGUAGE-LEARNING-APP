# MVP Architecture Planning Index

**Status:** Draft  
**Version:** 1.0.0  
**Last updated:** 2026-06-10

---

## Purpose

This index provides a complete map of all MVP architecture planning artifacts for the Language Learning App. Every document listed here defines the product scope, architecture, technology decisions, and implementation plan for the MVP milestone. This layer builds on the canonical documentation foundation and prepares for the first implementation sprint.

---

## Document tree

| # | Document | Path | Description |
|---|----------|------|-------------|
| 00 | MVP Architecture Index | `00_mvp_architecture_index.md` | This index |
| 01 | MVP Product Scope | `01_mvp_product_scope.md` | MVP definition, must-have capabilities, out-of-scope items |
| 02 | Personas | `02_personas.md` | Four learner personas with goals, frustrations, and needs |
| 03 | User Story Catalog | `03_user_story_catalog.md` | Full user story catalog across 20 epics (50+ stories) |
| 04 | User Journeys | `04_user_journeys.md` | Eight end-to-end user journeys with system decisions |
| 05 | Functional Requirements | `05_functional_requirements.md` | Complete functional requirements catalog (55+ FRs) |
| 06 | Non-Functional Requirements | `06_non_functional_requirements.md` | NFRs with measurable targets (25+ NFRs) |
| 07 | Technology Stack Comparison | `07_technology_stack_comparison.md` | Comparison matrix for all technology options |
| 08 | Selected Technology Stack | `08_selected_technology_stack.md` | Final stack decision with rationale |
| 09 | System Context | `09_system_context.md` | C4 context diagram and external system interfaces |
| 10 | Container Architecture | `10_container_architecture.md` | C4 container diagram and container responsibilities |
| 11 | Module Architecture | `11_module_architecture.md` | 20 bounded modules with contracts and dependencies |
| 12 | Processing Pipeline | `12_processing_pipeline.md` | End-to-end lesson submission pipeline with 17 steps |
| 13 | Dangerous Action Gates | `13_dangerous_action_gates.md` | 8 control gates for dangerous system actions |
| 14 | API Architecture | `14_api_architecture.md` | REST API design, endpoint catalog, error model |
| 15 | Data Model | `15_data_model.md` | 27 core entities with fields, indexes, privacy |
| 16 | State Machines | `16_state_machines.md` | 7 entity state machines with transitions and guards |
| 17 | LLM Gateway Architecture | `17_llm_gateway_architecture.md` | Provider-independent AI gateway with structured output |
| 18 | Prompt Management | `18_prompt_management.md` | Prompt versioning, evaluation, and security policies |
| 19 | Security Threat Model | `19_security_threat_model.md` | 15 threat entries using STRIDE methodology |
| 20 | Privacy and Data Retention | `20_privacy_and_data_retention.md` | Data classification, retention periods, deletion/export |
| 21 | Observability | `21_observability.md` | Logging, metrics, tracing, alerting, cost tracking |
| 22 | Deployment Topology | `22_deployment_topology.md` | Local/test/staging environments, CI/CD, rollback |
| 23 | Testing Strategy | `23_testing_strategy.md` | 11-layer test pyramid with 13 required test scenarios |
| 24 | First Implementation Sprint | `24_first_implementation_sprint.md` | Sprint 1 vertical slice scope and deliverables |
| 25 | Architecture Decision Log | `25_architecture_decision_log.md` | 12 ADRs covering all major technology decisions |
| 26 | Risk Register | `26_risk_register.md` | 18 risks with likelihood, impact, mitigation |
| 27 | Acceptance Criteria | `27_acceptance_criteria.md` | Verification criteria for MVP architecture acceptance |
| 28 | Requirements Traceability Matrix | `28_requirements_traceability_matrix.md` | Complete traceability across all artifacts |

---

## Related directories

| Directory | Content |
|-----------|---------|
| `schemas/` | JSON Schema files for validation (5 schemas) |
| `examples/` | Example JSON fixtures (3 examples) |
| `diagrams/` | Mermaid and other diagrams |
| `api/` | OpenAPI specification |

---

## External dependencies

This layer depends on the canonical foundation documentation at `documents/language_learning_app/`:

- Product vision and principles (documents 10-14)
- Methodology and curriculum (documents 20-32)
- Diagnostics and learner model (documents 40-46)
- Lesson and content systems (documents 50-72)
- Memory and engagement (documents 80-88)
- Architecture (documents 90-103)
- Security (documents 110-120)
- Validation and acceptance (documents 130-144)

---

## Governance

Every artifact in this layer MUST:

1. Be listed in this index on creation
2. Be registered in `architecture_artifact_index.json`
3. Be referenced in the requirements traceability matrix if it contains requirements
4. Pass the MVP architecture validation tests
5. Have no placeholder content (no TODO, TBD, empty sections)
6. Be consistent with the canonical foundation documentation
7. Preserve LLM authority restrictions from the foundation
8. Have deterministic reward and mastery authority
9. Not contain application/runtime source code
10. Not contain real secrets or credentials
