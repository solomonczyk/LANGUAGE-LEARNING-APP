# Design System

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  
**ADR:** ADR-016  
**Schema:** `schemas/design_tokens.schema.json`  
**Example:** `examples/design_tokens.example.json`

---

## 1. Design Tokens

### 1.1 Colors

| Token | Value | Usage |
|-------|-------|-------|
| `color.primary` | #2563EB (Blue 600) | Primary actions, active states, links |
| `color.primaryDark` | #1D4ED8 (Blue 700) | Pressed state of primary |
| `color.secondary` | #7C3AED (Violet 600) | Secondary actions, highlights |
| `color.success` | #16A34A (Green 600) | Success states, completion |
| `color.warning` | #D97706 (Amber 600) | Warnings, cautions |
| `color.error` | #DC2626 (Red 600) | Errors, destructive actions |
| `color.info` | #0284C7 (Sky 600) | Informational banners |
| `color.background` | #FFFFFF | Screen backgrounds |
| `color.surface` | #F8FAFC (Slate 50) | Card surfaces, secondary areas |
| `color.surfaceSecondary` | #F1F5F9 (Slate 100) | Tertiary surfaces |
| `color.textPrimary` | #0F172A (Slate 900) | Primary body text |
| `color.textSecondary` | #475569 (Slate 600) | Secondary/helper text |
| `color.textDisabled` | #94A3B8 (Slate 400) | Disabled content |
| `color.border` | #E2E8F0 (Slate 200) | Borders, dividers |
| `color.borderFocus` | #2563EB (Blue 600) | Focus ring |
| `color.borderError` | #DC2626 (Red 600) | Error border |
| `color.overlay` | rgba(15, 23, 42, 0.4) | Modal/backdrop overlays |

