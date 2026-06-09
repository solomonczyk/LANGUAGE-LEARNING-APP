# Anti-Cheat and Learning Integrity

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Measures to protect the integrity of learning data, rewards, and progression.

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

## Server-authoritative state

All learning state is managed server-side. Client-side data is considered untrusted until verified.

## Integrity mechanisms

### Idempotency keys
Every state-changing operation includes a unique idempotency key. Duplicate submissions are silently ignored.

### Unique attempt IDs
Every exercise attempt has a unique ID. Attempt IDs are generated server-side and cannot be forged client-side.

### Replay protection
- Nonces with expiry for sensitive operations
- Timestamp validation
- Session-scoped tokens

### Atomic transactions
Reward transactions are atomic: all-or-nothing. Partial completion is not possible.

### Anti-farm limits
- Per-user daily limits on XP and rewards
- Per-IP rate limits
- Unusual pattern detection (same actions at inhuman speed)

### Anomaly signals
- Response time < 500ms for human tasks (likely automated)
- Perfect score sequences
- Off-session submissions (timestamps don't match activity)
- Multiple accounts from same device/IP

## Practical revalidation

When contradictory evidence is detected (e.g., quiz says mastery, but free production shows errors):
1. Flag the contradiction
2. Reduce confidence in affected dimensions
3. Schedule focused assessment
4. If automation suspected, flag for review
