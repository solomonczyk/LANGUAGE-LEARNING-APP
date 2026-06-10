# API Architecture

**Status:** Draft  
**Version:** 1.0.0  
**Last updated:** 2026-06-10

---

## Design Principles

1. **RESTful**: Resource-oriented URLs, HTTP methods for CRUD operations
2. **JSON-only**: Request and response bodies in JSON
3. **Idempotent mutations**: All POST/PUT/PATCH endpoints support Idempotency-Key header
4. **Structured errors**: Unified error response contract for all endpoints
5. **Versioned**: Base path `/api/v1/`
6. **Authenticated by default**: All endpoints require Bearer JWT except `/auth/*` and `/health`
7. **Pagination**: List endpoints support `limit` and `offset` query parameters

---

## Base URL

```
Production:  https://api.llapp.com/api/v1
Staging:     https://api-staging.llapp.com/api/v1
Local:       http://localhost:8000/api/v1
```

---

## Authentication

**Method:** Bearer JWT in `Authorization` header  
**Token expiry:** Access token 15 minutes, refresh token 7 days  
**Provider:** Supabase Auth

---

## Endpoint Catalog

### Auth

| Method | Path | Description | Auth | Idempotent | Module |
|--------|------|-------------|------|------------|--------|
| POST | `/api/v1/auth/register` | Register new user | No | Yes (email key) | identity |
| POST | `/api/v1/auth/login` | Login with email/password | No | No | identity |
| POST | `/api/v1/auth/login/social` | Login with social provider | No | No | identity |
| POST | `/api/v1/auth/refresh` | Refresh access token | Yes (refresh) | No | identity |
| POST | `/api/v1/auth/logout` | Invalidate session | Yes | Yes | identity |

**Linked US:** US-001, US-004, US-005, US-006  
**Linked FR:** FR-001, FR-004, FR-005, FR-006

### User Profile

| Method | Path | Description | Auth | Idempotent | Module |
|--------|------|-------------|------|------------|--------|
| GET | `/api/v1/users/me` | Get current user info | Yes | Yes | identity |
| PATCH | `/api/v1/users/me` | Update current user | Yes | Yes (Idempotency-Key) | identity |

### Learner Profile

| Method | Path | Description | Auth | Idempotent | Module |
|--------|------|-------------|------|------------|--------|
| GET | `/api/v1/learner-profile` | Get learner profile | Yes | Yes | learner_profile |
| PUT | `/api/v1/learner-profile` | Update learner profile | Yes | Yes (Idempotency-Key) | learner_profile |

**Linked US:** US-011, US-012  
**Linked FR:** FR-011, FR-012

### Diagnostics

| Method | Path | Description | Auth | Idempotent | Module |
|--------|------|-------------|------|------------|--------|
| POST | `/api/v1/diagnostics/sessions` | Start diagnostic session | Yes | Yes (Idempotency-Key) | diagnostics |
| POST | `/api/v1/diagnostics/{sessionId}/responses` | Submit diagnostic response | Yes | Yes (Idempotency-Key) | diagnostics |
| POST | `/api/v1/diagnostics/{sessionId}/complete` | Complete diagnostic | Yes | Yes (Idempotency-Key) | diagnostics |
| GET | `/api/v1/diagnostics/{sessionId}` | Get diagnostic session | Yes | Yes | diagnostics |

**Linked US:** US-007, US-008, US-009, US-010  
**Linked FR:** FR-007, FR-008, FR-009, FR-010

### Learning Contract

| Method | Path | Description | Auth | Idempotent | Module |
|--------|------|-------------|------|------------|--------|
| GET | `/api/v1/learning-contract/current` | Get current contract | Yes | Yes | learning_contract |
| POST | `/api/v1/learning-contract/current` | Create contract | Yes | Yes (Idempotency-Key) | learning_contract |
| PUT | `/api/v1/learning-contract/current` | Update contract | Yes | Yes (Idempotency-Key) | learning_contract |

**Linked US:** US-014, US-015, US-016  
**Linked FR:** FR-014, FR-015, FR-016

### Lessons

