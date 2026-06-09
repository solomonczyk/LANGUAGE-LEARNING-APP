# Data Retention, Export and Deletion

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Policies for data retention periods, user data export, and account deletion.

## In scope

- AI security and prompt injection defense
- Anti-cheat and learning integrity
- Authorization and tool access policy
- Reward economy integrity
- Untrusted content handling
- User data isolation and privacy
- Rate limiting, logging, red team testing
- Sensitive content and data retention

## Out of scope

- Implementation of security controls
- Specific encryption libraries
- Production security configuration
- Penetration testing reports

## Core decisions

1. All user content is untrusted
2. State is server-authoritative with idempotency
3. Cross-user isolation prevents data access
4. Structured output with JSON Schema validation on all LLM outputs
5. No secrets in prompts

## Acceptance criteria

1. All 11 security documents exist
2. Prompt injection defense has multiple layers
3. Anti-cheat covers all reward and progression mechanisms
4. Data retention and deletion policy is specified

---

## Data retention periods

| Data type | Retention period | Rationale |
|-----------|-----------------|-----------|
| Learner profile | Active account + 12 months | Learning continuity |
| Personal stories | Active account + 12 months | Content personalization |
| Error evidence | Active account + 12 months | Error-based personalization |
| Reward history | Active account + 12 months | Economy integrity |
| Audit logs | 24 months | Security and compliance |
| Session logs | 6 months | Performance analysis |
| Anonymized analytics | Indefinite | Product improvement |

## Data export

Learners can export their data at any time:
- Format: JSON (machine-readable) and PDF (human-readable)
- Content: All personal data, learning history, stories, progress
- Delivery: Email download link
- Response time: Within 72 hours
- Free of charge

## Account deletion

Learners can delete their account and all associated data:
1. Learner requests deletion (in-app or via support)
2. 7-day cooling-off period (optional, can be immediate)
3. All personal data permanently deleted
4. Anonymized analytics retained (no identifying information)
5. Confirmation sent to learner
6. Deletion complete within 30 days

## Backup retention

- Backups retained for 30 days
- Backups include encrypted user data
- After 30 days, backups rotated and old data irrecoverable
- Deletion request extends to backup data (purged on next rotation)
