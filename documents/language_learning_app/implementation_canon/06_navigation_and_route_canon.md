# Navigation and Route Canon

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  
**ADR:** ADR-017

---

## 1. Navigation Framework

**Tool:** Expo Router v4  
**Type:** File-based routing  
**Platforms:** iOS, Android (Web/PWA not for learner use)

---

## 2. Route Map

```
/auth/*              → auth group (public)
/onboarding/*        → onboarding group (authenticated, guarded)
/profile             → learner profile (authenticated)
/diagnostic/*        → diagnostic group (authenticated, guarded)
/learning-contract   → learning entry contract (authenticated, guarded)
(app)/               → tab layout (authenticated)
  (app)/home         → dashboard
  (app)/lessons      → lesson catalog
  (app)/reviews      → review queue
  (app)/rewards      → rewards and achievements
  (app)/settings     → settings
/lesson-session/:id  → active lesson session (full-screen, no tabs)
/submission/:id      → submission result (full-screen or modal)
/operator/*          → operator read-only (authenticated, operator role)
```

---

## 3. Route Classification

| Route Group | Access | Auth Required | Guards |
|-------------|--------|---------------|--------|
| `/auth/*` | Public | No | Redirect to (app) if already authenticated |
| `/onboarding/*` | Authenticated | Yes | Redirect to /auth if not authenticated; redirect to (app) if onboarding complete |
| `/diagnostic/*` | Authenticated | Yes | Redirect to /onboarding if not started; redirect to (app) if diagnostic complete |
| `/learning-contract` | Authenticated | Yes | Redirect to /diagnostic if not completed |
| `(app)/*` | Authenticated | Yes | Redirect to /auth if not authenticated; redirect to /onboarding if onboarding incomplete; redirect to /diagnostic if diagnostic not done; redirect to /learning-contract if no contract |
| `/lesson-session/:id` | Authenticated | Yes | Redirect to (app)/lessons if session invalid/expired |
| `/submission/:id` | Authenticated | Yes | Redirect to (app)/home if submission not found |
| `/operator/*` | Operator role | Yes | 403 if not operator role |

---

## 4. Route Guards (Execution Order)

1. **Auth guard** — check valid JWT; redirect to `/auth/login` if expired/missing
2. **Onboarding guard** — check `profile.onboarding_completed`; redirect to `/onboarding` if false
3. **Diagnostic guard** — check `learner_profile.diagnostic_completed`; redirect to `/diagnostic/start` if false
4. **Learning contract guard** — check `learning_contract.signed`; redirect to `/learning-contract` if false
5. **Lesson access guard** — check session ownership and validity
6. **Operator guard** — check `user.role == 'operator'`; return 403 if not

---

## 5. Back Behaviour

| Context | Behaviour |
|---------|-----------|
| Standard stack | Expo Router default back (previous screen in stack) |
| Lesson session (active) | Show confirmation: "Exit lesson? Your progress will be saved." |
| Lesson session (submitting) | Block back (gesture disabled); show "Submission in progress" |
| Auth screens (post-login) | No back — clear stack to (app) |
| Modal screens | Swipe down / tap outside to dismiss |
| Tab navigation | Previous tab remembered; back within tab stack |

---

## 6. Deep Links

| URL | Target | Notes |
|-----|--------|-------|
| `llapp://lesson-session/{id}` | Resume lesson session | Only if session is in active/paused state |
| `llapp://reviews` | Open review queue | Direct to (app)/reviews tab |
| `llapp://settings/profile` | Profile settings | Direct to settings with profile section |

Deep links only work for authenticated users. If user is not authenticated, deep link is stored and navigated after login.

---

## 7. Modal Routes

| Route | Presentation | Use Case |
|-------|-------------|----------|
| `/submission/:id` | modal (iOS sheet, Android dialog) | Post-submission analysis view |
| `/settings/edit-profile` | modal | Edit profile fields |
| `/lesson-session/:id/confirm-exit` | modal | Confirm exit dialog |
| `/auth/delete-account` | modal full-screen | Account deletion flow |

---

## 8. Full-Screen Routes

| Route | Hides Tab Bar | Hides Header | Use Case |
|-------|--------------|--------------|----------|
| `/lesson-session/:id` | Yes | Yes (custom lesson header shown) | Immersive lesson experience |
| `/auth/*` | Yes | Yes | Auth flow |
| `/onboarding/*` | Yes | Yes | Onboarding flow |
| `/diagnostic/*` | Yes | Yes (custom header) | Diagnostic flow |

---

## 9. Interrupted Session Restoration

| Condition | Behaviour |
|-----------|-----------|
| App opened to resume lesson | Detect `lesson_session` in `active` or `paused` state → offer "Resume lesson?" dialog |
| Session expired (>24h paused) | Mark as `abandoned`; redirect to lesson catalog |
| Lesson complete (server-side) | Navigate to submission result |
| App crash during submission | On reopen: check submission state; if `created` or `validated`, retry submission; if `completed` or `failed`, show result |

Restoration logic: `src/features/lesson-session/hooks/useSessionRestoration.ts`

---

## 10. Stale Route Handling

| Condition | Behaviour |
|-----------|-----------|
| Navigate to expired session | Redirect to lesson catalog with toast "Session expired" |
| Navigate to deleted submission | Redirect to home with toast "Submission not found" |
| Navigate to completed lesson | Show summary (read-only), do not allow re-submission |
| Navigate with invalid ID | 404 screen with back-to-home button |

---

## 11. Invalid Route Handling

- Unknown routes: custom 404 screen with "Go Home" button
- Malformed parameters: redirect to parent route with error toast
- Non-numeric ID where numeric expected: 404

---

## 12. Navigation Persistence

- TanStack Query cache persists server state across navigation (via `gcTime`)
- Zustand persisted state (lesson draft, UI state) restored on navigation return
- Scroll position restored on back navigation (React Navigation default)

---

## 13. Logout Reset

On logout:
1. Clear TanStack Query cache (`queryClient.clear()`)
2. Reset Zustand stores to initial state (except persisted preference like language)
3. Clear secure storage (tokens)
4. Navigate to `/auth/login` (reset navigation stack)

---

## 14. Account Deletion Reset

On account deletion:
1. All local data cleared (AsyncStorage, SecureStore, all Zustand stores)
2. TanStack Query cache cleared
3. Navigated to `/auth/login` with message "Account deleted"

---

## 15. Navigation Test Requirements

| Test | Scope |
|------|-------|
| Route guard chain | Auth → onboarding → diagnostic → contract redirects |
| Deep link resolution | Valid and invalid deep links |
| Back behaviour | Normal, lesson session (active/submitting), modal |
| Interrupted session restoration | Resume, expired, completed scenarios |
| Logout reset | Cache clear + store reset + redirect |
| Invalid route | 404 screen display |
| Tab navigation | Tab switch preserves state |
