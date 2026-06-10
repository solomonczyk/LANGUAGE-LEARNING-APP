# Acceptance Criteria

**Status:** Draft  
**Version:** 1.0.0  
**Last updated:** 2026-06-10

---

## Task Acceptance Criteria

This document defines the verification criteria for the MVP Architecture Planning task (LANGUAGE-LEARNING-APP-MVP-ARCHITECTURE-PLANNING-002).

---

## 1. Product Definition

| ID | Criterion | Verification Method | Criticality |
|----|-----------|-------------------|-------------|
| AC-01 | MVP product scope is defined with must-have capabilities and out-of-scope items | Read 01_mvp_product_scope.md | Blocker |
| AC-02 | At least 4 personas are defined with goals, frustrations, and needs | Read 02_personas.md | Blocker |
| AC-03 | At least 45 user stories are created across 20 epics | Count entries in 03_user_story_catalog.md | Blocker |
| AC-04 | At least 8 end-to-end user journeys are defined | Count journeys in 04_user_journeys.md | Blocker |
| AC-05 | Each user journey has trigger, preconditions, steps, failure branches | Read 04_user_journeys.md | Blocker |

## 2. Requirements

| ID | Criterion | Verification Method | Criticality |
|----|-----------|-------------------|-------------|
| AC-06 | Functional requirements catalog covers all required domains | Read 05_functional_requirements.md | Blocker |
| AC-07 | Every functional requirement has title, description, priority, acceptance criteria | Read 05_functional_requirements.md | Blocker |
| AC-08 | Non-functional requirements include all required initial targets | Read 06_non_functional_requirements.md; verify targets present | Blocker |
| AC-09 | All NFR targets are specified (none left as TODO/TBD) | Read 06_non_functional_requirements.md | Blocker |

## 3. Technology

| ID | Criterion | Verification Method | Criticality |
|----|-----------|-------------------|-------------|
| AC-10 | Technology stack comparison includes all required categories | Read 07_technology_stack_comparison.md | Blocker |
| AC-11 | Each comparison entry has fit assessment and rationale | Read 07_technology_stack_comparison.md | Blocker |
| AC-12 | Selected stack is documented with version requirements | Read 08_selected_technology_stack.md | Blocker |
| AC-13 | Every selected technology has an ADR | Verify ADR-001 through ADR-012 in 25_architecture_decision_log.md | Blocker |

## 4. Architecture

| ID | Criterion | Verification Method | Criticality |
|----|-----------|-------------------|-------------|
| AC-14 | Modular monolith is chosen and justified | Read 11_module_architecture.md | Blocker |
| AC-15 | All 20 required modules are defined with boundaries | Read 11_module_architecture.md | Blocker |
| AC-16 | Processing pipeline has all 15 steps with input/output/retry defined | Read 12_processing_pipeline.md | Blocker |
| AC-17 | All 8 dangerous action gates are defined | Read 13_dangerous_action_gates.md | Blocker |
| AC-18 | API contracts exist for all required endpoint groups | Read 14_api_architecture.md | Blocker |
| AC-19 | Core entity definitions include all 27 required entities | Read 15_data_model.md | Blocker |
| AC-20 | State machines exist for all 7 required entities | Read 16_state_machines.md | Blocker |

## 5. LLM & Security

| ID | Criterion | Verification Method | Criticality |
|----|-----------|-------------------|-------------|
| AC-21 | LLM gateway has provider-independent interface with structured output | Read 17_llm_gateway_architecture.md | Blocker |
| AC-22 | LLM authority restrictions are explicitly documented | Read 17_llm_gateway_architecture.md | Blocker |
| AC-23 | Prompt management includes versioning, separation, evaluation | Read 18_prompt_management.md | Blocker |
| AC-24 | Threat model covers all 15 required threats | Read 19_security_threat_model.md | Blocker |
| AC-25 | Privacy model defines data classification and retention periods | Read 20_privacy_and_data_retention.md | Blocker |

## 6. Operations

| ID | Criterion | Verification Method | Criticality |
|----|-----------|-------------------|-------------|
| AC-26 | Observability defines logs, metrics, traces, and dashboards | Read 21_observability.md | Blocker |
| AC-27 | Deployment topology defines local, test, and staging environments | Read 22_deployment_topology.md | Blocker |
| AC-28 | Testing strategy defines all 11 test layers and 13 scenarios | Read 23_testing_strategy.md | Blocker |
| AC-29 | First implementation sprint has vertical slice scope and deliverables | Read 24_first_implementation_sprint.md | Blocker |

