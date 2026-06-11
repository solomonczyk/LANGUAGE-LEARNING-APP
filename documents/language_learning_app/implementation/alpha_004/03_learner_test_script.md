# 03 — Learner Test Script

## For Closed Alpha Testers (T1–T5)

### Prerequisites

- Access to a Chromium-based browser (Chrome, Edge, Brave)
- Backend running at http://localhost:8000
- Expo Web running at http://localhost:8081
- 1–2 hours available (can be split across sessions)

### Important Rules

1. **Do NOT enter real personal data.** Use only the synthetic data provided.
2. **Do NOT share your test credentials** outside the alpha.
3. **Report ALL issues** — no issue is too small.
4. **Don't skip steps** — follow the script in order.
5. **Take screenshots** of any unexpected behavior.

---

## Script: Full Learner Journey

### Step 1: Open the App

1. Open http://localhost:8081 in a Chromium browser
2. Expected: Onboarding screen appears with "Step 1 of 4"
3. **Check:** CTA button visible and labeled
4. **If blank/wrong:** Report with browser and URL

**Record:** `[  ] PASS  [  ] FAIL  [  ] BLOCKED`

### Step 2: Onboarding — Target Language

1. Select "Spanish" from the language grid (or type another)
2. Click "Continue"
3. Expected: Step 2 appears

**Record:** `[  ] PASS  [  ] FAIL  [  ] BLOCKED`

### Step 3: Onboarding — Native Language

1. Select "English"
2. Click "Continue"
3. Expected: Step 3 appears

**Record:** `[  ] PASS  [  ] FAIL  [  ] BLOCKED`

### Step 4: Onboarding — Preferences

1. Select learning goal (any)
2. Select preferred duration (any)
3. Click "Continue"
4. Expected: Step 4 appears

**Record:** `[  ] PASS  [  ] FAIL  [  ] BLOCKED`

### Step 5: Onboarding — Level

1. Select self-reported level (use your assigned value)
2. Click "Start Learning!"
3. Expected: Loading state → redirects to Diagnostic
4. **Check:** Loading state is understandable (spinner + message)

**Record:** `[  ] PASS  [  ] FAIL  [  ] BLOCKED`

### Step 6: Diagnostic — Initial Load

1. Expected: Loading "Starting diagnostic..." → Diagnostic screen
2. **Check:** Step indicator shows 4 steps, first step highlighted
3. **Check:** Title and prompt are visible

**Record:** `[  ] PASS  [  ] FAIL  [  ] BLOCKED`

### Step 7: Diagnostic — Grammar Step

1. Read the prompt "Which sentence is correct?"
2. Click "Next"
3. Expected: Advances to step 2 (Vocabulary)

**Record:** `[  ] PASS  [  ] FAIL  [  ] BLOCKED`

### Step 8: Diagnostic — Vocabulary Step

1. Read the prompt "Match the words"
2. Click "Next"
3. Expected: Advances to step 3 (Writing)

**Record:** `[  ] PASS  [  ] FAIL  [  ] BLOCKED`

### Step 9: Diagnostic — Writing Step

1. Type **at least 10 characters** in the text area (e.g., "I wake up in the morning and eat breakfast.")
2. Click "Next"
3. Expected: Advances to step 4 (Coherence)

**Test:** Try clicking "Next" with fewer than 10 characters — button should be disabled.
**Test:** Keyboard should not hide the text input.

**Record:** `[  ] PASS  [  ] FAIL  [  ] BLOCKED`

### Step 10: Diagnostic — Coherence Step

1. Read the prompt
2. Click "Complete Diagnostic"
3. Expected: Loading → redirects to Learning Contract

**Record:** `[  ] PASS  [  ] FAIL  [  ] BLOCKED`

### Step 11: Learning Contract

1. Expected: "Your Learning Plan" with contract details
2. **Check:** Target language, duration, scaffolding level shown
3. **Check:** Skill profile section shows assessments with CEFR levels
4. Click "Start Your First Lesson!"
5. Expected: Redirects to Home/Dashboard

**Record:** `[  ] PASS  [  ] FAIL  [  ] BLOCKED`

### Step 12: Home Dashboard

1. Expected: "Welcome back!" greeting
2. **Check:** Current Lesson Plan card shows language and duration
3. **Check:** "My Morning with My Pet" lesson card visible
4. **Check:** "Start Lesson" CTA visible and enabled
5. Click "Start Lesson"

