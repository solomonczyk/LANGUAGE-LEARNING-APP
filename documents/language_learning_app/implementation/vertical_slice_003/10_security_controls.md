# 10 — Security Controls (Vertical Slice 003)

## Authorization

### User Identity
- `X-User-Id` header for local development
- Intent: JWT in production
- Auth stub mode enabled via `AUTH_STUB_ENABLED=true`

### Operator Authorization
- `_require_operator()` dependency in operator router
- Verifies `is_operator` flag on User model
- Returns 403 FORBIDDEN if non-operator user tries to access audit

### Cross-User Isolation
Every service-level query checks ownership:
- `get_session()` validates `session.user_id == user_id`
- `submit_response()` validates session ownership
- `get_submission()` validates submission ownership
- `process_lesson_session()` validates session + submission ownership
- Violation returns `INVALID_STATE_TRANSITION` (409)

### Request Body User ID Ignored
- User identity comes from header/middleware, not request body
- Tested: spoofed user_id in body is not honored

## Input Validation

### Text Submission
- Minimum 10 character length enforced
- Unicode NFC normalization
- SQL injection attempt handled safely (ORM parameterization)
- Tested: SQL-like injection text accepted without issues

### Malformed Payload
- FastAPI Pydantic validation rejects malformed JSON (422)
- Missing fields return validation errors

## Audit Security
- Audit events are append-only (no deletion endpoints)
- Operator-only read access
- No raw secrets or stack traces in audit data

## Idempotency
- `X-Idempotency-Key` header for submission deduplication
- Same key returns same submission ID
- Prevents duplicate processing

## Verified
- Cross-user access blocked: PASSED
- Operator authorization enforced: PASSED
- Request body spoofing ignored: PASSED
- Malformed payload rejected: PASSED
- Idempotency enforced: PASSED
- Unknown resource returns 404: PASSED
- No secrets in compose: PASSED
- No real provider config: PASSED
