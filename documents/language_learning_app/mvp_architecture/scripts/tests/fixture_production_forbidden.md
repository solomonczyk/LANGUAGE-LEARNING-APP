# Fixture: Production Gate FORBIDDEN

**Purpose:** Negative regression test — MUST NOT trigger a warning in Test 26.

---

## Production Gate (FORBIDDEN)

**Status:** FOREVER BLOCKED in MVP planning

**What it protects:** Production environment from premature release
**Pass Criteria:** `production_accepted=true` — which is FORBIDDEN
**Consequence:** Setting `production_accepted=true` violates the MVP architecture planning contract

This gate exists as a marker. In the current MVP planning phase, the production gate is permanently locked.
