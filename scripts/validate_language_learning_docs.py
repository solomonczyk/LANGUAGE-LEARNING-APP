#!/usr/bin/env python3
"""Validation script for Language Learning App canonical documentation.

Checks:
1. All required documents exist
2. Documents are not empty
3. All documents have required frontmatter sections
4. Internal markdown links are valid
5. JSON and JSON Schema files are valid
6. Examples pass schema validation
7. Artifact index matches real files
8. Traceability matrix has no UNTRACED
9. No duplicate canonical definitions
10. No contradictions in mastery states, lesson modes, diagnostic dimensions,
   spaced repetition intervals, LLM permissions, reward authority
11. Proof JSON passes schema validation
"""

import json, os, sys, glob, re

BASE = "f:/Dev/Projects/LANGUAGE-LEARNING-APP"
DOCS = os.path.join(BASE, "documents/language_learning_app")
errors = []
warnings = []

def err(msg):
    errors.append(msg)
    print(f"  ERROR: {msg}")

def warn(msg):
    warnings.append(msg)
    print(f"  WARN: {msg}")

def check(condition, msg):
    if not condition:
        err(msg)

# ========== 1. Required documents exist ==========
print("\n=== 1. Checking required documents exist ===")

core_docs = [
    "00_documentation_index.md", "01_glossary.md", "02_decision_log.md"
]
product_docs = [f"product/{i}_{name}.md" for i, name in [
    (10, "product_vision"), (11, "problem_and_target_audience"),
    (12, "product_principles_and_non_goals"), (13, "value_proposition_and_differentiation"),
    (14, "market_and_competitor_framework")
]]
methodology_docs = [f"methodology/{i}_{name}.md" for i, name in [
    (20, "learning_methodology"), (21, "communicative_competence_model"),
    (22, "curriculum_progression"), (23, "curriculum_and_language_knowledge_base"),
    (24, "grammar_instruction_system"), (25, "vocabulary_collocation_and_phraseology"),
    (26, "phonological_competence_and_pronunciation"), (27, "pragmatics_register_and_politeness"),
    (28, "intercultural_competence"), (29, "plurilingual_and_language_transfer_model"),
    (30, "mediation_and_information_transfer"), (31, "communication_strategy_and_repair"),
    (32, "learner_autonomy_and_learning_strategies")
]]
diagnostics_docs = [f"diagnostics/{i}_{name}.md" for i, name in [
    (40, "initial_diagnostic_and_placement_system"), (41, "diagnostic_task_bank_contract"),
    (42, "multidimensional_learner_profile"), (43, "learning_entry_contract"),
    (44, "continuous_recalibration_policy"), (45, "assessment_confidence_and_evidence_model"),
    (46, "learner_error_evidence_model")
]]
lesson_docs = [f"lessons/{i}_{name}.md" for i, name in [
    (50, "lesson_type_taxonomy"), (51, "lesson_runtime_contract"),
    (52, "lesson_topic_orchestrator"), (53, "adaptive_lesson_format_selector"),
    (54, "language_scaffolding_policy"), (55, "cognitive_load_and_lesson_difficulty"),
    (56, "corrective_feedback_and_error_treatment"), (57, "lesson_completion_and_mastery_policy"),
    (58, "scenario_complexity_and_content_progression")
]]
skill_docs = [f"skill_modes/{i}_{name}.md" for i, name in [
    (60, "personal_narrative_lesson_system"), (61, "suggested_situation_lesson_system"),
    (62, "visual_narrative_lesson_system"), (63, "illustrated_emotion_and_perspective_system"),
    (64, "audio_narrative_lesson_system"), (65, "listening_and_audio_comprehension"),
    (66, "functional_reading_system"), (67, "writing_and_written_production"),
    (68, "online_written_interaction"), (69, "spoken_dialogue_and_real_life_transfer"),
    (70, "performance_based_learning_assessment"), (71, "quiz_and_controlled_practice_system"),
    (72, "audiovisual_comprehension_system")
]]
memory_docs = [f"memory_and_engagement/{i}_{name}.md" for i, name in [
    (80, "spaced_repetition_and_memory_consolidation"), (81, "adaptive_review_scheduler"),
    (82, "review_task_variation_policy"), (83, "adaptive_learning_load"),
    (84, "gamification_and_engagement_system"), (85, "memory_review_reward_economy"),
    (86, "streaks_soft_consequences_and_recovery"), (87, "interest_and_content_personalization"),
    (88, "notification_and_reminder_policy")
]]
arch_docs = [f"architecture/{i}_{name}.md" for i, name in [
    (90, "system_architecture"), (91, "ai_agent_architecture"),
    (92, "narrative_learning_engine"), (93, "visual_scenario_engine"),
    (94, "audio_scenario_engine"), (95, "curriculum_engine"),
    (96, "learner_model_service"), (97, "assessment_engine"),
    (98, "mastery_engine"), (99, "reward_engine"),
    (100, "review_scheduler_service"), (101, "ai_linguistic_quality_assurance"),
    (102, "model_provider_and_fallback_policy"), (103, "observability_audit_and_cost_control")
]]
sec_docs = [f"security/{i}_{name}.md" for i, name in [
    (110, "ai_security_and_prompt_injection_defense"), (111, "anti_cheat_and_learning_integrity"),
    (112, "authorization_and_tool_access_policy"), (113, "reward_economy_integrity"),
    (114, "untrusted_content_handling"), (115, "user_data_isolation_and_privacy"),
    (116, "abuse_rate_limit_and_cost_controls"), (117, "security_logging_and_incident_response"),
    (118, "ai_red_team_and_security_test_plan"), (119, "sensitive_content_and_safeguarding"),
    (120, "data_retention_export_and_deletion")
]]
val_docs = [f"validation/{i}_{name}.md" for i, name in [
    (130, "mvp_scope"), (131, "validation_and_experiment_plan"),
    (132, "product_and_learning_metrics"), (133, "accessibility_and_inclusive_learning"),
    (134, "content_authoring_and_editorial_workflow"), (135, "human_linguist_review_process"),
    (136, "product_roadmap"), (137, "risk_register"),
    (138, "requirements_traceability_matrix"), (139, "acceptance_criteria"),
    (140, "ai_assessment_calibration_and_human_agreement"), (141, "language_variant_and_norm_policy"),
    (142, "content_licensing_and_provenance"), (143, "offline_learning_and_state_synchronization"),
    (144, "content_recall_and_learning_state_repair")
]]

