# 07 — State Machines (Vertical Slice 003)

## DiagnosticSession States
```
CREATED ──start──► IN_PROGRESS ──complete──► COMPLETED
   │                    │
   └──fail──► FAILED ◄──┘
```

Transitions:
- CREATED → start → IN_PROGRESS
- IN_PROGRESS → complete → COMPLETED
- IN_PROGRESS → fail → FAILED
- CREATED → fail → FAILED

Forbidden:
- COMPLETED → any (terminal)
- FAILED → any (terminal)
- CREATED → complete (must start first)

## LessonSession States
```
CREATED ──activate──► ACTIVE ──submit──► SUBMITTED
                         │                   │
                         │         ┌─────────┘
                         │         ▼
                         │    ANALYSIS_PENDING ──validate──► ANALYSIS_VALIDATED
                         │         │                               │
                         │         │                    ┌──────────┴──────────┐
                         │         │                    ▼                     ▼
                         │         │               COMPLETED              REJECTED
                         │         │
                         ▼         ▼
                       FAILED ◄───┘ (from ACTIVE, SUBMITTED, ANALYSIS_PENDING, ANALYSIS_VALIDATED)
```

Transitions:
- CREATED → activate → ACTIVE
- ACTIVE → submit → SUBMITTED
- SUBMITTED → start_analysis → ANALYSIS_PENDING
- ANALYSIS_PENDING → validate → ANALYSIS_VALIDATED
- ANALYSIS_VALIDATED → complete → COMPLETED
- ANALYSIS_VALIDATED → reject → REJECTED
- Any state → fail → FAILED (except CREATED→fail, ACTIVE→fail, SUBMITTED→fail, ANALYSIS_PENDING→fail, ANALYSIS_VALIDATED→fail)

## State Machine Implementation
- Generic `StateMachine` class in `app/shared/state_machine.py`
- Deterministic, auditable transitions
- Guard predicates support
- `allowed_events()` introspection
- ValueError on invalid transition

## Verified
- All transitions tested: PASSED
- All forbidden transitions blocked: PASSED
- Duplicate event safety: PASSED
- Guard denied transitions: PASSED
- Reset functionality: PASSED
