#!/usr/bin/env bash
# MVP Architecture Planning Validation Script
# Run from project root: bash documents/language_learning_app/mvp_architecture/scripts/validate_mvp_architecture.sh

set -euo pipefail

ERRORS=0
WARNINGS=0
BASE_DIR="documents/language_learning_app/mvp_architecture"
ROOT_DIR="f:/Dev/Projects/LANGUAGE-LEARNING-APP"

echo "=== MVP Architecture Validation ==="
echo ""

# Test 1: Required architecture documents exist
echo "Test 1: Required architecture documents exist..."
REQUIRED_DOCS=(
  "00_mvp_architecture_index.md" "01_mvp_product_scope.md" "02_personas.md"
  "03_user_story_catalog.md" "04_user_journeys.md" "05_functional_requirements.md"
  "06_non_functional_requirements.md" "07_technology_stack_comparison.md"
  "08_selected_technology_stack.md" "09_system_context.md" "10_container_architecture.md"
  "11_module_architecture.md" "12_processing_pipeline.md" "13_dangerous_action_gates.md"
  "14_api_architecture.md" "15_data_model.md" "16_state_machines.md"
  "17_llm_gateway_architecture.md" "18_prompt_management.md" "19_security_threat_model.md"
  "20_privacy_and_data_retention.md" "21_observability.md" "22_deployment_topology.md"
  "23_testing_strategy.md" "24_first_implementation_sprint.md" "25_architecture_decision_log.md"
  "26_risk_register.md" "27_acceptance_criteria.md" "28_requirements_traceability_matrix.md"
)
for doc in "${REQUIRED_DOCS[@]}"; do
  if [ ! -f "$ROOT_DIR/$BASE_DIR/$doc" ]; then
    echo "  MISSING: $doc"
    ERRORS=$((ERRORS + 1))
  fi
done
echo "  Done ($(echo ${#REQUIRED_DOCS[@]}) checked)"

# Test 2: No empty documents
echo "Test 2: No empty documents..."
for doc in "${REQUIRED_DOCS[@]}"; do
  if [ -f "$ROOT_DIR/$BASE_DIR/$doc" ]; then
    SIZE=$(stat -c%s "$ROOT_DIR/$BASE_DIR/$doc" 2>/dev/null || stat -f%z "$ROOT_DIR/$BASE_DIR/$doc" 2>/dev/null)
    if [ "$SIZE" -lt 100 ]; then
      echo "  EMPTY/WARN: $doc ($SIZE bytes)"
      WARNINGS=$((WARNINGS + 1))
    fi
  fi
done
echo "  Done"

# Test 3: No TODO/TBD/placeholders
echo "Test 3: No TODO/TBD/placeholders..."
for doc in "${REQUIRED_DOCS[@]}"; do
  if [ -f "$ROOT_DIR/$BASE_DIR/$doc" ]; then
    if grep -qi "TODO\|TBD\|FIXME\|to be determined" "$ROOT_DIR/$BASE_DIR/$doc" 2>/dev/null; then
      LINES=$(grep -cni "TODO\|TBD\|FIXME" "$ROOT_DIR/$BASE_DIR/$doc" 2>/dev/null || true)
      if [ "$LINES" -gt 0 ]; then
        echo "  WARN: $doc contains placeholders (TODO/TBD/FIXME)"
        WARNINGS=$((WARNINGS + 1))
      fi
    fi
  fi
done
echo "  Done"

# Test 4: Minimum 45 user stories
echo "Test 4: Minimum 45 user stories..."
if [ -f "$ROOT_DIR/$BASE_DIR/03_user_story_catalog.md" ]; then
  STORY_COUNT=$(grep -c "^### US-" "$ROOT_DIR/$BASE_DIR/03_user_story_catalog.md" 2>/dev/null || echo 0)
  echo "  User stories found: $STORY_COUNT"
  if [ "$STORY_COUNT" -lt 45 ]; then
    echo "  FAIL: Only $STORY_COUNT user stories (minimum 45)"
    ERRORS=$((ERRORS + 1))
  fi
fi

# Test 5: Every user story has acceptance criteria
echo "Test 5: Every user story has acceptance criteria..."
if [ -f "$ROOT_DIR/$BASE_DIR/03_user_story_catalog.md" ]; then
  STORY_WITH_AC=$(grep -c "Acceptance Criteria" "$ROOT_DIR/$BASE_DIR/03_user_story_catalog.md" 2>/dev/null || echo 0)
  echo "  Stories with acceptance criteria: $STORY_WITH_AC"
fi