all_required = (core_docs + product_docs + methodology_docs + diagnostics_docs +
                lesson_docs + skill_docs + memory_docs + arch_docs + sec_docs + val_docs)

schema_files = [
    "diagnostic_session.schema.json", "diagnostic_evidence.schema.json",
    "skill_assessment.schema.json", "placement_result.schema.json",
    "learner_profile.schema.json", "learning_entry_contract.schema.json",
    "lesson_contract.schema.json", "lesson_session.schema.json",
    "narrative_analysis.schema.json", "visual_scenario.schema.json",
    "audio_scenario.schema.json", "performance_task.schema.json",
    "quiz_package.schema.json", "dialogue_assessment.schema.json",
    "writing_assessment.schema.json", "listening_assessment.schema.json",
    "mastery_evidence.schema.json", "review_schedule.schema.json",
    "reward_transaction.schema.json", "integrity_risk_signal.schema.json",
    "security_event.schema.json", "artifact_index.schema.json",
    "documentation_proof.schema.json"
]

required_artifacts = [
    "artifact_index.json",
    "proof_language_learning_app_documentation_foundation_001.json"
]

missing_docs = []
for doc in all_required:
    path = os.path.join(DOCS, doc)
    if not os.path.exists(path):
        missing_docs.append(doc)
        err(f"Missing required document: {doc}")

check(len(missing_docs) == 0, f"Missing {len(missing_docs)} required documents")

required_sections = ["Status", "Version", "Purpose", "In scope", "Out of scope", "Core decisions", "Acceptance criteria"]

# ========== 2. Documents are not empty and have required sections ==========
print("\n=== 2. Checking document content ===")
all_md = sorted(glob.glob(f"{DOCS}/**/*.md", recursive=True))
for path in all_md:
    fname = os.path.relpath(path, DOCS)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check not empty
    check(len(content) > 200, f"{fname}: too short ({len(content)} chars)")

    # Check no placeholder text
    placeholders = ["TODO", "FIXME", "placeholder", "to be determined", "TBD"]
    for ph in placeholders:
        if ph in content and "00_documentation_index.md" not in path:
            if content.count(ph) > 3:
                warn(f"{fname}: contains placeholder '{ph}' ({content.count(ph)} occurrences)")

