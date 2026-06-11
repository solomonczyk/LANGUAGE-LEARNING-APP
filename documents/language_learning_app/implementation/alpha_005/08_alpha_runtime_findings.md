# Alpha Runtime Findings

## Environment Health

| Component | Status | Notes |
|-----------|--------|-------|
| Backend (FastAPI) | ✓ Healthy | Server port 8000, hot-reload enabled |
| PostgreSQL | ✓ Healthy | All connections, migrations applied |
| Mock AI Gateway | ✓ Active | Valid fixture mode, deterministic |
| Auth Stub | ✓ Active | X-User-Id header-based auth |
| API Connectivity | ✓ All endpoints reachable | No timeouts or connection errors |

## Performance Observations

### Response Times
All API responses returned within normal bounds (< 500ms per request). The processing pipeline step completed with decision=COMPLETE for all 5 testers.

| Endpoint | Avg Response Time | Notes |
|----------|-----------------|-------|
| /api/v1/health | < 50ms | Database query + response |
| /api/v1/identity/register | < 100ms | User creation + DB write |
| /api/v1/learner-profile | < 100ms | Profile creation |
| /api/v1/diagnostics/sessions | < 100ms | Session creation |
| /api/v1/diagnostics/sessions/{id}/responses | < 100ms | Response recording |
| /api/v1/diagnostics/sessions/{id}/complete | < 200ms | Assessment calculation |
| /api/v1/learning-contract/current | < 100ms | Contract generation |
| /api/v1/lesson-sessions | < 100ms | Session creation |
| /api/v1/lesson-sessions/{id}/submissions | < 100ms | Text submission |
| /api/v1/lesson-sessions/{id}/process | < 1000ms | Full pipeline (mock AI + validations) |
| /api/v1/mastery/profile | < 100ms | Profile read |
| /api/v1/operator/audit-events | < 200ms | Event listing |

### Database Operations
- 50 audit events recorded during tester sessions
- All diagnostic sessions properly completed with 4 assessments each
- Learning contracts created with version 1.0.0
- Lesson sessions completed with mastery records created

## State Machine Verification

| State Machine | Transitions Verified | Result |
|--------------|---------------------|--------|
| Diagnostic | CREATED → IN_PROGRESS → COMPLETED | ✓ (5/5) |
| Lesson | CREATED → ACTIVE → RECEIVED → COMPLETED | ✓ (5/5) |

## Error Handling

No errors were encountered during any tester session. Error handling was verified independently through integration tests:

| Scenario | Expected Behavior | Result |
|----------|------------------|--------|
| Incomplete text submission | Rejected by frontend (min 10 chars) | ✓ (not tested in API flow) |
| Unknown session ID | 404 + error structure with trace_id | ✓ |
| Cross-user access | 403/404/409 | ✓ |
| Malformed payload | 400/422 | ✓ |
| Duplicate process request | Idempotent/rejected safely | ✓ |

## Known Runtime Limitations

1. **Mock AI mode**: All analysis uses deterministic fixtures, not real AI
2. **Single lesson definition**: Only one lesson type available for testing
3. **Auth stub mode**: No real authentication or authorization
4. **Web-only testing**: Mobile native (iOS/Android) not tested in this session
