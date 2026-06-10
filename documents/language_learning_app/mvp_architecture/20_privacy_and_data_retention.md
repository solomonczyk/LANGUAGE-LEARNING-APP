# Privacy and Data Retention

**Status:** Draft  
**Version:** 1.0.0  
**Last updated:** 2026-06-10

---

## Data Classification

| Category | Data Elements | Classification | Collected | Purpose |
|----------|--------------|----------------|-----------|---------|
| Personal data | Email, display name, auth identity | **Confidential** | Registration | Account management, authentication |
| Profile data | Target language, native language, goals, interests | **Internal** | Onboarding, settings | Personalization |
| Learning data | Submissions, responses, scores, assessments | **Internal** | Lessons, diagnostics | Progress tracking, analysis |
| Audio data | Voice recordings | **Confidential** | Audio lessons | Speech analysis, pronunciation assessment |
| Transcript data | Text versions of audio, STT output | **Internal** | Audio processing | Analysis pipeline |
| AI provider payloads | Submissions sent to LLM for analysis | **Confidential** | Lesson pipeline | AI-powered analysis |
| Analytics data | Usage stats, device info, session duration | **Internal** | All sessions | Product improvement |
| Audit data | Event logs with user references | **Confidential** | All operations | Accountability, troubleshooting |

---

## Retention Periods

| Data Category | Active Retention | Archive/Anonymized | Deletion |
|---------------|-----------------|-------------------|----------|
| Auth identity | Until account deletion | N/A | Immediate on deletion request |
| Profile data | Until account deletion | N/A | Deletes with account |
| Learning data | 2 years post-last-activity | Anonymized after 2 years | Deleted after 5 years |
| Audio recordings | 90 days | Transcripts retained (internal) | Audio deleted after 90 days |
| AI provider payloads | 30 days (operational logs) | 90 days (audit logs) | Deleted after 90 days |
| Analytics data | 13 months | Aggregated (no PII) indefinitely | Raw data deleted after 13 months |
| Audit data | 3 years | N/A | Deleted after 3 years |
| Security events | 1 year | N/A | Deleted after 1 year |

---

## Deletion Workflow

### User-Initiated Deletion

1. **Request**: User submits deletion request via app settings or contacts operator
2. **Verification**: User identity verified (re-authentication required)
3. **Processing** (within 72 hours):
   - User record soft-deleted (immediate login block)
   - Auth identity removed from auth provider
   - Profile data deleted
   - Learning data anonymized (profile_id disassociated from user identity)
   - Audio recordings deleted (or marked for deletion within 24h)
   - Audit events retained (user reference pseudonymized)
   - Analytics data anonymized
4. **Confirmation**: User notified via email
5. **Hard deletion**: After 90-day grace period, soft-deleted records purged

### What Is Retained After Deletion
- Audit events (with pseudonymized user reference — traceable to action but not to individual)
- Anonymized learning data (no PII link)
- Aggregated analytics (no individual identification)

---

## Export Workflow

1. **Request**: User requests data export via app settings
2. **Preparation** (within 7 days):
   - Profile data packaged as JSON
   - Learning history packaged as JSON
   - Reward history packaged as JSON
   - Audio recordings packaged as downloadable files
3. **Delivery**: Secure download link sent to user email (expires in 14 days)
4. **Format**: JSON files with documentation, organized by category
5. **Scope**: All personal data, learning data, and reward data

---

## Data Minimization

### What is NOT Collected
- Exact location data (only language region preference)
- Contact list or address book
- Biometric data beyond voice recordings
- Browsing history outside the app
- Payment information (MVP has no payments)
- Social network connections (MVP has no social features)

### Purpose Limitation
Data collected for one purpose is not used for another purpose without explicit consent. Specifically:
- Learning data is used only for personalization and improvement
- Audio recordings are used only for analysis; not for training external models
- Analytics data is used only for product improvement, not for advertising

---

## Consent Boundaries

| Action | Consent Required | Revocable |
|--------|-----------------|-----------|
| Account creation and data storage | Yes (ToS acceptance) | Yes (account deletion) |
| Audio recording | Yes (per-session permission) | Yes (deny microphone) |
| AI analysis of submissions | Yes (implicit in lesson start) | Yes (stop using AI features) |
| Push notifications | Yes (OS-level) | Yes (OS settings) |
| Analytics collection | Yes (implicit in ToS) | Yes (opt-out in settings) |
| Data processing by AI providers | Yes (implicit in ToS) | Yes (delete account) |

---

## Child User Assumptions

**The MVP assumes all users are 16 years of age or older.**

- No child-specific data handling or consent mechanisms are implemented
- No COPPA/GDPR-K compliance measures are included in MVP scope
- Age verification at registration (self-reported, minimum 16)
- If under-16 users are identified, their accounts will be suspended pending parental consent (manual process)
- A future legal review is required before expanding to younger users

---

## Cross-Border Data Risks

| Risk | Description | Mitigation |
|------|-------------|------------|
| AI provider data processing | Learner submissions sent to LLM providers may be processed on servers in different jurisdictions | Provider data processing agreements; data minimization; avoid sending PII to providers |
| Auth provider data storage | Auth identity stored by Supabase (US-based) | Supabase SOC 2 compliance; data processing agreement |
| Object storage location | Audio files stored in region-configured S3-compatible storage | Configure storage region close to user base |
| Analytics data transfer | Usage analytics may be processed across regions | Analytics data anonymized; processing agreement with analytics provider |

---

## Legal Notice

**This document describes privacy and data retention plans for the MVP architecture. It does not constitute a legal privacy policy or compliance verification.**

**Required actions before production release:**
- Separate legal review of data processing practices
- Privacy policy drafted by legal counsel
- Data processing agreements with all third-party providers
- Regulatory compliance assessment (GDPR, CCPA, etc.)
- DPA (Data Processing Agreement) with AI providers
- User-facing privacy policy implementation
- Consent mechanism implementation
