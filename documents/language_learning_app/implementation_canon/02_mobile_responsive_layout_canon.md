# Mobile Responsive Layout Canon

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  
**ADR:** ADR-015

---

## 1. Breakpoint System

Layout decisions use **window width in density-independent pixels (dp)**, not device type. React Native `useWindowDimensions()` from `Dimensions` API.

| Breakpoint Name | Width Range (dp) | Target |
|----------------|-----------------|--------|
| `compact` | 0–374 | Small phones (iPhone SE) |
| `regular` | 375–427 | Most phones (iPhone, Pixel) |
| `expanded` | 428–599 | Large phones (Pro Max, Ultra) |
| `tablet-compact` | 600–719 | Small tablets portrait |
| `tablet-expanded` | 720–839 | Large tablets portrait |
| `max-content` | ≥840 | Max content container width |

Classes map via: `if (width >= 600 && isTablet) → tablet class; else if (width >= 428) → expanded; else if (width >= 375) → regular; else → compact`

---

## 2. Layout Width Classes

| Class | Columns | Content Max Width | Horizontal Padding | Card Layout |
|-------|---------|------------------|-------------------|-------------|
| compact | Single | 100% | 16dp | Full-width cards |
| regular | Single | 400dp centered | 20dp | Full-width cards |
| expanded | Single | 480dp centered | 24dp | Full-width cards |
| tablet-compact | Two-column | 600dp | 32dp | Grid (2 cols) |
| tablet-expanded | Two-column | 720dp | 32dp | Grid (2 cols) |

---

## 3. Horizontal Padding by Breakpoint

| Breakpoint | Padding (dp) |
|-----------|-------------|
| compact | 16 |
| regular | 20 |
| expanded | 24 |
| tablet (all) | 32 |

---

## 4. Vertical Rhythm

| Element | Spacing (dp) |
|---------|-------------|
| Base unit | 4 |
| Content spacing | 16 |
| Section spacing | 24 |
| Screen top inset | Safe area top + 8 |
| Between cards | 12 |
| Between form fields | 16 |
| Between list items | 8 |

---

## 5. Column Rules

| Screen Type | Phones | Tablets |
|-------------|--------|---------|
| Auth | Single column | Single column |
| Onboarding | Single column | Single column |
| Home/Dashboard | Single column | Two-column (catalog + focus panel) |
| Lessons | Single column | Two-column (content + analysis) |
| Lesson session | Single column | Single column (input-focused) |
| Reviews | Single column | Two-column (item + controls) |
| Settings | Single column | Single column |
| Rewards | Single column | Two-column (grid achievements) |

---

## 6. Tablet Navigation Behaviour

- Bottom tab bar remains on tablets (for thumb reachability, consistent with phone UX)
- Side rail navigation considered post-MVP
- Tab bar adapts: labels shown beside icons on tablets, icons-only on compact

---

## 7. Scrolling Rules

- **Vertical scroll:** Permitted on all screens
- **Horizontal scroll:** FORBIDDEN on auth, onboarding, lesson primary content, settings
- **Horizontal scroll:** Permitted only on horizontal carousels (lesson cards, achievement badges) with visible scroll indicators (dots or chevrons)
- Scroll position must persist on navigation stack (except on back from deep link)

---

## 8. Fixed Footer Restrictions

| Element | Max Height | Rules |
|---------|-----------|-------|
| Primary action button | 56dp | Bottom safe area + 16dp padding |
| Audio recorder bar | 72dp | Bottom safe area + 8dp padding |
| Offline banner | 40dp | Top of screen, below status bar |

- Fixed footer must not overlap with keyboard
- On keyboard open: footer should scroll up with content (KeyboardAvoidingView)
- Maximum one fixed element at a time

---

## 9. Bottom Action Area

- Safe area bottom inset + 16dp padding
- Single primary button centered
- Secondary actions rendered inline above primary (not overlapping)
- Button min height: 48dp
- No fixed bottom bar during lesson input (screen scrolls fully)

---

## 10. Keyboard Avoidance

- `KeyboardAvoidingView` on all form screens
  - iOS: `behavior="padding"`
  - Android: `behavior="height"`
- Input must remain visible when keyboard is open
- `ScrollView` with `keyboardShouldPersistTaps="handled"` on form screens
- Submit / Continue button must scroll into view (not hidden behind keyboard)
- Test with keyboard types: default, email, numeric

---

## 11. Safe Area

- Library: `react-native-safe-area-context` via Expo
- All screens wrapped in `SafeAreaView` with `edges={['top', 'bottom']}`
- iOS: respect status bar, notch, home indicator
- Android: respect status bar, navigation bar (gesture navigation)
- Content must not render under system bars

---

## 12. Notch Handling

