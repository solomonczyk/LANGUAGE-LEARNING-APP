# Authorization and Tool Access Policy

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Service-to-service and user authentication, authorization, and access control.

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

## Service-to-service authentication

- All inter-service communication requires authentication
- Service accounts with least-privilege permissions
- API keys rotated quarterly
- Internal services not exposed to external network

## User authentication

- Standard authentication (email/password, OAuth providers)
- Session tokens with expiry
- Refresh token rotation
- Device tracking for anomaly detection
- Multi-factor authentication option

## Access control

| Resource | Who can access | Notes |
|----------|---------------|-------|
| Own learner profile | Learner only | With explicit sharing |
| Other learner profiles | No one | Strict isolation |
| LKB content | All services (read) | Authoring requires admin |
| Reward state | Reward Engine only | Read-only for others |
| Mastery state | Mastery Engine only | Read-only for others |
| Audit logs | Admin only | Read-only |
| System prompts | Admin only | Version-controlled |

## Least privilege principle

Each service has access only to the data it needs to function. No service has blanket data access.
