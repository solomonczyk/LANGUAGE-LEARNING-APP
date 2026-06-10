# Frontend Architecture

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  
**ADR:** ADR-018  
**Schema:** `schemas/frontend_module.schema.json`  
**Example:** `examples/frontend_module.example.json`

---

## 1. Frontend Structure

```
mobile/
├── app/                          # Expo Router file-based routes
│   ├── _layout.tsx               # Root layout (providers, auth guard)
│   ├── auth/                     # Auth route group
│   ├── onboarding/               # Onboarding route group
│   ├── diagnostic/               # Diagnostic route group
│   ├── (app)/                    # Authenticated tab layout
│   │   ├── _layout.tsx           # Tab navigator
│   │   ├── home.tsx
│   │   ├── lessons.tsx
│   │   ├── reviews.tsx
│   │   ├── rewards.tsx
│   │   └── settings.tsx
│   ├── lesson-session/[id].tsx   # Full-screen lesson
│   └── submission/[id].tsx       # Submission result
├── src/
│   ├── features/                 # Feature modules
│   │   ├── auth/
│   │   ├── onboarding/
│   │   ├── diagnostic/
│   │   ├── lessons/
│   │   ├── lesson-session/
│   │   ├── submission/
│   │   ├── reviews/
│   │   ├── rewards/
│   │   ├── profile/
│   │   └── operator/
│   ├── entities/                 # Domain types and schemas
│   │   ├── user.ts
│   │   ├── lesson.ts
│   │   ├── submission.ts
│   │   ├── mastery.ts
│   │   └── reward.ts
│   ├── shared/                   # Shared UI and utilities
│   │   ├── components/           # Reusable UI components (design system)
│   │   ├── hooks/                # Shared hooks
│   │   ├── utils/                # Pure utility functions
│   │   └── constants/            # App constants, environment
│   ├── services/                 # Service modules
│   │   ├── api/                  # API client + interceptors
│   │   ├── storage/              # AsyncStorage + SecureStore wrappers
│   │   ├── audio/                # Audio recording/playback
│   │   ├── notifications/        # Push notification service
│   │   └── telemetry/            # OpenTelemetry mobile
│   ├── state/                    # Global state
│   │   ├── query/                # TanStack Query config + keys
│   │   └── stores/               # Zustand store definitions
│   ├── validation/               # Zod schemas (shared with backend contracts)
│   └── telemetry/                # Telemetry initialization and helpers
├── __tests__/                    # Test files (mirrors src/)
│   ├── features/
│   ├── shared/
│   └── services/
└── app.json                      # Expo configuration
```

---

## 2. Module Ownership

| Directory | Owner | Responsibility |
|-----------|-------|----------------|
| `app/` | Feature teams | Route definitions, layout composition, screen-level orchestration |
| `src/features/*` | Feature teams | Feature-specific screens, components, hooks, and logic |
| `src/entities/` | Shared | Domain type definitions and Zod validation schemas |
| `src/shared/components/` | Design system | Reusable UI components from the design system catalog |
| `src/shared/hooks/` | Shared | Cross-cutting hooks (usePermission, useNetwork, useBackNavigation) |
| `src/services/` | Infrastructure | External service integrations (API, storage, audio, notifications) |
| `src/state/` | State management | TanStack Query provider setup, Zustand store definitions |
| `src/validation/` | Shared | Shared Zod schemas that mirror backend Pydantic models |

---

## 3. Import Direction

```
entities ← shared (components, hooks, utils)
entities ← services
entities ← features
entities ← state
shared ← services
shared ← features
features ← features (cross-feature imports FORBIDDEN)
app ← everything
```

**Rules:**
- Features may import from `shared`, `entities`, `services`, `state`
- Features must NOT import from other features (duplicate or extract to shared)
- `shared` may NOT import from `features`
- `services` may NOT import from `features` or `shared/components`
- `entities` must have zero project imports (only external libraries)
- Circular dependencies are FORBIDDEN and must fail CI

