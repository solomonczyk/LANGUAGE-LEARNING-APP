# Notifications and Reminders

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  

---

## 1. Notification Types

| Type | Trigger | Delivery | Priority |
|------|---------|----------|----------|
| Lesson reminder | Scheduled daily at learner's preferred time | Push | Medium |
| Review reminder | Review items due | Push | High |
| Streak warning | 6h before streak expires (if enabled) | Push | Medium |
| Achievement unlocked | Real-time on reward commit | Push | Low |
| Session expired | Lesson session abandoned | Push | Low |

---

## 2. Permission Timing

| Permission | Request Timing | Rationale |
|------------|----------------|-----------|
| Notifications | After first lesson completion | User has experienced the app and understands notification value |
| Never on launch | — | Anti-pattern; high denial rate |

---

## 3. Quiet Hours

| Setting | Default | Configurable |
|---------|---------|-------------|
| Quiet hours start | 22:00 (learner's local time) | Yes (settings) |
| Quiet hours end | 08:00 (learner's local time) | Yes (settings) |
| Quiet hours behaviour | Notifications suppressed; delivered after quiet hours end | — |

Notifications during quiet hours are suppressed, NOT discarded. They are queued for delivery after quiet hours end.

---

## 4. Timezone Handling

- Learner's timezone detected from `expo-localization` on first launch
- Stored in `learner_profile.timezone` (IANA format: `Europe/Berlin`)
- All notification scheduling uses learner's stored timezone
- Timezone changes (daylight saving, travel): detected on app foreground; prompt learner to update

---

## 5. Duplicate Prevention

| Mechanism | Detail |
|-----------|--------|
| Notification ID | UUID v4 per notification, stored in backend |
| Deduplication | Backend checks `(user_id, notification_type, reference_id)` before dispatch |
| Rate limit | Max 5 notifications per hour per user |
| Quiet hours | Notifications outside window are suppressed (not duplicates) |

---

## 6. Notification Content

| Type | Title | Body | Deep Link |
|------|-------|------|-----------|
| Lesson reminder | "Time to learn! 🎯" | "Your next lesson is waiting." | `llapp://(app)/home` |
| Review reminder | "Review time! 📝" | "You have {count} items due for review." | `llapp://(app)/reviews` |
| Streak warning | "Don't lose your streak! 🔥" | "Complete a lesson in the next 6 hours." | `llapp://(app)/home` |
| Achievement | "Achievement unlocked! 🏆" | "{achievement_name}" | `llapp://(app)/rewards` |
| Session expired | "Session expired" | "Your lesson session was closed." | `llapp://(app)/lessons` |

---

## 7. Local Notifications

- Library: `expo-notifications`
- Scheduled locally for: lesson reminders, review reminders
- Pros: work without server, respect quiet hours
- Cons: device-dependent (cleared on reinstall)

**Local notification rescheduling:**
- On app login: fetch learner schedule from backend, reschedule local notifications
- On settings change: cancel all, reschedule with new preferences
- On logout: cancel all scheduled notifications

---

## 8. Push Notifications (Post-MVP)

- Library: `expo-notifications` with Expo Push Token
- Backend: `notifications` module sends via Expo Push API
- Fallback: local notifications (if push fails or no token)
- Implementation: Sprint 2+ (MVP Sprint 1 uses local only)

---

## 9. Audit

| Notification Event | Fields |
|--------------------|--------|
| Notification scheduled | `user_id`, `type`, `scheduled_at`, `trace_id` |
| Notification sent | `notification_id`, `user_id`, `type`, `delivery_method`, `timestamp` |
| Notification suppressed | `user_id`, `type`, `reason` (quiet hours, rate limit, opt-out) |
| Notification permission changed | `user_id`, `previous_status`, `new_status` |

---

## 10. LLM Notification Restrictions

**LLM must NOT directly send or trigger notifications.** All notifications are:
1. Scheduled by deterministic business rules (review scheduler, streak engine)
2. Dispatched by the `notifications` module
3. Gated by `Notification Dispatch Gate`

---

## 11. MVP Scope

Sprint 1 (vertical slice 003): notification infrastructure only.
- `expo-notifications` set up
- Permission request flow implemented
- Local notification channel created
- Backend notification module scaffolded
- Actual notifications: Sprint 2+.
