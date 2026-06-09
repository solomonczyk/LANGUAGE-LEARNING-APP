# Security Logging and Incident Response

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

What security events are logged, how they are monitored, and the incident response process.

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

## Security events logged

- Authentication failures (successful and failed)
- Authorization violations
- Data access outside scope
- Injection attempt detection
- Rate limit violations
- Anomalous usage patterns
- State mutation attempts from unauthorized sources
- System configuration changes

## Logging requirements

- Timestamp with timezone
- Event type and severity
- Source (IP, service, user ID if applicable)
- Description of event
- Action taken (logged, blocked, escalated)
- Correlation ID for related events

## Alert triggers

- Critical: Any detected injection bypass, data breach evidence, unauthorized access -> immediate notification
- High: Multiple injection attempts, rate limit patterns, unusual data access -> within 1 hour
- Medium: Single injection attempt, minor policy violation -> within 24 hours
- Low: Rate limit warnings, configuration drift -> within 1 week

## Incident response

1. **Detection** — Alert triggered by logging system
2. **Triage** — Assess severity and impact (within 15 min for critical)
3. **Containment** — Block access, rotate keys, isolate affected systems
4. **Investigation** — Root cause analysis
5. **Remediation** — Fix vulnerability, restore systems
6. **Post-mortem** — Document incident, update procedures, implement preventive measures
