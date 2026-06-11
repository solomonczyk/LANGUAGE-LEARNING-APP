# Change Control and Scope Governance

**Status:** CANONICAL  
**Version:** 1.0.0  
**Effective date:** 2026-06-10  
**Owner:** Product Owner  
**Change control:** Changes require a documented change request or ADR where specified.

## Locked decisions after acceptance

Changes require formal approval for:

- primary segment;
- primary problem;
- value proposition;
- first commercial offer;
- MVP cut line;
- target language;
- stage deadlines;
- maximum budgets;
- pricing test;
- supported platforms;
- authority boundaries;
- zero-tolerance criteria;
- production gate.

## Change request contents

- request ID;
- requester;
- current decision;
- proposed decision;
- evidence;
- reason;
- scope impact;
- schedule impact;
- budget impact;
- risk impact;
- migration/rollback;
- affected artifacts;
- decision;
- approver.

## Decision classes

- editorial correction;
- operational adjustment;
- scope change;
- architecture ADR;
- commercial change;
- safety-critical change.

## Emergency change

Only safety or severe security may bypass the normal timing, but never the audit trail.

## No-new-foundation rule

After acceptance, a new foundational documentation layer is forbidden unless:

1. a canonical assumption materially changes;
2. the impact cannot be handled by an existing document update;
3. a change request demonstrates the need;
4. affected stage gates are re-evaluated.