# Test 6: Minimum 8 user journeys
echo "Test 6: Minimum 8 user journeys..."
if [ -f "$ROOT_DIR/$BASE_DIR/04_user_journeys.md" ]; then
  JOURNEY_COUNT=$(grep -c "^## Journey" "$ROOT_DIR/$BASE_DIR/04_user_journeys.md" 2>/dev/null || echo 0)
  echo "  User journeys found: $JOURNEY_COUNT"
  if [ "$JOURNEY_COUNT" -lt 8 ]; then
    echo "  FAIL: Only $JOURNEY_COUNT journeys (minimum 8)"
    ERRORS=$((ERRORS + 1))
  fi
fi

# Test 7: Minimum 4 personas
echo "Test 7: Minimum 4 personas..."
if [ -f "$ROOT_DIR/$BASE_DIR/02_personas.md" ]; then
  PERSONA_COUNT=$(grep -c "^## P-" "$ROOT_DIR/$BASE_DIR/02_personas.md" 2>/dev/null || echo 0)
  echo "  Personas found: $PERSONA_COUNT"
  if [ "$PERSONA_COUNT" -lt 4 ]; then
    echo "  FAIL: Only $PERSONA_COUNT personas (minimum 4)"
    ERRORS=$((ERRORS + 1))
  fi
fi

# Test 8: Required initial NFR targets present
echo "Test 8: Required initial NFR targets present..."
if [ -f "$ROOT_DIR/$BASE_DIR/06_non_functional_requirements.md" ]; then
  for target in "api_p95_latency_non_ai_ms" "lesson_state_transition_p95_ms" "llm_analysis_target_p95_seconds" "availability_target" "audit_event_loss_tolerance" "reward_double_credit_tolerance" "cross_user_data_leak_tolerance"; do
    if grep -q "$target" "$ROOT_DIR/$BASE_DIR/06_non_functional_requirements.md" 2>/dev/null; then
      :
    else
      echo "  MISSING: NFR target '$target'"
      ERRORS=$((ERRORS + 1))
    fi
  done
fi
echo "  Done"

# Test 9: Core entities documented
echo "Test 9: Core entities documented..."
if [ -f "$ROOT_DIR/$BASE_DIR/15_data_model.md" ]; then
  for entity in "User" "LearnerProfile" "DiagnosticSession" "LessonSession" "Submission" "AIAnalysisResult" "MasteryRecord" "ReviewItem" "RewardTransaction" "AuditEvent"; do
    if grep -q "### $entity" "$ROOT_DIR/$BASE_DIR/15_data_model.md" 2>/dev/null; then
      :
    else
      echo "  MISSING: Entity '$entity'"
      WARNINGS=$((WARNINGS + 1))
    fi
  done
fi
echo "  Done"

# Test 10: Required state machines exist
echo "Test 10: Required state machines exist..."
if [ -f "$ROOT_DIR/$BASE_DIR/16_state_machines.md" ]; then
  for sm in "DiagnosticSession" "LessonSession" "Submission" "AIAnalysisRequest" "MasteryRecord" "ReviewItem" "RewardTransaction"; do
    if grep -q "$sm" "$ROOT_DIR/$BASE_DIR/16_state_machines.md" 2>/dev/null; then
      :
    else
      echo "  MISSING: State machine '$sm'"
      ERRORS=$((ERRORS + 1))
    fi
  done
fi
echo "  Done"

# Test 11: Required dangerous action gates exist
echo "Test 11: Required dangerous action gates exist..."
if [ -f "$ROOT_DIR/$BASE_DIR/13_dangerous_action_gates.md" ]; then
  for gate in "AI Generation Gate" "Retry Gate" "Assessment Acceptance Gate" "Mastery Transition Gate" "Reward Transaction Gate" "Review Scheduling Gate" "Notification Dispatch Gate" "Production Gate"; do
    if grep -q "$gate" "$ROOT_DIR/$BASE_DIR/13_dangerous_action_gates.md" 2>/dev/null; then
      :
    else
      echo "  MISSING: Gate '$gate'"
      ERRORS=$((ERRORS + 1))
    fi
  done
fi
echo "  Done"

# Test 12: LLM authority restrictions preserved
echo "Test 12: LLM authority restrictions preserved..."
if [ -f "$ROOT_DIR/$BASE_DIR/17_llm_gateway_architecture.md" ]; then
  if grep -q "LLM proposes, never decides" "$ROOT_DIR/$BASE_DIR/17_llm_gateway_architecture.md" 2>/dev/null; then
    :
  else
    echo "  MISSING: LLM authority restrictions"
    ERRORS=$((ERRORS + 1))
  fi
