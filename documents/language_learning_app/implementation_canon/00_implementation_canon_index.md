# Implementation Canon Index

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  
**Task:** LANGUAGE-LEARNING-APP-IMPLEMENTATION-CANON-AND-READINESS-002B

---

## Purpose

This index provides a complete map of the Implementation Canon — the authoritative specification layer that fixes all mandatory development rules before any runtime implementation begins. Every document listed here is a **binding rule** that future implementation tasks must follow.

Once accepted, future implementation tasks (starting with `003`) **must** reference this canon and **cannot** unilaterally change the decisions fixed here. Changes require a new ADR following the [change control policy](30_change_control_and_adr_policy.md).

---

## Canon dependency structure

```
00_implementation_canon_index.md
├── 01_supported_platforms_and_devices.md        ← Platform decisions
├── 02_mobile_responsive_layout_canon.md         ← Layout rules
├── 03_mobile_platform_behaviour.md              ← OS-specific rules
├── 04_design_system.md                          ← Design tokens + components
├── 05_accessibility_and_localization.md         ← a11y + i18n rules
├── 06_navigation_and_route_canon.md             ← Route map + guards
├── 07_frontend_architecture.md                  ← Frontend structure
├── 08_frontend_state_management.md              ← Zustand + TanStack Query
├── 09_frontend_api_and_error_handling.md        ← API client + errors
├── 10_backend_architecture.md                   ← Backend structure
├── 11_backend_module_and_dependency_rules.md    ← Module boundaries
├── 12_api_design_canon.md                       ← API contract conventions
├── 13_database_and_migration_canon.md           ← DB conventions
├── 14_authentication_and_authorization.md       ← Supabase Auth
├── 15_ai_gateway_runtime_canon.md               ← AI Gateway contract
├── 16_dangerous_action_gates.md                 ← Control gates
├── 17_audio_and_media_canon.md                  ← Audio handling
├── 18_notifications_and_reminders.md            ← Notification rules
├── 19_offline_sync_and_recovery.md              ← Offline policy
├── 20_security_implementation_canon.md          ← Security controls
├── 21_privacy_and_data_handling.md              ← Privacy rules
├── 22_testing_canon.md                          ← Test requirements
├── 23_mobile_device_acceptance_matrix.md        ← Device testing
├── 24_ci_cd_and_quality_gates.md               ← CI/CD requirements
├── 25_observability_and_audit.md                ← Observability
├── 26_environment_and_configuration_canon.md    ← Environment defs
├── 27_code_quality_and_repository_conventions.md ← Code standards
├── 28_git_delivery_and_feature_closeout.md      ← Git protocol
├── 29_first_vertical_slice_readiness.md         ← Readiness review
├── 30_change_control_and_adr_policy.md          ← ADR policy
├── 31_implementation_acceptance_criteria.md     ← Acceptance criteria
├── 32_implementation_traceability_matrix.md     ← Traceability
├── 33_risk_register.md                          ← Risks
├── architecture_decision_log.md                 ← ADR-013 through ADR-026
└── implementation_artifact_index.json           ← Artifact registry
```

---

## Canon documents

