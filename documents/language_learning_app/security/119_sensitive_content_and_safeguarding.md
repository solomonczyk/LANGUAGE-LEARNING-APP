# Sensitive Content and Safeguarding

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Handling of sensitive topics, content moderation, and learner safeguarding.

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

## Sensitive topic categories

| Category | Handling |
|----------|----------|
| Violence | Excluded from system-generated content. User-initiated: flag for review. |
| Politics | Neutral framing. Diverse perspectives presented. No platform for hate. |
| Religion | Factual, respectful treatment. User stories accepted, system content neutral. |
| Personal trauma | User may share. System responds with empathy, no probing. Flag if pattern indicates distress. |
| Adult content | Excluded from all content. User-generated: filter and flag. |
| Hate speech | Zero tolerance. Immediate content removal. Account review. |

## Proactive filtering

All system-generated content is filtered against sensitive content categories. User-generated content is filtered on upload/ submission.

## Reactive handling

When sensitive content is detected:
1. Content is flagged
2. Depending on severity: blocked, reviewed, or allowed with warning
3. Repeated violations trigger account review
4. Escalation path for serious concerns

## Safeguarding for minors

- Age verification at sign-up
- Minors (under 18) have additional content restrictions
- Parental controls for minor accounts
- No advertising to minors
- Reporting mechanism for concerns

## Reporting mechanism

Clear, accessible reporting for any content concerns. Reports reviewed within 24 hours. Reporter can remain anonymous.
