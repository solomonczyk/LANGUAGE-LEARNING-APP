"""Linguistic validation services — deterministic analysis checks."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ValidationResult

ALLOWED_ISSUE_CODES = {
    "VERB_FORM", "ARTICLE", "PREPOSITION", "WORD_ORDER",
    "COLLOCATION", "SPELLING", "TENSE", "PLURAL",
    "SUBJECT_VERB_AGREEMENT", "MODAL",
}
ALLOWED_SEVERITIES = {"major", "minor", "info"}


async def validate_linguistic(
    db: AsyncSession,
    submission_id: str,
    analysis_result: dict,
) -> dict:
    """Deterministically validate the linguistic quality of an AI analysis.

    Checks performed:
    1. output_consistency — analysis has all required fields
    2. issue_structure — each issue has code, severity, span, suggestion
    3. severity_validity — severity is one of major/minor/info
    4. span_validity — span is a non-empty string
    5. allowed_codes — issue code is in allowed set
    6. confidence_range — confidence is 0.0-1.0
    """
    checks = {}
    failed_checks = []

    # 1. Output consistency
    required_fields = ["analysis_version", "meaning_preserved", "detected_issues", "confidence"]
    has_fields = all(f in analysis_result for f in required_fields)
    checks["output_consistency"] = has_fields
    if not has_fields:
        failed_checks.append("output_consistency")

    # 2. Issue structure
    issues = analysis_result.get("detected_issues", [])
    if isinstance(issues, list) and all(isinstance(i, dict) for i in issues):
        issues_valid = all(
            "code" in i and "severity" in i and "span" in i and "suggestion" in i
            for i in issues
        )
    else:
        issues_valid = False
    checks["issue_structure"] = issues_valid
    if not issues_valid:
        failed_checks.append("issue_structure")

    # 3. Severity validity
    if isinstance(issues, list):
        severity_valid = all(
            i.get("severity") in ALLOWED_SEVERITIES
            for i in issues
        )
    else:
        severity_valid = False
    checks["severity_validity"] = severity_valid
    if not severity_valid:
        failed_checks.append("severity_validity")

    # 4. Span validity
    if isinstance(issues, list):
        span_valid = all(
            isinstance(i.get("span"), str) and len(i["span"].strip()) > 0
            for i in issues
        )
    else:
        span_valid = False
    checks["span_validity"] = span_valid
    if not span_valid:
        failed_checks.append("span_validity")

    # 5. Allowed codes
    if isinstance(issues, list):
        codes_valid = all(
            i.get("code") in ALLOWED_ISSUE_CODES
            for i in issues
        )
    else:
        codes_valid = False
    checks["allowed_codes"] = codes_valid
    if not codes_valid:
        failed_checks.append("allowed_codes")

    # 6. Confidence range
    confidence = analysis_result.get("confidence")
    if isinstance(confidence, (int, float)):
        confidence_valid = 0.0 <= confidence <= 1.0
    else:
        confidence_valid = False
    checks["confidence_range"] = confidence_valid
    if not confidence_valid:
        failed_checks.append("confidence_range")

    passed = len(failed_checks) == 0

    # Save validation result
    sid = UUID(submission_id)
    vr = ValidationResult(
        submission_id=sid,
        validation_type="linguistic",
        passed=passed,
        details={"checks": checks, "failed_checks": failed_checks},
    )
    db.add(vr)
    await db.flush()

    return {"passed": passed, "details": {"checks": checks, "failed_checks": failed_checks}}


async def validate_linguistic_standalone(
    analysis_result: dict,
) -> dict:
    """Standalone linguistic validation without DB persistence."""
    checks = {}
    failed_checks = []

    required_fields = ["analysis_version", "meaning_preserved", "detected_issues", "confidence"]
    has_fields = all(f in analysis_result for f in required_fields)
    checks["output_consistency"] = has_fields
    if not has_fields:
        failed_checks.append("output_consistency")

    issues = analysis_result.get("detected_issues", [])
    checks["issue_structure"] = isinstance(issues, list) and all(
        isinstance(i, dict) and all(k in i for k in ("code", "severity", "span", "suggestion"))
        for i in issues
    )
    if not checks["issue_structure"]:
        failed_checks.append("issue_structure")

    confidence = analysis_result.get("confidence")
    checks["confidence_range"] = isinstance(confidence, (int, float)) and 0.0 <= confidence <= 1.0
    if not checks["confidence_range"]:
        failed_checks.append("confidence_range")

    passed = len(failed_checks) == 0
    return {"passed": passed, "details": {"checks": checks, "failed_checks": failed_checks}}
