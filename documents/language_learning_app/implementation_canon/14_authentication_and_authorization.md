# Authentication and Authorization

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  
**ADR:** ADR-007, ADR-021

---

## 1. Authentication Provider

- **Provider:** Supabase Auth (final — no alternatives)
- **Methods:** Email/password, Google OAuth (MVP); Apple OAuth (added for iOS release)
- **Token type:** JWT (access + refresh tokens)
- **Access token expiry:** 15 minutes
- **Refresh token expiry:** 7 days

---

## 2. Authentication Flow

### Signup
1. Mobile sends email + password to `POST /api/v1/auth/register`
2. Backend delegates to Supabase Auth API to create user
3. Backend creates local `User` record with Supabase user ID
4. Mobile receives access token + refresh token
5. Tokens stored in `expo-secure-store`

### Signin
1. Mobile sends credentials to `POST /api/v1/auth/login`
2. Backend authenticates via Supabase Auth
3. Returns access + refresh tokens
4. Mobile stores tokens securely

### Token Verification
1. Mobile sends `Authorization: Bearer <access_token>` on all requests
2. Backend middleware verifies JWT signature with Supabase JWKS endpoint
3. Extracts `sub` (user UUID) from JWT payload
4. Attaches user to request context via dependency injection

### Token Refresh
1. On 401 response (access token expired), mobile calls `POST /api/v1/auth/refresh`
2. Backend calls Supabase Auth to refresh using refresh token
3. Returns new access + refresh tokens
4. Mobile updates tokens in secure store
5. Retries original request with new access token

### Logout
1. Mobile calls `POST /api/v1/auth/logout` (optional, best-effort)
2. Mobile clears tokens from secure store
3. Mobile clears TanStack Query cache and Zustand stores
4. Mobile navigates to `/auth/login`

---

## 3. Secure Token Storage

| Token | Storage | Key |
|-------|---------|-----|
| Access token | `expo-secure-store` | `auth_access_token` |
| Refresh token | `expo-secure-store` | `auth_refresh_token` |
| User ID | `expo-secure-store` | `auth_user_id` |

**Rules:**
- Tokens NEVER stored in AsyncStorage
- Tokens NEVER logged or sent to telemetry
- On app cold start, mobile checks secure store for existing tokens
- No tokens in URL parameters or request bodies (header only)

---

## 4. Backend Verification

- Every endpoint (except `/auth/*` and `/health`) verifies JWT
- Verification: download Supabase JWKS keys, verify JWT signature, check expiry
- Verified JWT payload → extract `sub` → query `User` by Supabase ID → attach to request
- Backend NEVER trusts `user_id` or `role` from request body

---

## 5. User ID Mapping

- Supabase Auth user ID = source of truth for identity
- Backend `users` table: `id` (UUID, PK) + `supabase_id` (UUID, unique, from Supabase)
- `supabase_id` is the `sub` claim in JWT
- Backend maps JWT `sub` → internal `user.id` via `supabase_id` lookup

---

## 6. Role Model

| Role | Permissions | Created |
|------|-------------|---------|
| `learner` | Default role. Full access to learner features. | On signup |
| `operator` | Read-only access to: audit log, user diagnostics, health. | Manual (via DB seed) |
| `admin` | Not implemented in MVP. Post-MVP. | — |

- Roles stored in `users.role` column
- Role changes require backend action (no self-service role change)
- Operator role is assigned manually (seed data or migration)

---

## 7. Authorization Enforcement

| Pattern | Enforcement |
|---------|-------------|
| Cross-user isolation | Every query includes `WHERE user_id = current_user_id` |
| IDOR protection | Backend verifies resource ownership on every request |
| Role-based access | `operator` decorator on operator endpoints |
| No client trust | Backend never uses `role` or `user_id` from request body |

### IDOR Protection Example
```python
@router.get("/lesson-sessions/{session_id}")
async def get_session(session_id: UUID, user: User = Depends(get_current_user)):
    session = await lesson_engine.get_session(session_id)
    if session.user_id != user.id:
        raise HTTPException(status_code=404, detail="Not found")
    return session
```

---

## 8. Deleted Account

- Soft delete: `users.deleted_at` set to current timestamp
- On delete: anonymize personal data, clear profile data
- Auth provider: revoke Supabase Auth user
- Subsequent API requests: 401 (token revoked)
- Data retained for 90 days per retention policy, then fully purged

---

## 9. Banned Account

- `users.status` set to `suspended`
- Auth: tokens remain valid but all API requests return 403
- Reason stored in `users.suspension_reason`
- Appeal process: out of scope for MVP (operator may reinstate via DB)

---

## 10. Security Rules

| Rule | Rationale |
|------|-----------|
| Trust JWT `sub` claim, not request body | Prevents impersonation |
| Always re-verify JWT on each request | Token revocation |
| Never log tokens or session secrets | Prevent leakage |
| Never store tokens in AsyncStorage | Unencrypted storage |
| Rate limit auth endpoints (10 req/min) | Brute force prevention |
| Rate limit refresh (5 req/min) | Abuse prevention |
