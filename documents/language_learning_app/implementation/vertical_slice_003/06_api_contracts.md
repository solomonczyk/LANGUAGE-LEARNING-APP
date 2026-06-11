# 06 — API Contracts (Vertical Slice 003)

## OpenAPI v3.1.0 — 22 endpoints

### Identity
| Method | Path | Purpose |
|--------|------|---------|
| POST | /api/v1/identity/register | Register new user |
| POST | /api/v1/identity/login | Stub login |
| GET | /api/v1/identity/me | Current user info |

### Learner Profile
| Method | Path | Purpose |
|--------|------|---------|
| POST | /api/v1/learner-profile | Create/update profile |
| GET | /api/v1/learner-profile/me | Read profile |

### Diagnostics
| Method | Path | Purpose |
|--------|------|---------|
| POST | /api/v1/diagnostics/sessions | Create session |
| POST | /api/v1/diagnostics/sessions/{id}/responses | Submit response |
| POST | /api/v1/diagnostics/sessions/{id}/complete | Complete session |
| GET | /api/v1/diagnostics/sessions/{id} | Get status |

### Learning Contract
| Method | Path | Purpose |
|--------|------|---------|
| GET | /api/v1/learning-contract/current | Get contract |
| POST | /api/v1/learning-contract/current | Create contract |

### Lesson Engine
| Method | Path | Purpose |
|--------|------|---------|
| POST | /api/v1/lesson-sessions | Create session |
| GET | /api/v1/lesson-sessions/{id} | Get session |
| POST | /api/v1/lesson-sessions/{id}/submissions | Submit text |
| POST | /api/v1/lesson-sessions/{id}/process | Process |

### Mastery
| Method | Path | Purpose |
|--------|------|---------|
| POST | /api/v1/mastery/evidence | Create evidence |
| GET | /api/v1/mastery/profile | Get profile |

### Audit
| Method | Path | Purpose |
|--------|------|---------|
| POST | /api/v1/audit/events | Record event |
| GET | /api/v1/audit/events | List events |

### Operator
| Method | Path | Purpose |
|--------|------|---------|
| GET | /api/v1/operator/health | Extended health |
| GET | /api/v1/operator/audit-events | All audit events |

### Health
| Method | Path | Purpose |
|--------|------|---------|
| GET | /api/v1/health | Service health |

## Canonical Error Contract
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable",
    "details": {},
    "trace_id": "uuid",
    "retryable": false
  }
}
```

## Verified
- All 22 endpoints generate in OpenAPI: PASSED
- All endpoints respond to valid requests: PASSED
- Error contract validated: PASSED
- Cross-user access blocked: PASSED