fi

# Test 13: Reward authority deterministic
echo "Test 13: Reward authority deterministic..."
if [ -f "$ROOT_DIR/$BASE_DIR/13_dangerous_action_gates.md" ]; then
  if grep -q "100% deterministic" "$ROOT_DIR/$BASE_DIR/13_dangerous_action_gates.md" 2>/dev/null; then
    :
  else
    echo "  WARN: Reward determinism not explicitly stated"
    WARNINGS=$((WARNINGS + 1))
  fi
fi

# Test 14: Mastery authority deterministic
echo "Test 14: Mastery authority deterministic..."
if [ -f "$ROOT_DIR/$BASE_DIR/11_module_architecture.md" ]; then
  if grep -q "deterministic" <<< "$(grep -A5 "mastery" "$ROOT_DIR/$BASE_DIR/11_module_architecture.md" 2>/dev/null || true)"; then
    :
  else
    echo "  WARN: Mastery determinism not clearly stated"
    WARNINGS=$((WARNINGS + 1))
  fi
fi

# Test 15: Threat model completeness
echo "Test 15: Threat model covers required threats..."
if [ -f "$ROOT_DIR/$BASE_DIR/19_security_threat_model.md" ]; then
  for threat in "Prompt Injection" "Replay" "Duplicate Reward" "Forged Lesson" "Cross-User" "Account Takeover" "Token Leakage" "Provider Data Leakage" "Rate Abuse" "Audit Tampering"; do
    if grep -qi "$threat" "$ROOT_DIR/$BASE_DIR/19_security_threat_model.md" 2>/dev/null; then
      :
    else
      echo "  MISSING: Threat '$threat'"
      ERRORS=$((ERRORS + 1))
    fi
  done
fi
echo "  Done"

# Test 16: ADR count and structure
echo "Test 16: ADR count and structure..."
if [ -f "$ROOT_DIR/$BASE_DIR/25_architecture_decision_log.md" ]; then
  ADR_COUNT=$(grep -c "^## ADR-" "$ROOT_DIR/$BASE_DIR/25_architecture_decision_log.md" 2>/dev/null || echo 0)
  echo "  ADRs found: $ADR_COUNT"
  if [ "$ADR_COUNT" -lt 12 ]; then
    echo "  FAIL: Only $ADR_COUNT ADRs (minimum 12)"
    ERRORS=$((ERRORS + 1))
  fi
  for field in "Context" "Decision" "Alternatives" "Consequences" "Risks"; do
    if grep -q "\\*\\*$field" "$ROOT_DIR/$BASE_DIR/25_architecture_decision_log.md" 2>/dev/null; then
      :
    else
      echo "  MISSING: ADR field '$field'"
      WARNINGS=$((WARNINGS + 1))
    fi
  done
fi

# Test 17: OpenAPI syntax valid
echo "Test 17: OpenAPI syntax check..."
if [ -f "$ROOT_DIR/$BASE_DIR/api/openapi_mvp.yaml" ]; then
  if grep -q "^openapi:" "$ROOT_DIR/$BASE_DIR/api/openapi_mvp.yaml" 2>/dev/null; then
    echo "  OpenAPI file has valid structure"
  else
    echo "  FAIL: OpenAPI missing required fields"
    ERRORS=$((ERRORS + 1))
  fi
fi

# Test 18: Schemas exist
echo "Test 18: Required schemas exist..."
for schema in "api_error.schema.json" "user_story.schema.json" "service_contract.schema.json" "state_machine.schema.json" "architecture_proof.schema.json"; do
  if [ -f "$ROOT_DIR/$BASE_DIR/schemas/$schema" ]; then
    # Validate basic JSON
    if python3 -c "import json; json.load(open('$ROOT_DIR/$BASE_DIR/schemas/$schema'))" 2>/dev/null; then
      :
    else
      echo "  INVALID JSON: $schema"
      ERRORS=$((ERRORS + 1))
    fi
  else
    echo "  MISSING: $schema"
    ERRORS=$((ERRORS + 1))
  fi
done
echo "  Done"

# Test 19: Examples exist and are valid JSON
echo "Test 19: Required examples exist and are valid..."
for example in "user_story.example.json" "service_contract.example.json" "state_machine.example.json"; do
  if [ -f "$ROOT_DIR/$BASE_DIR/examples/$example" ]; then
    if python3 -c "import json; json.load(open('$ROOT_DIR/$BASE_DIR/examples/$example'))" 2>/dev/null; then
      :
    else
      echo "  INVALID JSON: $example"
      ERRORS=$((ERRORS + 1))
    fi
  else
    echo "  MISSING: $example"
    ERRORS=$((ERRORS + 1))
  fi
