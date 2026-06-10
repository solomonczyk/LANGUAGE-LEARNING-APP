# Accessibility and Localization

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  
**ADR:** ADR-016  

---

## 1. Accessibility Targets

- **WCAG 2.1 Level AA** for mobile (including mobile-specific Success Criteria 2.5.8, 2.5.6, 2.6.1)
- Screen reader support: VoiceOver (iOS) and TalkBack (Android)
- Accessibility is **not optional** before production — every screen must pass basic a11y checks before acceptance

---

## 2. Screen Reader Support

| Element | Requirement |
|---------|-------------|
| Touchable elements | `accessibilityLabel` + `accessibilityRole` on every interactive element |
| Form inputs | `accessibilityLabel` with field name + `accessibilityHint` with expected format |
| Dynamic content | `accessibilityLiveRegion="polite"` for status updates |
| Headers | `accessibilityRole="header"` on section headings |
| Images | `accessibilityIgnoresInvertColors` + `accessibilityLabel` (empty string for decorative) |
| Status updates | `accessibilityLiveRegion="assertive"` for errors and important transient messages |
| Loading states | Announce "Loading" via `accessibilityLiveRegion="polite"` |
| Error states | Announce error message and field name; focus first error field |

---

## 3. Focus Order

- Natural DOM order (top-to-bottom, left-to-right in LTR)
- No manual `tabIndex` except a single skip-link: "Skip to content" at top of scrollable screens
- Modal/Dialog: trap focus within; restore focus to trigger element on close
- Bottom sheet: focus first interactive element on open
- Navigation: focus screen title on route change

---

## 4. Dynamic Font Scaling

- `allowFontScaling` = `true` on all `Text` and `TextInput` components (default)
- Important labels and buttons scale with system font size
- Test at 150% and 200% system font scale
- Minimum effective sizes:
  - Body text: 14sp/14pt
  - Caption: 12sp/12pt
  - Button: 16sp/16pt (or scale-equiv at 200%)
- Below 320dp effective width at 200% scale: switch to single-column minimal layout

---

## 5. Minimum Contrast

