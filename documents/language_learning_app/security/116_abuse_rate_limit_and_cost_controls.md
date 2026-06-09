# Abuse Rate Limit and Cost Controls

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Rate limiting, cost controls, and abuse detection across all services.

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

## Rate limits

| Operation | Limit | Scope |
|-----------|-------|-------|
| Lesson generation | 5 per hour | Per user |
| Quiz submissions | 10 per hour | Per user |
| LLM requests | Configurable | Per user tier |
| API calls | 100 per minute | Per user |
| Authentication attempts | 5 per minute | Per IP |

## Cost controls

- Per-user daily cost cap (configurable at plan level)
- Per-session cost tracking with alerts
- Model tier selection based on task complexity
- Automatic throttling when approaching limits
- Monthly cost reports with anomaly detection

## Anomaly detection

Signal processing for:
- Unusual request frequency
- Unusual request patterns (same action repeated)
- Off-hours usage spikes
- Multiple accounts from same origin
- API call patterns matching automation

## Response to abuse

1. Rate limit exceeded: Return 429 with retry-after header
2. Suspicious pattern: Increase monitoring, reduce limits
3. Confirmed abuse: Suspend account, flag for manual review
4. Appeal process: User can appeal via support