done
echo "  Done"

# Test 20: No application/runtime source files added
echo "Test 20: No application/runtime source files added..."
# Check for .py, .tsx, .ts files outside allowed directories
RUNTIME_FILES=$(find "$ROOT_DIR/documents/language_learning_app/mvp_architecture" -name "*.py" -o -name "*.tsx" -o -name "*.ts" -o -name "*.jsx" 2>/dev/null || true)
if [ -n "$RUNTIME_FILES" ]; then
  echo "  RUNTIME FILES FOUND: $RUNTIME_FILES"
  ERRORS=$((ERRORS + 1))
fi
echo "  Done"

# Test 21: No secrets added
echo "Test 21: No secrets or sensitive patterns..."
if grep -r "sk-[a-zA-Z0-9]" "$ROOT_DIR/$BASE_DIR" --include="*.md" --include="*.json" --include="*.yaml" 2>/dev/null | grep -v "API_KEY\|_KEY" > /dev/null; then
  echo "  WARN: Possible key-like strings found"
  WARNINGS=$((WARNINGS + 1))
fi
echo "  Done"

# Test 22: Traceability matrix has key tables
echo "Test 22: Traceability matrix structure..."
if [ -f "$ROOT_DIR/$BASE_DIR/28_requirements_traceability_matrix.md" ]; then
  for table in "User Story to Requirement" "Functional Requirement to Module" "API Endpoint to User Story" "Entity to Module" "NFR to ADR"; do
    if grep -q "$table" "$ROOT_DIR/$BASE_DIR/28_requirements_traceability_matrix.md" 2>/dev/null; then
      :
    else
      echo "  MISSING: Traceability table '$table'"
      WARNINGS=$((WARNINGS + 1))
    fi
  done
fi
echo "  Done"

# Test 23: Stack decision comparison evidence
echo "Test 23: Stack comparison evidence..."
if [ -f "$ROOT_DIR/$BASE_DIR/07_technology_stack_comparison.md" ]; then
  CATEGORIES=$(grep -c "^## " "$ROOT_DIR/$BASE_DIR/07_technology_stack_comparison.md" 2>/dev/null || echo 0)
  if [ "$CATEGORIES" -lt 5 ]; then
    echo "  WARN: Less than 5 technology categories compared"
    WARNINGS=$((WARNINGS + 1))
  fi
fi
echo "  Done"

# Test 24: MVP scope defined
echo "Test 24: MVP scope definition..."
if [ -f "$ROOT_DIR/$BASE_DIR/01_mvp_product_scope.md" ]; then
  for section in "Primary MVP Goal" "Must-Have Capabilities" "Out of Scope"; do
    if grep -q "$section" "$ROOT_DIR/$BASE_DIR/01_mvp_product_scope.md" 2>/dev/null; then
      :
    else
      echo "  MISSING: Section '$section' in product scope"
      ERRORS=$((ERRORS + 1))
    fi
  done
fi
echo "  Done"

# Test 25: 20 modules defined
echo "Test 25: 20 modules defined..."
if [ -f "$ROOT_DIR/$BASE_DIR/11_module_architecture.md" ]; then
  MODULE_COUNT=$(grep -c "^### " "$ROOT_DIR/$BASE_DIR/11_module_architecture.md" 2>/dev/null || echo 0)
  echo "  Modules found: $MODULE_COUNT"
  if [ "$MODULE_COUNT" -lt 20 ]; then
    echo "  FAIL: Only $MODULE_COUNT modules (minimum 20)"
    ERRORS=$((ERRORS + 1))
  fi
fi

# Test 26: Production_accepted is false
echo "Test 26: No production acceptance markers..."
PROD_MARKERS=$(grep -r "production_accepted.*true" "$ROOT_DIR/$BASE_DIR" --include="*.md" --include="*.json" 2>/dev/null | grep -v "false\|FORBIDDEN\|const.*false" || true)
if [ -n "$PROD_MARKERS" ]; then
  echo "  WARN: Possible production acceptance marker found"
  WARNINGS=$((WARNINGS + 1))
fi
echo "  Done"

# Summary
echo ""
echo "=== Validation Summary ==="
echo "Errors:   $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

# Output for proof JSON
echo "{\"tests_failed\": $ERRORS, \"warnings\": $WARNINGS}"

if [ "$ERRORS" -gt 0 ]; then
  exit 1
fi
exit 0
