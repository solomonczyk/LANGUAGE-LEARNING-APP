# Alpha Session Logs

## Execution Log

**Date**: 2026-06-11
**Environment**: Docker Compose (Postgres + Backend), localhost:8000
**Operator**: Automated script execution

### Console Output

All 5 testers completed the full flow. Full console output:

```
======================================================================
ALPHA 005 - CLOSED LEARNER ALPHA EXECUTION
======================================================================

----------------------------------------------------------------------
RUNNING: ALPHA-001 (returning_learner)
----------------------------------------------------------------------
  [PASS] ALPHA-001 | health_check | status=200
  [PASS] ALPHA-001 | register | user_id=58fe2754-0603-4802-930a-890c8097b233
  [PASS] ALPHA-001 | create_profile | lang=English level=A2
  [PASS] ALPHA-001 | diagnostic_create |
  [PASS] ALPHA-001 | diagnostic_response_grammar_recognition |
  [PASS] ALPHA-001 | diagnostic_response_active_vocabulary |
  [PASS] ALPHA-001 | diagnostic_response_written_production |
  [PASS] ALPHA-001 | diagnostic_response_narrative_coherence |
  [PASS] ALPHA-001 | diagnostic_complete | 4 assessments
  [PASS] ALPHA-001 | learning_contract_create | lang=English version=1.0.0
  [PASS] ALPHA-001 | mastery_profile |
  [PASS] ALPHA-001 | lesson_create | session_id=4bc69e27-...
  [PASS] ALPHA-001 | lesson_submit | submission_id=d44729a6-...
  [PASS] ALPHA-001 | lesson_process | decision=COMPLETE has_validation=True
  [PASS] ALPHA-001 | lesson_result |
  [PASS] ALPHA-001 | mastery_after_lesson | records=1
  [PASS] ALPHA-001 | audit_events | total_events=50

  ALPHA-001 RESULT: 17/17 steps passed

  ... (same pattern for ALPHA-002 through ALPHA-005)

======================================================================
OVERALL: 85/85 steps passed across 5 testers
ALL TESTERS COMPLETED: True
======================================================================
```

### Steps executed per tester

| Step | Description | Expected | Result |
|------|-------------|----------|--------|
| 1 | Health check | 200 + status=ok | ✓ |
| 2 | Register synthetic user | 200 + user_id | ✓ |
| 3 | Create learner profile | 200 | ✓ |
| 4 | Create diagnostic session | 200 + IN_PROGRESS | ✓ |
| 5.1 | Submit grammar response | 200 | ✓ |
| 5.2 | Submit vocabulary response | 200 | ✓ |
| 5.3 | Submit writing response | 200 | ✓ |
| 5.4 | Submit coherence response | 200 | ✓ |
| 6 | Complete diagnostic | 200 + COMPLETED + 4 assessments | ✓ |
| 7 | Learning contract (get/create) | 200 + contract data | ✓ |
| 8 | Mastery profile pre-lesson | 200 | ✓ |
| 9 | Create lesson session | 200 | ✓ |
| 10 | Submit lesson text | 200 + RECEIVED | ✓ |
| 11 | Process lesson | 200 + COMPLETED | ✓ |
| 12 | Get lesson result | 200 + COMPLETED | ✓ |
| 13 | Mastery profile after lesson | 200 + records>0 | ✓ |
| 14 | Verify audit events | 200 + events exist | ✓ |

### Raw session data

See [raw_session_results.json](evidence/operator_notes/raw_session_results.json)
