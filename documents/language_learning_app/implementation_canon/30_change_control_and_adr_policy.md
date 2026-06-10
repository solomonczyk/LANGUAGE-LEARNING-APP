# Change Control and ADR Policy

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  
**ADR:** ADR-026

---

## 1. Principle

After the implementation canon is accepted, any change to a fundamental decision requires a new ADR. Feature implementation tasks (starting with `003`) may NOT unilaterally change decisions fixed in this canon.

---

## 2. Changes Requiring ADR

| Category | Examples |
|----------|----------|
| Framework | React Native → Flutter, FastAPI → NestJS |
| State management | Zustand → Redux, TanStack Query → SWR |
| Database | PostgreSQL → MySQL, SQLite |
| Queue | Arq → Celery |
| Auth provider | Supabase Auth → Clerk, Firebase Auth |
| AI provider boundary | Provider-independent → provider-specific |
| API versioning | `/api/v1` → `/api/v2` or breaking changes |
| Responsive breakpoints | Changing defined breakpoint values |
| Supported OS versions | Dropping Android 12, dropping iOS 16 |
| Design tokens | Changing primary color palette |
| Mastery authority | Allowing LLM-influenced mastery |
| Reward authority | Allowing non-deterministic rewards |
| Production gate | Opening production (separate authorized task) |
| Module boundaries | Merging or splitting 20 modules |
| Data source of truth | Adding secondary authoritative store |

---

## 3. ADR Template

```markdown
# ADR-NNN: Title

**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-NNN  
**Date:** YYYY-MM-DD  
**Deciders:** [list of participants]

## Context
What is the issue that we're seeing that is motivating this decision or change?

## Problem Description
What is the specific problem we need to solve?

## Decision
What is the change that we're proposing and/or doing?

## Alternatives Considered
What other options were considered and why were they rejected?

## Consequences
What becomes easier or harder as a result of this change?

## Migration Impact
What needs to change in existing code/documentation?

## Rollback
How can this decision be reversed if needed?

## Compatibility
Is this change backward-compatible? If not, what breaks?

## Tests
What tests verify this change works correctly?

## Affected Documents
Which canonical documents need updating?

## Affected Modules
Which modules are affected by this change?
```

---

## 4. ADR Lifecycle

```
Proposed → Review → Accepted | Deprecated
                              ↓
                         Superseded by ADR-NNN
```

| State | Meaning |
|-------|---------|
| Proposed | ADR drafted, under review |
| Accepted | ADR approved, change is effective |
| Deprecated | ADR no longer in effect (superseded) |
| Superseded by ADR-NNN | Another ADR replaced this decision |

---

## 5. ADR Maintenance

| Rule | Detail |
|------|--------|
| Sequential numbering | ADR numbers must not have gaps |
| Updates | When an ADR is superseded, update the old ADR status |
| Back-references | Old ADR links to superseding ADR and vice versa |
| Storage | All ADRs in `architecture_decision_log.md` |
| Searchable | ADR index at top of the decision log |
