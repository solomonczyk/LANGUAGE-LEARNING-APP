# Implementation Canon Architecture Decision Log

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  

---

## ADR Index

| ADR | Title | Status |
|-----|-------|--------|
| ADR-013 | Zustand for Local State | Accepted |
| ADR-014 | Supported Mobile Platforms | Accepted |
| ADR-015 | Responsive Layout Policy | Accepted |
| ADR-016 | Design System Token Architecture | Accepted |
| ADR-017 | Navigation Architecture | Accepted |
| ADR-018 | Frontend Feature Architecture | Accepted |
| ADR-019 | API Versioning and Error Contract | Accepted |
| ADR-020 | Database Migration Policy | Accepted |
| ADR-021 | Supabase Auth Boundary | Accepted |
| ADR-022 | Audio Storage and Processing Boundary | Accepted |
| ADR-023 | Offline and Sync Policy | Accepted |
| ADR-024 | Mobile Observability | Accepted |
| ADR-025 | Device Acceptance Strategy | Accepted |
| ADR-026 | Implementation Change-Control Policy | Accepted |

---

## ADR-013: Zustand for Local State

**Status:** Accepted  
**Date:** 2026-06-10  
**ADRs superseded:** None

### Context
The frontend needs a local state management solution for UI state, temporary data, and non-server state. Options included Zustand, Redux Toolkit, Jotai, Valtio, and React Context.

### Decision
Use Zustand as the exclusive local state management library. Redux, MobX, Jotai, Valtio, and other alternatives are not permitted without a new ADR.

### Alternatives Considered
- Redux Toolkit — more boilerplate, steeper learning curve, over-engineered for MVP scope
- Jotai — good for atomic state but less mature ecosystem than Zustand
- React Context — not suitable for frequent updates or cross-component state without re-render issues
- Valtio — proxy-based, less familiar pattern

### Consequences
Positive: minimal boilerplate, TypeScript-native, simple API, middleware support for persistence, small bundle size. Negative: less opinionated than Redux, team must enforce store structure discipline.

### Affected Documents
08_frontend_state_management.md

---

## ADR-014: Supported Mobile Platforms

**Status:** Accepted  
**Date:** 2026-06-10

### Context
The mobile app must define which platforms and OS versions are supported. The decision must align with Expo SDK 52 support policy and provide sufficient market coverage.

### Decision
Primary platforms: Android phones (Android 12+, API 31) and iPhone (iOS 16+). Adaptive layouts: Android tablets and iPad (iPadOS 16+). Secondary: Web/PWA for operator/staff read-only access only.

### Alternatives Considered
- Android 8+ (API 26) — broader reach but Expo SDK 52 requires API 31+
- iOS 15 — Expo SDK 52 requires iOS 16+
- Flutter — cross-platform but adds Dart language to the stack
- PWA-only — insufficient native API access (audio, notifications, biometrics)
- Native Android + iOS — too slow for MVP

### Consequences
Positive: aligned with Expo SDK support, covers ~85% Android and ~90% iOS market. Negative: excludes older devices that may still be in use.

### Affected Documents
01_supported_platforms_and_devices.md, 23_mobile_device_acceptance_matrix.md

---

## ADR-015: Responsive Layout Policy

**Status:** Accepted  
**Date:** 2026-06-10

### Context
The app must render correctly across phone and tablet screen sizes. The layout system must handle breakpoints, safe areas, keyboard avoidance, and orientation changes.

### Decision
Use window width (dp) based breakpoints with 6 classes (compact, regular, expanded, tablet-compact, tablet-expanded, max-content). Phones are single-column; tablets use two-column layout where beneficial. SafeAreaContext for system bars. KeyboardAvoidingView for all forms. Minimum touch target 44×44dp.

### Alternatives Considered
- Device-type-based breakpoints — less reliable (device detection is fragile)
- Single breakpoint — insufficient for the device range
- CSS media query approach — React Native uses JS-based breakpoints
- No responsive (separate phone/tablet codebases) — double maintenance

### Consequences
Positive: single codebase adapts to all supported devices, consistent UX. Negative: testing burden across breakpoints.

### Affected Documents
02_mobile_responsive_layout_canon.md

---

## ADR-016: Design System Token Architecture

**Status:** Accepted  
**Date:** 2026-06-10

### Context
A consistent design system is required for UI coherence, accessibility compliance, and developer velocity. The system needs tokens (colors, typography, spacing) and a component catalog.

### Decision
Create a token-based design system with defined colors (accessible contrast), typography (system fonts), spacing scale (4dp base), border radius, elevation, and a catalog of 32 components. Tokens defined in a JSON schema with examples.

### Alternatives Considered
- CSS-in-JS (styled-components) — adds dependency, runtime overhead
- Tailwind for React Native — not yet mature
- Platform-native components only — inconsistent across platforms
- Third-party UI library (NativeBase, Paper) — bundle size, styling conflicts, maintenance risk

