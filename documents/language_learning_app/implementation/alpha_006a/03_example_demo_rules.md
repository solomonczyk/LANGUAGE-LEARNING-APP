# Example/Demo Rules — Separation Verification

## Rule Enforcement

### Before (Alpha 006)
- **"Example only" badge** was displayed on 3 of 4 diagnostic steps
- **Demo content** was shown as the primary task (e.g., "✓ Sentence B is correct" pre-displayed)
- **Hardcoded correct answers** were submitted to backend regardless of user interaction
- **Helper text** told users "we'll submit this for you" — encouraging passivity

### After (Alpha 006A)
- **No "Example only" badge** on any step — all steps are real, interactive tasks
- **No demo content** replaces real task content
- **No prefilled answers** — user must actively select/type
- **No helper text** telling users their answers will be auto-submitted

## Separation Verification

| Rule | Before | After | Verdict |
|------|--------|-------|---------|
| Example content must not contain actual task answer | ❌ "✓ Sentence B is correct" shown | ✅ Correct answer hidden until user submits | PASS |
| Example content must not be submitted automatically | ❌ Hardcoded `is_correct: true` submitted | ✅ User's actual selection submitted | PASS |
| Example must not look like completed diagnostic feedback | ❌ Green ✓ shown before any action | ✅ Green ✓ only shown after user submits | PASS |
| User must be able to distinguish demo from real task | ❌ Demo badge was small, easy to miss | ✅ No demo content — all tasks are real | PASS |
| Example/demo is allowed as instruction support only | ❌ Demo was the main task | ✅ N/A — no demo content | PASS |