| # | Document | Path | Status |
|---|----------|------|--------|
| 00 | Implementation Canon Index | `00_implementation_canon_index.md` | ✅ Accepted |
| 01 | Supported Platforms and Devices | `01_supported_platforms_and_devices.md` | ✅ Accepted |
| 02 | Mobile Responsive Layout Canon | `02_mobile_responsive_layout_canon.md` | ✅ Accepted |
| 03 | Mobile Platform Behaviour | `03_mobile_platform_behaviour.md` | ✅ Accepted |
| 04 | Design System | `04_design_system.md` | ✅ Accepted |
| 05 | Accessibility and Localization | `05_accessibility_and_localization.md` | ✅ Accepted |
| 06 | Navigation and Route Canon | `06_navigation_and_route_canon.md` | ✅ Accepted |
| 07 | Frontend Architecture | `07_frontend_architecture.md` | ✅ Accepted |
| 08 | Frontend State Management | `08_frontend_state_management.md` | ✅ Accepted |
| 09 | Frontend API and Error Handling | `09_frontend_api_and_error_handling.md` | ✅ Accepted |
| 10 | Backend Architecture | `10_backend_architecture.md` | ✅ Accepted |
| 11 | Backend Module and Dependency Rules | `11_backend_module_and_dependency_rules.md` | ✅ Accepted |
| 12 | API Design Canon | `12_api_design_canon.md` | ✅ Accepted |
| 13 | Database and Migration Canon | `13_database_and_migration_canon.md` | ✅ Accepted |
| 14 | Authentication and Authorization | `14_authentication_and_authorization.md` | ✅ Accepted |
| 15 | AI Gateway Runtime Canon | `15_ai_gateway_runtime_canon.md` | ✅ Accepted |
| 16 | Dangerous Action Gates | `16_dangerous_action_gates.md` | ✅ Accepted |
| 17 | Audio and Media Canon | `17_audio_and_media_canon.md` | ✅ Accepted |
| 18 | Notifications and Reminders | `18_notifications_and_reminders.md` | ✅ Accepted |
| 19 | Offline Sync and Recovery | `19_offline_sync_and_recovery.md` | ✅ Accepted |
| 20 | Security Implementation Canon | `20_security_implementation_canon.md` | ✅ Accepted |
| 21 | Privacy and Data Handling | `21_privacy_and_data_handling.md` | ✅ Accepted |
| 22 | Testing Canon | `22_testing_canon.md` | ✅ Accepted |
| 23 | Mobile Device Acceptance Matrix | `23_mobile_device_acceptance_matrix.md` | ✅ Accepted |
| 24 | CI/CD and Quality Gates | `24_ci_cd_and_quality_gates.md` | ✅ Accepted |
| 25 | Observability and Audit | `25_observability_and_audit.md` | ✅ Accepted |
| 26 | Environment and Configuration Canon | `26_environment_and_configuration_canon.md` | ✅ Accepted |
| 27 | Code Quality and Repository Conventions | `27_code_quality_and_repository_conventions.md` | ✅ Accepted |
| 28 | Git Delivery and Feature Closeout | `28_git_delivery_and_feature_closeout.md` | ✅ Accepted |
| 29 | First Vertical Slice Readiness | `29_first_vertical_slice_readiness.md` | ✅ Accepted |
| 30 | Change Control and ADR Policy | `30_change_control_and_adr_policy.md` | ✅ Accepted |
| 31 | Implementation Acceptance Criteria | `31_implementation_acceptance_criteria.md` | ✅ Accepted |
| 32 | Implementation Traceability Matrix | `32_implementation_traceability_matrix.md` | ✅ Accepted |
| 33 | Risk Register | `33_risk_register.md` | ✅ Accepted |

---

## Supporting artifacts

| Type | Path | Count |
|------|------|-------|
| Schemas | `schemas/*.json` | 9 |
| Examples | `examples/*.json` | 6 |
| ADRs | `architecture_decision_log.md` | 14 (ADR-013–ADR-026) |
| Artifact Index | `implementation_artifact_index.json` | 1 |
| Proof JSON | `proof_language_learning_app_implementation_canon_002b.json` | 1 |

---

## Related documents

This canon builds on:

- [Canonical Documentation Foundation](../00_documentation_index.md) — Product, methodology, architecture, security foundations
- [MVP Architecture Planning](../mvp_architecture/00_mvp_architecture_index.md) — MVP scope, user stories, module definitions

---

## Governance

Every document in this canon MUST:

1. Have a unique numeric prefix consistent with this index
2. Be listed in this index on creation
3. Be registered in `implementation_artifact_index.json`
4. Have no placeholder content (no TODO, TBD, empty sections, "later" statements)
5. Make definitive decisions — no alternatives left unresolved
6. Reference the relevant ADR(s) for each major decision
7. Be validated by the implementation canon validation suite
8. Be linked in the traceability matrix
9. Be consistent with all other implementation canon documents
10. Preserve the rule: this canon cannot be changed by future feature tasks without a new ADR

## Change log

| Date | Version | Change |
|------|---------|--------|
| 2026-06-10 | 1.0.0 | Initial implementation canon created for task 002B |
