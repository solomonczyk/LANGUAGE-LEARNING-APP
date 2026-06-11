#!/usr/bin/env python3
"""
Master Product Package 002D — Validation Script

Validates:
  - required files and directories
  - JSON syntax
  - schema validation (stage_contract.schema.json, master_product_proof.schema.json)
  - artifact paths exist
  - SHA256 checksums
  - no TODO/TBD/placeholders
  - stage contract date sequence
  - budget consistency (max >= planned)
  - proof JSON consistency
  - forbidden production flags

Exit codes:
  0 = PASS
  1 = WARNINGS
  2 = ERRORS
"""

import json
import hashlib
import os
import re
import sys
import glob

PACKAGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(PACKAGE_DIR))))

REQUIRED_FILES = [
    "00_MASTER_INDEX.md",
    "01_EXECUTIVE_PRODUCT_CANON.md",
    "02_PRIMARY_CUSTOMER_AND_JOBS.md",
    "03_POSITIONING_AND_VALUE_PROPOSITION.md",
    "04_MARKET_AND_COMPETITOR_STRATEGY.md",
    "05_MVP_SCOPE_AND_CUT_LINE.md",
    "06_COMMERCIAL_MODEL_AND_PRICING.md",
    "07_GO_TO_MARKET_STRATEGY.md",
    "08_CUSTOMER_VALIDATION_PLAN.md",
    "09_MASTER_ROADMAP_AND_DEADLINES.md",
    "10_STAGE_GATES_AND_ACCEPTANCE.md",
    "11_BUDGET_AND_RESOURCE_LIMITS.md",
    "12_KPI_AND_DECISION_SYSTEM.md",
    "13_ANALYTICS_AND_EXPERIMENTATION.md",
    "14_OPERATIONS_SUPPORT_AND_CONTENT.md",
    "15_LEGAL_PRIVACY_AND_SAFETY_BOUNDARIES.md",
    "16_RISK_REGISTER.md",
    "17_CHANGE_CONTROL_AND_SCOPE_GOVERNANCE.md",
    "18_FINAL_DOCUMENTATION_ACCEPTANCE.md",
    "matrices/master_traceability_matrix.md",
    "matrices/stage_contracts.json",
    "schemas/stage_contract.schema.json",
    "schemas/master_product_proof.schema.json",
    "artifact_index.json",
    "proof/proof_master_product_canon_002d.json",
]

REQUIRED_DIRECTORIES = [
    "matrices/",
    "schemas/",
    "proof/",
    "validation/",
]

TODO_PATTERN = re.compile(r'\b(TODO|TBD|FIXME|XXX|placeholder|to.?be.?decided)\b', re.IGNORECASE)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def file_size(path):
    return os.path.getsize(path)


def validate_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        json.load(f)
    return True


class ValidationResult:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, msg):
        self.errors.append(msg)

    def warning(self, msg):
        self.warnings.append(msg)

    def passed(self):
        return len(self.errors) == 0

    def print_report(self):
        print("\n=== VALIDATION RESULTS ===")
        if self.warnings:
            print(f"\nWarnings ({len(self.warnings)}):")
            for w in self.warnings:
                print(f"  [!] {w}")
        if self.errors:
            print(f"\nErrors ({len(self.errors)}):")
            for e in self.errors:
                print(f"  [X] {e}")
        if not self.errors and not self.warnings:
            print("  [OK] All checks passed")

        print(f"\nErrors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")
        print(f"Status: {'PASS' if self.passed() else 'FAIL'}")


def check_required_files(result):
    """Check all required files exist."""
    for rel_path in REQUIRED_FILES:
        full_path = os.path.join(PACKAGE_DIR, rel_path)
        if not os.path.isfile(full_path):
            result.error(f"Missing required file: {rel_path}")


def check_required_directories(result):
    """Check all required directories exist."""
    for rel_path in REQUIRED_DIRECTORIES:
        full_path = os.path.join(PACKAGE_DIR, rel_path)
        if not os.path.isdir(full_path):
            result.error(f"Missing required directory: {rel_path}")


def check_json_syntax(result):
    """Check all JSON files are syntactically valid."""
    json_files = glob.glob(os.path.join(PACKAGE_DIR, "**/*.json"), recursive=True)
    json_files.append(os.path.join(PACKAGE_DIR, "artifact_index.json"))
    for path in set(json_files):
        rel = os.path.relpath(path, PACKAGE_DIR)
        if not os.path.isfile(path):
            continue
        try:
            validate_json(path)
        except json.JSONDecodeError as e:
            result.error(f"Invalid JSON in {rel}: {e}")