---

## 4. Shared Component Rules

| Rule | Enforcement |
|------|-------------|
| All shared components in `src/shared/components/` must match a design system component | Code review |
| No feature-specific logic inside shared components | Code review |
| Shared components receive data via props only | Code review |
| No direct API calls from shared components | Code review |

---

## 5. Feature Isolation

| Rule | Enforcement |
|------|-------------|
| Feature directory is self-contained (components, hooks, types) | Directory structure review |
| Feature may expose a public index.ts with its API | Code review |
| Feature internal modules are private (not imported from outside) | CI lint |
| Feature state is local unless it must be global | Code review |
| Feature may define its own TanStack Query hooks prefixed with feature name | Convention |

---

## 6. API Client

- **Library:** TanStack Query with `fetch` (no axios)
- **Base:** `src/services/api/client.ts` — configured with base URL, auth interceptor, timeout
- **Interceptors:** Add Authorization header, trace ID header, handle 401 (refresh/redirect)
- **Timeout:** 30s default, 120s for file uploads
- **Error mapping:** Transform HTTP errors to typed `ApiError` with code and message

---

## 7. Schema Validation (Frontend)

- **Library:** Zod
- All API responses validated with Zod schemas on receipt (defense in depth)
- Form inputs validated with Zod via React Hook Form resolver
- Shared types between frontend/backend maintained as Zod schemas in `src/validation/`
- No `any` or `unknown` escaping from validation (strict parsing)

---

## 8. Environment Configuration

- **Library:** `expo-constants` + `expo-config` (or `.env` via `@expo/config`)
- Configs: API base URL, auth provider URL, feature flags, telemetry key
- No secrets in config (secrets are backend-only)
- Environment files: `.env.development`, `.env.staging`, `.env.production`
- All env vars accessed through typed config object in `src/shared/constants/env.ts`

---

## 9. Error Boundaries

- React Error Boundary at root layout level
- Feature-level error boundary wrapping lesson session and submission screens
- Error boundary catches unhandled exceptions, logs to telemetry, shows error screen
- Does not recover automatically — user taps "Try Again" to reload

---

## 10. Retry Policy

| Operation | Retry Count | Condition |
|-----------|-------------|-----------|
| API GET (TanStack Query) | 3 | 5xx, network error (not 4xx) |
| API POST/PUT | 0 | Idempotency key prevents duplicates; retry handled by user |
| File upload | 1 | Network error only |
| Token refresh | 1 | On 401 |

---

## 11. Offline Detection

- Library: `@react-native-community/netinfo`
- State: accessible via `useNetwork` hook (online/offline)
- Banner: `OfflineBanner` component at top when offline (shared component)
- TanStack Query: `networkMode: 'offlineFirst'` — serve cache when offline, refetch on reconnect

---

## 12. Test Placement

| Test Type | Location |
|-----------|----------|
| Unit tests (pure functions) | Co-located `__tests__/` directory next to source file |
| Component tests | `__tests__/components/` mirroring `shared/components/` |
| Feature integration tests | `__tests__/features/<feature-name>/` |
| Service tests | `__tests__/services/` |
| E2E tests | `e2e/` at project root |

---

## 13. Forbidden Patterns

| Pattern | Reason | Enforcement |
|---------|--------|-------------|
| Circular dependencies | Unmaintainable, causes runtime issues | CI circular dependency check |
| Direct network calls from UI components | Bypasses caching, error handling, auth | Code review |
| Direct database/Supabase access from client | Bypasses backend validation | Code review + schema check |
| Business rules inside screens | Untestable, violates separation | Code review |
| Mastery/reward logic on client | Authority violation | Code review |
| Hardcoded environment URLs | Breaks on environment switch | CI check for absolute URLs |
| Secrets in mobile bundle | Security risk | CI secret scan |
