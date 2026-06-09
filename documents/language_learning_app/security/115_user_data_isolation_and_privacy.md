# User Data Isolation and Privacy

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Ensuring complete isolation between users' data and compliance with privacy regulations.

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

## Cross-user isolation

- Each learner's data is stored in isolated partitions
- Service-level access controls prevent cross-user data access
- Prompt injection in one user's session cannot access another user's data
- LLM context includes only the current user's data

## Data encryption

- Data at rest: AES-256 encryption
- Data in transit: TLS 1.3
- Encryption keys managed through secure key management service
- Encryption key rotation: quarterly

## PII minimization

- Only collect data necessary for learning
- No tracking data for advertising
- No data sold or shared with third parties
- Aggregate analytics use anonymized data only
- Personal stories are stored separately from identity data

## GDPR compliance

- Right to access: Download all personal data
- Right to rectification: Correct inaccurate data
- Right to erasure: Delete account and all associated data
- Right to portability: Export data in machine-readable format
- Data Processing Agreement for any sub-processors
- DPO contact available
