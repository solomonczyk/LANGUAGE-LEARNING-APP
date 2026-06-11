# Analytics and Experimentation Canon

**Status:** CANONICAL  
**Version:** 1.0.0  
**Effective date:** 2026-06-10  
**Owner:** Product Owner  
**Change control:** Changes require a documented change request or ADR where specified.

## Required event chain

`landing_viewed → diagnostic_started → diagnostic_completed → trial_started → lesson_submitted → validation_completed → lesson_completed → review_completed → offer_viewed → payment_completed`

## Required product events

- onboarding_started/completed;
- profile_created;
- diagnostic_started/answered/completed;
- contract_created/viewed;
- lesson_started;
- draft_saved/restored;
- submission_created;
- analysis_started/completed/failed;
- validation_rejected;
- lesson_completed;
- mastery_evidence_recorded;
- review_due/completed;
- offer_viewed;
- checkout_started;
- payment_completed/refunded.

## Event quality

Every event must specify:

- event name;
- purpose;
- trigger;
- required properties;
- forbidden properties;
- owner;
- retention;
- test.

## Privacy

Use pseudonymous identifiers. Do not place raw learner text, audio, tokens, or secrets in analytics events.

## Experiment contract

Every experiment requires:

- hypothesis;
- audience;
- start/end;
- single primary metric;
- guardrail metrics;
- sample target;
- stop rule;
- decision owner;
- result document.

## Anti-bias rule

Do not compare groups with materially different acquisition intent or support levels as if they were equivalent cohorts.
