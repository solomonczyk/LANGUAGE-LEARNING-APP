# Legal, Privacy, and Safety Boundaries

**Status:** CANONICAL  
**Version:** 1.0.0  
**Effective date:** 2026-06-10  
**Owner:** Product Owner  
**Change control:** Changes require a documented change request or ADR where specified.

## Legal boundary

This package does not declare GDPR, COPPA, consumer-law, accessibility-law, tax, payment, or educational-certification compliance. Formal legal review is required before public paid launch.

## Minimum privacy requirements

- data inventory;
- purpose limitation;
- minimal collection;
- retention schedule;
- deletion process;
- export process;
- processor inventory;
- provider payload policy;
- breach response;
- user-facing privacy summary.

## Child-user boundary

The first commercial release targets adults. Do not market to children or enable child accounts without a dedicated safeguarding and legal layer.

## Sensitive content

The product must support safe refusal, redirection, and human escalation for self-harm, abuse, exploitation, or imminent danger content according to applicable policy and jurisdiction.

## Payment boundary

Before accepting payment:

- seller identity and jurisdiction determined;
- terms and refund rule documented;
- tax/accounting path reviewed;
- payment processor data flow documented;
- support contact available.

## AI transparency

Users must be told when feedback is AI-generated and that AI can be wrong. High-impact decisions remain deterministic or human-reviewed.

## Data prohibition

Do not request unnecessary:

- passport data;
- health data;
- precise location;
- employer confidential data;
- private third-party conversations.