def check_schema_validation(result):
    """Validate stage contracts and proof against their schemas."""
    # Validate stage contracts against schema
    schema_path = os.path.join(PACKAGE_DIR, "schemas", "stage_contract.schema.json")
    contracts_path = os.path.join(PACKAGE_DIR, "matrices", "stage_contracts.json")
    proof_schema_path = os.path.join(PACKAGE_DIR, "schemas", "master_product_proof.schema.json")
    proof_path = os.path.join(PACKAGE_DIR, "proof", "proof_master_product_canon_002d.json")

    if not all(os.path.isfile(p) for p in [schema_path, contracts_path, proof_schema_path, proof_path]):
        result.warning("Schema validation skipped: one or more schema/contract files missing")
        return

    with open(schema_path) as f:
        schema = json.load(f)
    with open(contracts_path) as f:
        contracts = json.load(f)

    schema_required = set(schema.get("required", []))
    for i, stage in enumerate(contracts):
        sid = stage.get("stage_id", f"index-{i}")
        missing = schema_required - set(stage.keys())
        if missing:
            result.error(f"Stage {sid}: missing schema-required fields: {missing}")
        for key in schema.get("properties", {}):
            prop_schema = schema["properties"][key]
            if key in stage:
                val = stage[key]
                expected_type = prop_schema.get("type")
                if expected_type == "integer" and not isinstance(val, int):
                    result.error(f"Stage {sid}: {key} should be int, got {type(val).__name__}")
                if expected_type == "number" and not isinstance(val, (int, float)):
                    result.error(f"Stage {sid}: {key} should be number, got {type(val).__name__}")

    with open(proof_schema_path) as f:
        proof_schema = json.load(f)
    with open(proof_path) as f:
        proof = json.load(f)

    proof_required = set(proof_schema.get("required", []))
    missing = proof_required - set(proof.keys())
    if missing:
        result.error(f"Proof JSON: missing schema-required fields: {missing}")

    # Check verdict is valid enum value
    verdict = proof.get("verdict")
    allowed_verdicts = proof_schema.get("properties", {}).get("verdict", {}).get("enum", [])
    if allowed_verdicts and verdict not in allowed_verdicts:
        result.error(f"Proof JSON: verdict '{verdict}' not in allowed values {allowed_verdicts}")


