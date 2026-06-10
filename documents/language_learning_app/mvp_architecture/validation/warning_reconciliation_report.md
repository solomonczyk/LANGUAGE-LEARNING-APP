# Warning Reconciliation Report

**Task:** LANGUAGE-LEARNING-APP-MVP-ARCHITECTURE-PLANNING-002A  
**Parent Task:** LANGUAGE-LEARNING-APP-MVP-ARCHITECTURE-PLANNING-002  
**Date:** 2026-06-10  
**Status:** COMPLETED  

---

## 1. Warning Classification Table

| Warning ID | Validator | File | Trigger | Classification | Root Cause | Resolution |
|---|---|---|---|---|---|---|
| W-001 | Test 3 | `00_mvp_architecture_index.md` | Line 85: "no TODO, TBD, empty sections" in governance rules | FALSE POSITIVE | Validator regex `TODO\|TBD\|FIXME` matches governance prose that *describes* the placeholder rule, not actual placeholder content | Updated Test 3 to subtract governance reference lines matching `no TODO`, `TODO/TBD`, `none left as`, `no TBD` before counting actual placeholders |
| W-002 | Test 3 | `27_acceptance_criteria.md` | Line 32: "none left as TODO/TBD" in AC-09 criterion description | FALSE POSITIVE | Same root cause as W-001 — regex matches governance/ac-criterion text that references placeholder rules | Same resolution as W-001 (shared fix in Test 3) |
| W-003 | Test 26 | `13_dangerous_action_gates.md` | Line 196: "Setting `production_accepted=true` violates the MVP architecture planning contract" | FALSE POSITIVE | Existing `grep -v` filter excludes lines with `false`, `FORBIDDEN`, `const.*false` but line 196 uses "violates" instead of "FORBIDDEN" | Added `violates` to the `grep -v` exclusion pattern in Test 26 |

---

## 2. Corrections Performed

### Validator Fix 1: Test 3 — TODO/TBD placeholder detection refined

**File:** `scripts/validate_mvp_architecture.sh`

**Change:** Replaced simple `grep -qi` check with a two-pass subtraction:

```bash
# Before (overly broad):
if grep -qi "TODO\|TBD\|FIXME\|to be determined" ...; then
  LINES=$(grep -cni "TODO\|TBD\|FIXME" ...)
  if [ "$LINES" -gt 0 ]; then
    echo "WARN: ..."
  fi
fi

# After (excludes governance references):
TOTAL=$(grep -cni "TODO\|TBD\|FIXME" ... || true)
FP=$(grep -cni "no TODO\|TODO/TBD\|none left as\|no TBD" ... || true)
ACTUAL=$(( ${TOTAL:-0} - ${FP:-0} ))
if [ "$ACTUAL" -gt 0 ]; then
  echo "WARN: ..."
fi
```

**Rationale:** Governance documents describing the "no TBD" rule contain the word "TBD" in their prose. These are not actual placeholders. The exclusion patterns match such governance references while still detecting real placeholders like `TODO: implement`, `TBD: value`, or `FIXME: bug`.

### Validator Fix 2: Test 26 — Production acceptance marker exclusion expanded

**File:** `scripts/validate_mvp_architecture.sh`

**Change:** Added `violates` to the `grep -v` exclusion pattern:

```bash
# Before:
| grep -v "false\|FORBIDDEN\|const.*false"
# After:
| grep -v "false\|FORBIDDEN\|const.*false\|violates"
```

**Rationale:** Line 196 in `13_dangerous_action_gates.md` describes the consequence of setting `production_accepted=true` using the word "violates" rather than "FORBIDDEN". The text is documenting the prohibition, not actually setting the flag.

---

## 3. Regression Tests

All 4 regression tests created in `scripts/test_regression.sh`:

| Test | Type | Fixture | Expected | Actual | Status |
|---|---|---|---|---|---|
| R1 | Positive | `fixture_todo_placeholder.md` — actual TODO/TBD/FIXME | Warning triggered | 5 placeholders detected | PASS |
| R2 | Negative | `fixture_governance_reference.md` — governance "no TODO, TBD" text | No warning | 2 matches, 2 correctly excluded | PASS |
| R3 | Negative | `fixture_production_forbidden.md` — "production_accepted=true is FORBIDDEN / violates" | No warning | Correctly excluded | PASS |
| R4 | Positive | `fixture_production_real.md` — literal `production_accepted=true` | Warning triggered | Correctly detected | PASS |

**Fixtures directory:** `scripts/tests/`

---

## 4. Full Validation Suite Results

After all fixes were applied:

```json
{
  "tests_total": 26,
  "tests_passed": 26,
  "tests_failed": 0,
  "warnings": 0,
  "openapi_valid": true,
  "schemas_valid": true,
  "artifact_index_valid": true,
  "traceability_valid": true
}
```

---

## 5. Forbidden Action Scan

| Forbidden Action | Result |
|---|---|
| Application code changed | false |
| Runtime code added | false |
| Real LLM calls executed | false |
| Deployment executed | false |
| Production modified | false |
| Staging modified | false |
| Secrets added | false |

Only validation scripts and documentation were modified.

---

## 6. Proof JSON

- **002 proof:** `proof_language_learning_app_mvp_architecture_planning_002.json` (updated)
- **002A proof:** `proof_language_learning_app_mvp_architecture_planning_002a.json` (created)

---

## 7. Verdict

**ACCEPTED**

All acceptance criteria met:
- [x] All 3 warnings classified (all FALSE POSITIVE)
- [x] Root cause of each warning documented
- [x] False positives fixed in validator
- [x] Regression tests added (positive + negative for each fix)
- [x] Real violations still detected (verified with positive fixtures)
- [x] Full validation suite: 26 tests, 0 failed, 0 warnings
- [x] OpenAPI valid
- [x] Schemas valid
- [x] Artifact index valid
- [x] Traceability complete
- [x] Application/runtime code unchanged
- [x] No unresolved blockers

Next allowed action: `first_mvp_vertical_slice_implementation`
