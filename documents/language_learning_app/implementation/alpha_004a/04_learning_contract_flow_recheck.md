# Learning Contract Flow Recheck — Alpha 004A

## Issue

After completing diagnostic, navigating to `/learning-contract` showed:

> "No learning contract found yet. Complete your diagnostic first."

The ErrorScreen's only action was `onRetry={refetch}`, which re-fetched `getCurrent()` and failed with the same 404 — the user was stuck.

## Root Cause

- Diagnostic completion (`POST /diagnostics/sessions/{id}/complete`) creates **skill assessments** but does NOT create a learning entry contract
- The learning-contract screen called `getCurrent()` which correctly returned 404 (no contract exists yet)
- The screen had a `handleCreate()` function but it was never triggered automatically

## Fix

Modified `mobile/app/learning-contract.tsx`:

1. Added `needsContract` state to detect when `getCurrent()` returns 404
2. Added auto-create: when 404 detected, automatically calls `create()` with "Creating your learning plan..." loading state
3. After creation succeeds, refetches the contract data
4. If creation fails, shows error with retry option

## Verification

- Complete full diagnostic flow via browser → auto-navigated to `/learning-contract`
- Contract auto-created successfully
- Contract parameters displayed: target language, duration, scaffolding, vocabulary budget, etc.
- Skill profile from diagnostic shown in contract
- "Start Your First Lesson!" CTA visible and functional