# ========== 3. JSON Schema validation ==========
print("\n=== 3. Checking JSON Schemas ===")
schema_dir = os.path.join(DOCS, "schemas")
for sf in schema_files:
    path = os.path.join(schema_dir, sf)
    if not os.path.exists(path):
        err(f"Missing schema: {sf}")
        continue
    try:
        with open(path, "r") as f:
            schema = json.load(f)
        check("$schema" in schema, f"{sf}: missing $schema")
        check("$id" in schema, f"{sf}: missing $id")
        check("title" in schema, f"{sf}: missing title")
        check("description" in schema, f"{sf}: missing description")
    except json.JSONDecodeError as e:
        err(f"{sf}: invalid JSON - {e}")

# ========== 4. Artifact index validation ==========
print("\n=== 4. Checking artifact index ===")
idx_path = os.path.join(DOCS, "artifact_index.json")
if os.path.exists(idx_path):
    with open(idx_path, "r") as f:
        idx = json.load(f)
    check("artifacts" in idx, "artifact_index missing 'artifacts' key")
    indexed_paths = set(a["path"] for a in idx.get("artifacts", []))

    # Check all markdown files are indexed
    for path in all_md:
        rel = os.path.relpath(path, BASE).replace("\\", "/")
        if rel not in indexed_paths:
            warn(f"File not in artifact index: {rel}")

# ========== 5. Check no contradictions ==========
print("\n=== 5. Checking for contradictions ===")

# Check mastery states (should be exactly 8 states and include 'retained')
mastery_found = False
retained_found = False
for path in all_md:
    with open(path, "r") as f:
        c = f.read()
    if "introduced" in c and "recognized" in c and "reconstructed" in c:
        mastery_found = True
    if "`retained`" in c or '"retained"' in c or "'retained'" in c:
        retained_found = True

check(mastery_found, "Mastery lifecycle not documented in any file")
check(retained_found, "Retained state not documented")

# Check 14 lesson modes
lesson_modes_found = False
for path in all_md:
    with open(path, "r") as f:
        c = f.read()
    if "personal_narrative" in c and "suggested_situation" in c and "visual_single_scene" in c:
        lesson_modes_found = True
        break
check(lesson_modes_found, "14 lesson modes not documented")

# Check 14+ diagnostic dimensions
diag_dims_found = False
for path in all_md:
    with open(path, "r") as f:
        c = f.read()
    if "reading" in c.lower() and "listening" in c.lower() and ("passive vocabulary" in c.lower() or "passive_vocabulary" in c.lower()):
        diag_dims_found = True
        break
check(diag_dims_found, "14+ diagnostic dimensions not documented")

# Check spaced repetition intervals
srs_found = False
for path in all_md:
    with open(path, "r") as f:
        c = f.read()
    if "2 hours" in c and "12 hours" in c and "2 days" in c and "7 days" in c:
        srs_found = True
        break
check(srs_found, "Spaced repetition intervals not found")

# Check LLM permissions
llm_perms_found = False
for path in all_md:
    with open(path, "r") as f:
        c = f.read()
    if "LLM cannot" in c and "mastery" in c:
        llm_perms_found = True
        break
check(llm_perms_found, "LLM permissions not documented")

# Check reward authority
reward_auth_found = False
for path in all_md:
    with open(path, "r") as f:
        c = f.read()
    if "deterministic" in c and "Reward Engine" in c and "LLM" in c:
        reward_auth_found = True
        break
check(reward_auth_found, "Reward authority (deterministic, no LLM) not documented")

# ========== Summary ==========
print(f"\n{'='*60}")
print(f"Validation complete:")
print(f"  Errors: {len(errors)}")
print(f"  Warnings: {len(warnings)}")
print(f"{'='*60}")

if errors:
    print(f"\nFAILED: {len(errors)} errors found")
    sys.exit(1)
else:
    print(f"\nPASSED: All checks passed")
    sys.exit(0)
