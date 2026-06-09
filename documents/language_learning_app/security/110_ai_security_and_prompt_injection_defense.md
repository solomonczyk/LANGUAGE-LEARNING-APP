# AI Security and Prompt Injection Defense

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Comprehensive defense strategy against prompt injection and other AI-specific security threats.

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

## Threat model

All user-supplied content is considered untrusted and potentially malicious:
- Free text responses
- Voice transcriptions
- Images and image OCR
- Uploaded documents
- External materials

## Defense layers

### Layer 1: Input sanitization
- Strip or escape control characters
- Enforce input length limits
- Validate content type
- Remove known injection patterns

### Layer 2: Prompt architecture
- Clear separation between system instructions and user content
- Boundary tokens marking user content boundaries
- Instruction to ignore embedded instructions
- Output constraints in system prompt

### Layer 3: Output validation
- JSON Schema validation on all structured outputs
- Content type verification
- Instruction detection (does output contain commands?)
- Anomaly scoring

### Layer 4: Policy enforcement
- No state mutations from LLM outputs
- No access to other learners' data
- Rate limiting on anomalous requests
- Escalation for detected injection attempts

## Red team testing

Regular scheduled testing:
- Quarterly: Automated injection attempt suite
- Bi-annual: External red team engagement
- Event-driven: After major architecture changes

## Detection metrics

- Injection attempt rate
- Bypass rate
- Detection latency
- False positive rate
