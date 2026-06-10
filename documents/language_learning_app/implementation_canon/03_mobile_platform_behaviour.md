# Mobile Platform Behaviour

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  

---

## Principle

> Shared product behaviour + platform-native interaction where justified.

Platform-specific code is permitted **only** when:
1. A real, user-visible OS difference exists
2. The decision is documented with the specific OS reason
3. Tests exist for both platform behaviours

---

## 1. Back Navigation

| Behaviour | iOS | Android |
|-----------|-----|---------|
| Gesture | Swipe-back enabled on all stack screens (react-native-screens) | Hardware back button navigates stack |
| Header back button | Hidden by default; shown when navigation depth > 1 | Shown when navigation depth > 1 |
| Lesson session guard | Swipe-back disabled during active submission | Hardware back shows confirmation dialog: "Exit lesson? Progress will be saved." |
| Auth after login | Swipe-back disabled on post-auth screens | Hardware back goes to system home |
| Deep navigation | Back navigates within stack; no cross-stack back | Same via react-native-screens |

**Implementation:** Expo Router navigator with `gestureEnabled` prop. Set `gestureEnabled: false` on lesson routes during `submitting` state.

---

## 2. Modals

| Aspect | iOS | Android |
|--------|-----|---------|
| Presentation | Slide up from bottom | Dialog overlay (card-style) |
| Expo Router | `presentation: "modal"` | Same prop (platform adapts) |
| Dismiss | Swipe down to dismiss | Back button to dismiss |
| Use cases | Settings, confirmations, error details | Same |

---

## 3. Bottom Sheets

- Library: `@gorhom/bottom-sheet` (Expo-compatible)
- Both platforms: drag-to-dismiss gesture, backdrop overlay, snap points
- No behavioural difference between platforms for MVP

---

## 4. Permission Dialogs

**Rule:** Request permissions at point of need, never on app launch.

| Permission | When to Request | Denied Behaviour |
|------------|----------------|------------------|
| Microphone | When user taps record button (first time in lesson/recording) | Show explanation screen + "Open Settings" button (expo-linking openSettings) |
| Notifications | After first lesson completion | Show "Enable reminders?" prompt with benefits |
| Camera | Post-MVP (not in MVP) | — |

**Denied permission flow:**
1. Try request → denied
2. Show contextual explanation (why this is needed + what user is missing)
3. Single CTA: "Open Settings"
4. User returns from Settings → re-check permission → update UI
5. Never repeatedly prompt after denial

---

## 5. Notification Permissions

| Platform | Mechanism | Notes |
|----------|-----------|-------|
| iOS | `expo-notifications` requestPermissionsAsync | Requires usage description in Info.plist (`EXPermissions`) |
| Android 13+ | `POST_NOTIFICATIONS` runtime permission | `expo-notifications` handles automatically |
| Android <13 | No runtime permission needed | Notification channel created automatically |

---

## 6. Microphone Permission

| Platform | Mechanism | Notes |
|----------|-----------|-------|
| iOS | `expo-av` Audio.requestPermissionsAsync | Requires `NSMicrophoneUsageDescription` in Info.plist — set via Expo `app.json` plugin |
| Android | `expo-av` Audio.requestPermissionsAsync | Requires `RECORD_AUDIO` permission in AndroidManifest — set via Expo plugin |

---

## 7. Audio Recording Interruption

| Platform | Interruption Source | Behaviour |
|----------|-------------------|-----------|
| iOS | Phone call, alarm, Siri | Pause recording via AVAudioSession interruption handler; save draft; show "Recording paused" |
| Android | Phone call, alarm | Handle via AudioManager.OnAudioFocusChangeListener; same pause + save behaviour |
| Both | App backgrounded | Pause recording; save draft to local storage; resume on return (user re-taps record) |

---

## 8. App Lifecycle

