# Supported Platforms and Devices

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  
**ADR:** ADR-014

---

## 1. Primary MVP Platforms

| Platform | Minimum Version | Target Version | Rationale |
|----------|----------------|----------------|-----------|
| Android phones | Android 12 (API 31) | Android 14–15 | Expo SDK 52 supports API 31+ (min: API 24); ~69% Android market reach on API 31+ by mid-2025 (informational estimate) |
| iPhone | iOS 16 | iOS 18–19 | Expo SDK 52 supports iOS 16+ (min: iOS 15.1); ~89% iOS adoption on iOS 16+ by end-2024 (informational estimate) |

**Versioned decision.** Changing minimum versions requires a new ADR with compatibility analysis against current Expo SDK policy.

---

## 2. Supported Adaptive Layouts

| Device Class | Platform | Window Width Range | Layout Mode |
|-------------|----------|-------------------|-------------|
| Small tablet | Android 12+ / iPadOS 16+ | 600–719dp | Two-column adaptive |
| Large tablet | Android 12+ / iPadOS 16+ | 720–839dp | Two-column adaptive |
| iPad Pro | iPadOS 16+ | ≥840dp | Two-column with max content width 840dp |

---

## 3. Secondary Access

| Mode | Purpose | Restrictions |
|------|---------|-------------|
| Web / PWA | Operator read-only, staff diagnostics, emergency support | No learner functionality; no lesson, submission, or reward operations; basic auth and audit query only |

---

## 4. Out of Scope

| Device / Platform | Reason |
|-------------------|--------|
| HarmonyOS native | China-market-only; no Expo support |
| Windows Phone | Discontinued platform |
| Smart watches | Screen too small for meaningful input |
| Smart TV | No input capability for language exercises |
| Desktop native apps | No additional value over web + mobile |
| Foldable-specific UX | No device access; standard adaptive layout suffices |
| AR/VR devices | Post-MVP research required |

---

## 5. Phone Screen Width Classes

| Class | Width (dp) | Examples |
|-------|-----------|---------|
| Compact phone | 320–374 | iPhone SE (3rd gen: 375), Galaxy S23 (360dp in density) |
| Regular phone | 375–427 | iPhone 15 (393), Pixel 8 (412) |
| Large phone | 428–479 | iPhone 15 Pro Max (430), Galaxy S24 Ultra (456dp effective) |

---

## 6. Tablet Width Classes

| Class | Width (dp) | Layout |
|-------|-----------|--------|
| Small tablet portrait | 600–719 | Two-column, 600dp gutter |
| Large tablet portrait | 720–839 | Two-column, increased whitespace |
| Tablet landscape | ≥840 | Max content container 840dp, centered with gutters |

---

## 7. Small Device Policy

- Minimum supported width: **320dp** (Apple iPhone SE, compact Android)
- Core flows (auth, onboarding, lesson) must not have horizontal scroll
- Navigation labels may collapse to icons-only below 360dp
- Touch targets: minimum 44×44dp enforced regardless of device size
- Text must not truncate with ellipsis on primary action labels

---

## 8. Large Text Policy

- System font scale: up to 200% supported
- At 200% text on <360dp effective width: switch to single-column minimal layout (no side panels, reduced whitespace)
- All Text components must use `allowFontScaling` (default true)
- Body text minimum: 14sp/14pt
- No text clipping at any supported scale

---

## 9. Orientation Policy

| Device Class | Portrait | Landscape |
|-------------|----------|-----------|
| Phone | Primary orientation — all screens must work | Supported but not optimized; content scrolls vertically |
| Tablet | Fully supported | Full support with two-column layout where beneficial |

---

## 10. Foldable Fallback Behaviour

- Unfolded width ≥600dp: treated as tablet
- Folded: treated as phone
- No foldable-specific optimizations in MVP
- App must survive fold/unfold without crash (React Native `Dimensions` change event)

---

## 11. Unsupported Device Behaviour

| Condition | Behaviour |
|-----------|-----------|
| Below minimum OS version | Unsupported-device screen on launch with explanation |
| Web browser (non-operator) | Redirect to app store download page |
| Rooted / jailbroken | Warning on launch; allow use with disclaimer |

---

## 12. Emulator vs Real-Device Acceptance

| Requirement | Emulator/Simulator | Real Device |
|-------------|-------------------|-------------|
| Unit tests | Required | — |
| Component tests | Required | — |
| Integration tests | Required | — |
| Audio recording | — | Required (1 Android + 1 iOS) |
| Microphone permission flow | — | Required |
| Notification permission flow | — | Required |
| Offline mode | — | Required (1 device) |
| Interrupt recovery | — | Required (1 device) |
| App lifecycle (bg/fg) | — | Required (1 device) |
| Layout visual check | Required (all width classes via emulator) | Required (at least 1 phone + 1 tablet) |

Reference: [Device Acceptance Matrix](23_mobile_device_acceptance_matrix.md)

---

## 13. Versioning Governance

Any change to platform support requires:
1. Comparison matrix against current Expo SDK compatibility
2. ADR with migration impact analysis
3. Device matrix update
4. Compatibility tests for dropped and added versions
