# Alpha 006A — Diagnostic Interaction Recovery

## Purpose
Fix the diagnostic interaction blocker discovered during manual visual review of Alpha 006. All diagnostic steps are now interactive, user-driven, and do not prefill correct answers.

## Change Summary
| Area | Before | After |
|------|--------|-------|
| Grammar options | Non-interactive `<View>`, correct answer shown | Interactive `<Pressable>`, selection state, feedback after submit |
| Vocabulary | Static demo text, no interaction | 4-word multiple-choice, per-question selection |
| Written production | Already interactive (TextInput) — unchanged | Kept interactive, feedback after submit |
| Narrative coherence | Pre-ordered static list | Tap-to-order from scrambled display |
| Answer submission | Hardcoded `{is_correct: true}` | Actual user selection sent to backend |
| Demo/Example separation | "Example only" badge mixed with real tasks | No demo content — all steps are real interactive tasks |

## Files Changed
- `mobile/app/diagnostic.tsx` — Full rewrite of interaction model
- `backend/tests/unit/test_diagnostics.py` — Added 4 backward-compatibility tests

## Acceptance
Refer to [proof_language_learning_app_alpha_006a.json](proof_language_learning_app_alpha_006a.json)

## Artifacts
- [01 Diagnostic Section Audit](01_diagnostic_section_audit.md)
- [02 Interaction Model Recovery](02_interaction_model_recovery.md)
- [03 Example Demo Rules](03_example_demo_rules.md)
- [04 Backend State Recheck](04_backend_state_recheck.md)
- [05 Visual Recheck Report](05_visual_recheck_report.md)
- [06 Test Results](06_test_results.md)
- [07 Alpha 006 Supersession](07_alpha_006_supersession_report.md)
- [Artifact Index](alpha_006a_artifact_index.json)
- [Proof JSON](proof_language_learning_app_alpha_006a.json)
- [Screenshots](evidence/screenshots/)
- [Test Outputs](evidence/test_outputs/)
- [Backend Logs](evidence/backend_logs/)
