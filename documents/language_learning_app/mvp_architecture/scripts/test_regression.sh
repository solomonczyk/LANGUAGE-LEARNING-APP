#!/usr/bin/env bash
# Regression Tests for MVP Architecture Validation
# Validates that false positive fixes don't mask real violations
# Run from project root: bash documents/language_learning_app/mvp_architecture/scripts/test_regression.sh

set -euo pipefail

PASSED=0
FAILED=0
BASE_DIR="documents/language_learning_app/mvp_architecture"
ROOT_DIR="f:/Dev/Projects/LANGUAGE-LEARNING-APP"

echo "=== Regression Tests ==="
echo ""

# Test R1: Positive fixture — actual TODO should trigger warning
echo "R1: Positive — actual TODO placeholder triggers warning..."
RESULT=$(grep -cni "TODO\|TBD\|FIXME\|to be determined" "$ROOT_DIR/$BASE_DIR/scripts/tests/fixture_todo_placeholder.md" 2>/dev/null || true)
TOTAL=${RESULT:-0}
FP=$(grep -cni "no TODO\|TODO/TBD\|none left as\|no TBD" "$ROOT_DIR/$BASE_DIR/scripts/tests/fixture_todo_placeholder.md" 2>/dev/null || true)
FP=${FP:-0}
ACTUAL=$((TOTAL - FP))
if [ "$ACTUAL" -gt 0 ]; then
  echo "  PASS: Detected $ACTUAL placeholder(s) in fixture"
  PASSED=$((PASSED + 1))
else
  echo "  FAIL: Did not detect actual placeholders"
  FAILED=$((FAILED + 1))
fi

# Test R2: Negative fixture — governance reference should NOT trigger warning
echo "R2: Negative — governance reference to TBD does not trigger warning..."
TOTAL2=$(grep -cni "TODO\|TBD\|FIXME\|to be determined" "$ROOT_DIR/$BASE_DIR/scripts/tests/fixture_governance_reference.md" 2>/dev/null || true)
TOTAL2=${TOTAL2:-0}
FP2=$(grep -cni "no TODO\|TODO/TBD\|none left as\|no TBD" "$ROOT_DIR/$BASE_DIR/scripts/tests/fixture_governance_reference.md" 2>/dev/null || true)
FP2=${FP2:-0}
ACTUAL2=$((TOTAL2 - FP2))
if [ "$ACTUAL2" -eq 0 ]; then
  echo "  PASS: Governance reference correctly excluded ($TOTAL2 matches, $FP2 excluded as false positive)"
  PASSED=$((PASSED + 1))
else
  echo "  FAIL: Governance reference incorrectly flagged ($ACTUAL2 actual)"
  FAILED=$((FAILED + 1))
fi

# Test R3: Negative fixture — production gate FORBIDDEN should not trigger warning
echo "R3: Negative — production gate FORBIDDEN reference does not trigger warning..."
RESULT3=$(grep -r "production_accepted.*true" "$ROOT_DIR/$BASE_DIR/scripts/tests/fixture_production_forbidden.md" 2>/dev/null || true)
RESULT3=$(echo "$RESULT3" | grep -v "false\|FORBIDDEN\|const.*false\|violates" || true)
if [ -z "$RESULT3" ]; then
  echo "  PASS: Production-forbidden reference correctly excluded"
  PASSED=$((PASSED + 1))
else
  echo "  FAIL: Production-forbidden reference incorrectly flagged"
  echo "  Filtered output: $RESULT3"
  FAILED=$((FAILED + 1))
fi

# Test R4: Positive fixture — real production_accepted=true should trigger warning
echo "R4: Positive — actual production_accepted=true triggers warning..."
RESULT4=$(grep -r "production_accepted.*true" "$ROOT_DIR/$BASE_DIR/scripts/tests/fixture_production_real.md" 2>/dev/null || true)
RESULT4=$(echo "$RESULT4" | grep -v "false\|FORBIDDEN\|const.*false\|violates" || true)
if [ -n "$RESULT4" ]; then
  echo "  PASS: Detected real production_accepted=true marker"
  PASSED=$((PASSED + 1))
else
  echo "  FAIL: Did not detect real production_accepted=true marker"
  FAILED=$((FAILED + 1))
fi

# Summary
echo ""
echo "=== Regression Test Summary ==="
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo ""

if [ "$FAILED" -gt 0 ]; then
  exit 1
fi
exit 0