| Pair | Ratio | Status |
|------|-------|--------|
| Text Primary (#0F172A) on Background (#FFFFFF) | 15.0:1 | WCAG AAA |
| Text Secondary (#475569) on Background (#FFFFFF) | 5.2:1 | WCAG AA |
| Primary (#2563EB) on Background (#FFFFFF) | 4.8:1 | WCAG AA for large text |
| Error (#DC2626) on Background (#FFFFFF) | 4.6:1 | WCAG AA |
| Text on Surface (#F8FAFC) | All ≥ 4.5:1 | WCAG AA |

---

## 6. Reduced Motion

| Setting | Behaviour |
|---------|-----------|
| `prefers-reduced-motion: reduce` | Replace animations with fade (300ms) or instant transitions |
| Shimmer skeleton | Static placeholder color only |
| Parallax | Disabled |
| Scale animations | Disabled (use opacity only) |
| Page transitions | Fade only (300ms) or no animation |
| Confetti/celebration | Static badge only |

Detection: `AccessibilityInfo.isReduceMotionEnabled()` (React Native).

---

## 7. Haptic Alternatives

| Context | Visual Alternative |
|---------|-------------------|
| Correction feedback | Color flash on corrected element |
| Reward notification | Badge animation + screen change |
| Error alert | Color change + icon |

When reduced motion is enabled, haptics are also disabled.

---

## 8. Audio Alternatives

- All audio content (narratives, listening exercises, dialogue audio) must have a visible text transcript
- Transcript displayed alongside or below the audio player
- Audio player provides play/pause, progress, speed control (not just play-once)
- Transcription required before acceptance

---

## 9. Error Announcements

| Context | Announcement |
|---------|-------------|
| Form validation error | Screen reader announces "[Field name]: [error message]" on field focus |
| Submission error toast | `accessibilityLiveRegion="assertive"`: "Error: [message]" |
| Network error banner | `accessibilityLiveRegion="polite"`: "You are offline" |
| After form submit with errors | Focus first error field automatically |

---

## 10. Form Accessibility

| Element | Requirement |
|---------|-------------|
| Label | Visible label above input + `accessibilityLabel` on input |
| Required fields | Marked with "*" visually + announced as "required" |
| Error state | Visible error message + input border color + announced on focus |
| Success state | Brief checkmark announcement |
| Autofill | `textContentType` for iOS (name, email, password) + `autoComplete` for Android |

---

## 11. Localization Architecture

| Component | Technology |
|-----------|------------|
| Framework | `expo-localization` for device locale detection |
| String management | i18n strings in JSON files per locale |
| Library | `i18next` with `react-i18next` |
| ICU plurals | `i18next` ICU MessageFormat compatibility |
| Date/time | `date-fns` with locale from `date-fns/locale` |

**App UI languages (MVP):**
- `en` (English) — default, fully supported from sprint 1
- String externalization: all user-facing strings in i18n JSON files from sprint 1
- Hardcoded strings FORBIDDEN except in rapid prototypes (which must be externalized before acceptance)

---

## 12. Language Switching

| Setting | Location | Persistence |
|---------|----------|-------------|
| App UI language | Settings → Language | AsyncStorage, used as i18next language override |
| Target learning language | Learner profile → Target Language | Backend (learner_profile) |
| Native language | Learner profile → Native Language | Backend (learner_profile) |

App UI language changes apply immediately without app restart. i18next `changeLanguage()` triggers re-render.

---

## 13. Long Translations

- All text containers must accommodate **1.5× English string width** (for German, Russian, longer translations)
- Button labels: max 2 lines
- Labels and descriptions: no fixed width, wrap naturally
- Card titles: max 2 lines with `numberOfLines={2}` + ellipsis
- Use `flexShrink` + `flexWrap` to prevent overflow

---

## 14. Pluralization

- Use `i18next` plural forms (zero, one, other)
- Not: custom plural logic or string concatenation
- Example key: `{{count}} lesson` → resolves to "1 lesson" or "3 lessons" per locale

---

## 15. Date/Time Localization

- Library: `date-fns` with `date-fns/locale` (not `moment`)
- Format: relative for recent times ("2 hours ago"), absolute for older ("10 Jun 2026")
- Threshold: relative < 7 days; absolute ≥ 7 days
- Timezone: UTC stored in database; local timezone displayed via `Intl.DateTimeFormat` / `date-fns`

---

## 16. Locale-Safe Numbers

- All numeric display: use `Intl.NumberFormat` or locale-aware formatting
- Not: `Number.toString()` for user-facing values
- XP, scores, dates, times must respect locale formatting

---

## 17. RTL Readiness

- Layout direction: LTR by default (inferred from locale for future RTL languages)
- All layout uses `start` / `end` instead of `left` / `right` in StyleSheet (React Native)
- `I18nManager.isRTL` check for directional overrides
- Text alignment: `auto` (inferred from locale)
- Full RTL testing: post-MVP; structural readiness required from sprint 1

---

## 18. Mixed Native/Target Language Display

| Context | Display |
|---------|---------|
| Vocabulary card | Target word (bold) + native translation (secondary) |
| Sentence example | Target sentence (primary) + native gloss (secondary, italic) |
| Grammar explanation | Native language explanation with target language examples |
| Error correction | Target language correction + native explanation |

---

## 19. Non-Negotiable Rules

| Rule | Enforcement |
|------|-------------|
| Every interactive element must have `accessibilityLabel` | CI lint check + component test |
| No text below 14sp body / 12sp caption | Visual regression test at 200% font scale |
| All color pairs must meet 4.5:1 contrast | CI check with contrast ratio tool |
| All user-facing strings must be in i18n files | CI lint: no inline string literals in JSX |
| Every screen must have screen reader smoke test | E2E accessibility check |