| Method | Path | Description | Auth | Idempotent | Module |
|--------|------|-------------|------|------------|--------|
| GET | `/api/v1/lessons` | List available lessons | Yes | Yes | curriculum |
| GET | `/api/v1/lessons/recommended` | Get recommended lesson | Yes | Yes | curriculum |
| GET | `/api/v1/lessons/{id}` | Get lesson definition | Yes | Yes | curriculum |

**Linked US:** US-017, US-018  
**Linked FR:** FR-017, FR-018

### Lesson Sessions

| Method | Path | Description | Auth | Idempotent | Module |
|--------|------|-------------|------|------------|--------|
| POST | `/api/v1/lesson-sessions` | Start lesson session | Yes | Yes (Idempotency-Key) | lesson_engine |
| GET | `/api/v1/lesson-sessions/{id}` | Get session state | Yes | Yes | lesson_engine |
| POST | `/api/v1/lesson-sessions/{id}/attempts` | Submit attempt | Yes | Yes (Idempotency-Key) | lesson_engine |
| POST | `/api/v1/lesson-sessions/{id}/complete` | Complete session | Yes | Yes (Idempotency-Key) | lesson_engine |
| POST | `/api/v1/lesson-sessions/{id}/pause` | Pause session | Yes | Yes (Idempotency-Key) | lesson_engine |

**Linked US:** US-019, US-020, US-023, US-026, US-029, US-032, US-036  
**Linked FR:** FR-019, FR-030

### Submissions

| Method | Path | Description | Auth | Idempotent | Module |
|--------|------|-------------|------|------------|--------|
| POST | `/api/v1/submissions/text` | Submit text response | Yes | Yes (Idempotency-Key) | submission |
| POST | `/api/v1/submissions/audio` | Submit audio recording | Yes | Yes (Idempotency-Key) | submission |
| GET | `/api/v1/submissions/{id}` | Get submission | Yes | Yes | submission |
| GET | `/api/v1/submissions/{id}/analysis` | Get analysis result | Yes | Yes | submission |

**Linked US:** US-021, US-024, US-027, US-033, US-035  
**Linked FR:** FR-021, FR-024, FR-033, FR-035

### Dialogues

| Method | Path | Description | Auth | Idempotent | Module |
|--------|------|-------------|------|------------|--------|
| POST | `/api/v1/dialogues/{sessionId}/turn` | Submit dialogue turn | Yes | Yes (Idempotency-Key) | lesson_engine |
| GET | `/api/v1/dialogues/{sessionId}` | Get dialogue history | Yes | Yes | lesson_engine |

### Assessments

| Method | Path | Description | Auth | Idempotent | Module |
|--------|------|-------------|------|------------|--------|
| POST | `/api/v1/assessments` | Create assessment | Yes | Yes (Idempotency-Key) | assessment |
| POST | `/api/v1/assessments/performance` | Create performance task | Yes | Yes (Idempotency-Key) | assessment |
| GET | `/api/v1/assessments/{id}` | Get assessment result | Yes | Yes | assessment |

**Linked US:** US-039, US-040, US-041  
**Linked FR:** FR-039, FR-040, FR-041

### Mastery

| Method | Path | Description | Auth | Idempotent | Module |
|--------|------|-------------|------|------------|--------|
| GET | `/api/v1/mastery/profile` | Get mastery profile | Yes | Yes | mastery |
| PUT | `/api/v1/mastery/profile` | Update mastery profile | Yes | Yes (Idempotency-Key) | mastery |

**Linked US:** US-042, US-043, US-044  
**Linked FR:** FR-042, FR-043, FR-044

### Reviews

| Method | Path | Description | Auth | Idempotent | Module |
|--------|------|-------------|------|------------|--------|
| GET | `/api/v1/reviews/due` | Get due review items | Yes | Yes | review_scheduler |
| POST | `/api/v1/reviews/{id}/attempt` | Submit review attempt | Yes | Yes (Idempotency-Key) | review_scheduler |
| GET | `/api/v1/reviews` | Get review schedule | Yes | Yes | review_scheduler |

**Linked US:** US-045, US-046, US-047  
**Linked FR:** FR-045, FR-046, FR-047

### Rewards