**Contrast ratios** (all meet WCAG AA 4.5:1 minimum):
- Text Primary (#0F172A) on Background (#FFFFFF): 15.0:1
- Text Secondary (#475569) on Background (#FFFFFF): 5.2:1
- Text Primary (#0F172A) on Surface (#F8FAFC): 14.2:1

### 1.2 Typography

| Token | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| `typo.display` | 32sp | Bold (700) | 40sp | Hero titles |
| `typo.h1` | 28sp | Bold (700) | 36sp | Screen titles |
| `typo.h2` | 24sp | Bold (700) | 32sp | Section headers |
| `typo.h3` | 20sp | Semibold (600) | 28sp | Card titles |
| `typo.subtitle` | 18sp | Semibold (600) | 24sp | Subtitles |
| `typo.body` | 16sp | Regular (400) | 24sp | Body text |
| `typo.bodySmall` | 14sp | Regular (400) | 20sp | Secondary text |
| `typo.caption` | 12sp | Regular (400) | 16sp | Labels, timestamps |
| `typo.button` | 16sp | Semibold (600) | 24sp | Button labels |
| `typo.buttonSmall` | 14sp | Semibold (600) | 20sp | Small button labels |
| `typo.overline` | 12sp | Medium (500) | 16sp | Section overlines, uppercase |

Font family: system default (SF Pro on iOS, Roboto on Android). Use `Platform.select()` for platform-optimal font only if needed; otherwise unset.

### 1.3 Spacing Scale

| Token | Value (dp) |
|-------|-----------|
| `spacing.xxs` | 4 |
| `spacing.xs` | 8 |
| `spacing.sm` | 12 |
| `spacing.md` | 16 |
| `spacing.lg` | 20 |
| `spacing.xl` | 24 |
| `spacing.xxl` | 32 |
| `spacing.xxxl` | 40 |
| `spacing.huge` | 48 |
| `spacing.giant` | 64 |

### 1.4 Border Radius

| Token | Value (dp) |
|-------|-----------|
| `radius.sm` | 6 |
| `radius.md` | 10 |
| `radius.lg` | 16 |
| `radius.full` | 999 |

### 1.5 Elevation / Shadows

| Token | iOS Shadow | Android Elevation | Usage |
|-------|-----------|-------------------|-------|
| `elevation.sm` | color: #000, opacity: 0.08, y: 1, blur: 2 | 2 | Cards |
| `elevation.md` | color: #000, opacity: 0.10, y: 2, blur: 4 | 4 | Bottom sheet |
| `elevation.lg` | color: #000, opacity: 0.12, y: 4, blur: 8 | 8 | Modal backdrop |
| `elevation.xl` | color: #000, opacity: 0.16, y: 8, blur: 16 | 16 | Dialog |

### 1.6 Opacity

| Token | Value | Usage |
|-------|-------|-------|
| `opacity.disabled` | 0.40 | Disabled components |
| `opacity.overlay` | 0.50 | Modal backdrops |
| `opacity.subtle` | 0.08 | Ripple/focus backgrounds |

### 1.7 Motion Durations

| Token | Duration (ms) | Usage |
|-------|---------------|-------|
| `motion.fast` | 150 | Micro-interactions (press) |
| `motion.normal` | 250 | Transitions, navigation |
| `motion.slow` | 350 | Modals, bottom sheets |
| `motion.toast` | 4000 | Toast auto-dismiss |

### 1.8 Z-Index Layers

| Layer | Value | Elements |
|-------|-------|----------|
| `z.base` | 0 | Page content |
| `z.card` | 10 | Cards, elevated surfaces |
| `z.sticky` | 100 | Sticky headers |
| `z.header` | 200 | Navigation bar |
| `z.overlay` | 1000 | Backdrop overlays |
| `z.bottomSheet` | 1500 | Bottom sheet |
| `z.modal` | 2000 | Modal dialogs |
| `z.toast` | 3000 | Toast notifications |
| `z.offlineBanner` | 3100 | Offline/status banners |

---

## 2. Component Catalog

### 2.1 Button
- **Purpose:** Primary action trigger
- **Variants:** `primary` (filled, primary color), `secondary` (outlined, primary border), `text` (no border/background), `icon` (icon only)
- **States:** enabled, pressed (opacity 0.8), disabled (opacity 0.4), loading (spinner replacing icon)
- **Touch target:** minimum 48×48dp
- **Accessibility role:** `button`
- **Platform differences:** None
- **Forbidden:** Multiple primary buttons on one view without clear hierarchy

### 2.2 IconButton
- **Purpose:** Icon-only action trigger
- **Variants:** default, outlined
- **States:** enabled, pressed, disabled
- **Touch target:** minimum 44×44dp (icon may be 24×24 within)
- **Accessibility role:** `button` with `accessibilityLabel`

### 2.3 Input
- **Purpose:** Single-line text input
- **Variants:** text, email, password (with show/hide toggle), numeric
- **States:** default, focused (primary border), error (error border + message), disabled (gray background)
- **Accessibility role:** none (native TextInput)
- **Forbidden:** placeholder as label (use visible label always)

### 2.4 Textarea
- **Purpose:** Multi-line text input for lesson submissions
- **States:** same as Input
- **Min height:** 120dp
- **Max height:** 400dp (scroll within)
- **Character count:** optional, 0/500 style

### 2.5 Select
- **Purpose:** Single option selection from predefined list
- **Variants:** `native` (platform native picker for MVP), `custom` (post-MVP)
- **States:** default, focused, disabled
- **Platform:** iOS: wheel picker; Android: native dropdown

### 2.6 Checkbox
- **Purpose:** Binary/multi-select option
- **States:** checked, unchecked, indeterminate, disabled
- **Touch target:** 44×44dp
- **Accessibility role:** `checkbox` with `accessibilityState`

### 2.7 Radio
- **Purpose:** Single-select from small group (2–5 options)
- **States:** selected, unselected, disabled
- **Touch target:** 44×44dp
- **Accessibility role:** `radio`

### 2.8 Switch
- **Purpose:** Binary setting toggle
- **Variants:** default (primary color when on)
- **States:** on, off, disabled
- **Touch target:** 44×28dp
- **Accessibility role:** `switch`

### 2.9 Card
- **Purpose:** Content container for grouped information
- **Variants:** default, pressed (if tappable), disabled
- **Content:** title (optional), body, actions (optional)
- **Border radius:** 10dp (medium)
- **Elevation:** sm (shadow 2dp)
- **Padding:** 16dp
- **Forbidden:** cards inside scrollable cards

### 2.10 ListItem
- **Purpose:** Single row in a list/settings
- **Variants:** single-line, two-line, three-line; with/without icon; with/without chevron
- **Touch target:** minimum 48px height
- **Accessibility role:** `menuitem` or `button`

### 2.11 Progress
- **Purpose:** Visual progress indicator
- **Variants:** `linear` (0–100% bar), `circular` (lesson completion ring)
- **States:** determinate (known progress), indeterminate (unknown)
- **Linear height:** 4dp (bar), 8dp (with label)
- **Colors:** primary for active, success for complete, error for failed

### 2.12 Badge
- **Purpose:** Status indicator label
- **Variants:** default (neutral), success, warning, error, info
- **Size:** small (16dp), default (20dp+)
- **Position:** inline or top-right corner on icon

### 2.13 Alert
- **Purpose:** Inline contextual message
- **Variants:** success, warning, error, info
- **Content:** icon + title (optional) + message + optional dismiss button
- **Placement:** inline in content flow
- **Accessibility role:** `alert` with `accessibilityLiveRegion="polite"`

### 2.14 Toast
- **Purpose:** Transient notification at top of screen
- **Variants:** success, error, info
- **Duration:** auto-dismiss after 4s
- **Stack:** up to 3 toasts visible
- **Action:** optional undo/retry action
- **Z-index:** 3000
- **Accessibility:** `accessibilityLiveRegion="assertive"`

### 2.15 Dialog
- **Purpose:** Critical confirmation requiring user action
- **Variants:** alert (single acknowledge), confirm (accept/cancel)
- **Content:** title + message + action buttons (max 2)
- **Overlay:** opaque backdrop, dismissable via Cancel only
- **Z-index:** 2000

### 2.16 BottomSheet
- **Purpose:** Supplementary content or selection
- **Library:** @gorhom/bottom-sheet
- **Snap points:** dynamic based on content
- **Behaviour:** drag-to-dismiss, backdrop overlay, keyboard-aware
- **Z-index:** 1500

### 2.17 Tabs
- **Purpose:** Content category switching
- **Variants:** `underline` (underline active tab), `contained` (filled active tab)
- **Scrollable:** yes, when >4 tabs
- **States:** active (primary color), inactive (text secondary)

### 2.18 NavigationBar
- **Purpose:** Primary bottom navigation (tab bar)
- **Variants:** icons + labels, icons-only (compact <360dp)
- **States:** active tab (primary icon + label), inactive tab (text secondary)
- **Max tabs:** 5
- **Z-index:** 100
- **Forbidden:** more than 5 tabs; hidden tab bar during lesson

### 2.19 LessonHeader
- **Purpose:** Top bar during lesson session
- **Content:** back button + lesson title + progress indicator + menu
- **Sticky:** fixed below status bar during scroll
- **No platform differences**

### 2.20 TaskCard
- **Purpose:** Lesson/review task representation in lists
- **Content:** title + type badge + difficulty indicator + completion status
- **Variants:** available (tappable), completed (greyed + checkmark), locked (disabled + lock icon)

### 2.21 HintCard
- **Purpose:** Expandable hint/tip within lesson
- **Variants:** collapsed (show "Show hint") / expanded (show content)
- **States:** default, shown, dismissed
- **Dismiss:** "Got it" collapses for session duration
- **Content:** tip text, optional example

### 2.22 CorrectionBlock
- **Purpose:** Display AI correction with original and explanation
- **Content:** original text (strikethrough) → correction (highlighted) → explanation (body small)
- **Variants:** single correction, multiple corrections (list)

### 2.23 QuizOption
- **Purpose:** Selectable option in quiz/assessment
- **Variants:** letter (A/B/C/D prefix), icon
- **States:** default, selected (primary border), correct (green), incorrect (red), disabled
- **Touch target:** 48px height minimum

### 2.24 AudioRecorder
- **Purpose:** Record and review audio input
- **States:** idle, recording, paused, reviewing (playback), completed
- **Content:** waveform visual (placeholder), duration counter, controls (record/pause/stop/play)
- **Retry:** allow re-record before submission
- **Max duration:** displayed and enforced

### 2.25 AudioPlayer
- **Purpose:** Playback of audio content or recordings
- **Content:** play/pause button, progress bar, elapsed/total time, speed control (0.5×, 1×, 1.5×, 2×)

### 2.26 RetryPanel
- **Purpose:** Show retry status after failed submission
- **Content:** retry count (3 remaining), failure reason, retry button (or disabled if limit reached)

### 2.27 OfflineBanner
- **Purpose:** Persistent indicator when offline
- **Content:** icon + "You're offline" + "Changes will sync when connected"
- **Z-index:** 3100 (top of all content)
- **Dismissable:** yes (snooze until next offline detection)
- **Auto-show:** on network status change to offline

### 2.28 ErrorState
- **Purpose:** Screen-level error fallback
- **Content:** centered icon (80×80) + title + description + retry CTA button
- **Placement:** fills screen center
- **Accessibility:** focus set to error title on appearance

### 2.29 EmptyState
- **Purpose:** Placeholder when no data exists
- **Content:** illustration area (80×80) + title (18sp bold) + description (14sp) + optional CTA
- **Tone:** encouraging, not error-like

### 2.30 LoadingSkeleton
- **Purpose:** Placeholder during data loading
- **Variants:** card (rectangle with rounded corners), text (two lines), avatar (circle)
- **Animation:** shimmer (opacity wave) — disabled if prefers-reduced-motion
- **Dimension:** matches target content dimensions exactly to prevent layout shift

### 2.31 FormField
- **Purpose:** Composable form field wrapper
- **Content:** label + Input/Textarea/Select + helper text + error message
- **States:** default, focused, error, disabled
- **Spacing:** label 8dp above input, error 4dp below input

### 2.32 ScreenShell
- **Purpose:** Base screen wrapper that composes safe area, scroll, keyboard, and banner
- **Props:** `scroll` (boolean), `keyboardAvoid` (boolean), `padding` (boolean), `offlineBanner` (boolean)
- **Composition:** SafeAreaView → OfflineBanner(conditional) → KeyboardAvoidingView → ScrollView(conditional) → children
