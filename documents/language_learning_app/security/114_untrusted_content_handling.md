# Untrusted Content Handling

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

How all user-supplied content is processed, sanitized, and validated.

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

## Content types

- **Text** — Free-form responses, chat messages, narrative text
- **Voice** — Audio recordings for speech recognition
- **Images** — Photos, screenshots, camera capture
- **OCR** — Text extracted from images
- **Documents** — Uploaded PDF, Word, text files (future)
- **External links** — URLs shared by learner

## Processing pipeline

All untrusted content follows this pipeline:
1. **Type validation** — Is the content type expected for this context?
2. **Size validation** — Within acceptable limits?
3. **Sanitization** — Strip control characters, escape special characters
4. **Security scan** — Check for injection patterns, malicious content
5. **Isolation** — Process in isolated context
6. **Output validation** — Only safe, expected data is passed to other services

## Content-specific rules

| Content | Size limit | Sanitization | Additional checks |
|---------|-----------|--------------|-------------------|
| Text | 5000 chars | Escape/trim | Injection patterns |
| Voice | 5 min/10 MB | Audio sanitization | Speaker count |
| Images | 10 MB | Metadata stripping | Explicit content check |
| OCR text | 2000 chars | Same as text | Language detection |

## Rejection

Content that fails validation is rejected with a clear, learner-friendly message. Rejections are logged for security analysis.
