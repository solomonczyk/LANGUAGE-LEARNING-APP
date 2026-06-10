# Mobile Device Acceptance Matrix

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  
**ADR:** ADR-025  
**Schema:** `schemas/device_matrix.schema.json`  
**Example:** `examples/device_matrix.example.json`

---

## 1. Android Devices

| Profile | Device Class | Screen (dp) | OS Version | Emulator | Real Device | Notes |
|---------|-------------|-------------|------------|----------|-------------|-------|
| Small phone | Compact | 320–374 | Android 12+ | Required | Optional | e.g., Galaxy S3 emulator profile |
| Regular phone | Regular | 375–427 | Android 12+ | Required | Required (minimum 1) | e.g., Pixel 7 |
| Large phone | Expanded | 428–479 | Android 12+ | Required | Optional | e.g., Pixel 8 Pro emulator |
| Tablet | Tablet | 600+ | Android 12+ | Required | Optional | e.g., Pixel C emulator |
| Low memory | Compact | 320–374 | Android 12 | Required | Optional | 2GB RAM profile |

---

## 2. iOS Devices

| Profile | Device Class | Screen (dp) | OS Version | Simulator | Real Device | Notes |
|---------|-------------|-------------|------------|-----------|-------------|-------|
| Small iPhone | Compact | 320–374 | iOS 16+ | Required | Optional | iPhone SE (3rd gen) simulator |
| Regular iPhone | Regular | 375–427 | iOS 16+ | Required | Required (minimum 1) | iPhone 15 simulator, any real iPhone |
| Large iPhone | Expanded | 428–479 | iOS 16+ | Required | Optional | iPhone 15 Pro Max simulator |
| iPad | Tablet | 600+ | iPadOS 16+ | Required | Optional | iPad (10th gen) simulator |

---

## 3. Test Requirements Per Device

| Test | Android Emulator | Real Android | iOS Simulator | Real iOS | Notes |
|------|-----------------|--------------|---------------|----------|-------|
| Auth flow | ✓ | ✓ | ✓ | ✓ | |
| Onboarding | ✓ | ✓ | ✓ | ✓ | |
| Diagnostic | ✓ | ✓ | ✓ | ✓ | |
| Lesson flow | ✓ | ✓ | ✓ | ✓ | |
| Text input | ✓ | ✓ | ✓ | ✓ | |
| Navigation (all routes) | ✓ | ✓ | ✓ | ✓ | |
| Back behaviour | ✓ | — | ✓ | ✓ | Android = hardware back; iOS = swipe |
| Offline banner | ✓ | ✓ | ✓ | ✓ | |
| App background/foreground | ✓ | ✓ | ✓ | ✓ | |
| Interrupted session | ✓ | ✓ | ✓ | ✓ | |
| Keyboard overlap | ✓ | ✓ | ✓ | ✓ | |
| Small screen (320dp) | ✓ | — | ✓ | — | Emulator/simulator only |
| Large text (200%) | ✓ | — | ✓ | — | Emulator/simulator |
| Tablet layout | ✓ | — | ✓ | — | Emulator/simulator |
| Audio recording | — | ✓ | — | ✓ | Real device required (microphone) |
| Microphone permission | — | ✓ | — | ✓ | |
| Notification permission | — | ✓ | — | ✓ | |
| Performance (slow device) | ✓ (low RAM) | — | — | — | Low-memory emulator |

---

## 4. Orientation Test Requirements

| Orientation | Phone (Emulator) | Phone (Real) | Tablet (Emulator) |
|-------------|-----------------|--------------|-------------------|
| Portrait | ✓ | ✓ | ✓ |
| Landscape | ✓ | — | ✓ |
| Orientation switch | ✓ | — | ✓ |

---

## 5. Acceptance Criteria Per Device

| Criterion | All devices must: |
|-----------|------------------|
| Render | All screens render without layout breakage |
| Navigate | All routes navigable without crash |
| Input | All forms accept input |
| Offline | Offline banner displays on network loss |
| Keyboard | Input visible when keyboard open |
| Text scaling | Text readable at 200% font scale (where tested) |
| Safe area | No content under safe area/notch/home indicator |
| Touch targets | All targets ≥44dp (verified via automated check) |

---

## 6. Real Device Requirement

| Profile | Real Device Required | Fallback |
|---------|---------------------|----------|
| Regular Android phone | Yes (minimum 1) | BrowserStack or similar |
| Regular iPhone | Yes (minimum 1) | Mac mini + iPhone SE |
| Tablet | No | Emulator/simulator |
| Audio features | Yes | Microphone + speaker test |

Real devices can be physical devices or cloud-hosted (BrowserStack, AWS Device Farm).

---

## 7. Minimum Freshness

- Devices must be tested on the current OS version at time of release
- Minimum supported OS versions: Android 12 (API 31), iOS 16
- Devices are re-tested on every major release (not every CI run)

---

## 8. Automated vs Manual

| Test Type | Automation | Frequency |
|-----------|-----------|-----------|
| Layout breakpoints | Visual regression (Stories) | Per PR |
| Navigation | E2E (Detox) | Per PR |
| Auth flow | E2E + Integration | Per PR |
| Critical flows | E2E | Per PR |
| Visual QA on real devices | Manual | Per major release |
| Performance | Manual + Automation | Per milestone |
