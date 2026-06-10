# Offline Sync and Recovery

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  
**ADR:** ADR-023

---

## 1. Offline-Readable Data

Data available offline (cached by TanStack Query / persisted Zustand):

| Data | Cache Source | TTL |
|------|-------------|-----|
| Home screen data | TanStack Query (`gcTime: 30min`) | 30 min |
| Lesson definitions | TanStack Query | 24h |
| Lesson content (prompts) | TanStack Query | 24h |
| User profile | TanStack Query | 5 min |
| Settings (cached local) | Zustand persist | Persistent |
| Draft submission text | Zustand persist (lessonDraftStore) | Until submission |

---

## 2. Offline-Writable Data

Actions permitted while offline:

| Action | Storage | Sync on Reconnect |
|--------|---------|-------------------|
| Type/edit lesson response | Zustand draft store (AsyncStorage) | Content sent on submit (online required for submit) |
| Update local settings | Zustand settings store | Settings synced to server on reconnect |
| Review queue viewing | TanStack Query cache | Refetch on reconnect |

---

## 3. Network-Required Actions

| Action | Behaviour if Offline |
|--------|---------------------|
| Submit lesson response | Show "Submission requires internet" — disable submit, keep draft |
| Start new lesson session | Show "Connect to internet to start a lesson" — disable CTA |
| Complete diagnostic | Show "Connect to internet to continue" |
| View rewards/XP | Show cached data with "May be outdated" indicator |
| Authentication | Failed — must be online |

---

## 4. Local Draft

| Aspect | Detail |
|--------|--------|
| Store | `lessonDraftStore` (Zustand + AsyncStorage persist) |
| Key | `draft-{lesson_session_id}` |
| Content | `{ text: string, saved_at: ISO timestamp }` |
| Auto-save | On text change debounced (500ms) and on app background |
| Recovery | On app restart, check for drafts → offer "Resume where you left off?" |
| Clear | On successful submission |

---

## 5. Queued Submission (Post-MVP)

Sprint 1 has no offline submission queue. Submission requires connectivity.

Post-MVP: submissions queue stored locally and sent in order on reconnect, with idempotency keys preventing duplicates.

---

## 6. Conflict Policy

| Conflict | Resolution |
|----------|------------|
| Local draft vs server session | Server session state is authoritative; draft is local-only |
| Stale cached data vs server data | Server wins on refetch (TanStack Query default) |
| Offline settings change vs server profile | Server profile overwrites local on next fetch; local used until sync |
| Duplicate submission (offline queue) | Idempotency key prevents duplicates (409 returned, client ignores) |

**Rule:** Server is the source of truth for all state transitions. Stale local state is replaced on server sync.

---

## 7. Interrupted Lesson Recovery

| Interruption | Recovery |
|-------------|----------|
| App crash during lesson | On restart: detect "active" or "paused" LessonSession → offer "Resume?" dialog |
| App crash during submission | On restart: check Submission state → if still `created`/`validated`: retry; if `completed`: show result |
| Network loss during submission | Show "Submission queued" (post-MVP); Sprint 1: show error + save draft |
| Phone call during lesson | On return: session still active → resume |
| Session expired (>24h pause) | Mark as `abandoned`; show "Session expired" → start new session |

---

## 8. Cache Invalidation on Sync

| Event | Action |
|-------|--------|
| App foreground (online) | TanStack Query refetch stale queries (staleTime exceeded) |
| Network reconnect | TanStack Query refetch all active queries |
| Settings sync | PATCH to server, then refetch profile |
| Lesson session sync | Submit when online; invalidate lessons and session queries |

---

## 9. Forbidden Offline Patterns

| Pattern | Reason |
|---------|--------|
| Offline lesson completion | State transition must be confirmed by server |
| Offline reward claim | Reward integrity requires server-side validation |
| Offline mastery change | Mastery is deterministic server-side only |
| Storing tokens without encryption | `expo-secure-store` mandated |
| Local-only official progress | All official state transitions on server |