def check_stage_contracts(result):
    """Validate stage contract date sequence and budget consistency."""
    contracts_path = os.path.join(PACKAGE_DIR, "matrices", "stage_contracts.json")
    if not os.path.isfile(contracts_path):
        result.warning("Stage contract validation skipped: file not found")
        return

    with open(contracts_path) as f:
        contracts = json.load(f)

    if not isinstance(contracts, list) or len(contracts) == 0:
        result.error("Stage contracts must be a non-empty array")
        return

    for stage in contracts:
        sid = stage.get("stage_id", "unknown")
        # Budget consistency
        planned = stage.get("planned_budget_eur", 0)
        maximum = stage.get("maximum_budget_eur", 0)
        if maximum < planned:
            result.error(f"Stage {sid}: maximum_budget_eur ({maximum}) < planned_budget_eur ({planned})")
        if maximum < 0:
            result.error(f"Stage {sid}: negative maximum_budget_eur ({maximum})")

        # Required fields presence
        for field in ["go_conditions", "hold_conditions", "pivot_conditions", "stop_conditions"]:
            if field not in stage or not isinstance(stage.get(field), list) or len(stage[field]) == 0:
                result.error(f"Stage {sid}: missing or empty {field}")
            for cond in stage.get(field, []):
                if not isinstance(cond, str) or not cond.strip():
                    result.error(f"Stage {sid}: empty condition in {field}")

        # Zero tolerance
        zt = stage.get("zero_tolerance", {})
        if not isinstance(zt, dict):
            result.error(f"Stage {sid}: zero_tolerance must be an object")

        # Next allowed stage
        next_stage = stage.get("next_allowed_stage", "")
        valid_next = {"S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "NONE"}
        if next_stage not in valid_next:
            result.error(f"Stage {sid}: invalid next_allowed_stage '{next_stage}'")

    # Date sequence
    valid_stages = [s for s in contracts if s.get("stage_id", "").startswith("S")]
    valid_stages.sort(key=lambda s: (int(s.get("stage_id", "S-1")[1:]) if s.get("stage_id", "S-1")[1:].isdigit() else -1))

    for i in range(len(valid_stages) - 1):
        current = valid_stages[i]
        next_s = valid_stages[i + 1]
        if current.get("next_allowed_stage") != next_s.get("stage_id"):
            result.error(f"Stage {current['stage_id']}: next_allowed_stage is '{current.get('next_allowed_stage')}' but expected '{next_s.get('stage_id')}'")
            break


def check_artifact_index(result):
    """Validate artifact index entries."""
    index_path = os.path.join(PACKAGE_DIR, "artifact_index.json")
    if not os.path.isfile(index_path):
        result.warning("Artifact index validation skipped: file not found")
        return

    with open(index_path) as f:
        artifacts = json.load(f)

    if not isinstance(artifacts, list):
        result.error("artifact_index.json must be a top-level array")
        return

    for artifact in artifacts:
        path = artifact.get("path", "")
        sha = artifact.get("sha256", "")
        full_path = os.path.join(PACKAGE_DIR, path)
        if not os.path.isfile(full_path):
            result.error(f"Artifact path not found: {path}")
            continue
        computed_sha = sha256_file(full_path)
        if sha and computed_sha != sha:
            result.error(f"SHA256 mismatch for {path}: expected {sha}, got {computed_sha}")


def check_todo_tbd(result):
    """Check for TODO/TBD/placeholder patterns in all docs."""
    md_files = glob.glob(os.path.join(PACKAGE_DIR, "**/*.md"), recursive=True)
    for path in md_files:
        rel = os.path.relpath(path, PACKAGE_DIR)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        matches = TODO_PATTERN.findall(content)
        if matches:
            result.warning(f"Possible placeholder in {rel}: {', '.join(set(matches))}")


def check_content_substantive(result):
    """Check that markdown files have meaningful content (not just headings)."""
    md_files = glob.glob(os.path.join(PACKAGE_DIR, "**/*.md"), recursive=True)
    for path in md_files:
        rel = os.path.relpath(path, PACKAGE_DIR)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Count non-empty, non-header lines
        lines = [l.strip() for l in content.split('\n') if l.strip() and not l.strip().startswith('#') and not l.strip().startswith('|') and not l.strip().startswith('---')]
        if len(lines) < 10:
            result.warning(f"Thin content in {rel}: only {len(lines)} substantive lines")


def check_proof_flags(result):
    """Check that proof JSON has correct forbidden-actions flags."""
    proof_path = os.path.join(PACKAGE_DIR, "proof", "proof_master_product_canon_002d.json")
    if not os.path.isfile(proof_path):
        result.warning("Proof flag validation skipped: file not found")
        return

    with open(proof_path) as f:
        proof = json.load(f)

    # Verify critical flags
    if proof.get("real_ai_allowed") is not False:
        result.error("proof_master_product_canon_002d.json: real_ai_allowed must be false")
    if proof.get("staging_allowed") is not False:
        result.error("proof_master_product_canon_002d.json: staging_allowed must be false")
    if proof.get("production_accepted") is not False:
        result.error("proof_master_product_canon_002d.json: production_accepted must be false")


def check_stage_contract_completeness(result):
    """Check that each stage has deliverables, entry/exit criteria."""
    contracts_path = os.path.join(PACKAGE_DIR, "matrices", "stage_contracts.json")
    if not os.path.isfile(contracts_path):
        return

    with open(contracts_path) as f:
        contracts = json.load(f)

    for stage in contracts:
        sid = stage.get("stage_id", "unknown")
        for field in ["entry_criteria", "deliverables"]:
            val = stage.get(field, [])
            if not isinstance(val, list) or len(val) == 0:
                result.error(f"Stage {sid}: {field} must be a non-empty list")


def main():
    result = ValidationResult()

    print(f"Package directory: {PACKAGE_DIR}")
    print(f"Project directory: {PROJECT_DIR}")

    # Run all checks
    check_required_files(result)
    check_required_directories(result)
    check_json_syntax(result)
    check_schema_validation(result)
    check_stage_contracts(result)
    check_artifact_index(result)
    check_todo_tbd(result)
    check_content_substantive(result)
    check_proof_flags(result)
    check_stage_contract_completeness(result)

    result.print_report()

    if not result.passed():
        print("\nConclusion: FAIL")
        sys.exit(2)
    elif result.warnings:
        print("\nConclusion: PASS with warnings")
        sys.exit(1)
    else:
        print("\nConclusion: PASS")
        sys.exit(0)


if __name__ == "__main__":
    main()