### Consequences
Positive: consistent UI, accessibility built-in, developer reference, easier testing. Negative: upfront design cost, component maintenance.

### Affected Documents
04_design_system.md, 05_accessibility_and_localization.md

---

## ADR-017: Navigation Architecture

**Status:** Accepted  
**Date:** 2026-06-10

### Context
Navigation must support auth, onboarding, diagnostic, learning contract, lesson sessions, and standard tab-based navigation. Deep links, route guards, and session restoration are required.

### Decision
Use Expo Router v4 (file-based routing) with the defined route map covering /auth, /onboarding, /diagnostic, /learning-contract, /(app) tabs, /lesson-session/:id, /submission/:id, /operator. Route guard chain: auth → onboarding → diagnostic → learning-contract → lesson access.

### Alternatives Considered
- React Navigation directly — more control but more setup; Expo Router provides file-based convention
- React Native Navigation (Wix) — native, but less Expo-compatible

### Consequences
Positive: file-based convention simplifies route management, deep linking built-in, platform-adaptive modal/bottom-sheet presentation. Negative: Expo Router version upgrades may change API.

### Affected Documents
06_navigation_and_route_canon.md

---

## ADR-018: Frontend Feature Architecture

**Status:** Accepted  
**Date:** 2026-06-10

### Context
The frontend codebase needs a structure that supports feature isolation, clear import boundaries, and separation of concerns.

### Decision
Feature-based structure: `app/` (routes), `src/features/` (feature modules), `src/entities/` (domain types), `src/shared/` (reusable UI and utilities), `src/services/` (external integrations), `src/state/` (global state). Features may import from shared/entities/services/state but not from other features.

### Alternatives Considered
- Type-based (components/containers/hooks split by type) — harder to navigate as app grows, features scattered across directories
- Module-based per screen — excessive granularity
- Flat structure — unmanageable beyond ~20 files

### Consequences
Positive: clear ownership, isolated features, testable modules, scalable. Negative: requires discipline on import boundaries.

### Affected Documents
07_frontend_architecture.md

---

## ADR-019: API Versioning and Error Contract

**Status:** Accepted  
**Date:** 2026-06-10

### Context
The API needs a consistent versioning scheme, error contract, pagination convention, and deprecation policy.

### Decision
All endpoints under `/api/v1/`. Canonical JSON error contract with code, message, details, trace_id, retryable. Offset/limit pagination. Backward-compatible changes within v1; breaking changes require /api/v2/ with migration guide. OpenAPI spec auto-generated by FastAPI. Contract tests required for all endpoints.

### Alternatives Considered
- Header-based versioning (Accept: application/vnd.llapp.v1+json) — less discoverable, harder to test
- No versioning — breaks clients on any change
- Custom error formats per endpoint — inconsistent client handling

### Consequences
Positive: consistent client handling, discoverable versioning, auto-generated docs, contract-tested. Negative: URL versioning commits to path forever.

### Affected Documents
09_frontend_api_and_error_handling.md, 12_api_design_canon.md

---

## ADR-020: Database Migration Policy

**Status:** Accepted  
**Date:** 2026-06-10

### Context
Database schema changes must be managed with versioned, testable, reversible migrations. Convention is critical for team consistency.

### Decision
Alembic for migrations. Naming: snake_case tables (plural), UUID primary keys, timestamptz timestamps. Every migration must have upgrade and downgrade tested in CI. Migration names are immutable after commit. No application model references in migrations.

### Alternatives Considered
- Manual SQL scripts — no versioning, no rollback tracking
- ORM auto-migration only — misses edge cases and renames
- No rollback (upgrade only) — dangerous for staging/production

### Consequences
Positive: testable, reversible, consistent. Negative: migration overhead for each schema change.

### Affected Documents
13_database_and_migration_canon.md

---

## ADR-021: Supabase Auth Boundary

**Status:** Accepted  
**Date:** 2026-06-10

### Context
Authentication must integrate with Supabase Auth while maintaining clear boundaries between auth provider and application logic.

### Decision
Supabase Auth handles identity (signup, signin, token management). Backend verifies JWT on every request. Backend maps Supabase user ID to local user record. Backend NEVER trusts user_id or role from request body. Roles: learner (default), operator (read-only). Token storage: expo-secure-store only.

### Alternatives Considered
- Clerk — richer features but more expensive for scaling
- Firebase Auth — vendor lock-in, Google ecosystem dependency
- Self-hosted JWT — full control but significant implementation and security maintenance cost

### Consequences
Positive: quick integration, social login built-in, JWT management handled. Negative: third-party dependency, user data on Supabase infra.

### Affected Documents
14_authentication_and_authorization.md

---

## ADR-022: Audio Storage and Processing Boundary

**Status:** Accepted  
**Date:** 2026-06-10

### Context
Audio recording and processing requires storage, format decisions, and processing pipeline. Must work in MVP with mock mode and defer real AI analysis to post-MVP.

