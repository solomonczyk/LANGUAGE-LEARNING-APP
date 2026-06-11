# Environment Blockers — Visual QA for Vertical Slice 003A/003B

## Unable to Test

### iOS Simulator / iOS Physical Device / iPad
- **Status**: `BLOCKED_ENVIRONMENT`
- **Reason**: Windows 10 Pro environment. macOS is required for Xcode and iOS simulator.
- **Mitigation**: No alternative available. This is a permanent blocker on this platform.
- **Impact**: Cannot verify:
  - iOS-specific safe area behavior (notch, Dynamic Island)
  - iOS-specific keyboard handling
  - iOS gesture navigation
  - iPad split-view/multitasking layout
  - iOS font rendering differences

### Android Emulator
- **Status**: `BLOCKED_ENVIRONMENT`
- **Reason**: No Android Virtual Device (AVD) configured. Android SDK not detected.
- **Mitigation**: Expo Web with responsive viewport modes was used as fallback for Android viewport sizes (375px small phone, 390px regular phone, 768px tablet). This covers layout but not native Android behavior.

### Android Physical Device
- **Status**: `BLOCKED_ENVIRONMENT`
- **Reason**: No Android device connected via ADB.
- **Mitigation**: Same as emulator — responsive viewport testing via Expo Web.

## Partially Tested

### Expo Web (react-native-web on Chromium)
- **Status**: `TESTED_AS_FALLBACK`
- **What was tested**:
  - All 9 screens at phone-regular viewport (390x844)
  - Key screens at phone-small (375x667), tablet (768x1024), desktop (1280x800)
  - 200% browser zoom (large text)
  - Network-offline state simulation
  - Error/loading states
- **Limitations of fallback**:
  - Web rendering differs from native React Native in subtle ways (font rendering, scroll physics, gesture handling)
  - No native keyboard behavior testing
  - No hardware back button testing
  - No native date picker / file picker

## Summary

| Platform | Status | Evidence |
|----------|--------|----------|
| Expo Web | ✅ PASS (fallback) | 24 screenshots |
| Android emulator | ❌ BLOCKED | — |
| Android physical | ❌ BLOCKED | — |
| iOS simulator | ❌ BLOCKED | — |
| iOS physical | ❌ BLOCKED | — |
| iPad | ❌ BLOCKED | — |
