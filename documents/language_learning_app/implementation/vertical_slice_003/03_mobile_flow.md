# 03 — Mobile Flow (Vertical Slice 003)

## Screens / Routes

| Route | Screen | State | API Dependencies |
|-------|--------|-------|-----------------|
| `/onboarding` | Onboarding | Steps 0-3 profile form | POST /learner-profile |
| `/diagnostic` | Diagnostic | 4-step skill assessment | POST /diagnostics/sessions |
| `/learning-contract` | Contract | Summary of terms | GET /learning-contract/current |
| `/home` | Home | Available lessons list | GET /lesson-definitions |
| `/lesson/[id]` | Lesson | Narrative text input | POST /lesson-sessions |
| `/lesson-session/[id]` | Session | Active session status | GET /lesson-sessions/{id} |
| `/result/[id]` | Result | Processing outcome | POST /lesson-sessions/{id}/process |

## State Management

### Zustand Local Stores
- `useOnboardingStore` — draft recovery for onboarding form
- `useDiagnosticStore` — session ID + step progression
- `useLessonDraftStore` — text composition with auto-save
- `useRouteIntentStore` — navigation state for stale route handling

### API Client (TanStack Query)
- Centralized `api.ts` with `fetch()` wrapper
- Automatic error parsing
- Token/user ID header injection

## Data Flow

```
User Input → Zustand Draft → API Client → Backend → PostgreSQL
                                          ↓
                                     Response
                                          ↓
                                 Zustand Update + Route
```

## Key Features
- Offline draft recovery (local store persists)
- Duplicate tap prevention (`isSubmitting` flag)
- Loading states (`LoadingScreen` component)
- Error states (`ErrorScreen` component)
- Safe area handling in `_layout.tsx`
- Large text support via responsive layout

## Verified
- TypeScript typecheck: PASSED (0 errors)
- All routes defined: PASSED
- API client connects to backend: PASSED
- Draft store structure: PASSED
