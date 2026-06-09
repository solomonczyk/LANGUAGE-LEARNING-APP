# Reward Economy Integrity

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Security measures specific to the reward economy to prevent exploitation.

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

## Reward Engine as sole authority

The Reward Engine is the ONLY service that can award XP, currency, or other rewards. No other service, including any LLM, has reward authority.

## Audit trail

Every reward transaction is logged with:
- Transaction ID
- Learner ID
- Event type
- XP amount
- Idempotency key
- Source service
- Timestamp
- Previous and new balance

## Anti-farming measures

- Per-action rate limits (max 1 review XP per 3 seconds per item)
- Daily XP cap (based on CEFR level and engagement)
- Suspicious pattern detection
- Review rewards require minimum engagement duration
- Transfer rewards require novel production verification

## Duplicate detection

- Idempotency keys prevent duplicate reward processing
- Same-content detection for production tasks
- Cross-learner similarity detection (same text from multiple learners)

## Error correction

If an erroneous reward is detected:
1. Record the correction
2. Adjust balance
3. Log the correction
4. Notify learner (if applicable)

No retroactive punishment for system errors that the learner did not cause.
