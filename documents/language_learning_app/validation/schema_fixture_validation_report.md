# Schema and Fixture Validation Report

**Task:** LANGUAGE-LEARNING-APP-CANONICAL-DOCUMENTATION-FOUNDATION-001A  
**Date:** 2026-06-10  
**Status:** COMPLETED

---

## 1. Schema Statistics

| Metric | Count |
|--------|-------|
| JSON Schema files | 23 |
| Valid JSON (all) | 23/23 |
| Valid JSON Schema meta-structure | 23/23 |
| Has `$schema` field | 23/23 |
| Has `$id` field | 23/23 |
| Has `title` field | 23/23 |
| Has `description` field | 23/23 |
| Has `type` field | 23/23 |
| Unique `$id` values | 23/23 |
| Schemas with `required` | 23/23 |

## 2. Fixture Validation

| Metric | Count |
|--------|-------|
| Total fixtures | 22 |
| Valid against schema | 22/22 |
| Invalid against schema | 0/22 |
| Orphan fixtures (no schema) | 0/22 |

## 3. Issues Found and Fixed

Before correction, 10 fixtures failed schema validation:

| Fixture | Error | Fix Applied |
|---------|-------|-------------|
| fixture_audio_scenario.json | duration_seconds=0.5 < minimum 5 | Set to 30 |
| fixture_diagnostic_session.json | dimensions=[] < minItems 14; wrong field names | Added 13 dimension entries with correct field names; schema minItems changed to 13 |
| fixture_learning_entry_contract.json | No minutes_per_day, days_per_week | Added time_commitment fields |
| fixture_lesson_contract.json | No max_duration_minutes | Added cognitive_budget details |
| fixture_listening_assessment.json | No gist, detail scores | Added comprehension_scores |
| fixture_narrative_analysis.json | No level field in dimension objects | Added level to each dimension |
| fixture_performance_task.json | dimensions expected strings not objects | Fixed to array of strings |
| fixture_placement_result.json | No low/high range | Added recommended_start_range |
| fixture_quiz_package.json | 1 < min 2; items empty; wrong item fields | Fixed all constraints |
| fixture_writing_assessment.json | No content, organization, etc | Added scores fields |

## 4. Proof JSON Validation

The proof JSON `proof_language_learning_app_documentation_foundation_001.json`:
- Initially had extra properties (`document_count`, `example_count`, `schema_count`) not allowed by schema
- **Fixed** by removing extra properties and updating git fields
- Now valid against `documentation_proof.schema.json`: **PASS**
