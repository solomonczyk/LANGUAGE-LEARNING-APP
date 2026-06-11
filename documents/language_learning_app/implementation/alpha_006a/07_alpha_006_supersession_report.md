# Alpha 006 Supersession Report

## Reason for Supersession
Alpha 006 claimed "diagnostic demo confusion resolved" but manual visual review showed:
1. Diagnostic options were **not clickable**
2. Correct answers were **prefilled/shown by the system**
3. "Example only" blocks were treated as real tasks
4. Users **could not actively answer**
5. Backend received **hardcoded correct answers**, not user selections

## What Changed in 006A

| Dimension | Alpha 006 Claim | Alpha 006A Reality |
|-----------|----------------|-------------------|
| Grammar options | Non-interactive `<View>` | Interactive `<Pressable>` with selection |
| Correct answer prefilled | Yes — always visible | No — hidden until user submits |
| Demo/Real separation | "Example only" badge only | All steps are real, interactive tasks |
| User interaction | Read-only for 3/4 steps | Active selection/input for all 4 steps |
| Backend data source | Hardcoded correct | Actual user selections |
| Feedback timing | Always visible | Only after user submits |

## Key Files Overwritten
- `mobile/app/diagnostic.tsx` — Complete rewrite of all 4 diagnostic steps

## Key Files Added
- `backend/tests/unit/test_diagnostics.py` — 4 new backward-compatibility tests
- `documents/language_learning_app/implementation/alpha_006a/` — Full documentation

## Supersession Declaration
```
Alpha 006 status: SUPERSEDED_BY_006A
Alpha 006a status: IMPLEMENTED — pending acceptance verification
Reason: Diagnostic interaction blocker fixed — all options clickable,
correct answers not prefilled, backend receives real user selections,
feedback after user action only.
```
