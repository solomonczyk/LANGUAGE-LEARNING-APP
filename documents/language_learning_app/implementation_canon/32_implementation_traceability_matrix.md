# Implementation Traceability Matrix

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  

---

## 1. Traceability Overview

| Metric | Count |
|--------|-------|
| Requirements total | 43 |
| Requirements traced | 43 |
| Requirements untraced | 0 |
| Broken links | 0 |

---

## 2. Requirement-to-Document Mapping

| # | Requirement | Canon Document | ADR | Schema | Example | Future Module | Future Feature |
|---|-------------|---------------|-----|--------|---------|--------------|----------------|
| 1 | Platform support (Android) | 01 | ADR-014 | — | — | — | All features |
| 2 | Platform support (iOS) | 01 | ADR-014 | — | — | — | All features |
| 3 | Responsive layout | 02 | ADR-015 | — | — | — | All UI |
| 4 | Safe area rules | 02 | ADR-015 | — | — | — | All UI |
| 5 | Keyboard avoidance | 02 | ADR-015 | — | — | — | Form screens |
| 6 | Design tokens | 04 | ADR-016 | design_tokens.schema.json | design_tokens.example.json | — | All UI |
| 7 | Component catalog | 04 | ADR-016 | — | — | — | All UI |
| 8 | Accessibility | 05 | ADR-016 | — | — | — | All UI |
| 9 | Localization | 05 | ADR-016 | — | — | — | All UI |
| 10 | Navigation map | 06 | ADR-017 | — | — | — | Navigation |
| 11 | Route guards | 06 | ADR-017 | — | — | identity | Auth flow |
| 12 | Frontend structure | 07 | ADR-018 | frontend_module.schema.json | frontend_module.example.json | All frontend | — |
| 13 | Import rules | 07 | ADR-018 | — | — | All frontend | — |
| 14 | State (Zustand) | 08 | ADR-013 | — | — | All frontend | — |
| 15 | State (TanStack Query) | 08 | ADR-013 | — | — | All frontend | — |
| 16 | API client | 09 | ADR-019 | — | — | All frontend | API |
| 17 | API error handling | 09 | ADR-019 | — | — | All frontend | API |
| 18 | Backend structure | 10 | ADR-002 | — | — | All backend | — |
| 19 | Backend modular monolith | 10 | ADR-003 | — | — | All backend | — |
| 20 | Module definitions | 11 | — | backend_module.schema.json | backend_module.example.json | All modules | — |
| 21 | Module dependency matrix | 11 | — | — | — | All modules | — |
| 22 | API conventions | 12 | ADR-019 | api_convention.schema.json | — | — | All endpoints |
| 23 | Error contract | 12 | ADR-019 | — | — | — | All endpoints |
| 24 | Database conventions | 13 | ADR-020 | database_convention.schema.json | — | All backend | — |
| 25 | Migration rules | 13 | ADR-020 | — | — | All backend | Migrations |
| 26 | Auth (Supabase) | 14 | ADR-021 | — | — | identity | Auth |
| 27 | Authorization | 14 | ADR-021 | — | — | identity | Auth |
| 28 | AI Gateway | 15 | ADR-008 | — | — | ai_gateway | AI features |
| 29 | AI authority | 15 | ADR-009 | — | — | ai_gateway | AI features |
| 30 | Dangerous gates | 16 | — | — | — | All modules | Pipeline |
| 31 | Audio | 17 | ADR-022 | — | — | submission | Audio features |
| 32 | Notifications | 18 | — | — | — | notifications | Notifications |
| 33 | Offline | 19 | ADR-023 | — | — | All frontend | Offline |
| 34 | Sync & recovery | 19 | ADR-023 | — | — | All frontend | Sync |
| 35 | Security controls | 20 | — | — | — | integrity | Security |
| 36 | Privacy | 21 | — | — | — | all | Privacy |
| 37 | Testing | 22 | — | test_requirement.schema.json | test_requirement.example.json | All modules | Tests |
| 38 | Device matrix | 23 | ADR-025 | device_matrix.schema.json | device_matrix.example.json | — | QA |
| 39 | CI/CD | 24 | — | quality_gate.schema.json | quality_gate.example.json | — | CI |
| 40 | Observability | 25 | ADR-024 | — | — | All modules | O11y |
| 41 | Environments | 26 | — | — | — | — | Infra |
| 42 | Code quality | 27 | — | — | — | All | Code |
| 43 | Git protocol | 28 | — | — | — | — | Delivery |
| 44 | Change control | 30 | ADR-026 | — | — | — | Governance |
| 45 | Vertical slice readiness | 29 | — | — | — | — | Sprint 1 |

---

## 3. ADR-to-Document Mapping

| ADR | Title | Affected Documents |
|-----|-------|-------------------|
| ADR-001 | Mobile Framework | 07, 08 |
| ADR-002 | Backend Framework | 10 |
| ADR-003 | Modular Monolith | 10, 11 |
| ADR-004 | PostgreSQL Source of Truth | 13 |
| ADR-005 | Background Job Mechanism | 10 |
| ADR-006 | Object Storage | 17, 26 |
| ADR-007 | Authentication Strategy | 14 |
| ADR-008 | AI Gateway Abstraction | 15 |
| ADR-009 | Structured Output Validation | 15, 16 |
| ADR-010 | Deterministic Mastery & Rewards | 11, 16 |
| ADR-011 | Audit Architecture | 25 |
| ADR-012 | Observability Stack | 25 |
| ADR-013 | Zustand for Local State | 08 |
| ADR-014 | Supported Mobile Platforms | 01, 23 |
| ADR-015 | Responsive Layout Policy | 02 |
| ADR-016 | Design System Token Architecture | 04, 05 |
| ADR-017 | Navigation Architecture | 06 |
| ADR-018 | Frontend Feature Architecture | 07 |
| ADR-019 | API Versioning and Error Contract | 09, 12 |
| ADR-020 | Database Migration Policy | 13 |
| ADR-021 | Supabase Auth Boundary | 14 |
| ADR-022 | Audio Storage and Processing | 17 |
| ADR-023 | Offline and Sync Policy | 19 |
| ADR-024 | Mobile Observability | 25 |
| ADR-025 | Device Acceptance Strategy | 23 |
| ADR-026 | Implementation Change Control | 30 |

---

## 4. Schema-to-Document Mapping

| Schema | Document | Purpose |
|--------|----------|---------|
| `design_tokens.schema.json` | 04 | Validate design token structure |
| `device_matrix.schema.json` | 23 | Validate device test matrix entries |
| `frontend_module.schema.json` | 07 | Validate frontend module definition |
| `backend_module.schema.json` | 11 | Validate backend module definition |
| `api_convention.schema.json` | 12 | Validate API endpoint conventions |
| `database_convention.schema.json` | 13 | Validate database convention rules |
| `test_requirement.schema.json` | 22 | Validate test requirement definitions |
| `quality_gate.schema.json` | 24 | Validate quality gate definitions |
| `implementation_proof.schema.json` | 31 | Validate proof JSON structure |