**Record:** `[  ] PASS  [  ] FAIL  [  ] BLOCKED`

### Step 13: Lesson Screen

1. Expected: Lesson screen with title "My Morning with My Pet"
2. **Check:** Communicative Goal, Your Task, Grammar Focus, Key Vocabulary visible
3. **Check:** Text input area visible with placeholder
4. Expected: Loading state before screen appears

### Step 13a: Validation — Minimum Text

1. Try to click "Submit" with empty text — button should be disabled
2. Type only 5 characters — "minimum 10 characters" warning should appear

**Record:** `[  ] PASS  [  ] FAIL  [  ] BLOCKED`

### Step 14: Text Submission

1. Type 3–5 sentences about your morning with your pet:
   ```
   This morning I woke up and my cat was sleeping next to me.
   She wanted to go to the litter box so I opened the door.
   Then we had breakfast together and played a little.
   ```
2. Click "Submit"
3. Expected: Redirects to processing/analysis screen

**Record:** `[  ] PASS  [  ] FAIL  [  ] BLOCKED`

### Step 15: Processing Screen

1. Expected: "Analyzing Your Response" title
2. **Check:** Progress steps animate through: submitting → validating → analysis → linguistic → pedagogical → decision → finalizing
3. **Check:** Progress bar updates as steps complete
4. **Check:** No step hangs for more than 5 seconds
5. Expected: Auto-redirects to Result screen after ~5 seconds

**Record:** `[  ] PASS  [  ] FAIL  [  ] BLOCKED`

### Step 16: Result Screen

1. Expected: "Lesson Complete!" green status box
2. **Check:** Strengths section shows bullet points
3. **Check:** Corrections section shows VERB_FORM and PREPOSITION corrections
4. **Check:** Suggested Improved Phrasing visible
5. **Check:** Validation results show linguistic and pedagogical checks as "✓ Passed"
6. **Check:** Decision shown as "COMPLETE"
7. **Check:** "Back to Home" button visible
8. **Check:** ❌ Result screen does NOT show fake completion text

**Record:** `[  ] PASS  [  ] FAIL  [  ] BLOCKED`

### Step 17: Back to Home

1. Click "Back to Home"
2. Expected: Returns to Home dashboard
3. **Check:** Mastery progress section may now show guided_use evidence

**Record:** `[  ] PASS  [  ] FAIL  [  ] BLOCKED`

### Step 18: Duplicate Submission Test

1. Click "Start Lesson" again
2. Submit the same text
3. Expected: Processing completes successfully (idempotent)
4. Note: This tests the lesson engine handles re-submission gracefully

**Record:** `[  ] PASS  [  ] FAIL  [  ] BLOCKED`

---

## UX Checks (all testers)

### Viewport Test

Open Chrome DevTools (F12) → Toggle Device Toolbar and test:

| Viewport | Width | Expected | Result |
|----------|-------|----------|--------|
| Small phone | 375×667 | Scrolling works, no cutoff, CTA visible | `[  ]` |
| Regular phone | 390×844 | All content accessible | `[  ]` |
| Tablet | 768×1024 | Layout adapts | `[  ]` |
| Desktop | 1280×800 | Full layout | `[  ]` |
| Zoom 200% | Any | Text readable, no layout break | `[  ]` |

### Keyboard Test

- When text input is focused, keyboard should not hide the input
- "Submit" button should be accessible while keyboard is open
- Android back button (browser back) should not break state

### Error/Offline Test

1. Stop the backend (`docker compose stop backend`)
2. Refresh the app in browser
3. Expected: Error screen with understandable message and retry button
4. Restart backend: `docker compose start backend`

---

## Issue Classification

### Blocker (alpha cannot pass)
- Broken navigation (cannot reach a required screen)
- Submit button does not work
- Processing hangs indefinitely
- Fake success state (shows complete when not)
- Critical security issue (cross-user data leak)
- Database migration failure

### Non-blocking issue
- Text alignment issue
- Loading animation not perfectly smooth
- Minor color/shade inconsistency
- Missing transition animation
- Font size slightly off
- Missing period in label

## Feedback Submission

After completing the script, fill out the [feedback form](08_alpha_feedback_form.md).

---

*Created: 2026-06-11*