### Decision
Format: AAC-LC (.m4a), 44.1kHz, 128kbps. Max duration: 120s. Max file size: 5MB. Storage: S3-compatible (MinIO local, Cloudflare R2 staging). SHA-256 checksum for deduplication. Transcript via AI Gateway analyze_transcript(). Audio runtime is out of scope for Sprint 1 (vertical slice 003) — UI stubs only.

### Alternatives Considered
- WAV — lossless but too large (44.1kHz × 16bit × 120s = ~10MB)
- Opus — better compression but less universal playback
- Store in PostgreSQL as BLOB — anti-pattern for media
- Google Speech-to-Text — vendor lock-in for MVP

### Consequences
Positive: standard format, S3 portability, deduplication via checksum. Negative: audio runtime deferred to Sprint 2+.

### Affected Documents
17_audio_and_media_canon.md

---

## ADR-023: Offline and Sync Policy

**Status:** Accepted  
**Date:** 2026-06-10

### Context
The app must handle offline scenarios gracefully, preserve user drafts, and recover from interrupted sessions. The policy must define what works offline, what requires network, and conflict resolution.

### Decision
Offline-readable: cached server data (lesson definitions, home screen). Offline-writable: draft text (Zustand persist), local settings. Network-required: submission, lesson start, diagnostic, auth. Server is source of truth for all state transitions. Idempotency keys prevent duplicates on sync. Interrupted session recovery via draft preservation and server state check.

### Alternatives Considered
- Full offline mode (complete offline CRUD) — complex conflict resolution, risk of stale data
- No offline support — poor UX on mobile with intermittent connectivity
- Optimistic concurrency (client-first) — risk of server rejection

### Consequences
Positive: draft preservation, session recovery, clear offline boundaries. Negative: submission requires connectivity; full offline lesson completion deferred.

### Affected Documents
19_offline_sync_and_recovery.md

---

## ADR-024: Mobile Observability

**Status:** Accepted  
**Date:** 2026-06-10

### Context
The mobile app needs error tracking, performance monitoring, and usage analytics to debug issues and measure quality. Must respect user privacy.

### Decision
Sentry for error tracking (free tier). OpenTelemetry-compatible traces via HTTP headers (X-Trace-Id). Structured analytics events (opt-in, anonymous by default). No third-party analytics SDKs (no Firebase Analytics, no Mixpanel). All telemetry pseudonymized (user UUID, not email/name).

### Alternatives Considered
- Firebase Crashlytics — vendor lock-in, Google dependency
- Datadog RUM — expensive for MVP
- Self-hosted Grafana Faro — operational overhead
- No mobile telemetry — blind to issues

### Consequences
Positive: error visibility, performance tracking, privacy-respecting analytics. Negative: self-hosted backend observability stack needed.

### Affected Documents
25_observability_and_audit.md

---

## ADR-025: Device Acceptance Strategy

**Status:** Accepted  
**Date:** 2026-06-10

### Context
The mobile app must define which devices are tested, at what fidelity (emulator vs real), and the acceptance criteria per device.

### Decision
Minimum device matrix: 4 Android profiles (small/regular/large phone + tablet), 4 iOS profiles (small/regular/large iPhone + iPad). Real devices required: 1 Android phone + 1 iPhone. Emulator/simulator for other profiles. Real device required for: audio, microphone permission, notification permission, offline, lifecycle. Acceptance: all screens render, keyboard visible, safe area respected, touch targets ≥44dp, text at 200% readable.

### Alternatives Considered
- Emulator-only testing — misses real-device issues (audio, permissions, performance)
- Full real-device matrix (10+ devices) — expensive and hard to maintain for MVP
- Cloud device farm only — latency, limited interactive testing

### Consequences
Positive: practical coverage with minimum real devices, clear acceptance criteria. Negative: some device-specific issues may slip through emulator-only profiles.

### Affected Documents
23_mobile_device_acceptance_matrix.md

---

## ADR-026: Implementation Change-Control Policy

**Status:** Accepted  
**Date:** 2026-06-10

### Context
After the implementation canon is accepted, future feature tasks must not unilaterally change fundamental decisions. A change control mechanism is needed.

### Decision
Changes to fundamental decisions (framework, state management, database, auth provider, AI provider boundary, API versioning, breakpoints, OS support, design tokens, mastery authority, reward authority, production gate, module boundaries, data source of truth) require a new ADR. ADR template includes: context, problem, decision, alternatives, consequences, migration impact, rollback, compatibility, tests, affected documents, affected modules.

### Alternatives Considered
- No control (any task can change anything) — inconsistent decisions, architecture erosion
- Strict change board — too heavy for MVP team
- Verbal agreement — undocumented, unenforceable

### Consequences
Positive: documented decisions, traceable changes, prevented architecture erosion. Negative: overhead of ADR process for changes.

### Affected Documents
30_change_control_and_adr_policy.md