| Method | Path | Description | Auth | Idempotent | Module |
|--------|------|-------------|------|------------|--------|
| GET | `/api/v1/rewards/ledger` | Get XP transaction history | Yes | Yes | reward_engine |
| GET | `/api/v1/rewards/achievements` | Get achievements | Yes | Yes | reward_engine |

**Linked US:** US-048, US-049, US-050  
**Linked FR:** FR-048, FR-049, FR-050

### Notifications

| Method | Path | Description | Auth | Idempotent | Module |
|--------|------|-------------|------|------------|--------|
| GET | `/api/v1/notifications` | Get notifications | Yes | Yes | notifications |
| POST | `/api/v1/notifications/{id}/read` | Mark as read | Yes | Yes (Idempotency-Key) | notifications |
| PUT | `/api/v1/notifications/preferences` | Update notification prefs | Yes | Yes (Idempotency-Key) | notifications |

**Linked US:** US-051, US-052  
**Linked FR:** FR-051, FR-052

### Analytics

| Method | Path | Description | Auth | Idempotent | Module |
|--------|------|-------------|------|------------|--------|
| GET | `/api/v1/analytics` | Get learning analytics | Yes | Yes | analytics |

**Linked US:** US-056  
**Linked FR:** FR-056

### Operator

| Method | Path | Description | Auth | Idempotent | Module |
|--------|------|-------------|------|------------|--------|
| GET | `/api/v1/operator/diagnostics` | User diagnostic data (read-only) | Operator | Yes | operator |
| GET | `/api/v1/operator/audit` | Audit log query (read-only) | Operator | Yes | operator |

**Linked US:** US-059, US-060, US-061  
**Linked FR:** FR-059, FR-060, FR-061

### Health

| Method | Path | Description | Auth | Idempotent | Module |
|--------|------|-------------|------|------------|--------|
| GET | `/api/v1/health` | System health check | No | Yes | operator |

**Linked FR:** FR-059

---

## Error Model

### Unified Error Response

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request body contains invalid fields.",
    "details": {
      "fields": [
        {"field": "email", "error": "Invalid email format"}
      ]
    },
    "trace_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "retryable": false
  }
}
```

**Error Codes:**

| Code | HTTP Status | Description | Retryable |
|------|-------------|-------------|-----------|
| VALIDATION_ERROR | 422 | Request body validation failed | false |
| AUTHENTICATION_ERROR | 401 | Missing or invalid authentication | false |
| AUTHORIZATION_ERROR | 403 | Authenticated but not authorized | false |
| NOT_FOUND | 404 | Resource not found | false |
| CONFLICT | 409 | Resource conflict (duplicate) | false |
| RATE_LIMITED | 429 | Rate limit exceeded | true (after delay) |
| IDEMPOTENCY_ERROR | 422 | Idempotency key replay with different request | false |
| AI_SERVICE_ERROR | 502 | AI provider error | true |
| AI_TIMEOUT | 504 | AI provider timeout | true |
| INTERNAL_ERROR | 500 | Unexpected internal error | true |
| SERVICE_UNAVAILABLE | 503 | Service temporarily unavailable | true |

**Prohibited in error responses:**
- Stack traces
- LLM prompts or raw LLM responses
- Secrets or credentials
- Other user identifiers
- Internal IP addresses or hostnames

---

## Rate Limiting

| Scope | Limit | Window |
|-------|-------|--------|
| Authenticated (per user) | 100 requests | 1 minute |
| Unauthenticated (per IP) | 10 requests | 1 minute |
| Auth attempts (per IP) | 5 attempts | 1 minute |
| AI analysis (per user) | 10 requests | 1 minute |

Rate limit exceeded returns HTTP 429 with `Retry-After` header.

---

## Idempotency

All mutating endpoints (POST, PUT, PATCH) support the `Idempotency-Key` header. 

**Behavior:**
1. Client generates UUID v4 idempotency key
2. Client sends key in `Idempotency-Key` header
3. Server checks if key has been seen:
   - New key: process request, store result keyed by idempotency key
   - Existing key: return stored response (repeat detection for rewards)
4. Idempotency keys expire after 24 hours

**Key uniqueness:** Idempotency keys must be unique per user. Reusing a key with a different request body returns 422 IDEMPOTENCY_ERROR.