| Event | Action |
|-------|--------|
| Background (both) | Save lesson draft to local storage; pause audio recording; persist session state timestamp |
| Foreground (both) | Reload stale server data (TanStack Query refetch); check session expiry; restore draft from local storage |
| iOS inactive → active | Refresh auth token if expired; resume from saved state |
| Android config change (orientation) | Maintain state via ViewModel-equivalent (React state persists automatically if no explicit reset) |
| Kill/terminate | Draft recovery on next launch via Zustand persist + AsyncStorage |

---

## 9. Deep Links

| Platform | URL Scheme | Implementation |
|----------|-----------|----------------|
| iOS | `llapp://` + Universal Links (`app.llapp.com`) | Expo Router deep linking config in `app.json` |
| Android | `llapp://` + App Links (`app.llapp.com`) | Expo Router deep linking config + assetlinks.json |

**Supported links in MVP:**
- `llapp://lesson-session/{id}` — Resume interrupted lesson
- `llapp://reviews` — Open review queue (from notification)
- `llapp://settings/profile` — Profile settings

---

## 10. Status Bar

- Library: `expo-status-bar`
- Style: `dark` on light backgrounds (default), `light` on splash/dark screens
- Hidden: never during normal use
- Animation: `fade` or `slide` on hidden state (not used in MVP)

---

## 11. Haptics

- Library: `expo-haptics`
- Both platforms: same API (iOS uses Taptic Engine, Android uses Vibrator API)
- Usage: correction feedback (light impact), reward notifications (medium impact), error alerts (warning)
- Disabled when user has `AccessibilitySettings.isReduceMotionEnabled()` or haptics setting off

---

## 12. Keyboard Types

| Input Type | iOS keyboardType | Android keyboardType |
|-----------|-----------------|---------------------|
| Email | `email-address` | `email-address` |
| Password | `default` + secureTextEntry | `default` + secureTextEntry |
| Numeric | `number-pad` | `number-pad` |
| URL | `url` | `url` |
| Text | `default` | `default` |
| Multiline | `default` + multiline | `default` + multiline |

Return key type: `done` for single-field forms, `next` for multi-field, `go` for search.

---

## 13. Date/Time Pickers

- Library: React Native community DateTimePicker (@react-native-community/datetimepicker)
- iOS: inline spinner
- Android: native dialog
- Format: locale-aware via date-fns

---

## 14. Secure Storage

- Library: `expo-secure-store`
- iOS: Keychain Services
- Android: EncryptedSharedPreferences (API 23+)
- Stored securely: access token, refresh token, user ID, auth session data
- NOT stored in secure store: mastery data, rewards, lesson content, PII — use AsyncStorage (encrypted if sensitive but not Keychain-level)
- Keys are automatically accessible only to this app

---

## 15. External Links

- Library: `expo-linking`
- Open external URLs (privacy policy, terms of service, app store) via `Linking.openURL()`
- For app settings (permissions): `Linking.openSettings()`
- All external links open in system browser, not in-app WebView (MVP)

---

## 16. App Settings Redirection

When user denied a permission and needs to re-enable:

1. Show contextual explanation screen (why permission is needed, what they're missing)
2. Single button: "Open Settings" — calls `Linking.openSettings()`
3. On return from Settings: re-check permission with `expo-notifications` or `expo-av` API
4. Update UI to reflect new permission state
5. Do not auto-navigate — let user see the updated state and continue

---

## Summary: Platform-Specific Code Locations

| Concern | File Location | Test File |
|---------|--------------|-----------|
| Back navigation guard | `src/shared/hooks/useBackNavigation.ts` | `__tests__/hooks/useBackNavigation.test.ts` |
| Platform-specific keyboard handling | `src/shared/components/FormField.tsx` | `__tests__/components/FormField.test.tsx` |
| Audio interruption handler | `src/features/audio/hooks/useAudioRecorder.ts` | `__tests__/features/audio/useAudioRecorder.test.ts` |
| App lifecycle handler | `src/app/_layout.tsx` (App.tsx equivalent) | `__tests__/app/lifecycle.test.ts` |
| Permission flows | `src/shared/hooks/usePermission.ts` | `__tests__/hooks/usePermission.test.ts` |
| Secure storage wrapper | `src/services/storage.ts` | `__tests__/services/storage.test.ts` |