- `SafeAreaView` with `edges={['top', 'bottom']}` handles notch area
- Notch area is treated as system bar — no interactive content placed there
- Notch cutout: do not render critical info in the top safe area margins

---

## 13. Home Indicator

- Bottom safe area includes home indicator space (34dp on modern iPhones)
- Fixed bottom elements must not overlap home indicator
- Interactive elements must be at least 20dp above home indicator bottom edge

---

## 14. Status Bar

- Library: `expo-status-bar`
- Style: `dark` on light backgrounds (most screens)
- Style: `light` on dark/splash screens
- Status bar height varies by device — use safe area insets for positioning
- Never hide status bar during normal use

---

## 15. Orientation Change

- App must re-render without crash on orientation change
- Persistent state (form input text, lesson progress, scroll position) must survive orientation change
- Detect via `Dimensions` `change` event listener; re-run breakpoint logic
- No orientation lock in MVP (portrait recommended for phones, but not enforced)
- Test on both platforms

---

## 16. Split-Screen Behaviour (iPad / Samsung DeX)

- App must not crash when resized
- Falls back to responsive rules based on new window width
- No custom split-screen layout in MVP
- Form inputs must remain usable at any supported width

---

## 17. Dynamic Type / Accessibility Text

- Font scales up to 200% without content loss
- Labels truncate with ellipsis only as last resort (and only for decorative text)
- Core action text (button labels, input hints, error messages): never truncate
- Minimum body text: 14sp/14pt
- Test breakpoints at 150% and 200% system font scale

---

## 18. Long Localized Strings

- UI containers must accommodate 1.5× English character width for German/Russian/etc.
- Button text: max 2 lines
- Labels and descriptions: no fixed width constraint, may wrap
- Card titles: max 2 lines with ellipsis
- Translation placeholders: never used; always full real strings from sprint 1

---

## 19. RTL Readiness

- Default: LTR
- All layout must use `start`/`end` instead of `left`/`right` in StyleSheet (React Native supports this natively)
- All `TextInput` and `Text` components support RTL through React Native
- `I18nManager.isRTL` check for any directional logic
- Full RTL testing deferred to post-MVP; structural readiness required from sprint 1

---

## 20. Touch Target Minimums

| Control Type | Minimum Size (dp) |
|-------------|------------------|
| Buttons | 48×48 (recommended), 44×44 (minimum) |
| Icon buttons | 44×44 |
| List item tap areas | 48px tall |
| Checkbox tap area | 44×44 |
| Switch tap area | 44×28 |
| Links (inline) | 44×44 hit area with padding |

Spacing between adjacent touch targets: minimum 8dp.

---

## 21. Error Message Placement

| Context | Placement | Style |
|---------|-----------|-------|
| Form input | Directly below the relevant input | 14sp, error color, left icon area |
| Form submission | Scroll to first error, focus it | — |
| Toast error | Top of screen, auto-dismiss 4s | Error color, dismissable |
| Network error | Offline banner at top | Warning color |
| Screen-level error | Centered error state | Title + message + retry |

---

## 22. Loading State Layout

- Skeleton placeholders matching card/row/cell dimensions
- Banner at top for long operations: spinner + message
- No layout shift on content load — reserve space with fixed-height skeletons
- Button loading: spinner replacing icon or inline right of label
- Full-screen blocking loader only during auth token refresh (brief, expected)

---

## 23. Empty State Layout

- Centered layout: illustration area (80×80dp) → title (18sp bold) → description (14sp regular) → optional CTA button
- Empty state must not feel like an error — use info tone
- CTA: primary action to resolve emptiness (e.g., "Take your first lesson")
- No empty state on lesson/submission detail if data should exist (show error instead)

---

## 24. Offline State Layout

- Fixed banner at screen top: "You're offline. Changes will sync when connected." (info style)
- Non-interactive state for network-required actions: buttons show disabled state + tooltip "Available online"
- Offline-writable areas continue to function (text input, draft saving)
- No full-screen offline block — inline indicators only

---

## 25. Forbidden Patterns

| Pattern | Reason | Alternative |
|---------|--------|-------------|
| Pixel-perfect layout tied to one screen | Breaks on other devices | Responsive with breakpoints |
| Absolute positioning of main content flow | Overlaps safe area, keyboard | Flexbox layout |
| Fixed-height lesson screen without scroll | Content clipped on small devices | ScrollView with min-height |
| Input hidden behind keyboard | Unusable form | KeyboardAvoidingView |
| Content rendered under safe area | Covered by notch/nav bar | SafeAreaView |
| Text below 14sp minimum | Accessibility fail | Use minimum 14sp body |
| Horizontal scroll on primary content | Poor UX | Responsive layout |
| `position: absolute` for layout (not overlay) | Breaks on resized windows | Flexbox |