## 7. Governance

| ID | Criterion | Verification Method | Criticality |
|----|-----------|-------------------|-------------|
| AC-30 | All 12 ADRs are created with context, decision, alternatives, consequences | Read 25_architecture_decision_log.md | Blocker |
| AC-31 | Risk register has at least 15 risks with mitigation | Read 26_risk_register.md | Blocker |
| AC-32 | Acceptance criteria documented for the task itself | Read 27_acceptance_criteria.md | Blocker |
| AC-33 | Requirements traceability matrix has all required table types | Read 28_requirements_traceability_matrix.md | Blocker |

## 8. Schemas, Examples, API

| ID | Criterion | Verification Method | Criticality |
|----|-----------|-------------------|-------------|
| AC-34 | All 5 JSON Schemas exist and are valid | Validate schemas/ files | Blocker |
| AC-35 | All 3 example files exist and validate against schemas | Validate examples/ files | Blocker |
| AC-36 | OpenAPI spec exists and is valid YAML | Validate api/openapi_mvp.yaml | Blocker |
| AC-37 | Architecture artifact index exists and paths are valid | Read architecture_artifact_index.json | Blocker |

## 9. Validation

| ID | Criterion | Verification Method | Criticality |
|----|-----------|-------------------|-------------|
| AC-38 | All validation tests pass (tests_failed = 0) | Run validation tests | Blocker |
| AC-39 | No warnings from validation (warnings = 0) | Run validation tests | Blocker |
| AC-40 | No untraced requirements (untraced_requirements = 0) | Run validation tests | Blocker |
| AC-41 | No contradictions found (contradictions_found = 0) | Run validation tests | Blocker |

## 10. Forbidden Actions

| ID | Criterion | Verification Method | Criticality |
|----|-----------|-------------------|-------------|
| AC-42 | No application code changed | git diff | Blocker |
| AC-43 | No runtime code added | git diff | Blocker |
| AC-44 | No real LLM calls executed | Script verification | Blocker |
| AC-45 | No deployment executed | Script verification | Blocker |
| AC-46 | No secrets added | git diff, secret scan | Blocker |
| AC-47 | Production_accepted is false | Proof JSON check | Blocker |

## 11. Git Closeout

| ID | Criterion | Verification Method | Criticality |
|----|-----------|-------------------|-------------|
| AC-48 | Commit created and pushed | git log, git push verification | Blocker |
| AC-49 | Git working tree is clean | git status --porcelain | Blocker |
| AC-50 | HEAD matches origin/master | git rev-parse HEAD, origin/master | Blocker |
| AC-51 | No unpushed commits | git status | Blocker |

---

## Final Checklist

| # | Criterion | Status |
|---|-----------|--------|
| 1 | MVP scope defined | ☐ |
| 2 | Personas defined (4) | ☐ |
| 3 | User stories defined (45+) | ☐ |
| 4 | User journeys defined (8+) | ☐ |
| 5 | Functional requirements complete | ☐ |
| 6 | NFR targets defined | ☐ |
| 7 | Stack comparison performed | ☐ |
| 8 | Stack selected and ADR-ed | ☐ |
| 9 | Modular monolith justified | ☐ |
| 10 | Module boundaries defined (20) | ☐ |
| 11 | API contracts created | ☐ |
| 12 | OpenAPI valid | ☐ |
| 13 | Core entities defined (27) | ☐ |
| 14 | State machines defined (7) | ☐ |
| 15 | Dangerous action gates defined (8) | ☐ |
| 16 | LLM authority restrictions preserved | ☐ |
| 17 | Threat model complete (15) | ☐ |
| 18 | Privacy model defined | ☐ |
| 19 | Observability defined | ☐ |
| 20 | Deployment topology defined | ☐ |
| 21 | First sprint defined | ☐ |
| 22 | Traceability complete | ☐ |
| 23 | Tests failed = 0 | ☐ |
| 24 | Warnings = 0 | ☐ |
| 25 | Contradictions = 0 | ☐ |
| 26 | Application code changed = false | ☐ |
| 27 | Runtime code added = false | ☐ |
| 28 | LLM calls executed = false | ☐ |
| 29 | Deployment executed = false | ☐ |
| 30 | Secrets added = false | ☐ |
| 31 | Commit pushed | ☐ |
| 32 | Git clean | ☐ |
| 33 | HEAD == origin/master | ☐ |
| 34 | Unresolved blockers = [] | ☐ |
| 35 | Production_accepted = false | ☐ |
