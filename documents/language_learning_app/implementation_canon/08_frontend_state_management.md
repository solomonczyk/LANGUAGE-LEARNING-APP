# Frontend State Management

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  
**ADR:** ADR-013

---

## 1. State Management Decision

| Tool | Purpose | Status |
|------|---------|--------|
| **TanStack Query** (v5) | Server state, API data, caching, invalidation, request lifecycle, network status, controlled retries | **Final** |
| **Zustand** (v4+) | Local UI state, temporary/session state, non-server data, persisted UI preferences | **Final** |

**Decision:** Zustand is the exclusive local state management library. Redux, MobX, Jotai, Valtio, and other alternatives are NOT permitted without a new ADR.

---

## 2. TanStack Query — Scope

### Used for:
- All API data fetching (GET endpoints)
- All mutations (POST/PUT/PATCH/DELETE)
- Server cache management and invalidation
- Request lifecycle states (loading, error, success)
- Network status integration (`networkMode: 'offlineFirst'`)
- Controlled retries (3 retries for GET, 0 for mutations)
- Background refetching on app foreground
- Optimistic updates for UX-critical mutations (lesson submission progress indicator)

### NOT used for:
- Non-server UI state (use Zustand)
- Temporary form state (use React Hook Form internal state)
- Navigation state (Expo Router manages this)

---

## 3. TanStack Query — Query Key Policy

```
Query key format: ['domain', 'entity', { filters }]
```

| Domain | Key Pattern | Example |
|--------|-------------|---------|
| Profile | `['profile', 'learner']` | `queryClient.getQueryData(['profile', 'learner'])` |
| Lessons | `['lessons', { type, page }]` | `useQuery({ queryKey: ['lessons', { type: 'available' }] })` |
| Lesson Session | `['lesson-session', sessionId]` | `useQuery({ queryKey: ['lesson-session', id] })` |
| Submission | `['submission', submissionId]` | `useQuery({ queryKey: ['submission', id] })` |
| Reviews | `['reviews', { status }]` | `useQuery({ queryKey: ['reviews', { status: 'due' }] })` |
| Rewards | `['rewards', 'ledger']` | `useQuery({ queryKey: ['rewards', 'ledger'] })` |

---

## 4. TanStack Query — Mutation Policy

| Rule | Enforcement |
|------|-------------|
| All POST/PUT/DELETE use `useMutation` | Code review |
| Mutations invalidate related queries on success | Code review (`onSuccess` callback) |
| Mutations DO NOT update cache directly (invalidation does) | Code review |
| Idempotency key header sent with all mutation requests | API client interceptor |
| Optimistic updates only for non-critical UI feedback (progress indicators) | Code review |
| Mutations throw on error; error UI handled by component | Pattern |

---

## 5. Zustand — Scope

### Used for:
- Current onboarding progress (step index, completed steps)
- Unsaved lesson draft (text input before submission, preserved across navigation)
- Audio recorder state (recording, paused, playback)
- Transient session state (current screen, modals open)
- Local navigation-related state (scroll position, expanded sections)
- UI preferences (theme, language override, notification preferences local override)
- Feature flags (overridden per session)

### NOT used for (source of truth must be server):
- XP balance
- Mastery data
- Reward ledger
- Official lesson completion status
- Review schedule
- Security decisions
- Authentication tokens (stored in SecureStore)
- User identity (stored in SecureStore, fetched via TanStack Query)

---

## 6. Zustand — Store Definitions

Each store is a single file in `src/state/stores/`:

| Store | File | State | Persisted |
|-------|------|-------|-----------|
| OnboardingStore | `onboardingStore.ts` | `currentStep: number, completedSteps: Set<string>` | Yes (AsyncStorage) |
| LessonDraftStore | `lessonDraftStore.ts` | `drafts: Record<string, { text: string, savedAt: number }>` | Yes (AsyncStorage) |
| AudioRecorderStore | `audioRecorderStore.ts` | `state: idle|recording|paused|completed, uri?: string, duration: number` | No |
| UIStore | `uiStore.ts` | `toasts: Toast[], activeModal: string | null, expandedSections: string[]` | No |
| SettingsStore | `settingsStore.ts` | `language: string, notificationsEnabled: boolean, reducedMotion: boolean` | Yes (AsyncStorage) |

---

## 7. Zustand — Persistence Allowlist

Stores with async persistence (via `zustand/middleware` `persist`):

| Store | Storage | Key Prefix |
|-------|---------|------------|
| OnboardingStore | AsyncStorage | `onboarding-` |
| LessonDraftStore | AsyncStorage | `draft-{sessionId}` |
| SettingsStore | AsyncStorage | `settings-` |

Stores without persistence (session-only):
- AudioRecorderStore
- UIStore
- Any store holding transient state

---

## 8. Zustand — Reset Rules

| Event | Action |
|-------|--------|
| Logout | Reset ALL Zustand stores to initial state (except SettingsStore language) |
| Account deletion | Clear ALL persisted state including SettingsStore |
| Lesson session complete | Clear LessonDraftStore entry for that session |
| Onboarding complete | Clear OnboardingStore |
| App version upgrade with breaking state change | Clear all persisted Zustand state (version key check) |

Implementation: `src/state/stores/reset.ts` — `resetAllStores()` function called on logout and account deletion.

---

## 9. Zustand — Stale State Versioning

Each persisted store has a `version` field. On store definition change:
1. Increment `version` number
2. Old persisted state is discarded on next app launch
3. Store initializes with defaults

```typescript
// Example
const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      // ... state and actions
    }),
    {
      name: 'settings-store',
      version: 1, // Increment on breaking change
      migrate: (persistedState, version) => {
        // Optional migration logic
        return persistedState as SettingsState;
      },
    }
  )
);
```

---

## 10. Conflict Resolution with Server Data

| Conflict | Resolution |
|----------|------------|
| Local draft differs from server lesson state | Server state wins (draft is local-only, resubmission uses new session) |
| Local UI preference conflicts with server profile | Server profile wins on next fetch; local preference used until then |
| Offline mutation queued but server state changed | Backend idempotency key prevents duplicate; user sees latest server state on sync |
| Zustand cached profile vs TanStack Query profile | TanStack Query is source of truth; Zustand never caches server data |

---

## 11. State Architecture Diagram

```
┌──────────────────────────────────────────────────┐
│                  TanStack Query                   │
│  ┌─────────────┐  ┌─────────────┐  ┌───────────┐ │
│  │  Query Cache │  │  Mutations  │  │  Refetch  │ │
│  └──────┬──────┘  └──────┬──────┘  └─────┬─────┘ │
│         │                │                │       │
│    server data      write to API     revalidate    │
└─────────┼────────────────┼────────────────┼───────┘
          │                │                │
          ▼                ▼                ▼
┌──────────────────────────────────────────────────┐
│                   Zustand                         │
│  ┌─────────────┐  ┌─────────────┐  ┌───────────┐ │
│  │ UI State    │  │ Draft State │  │ Prefs     │ │
│  │ (session)   │  │ (persisted) │  │ (persist) │ │
│  └─────────────┘  └─────────────┘  └───────────┘ │
└──────────────────────────────────────────────────┘
          │                │                │
          ▼                ▼                ▼
┌──────────────────────────────────────────────────┐
│               React Hook Form                     │
│  ┌──────────────────────────────────────────────┐ │
│  │        Local form state (uncontrolled)        │ │
│  └──────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```
