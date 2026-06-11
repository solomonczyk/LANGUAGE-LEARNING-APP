# Interaction Model Recovery

## Principles Applied
1. **User must actively choose or type an answer** for every diagnostic task
2. **Selected option must have a visible selected state** (● indicator + colored border)
3. **Submit/Next must be disabled** until user provides the required input
4. **Correct answer must not be visible** before user selection
5. **Feedback appears only after answer is submitted** (green/red highlight + explanatory text)
6. **Demo/example content is never treated as a user answer**
7. **Backend receives the actual user answer**, not a prefilled/demo value

## Per-Step Interaction Model

### Grammar Recognition
```
State: NO_SELECTION       → Submit DISABLED
State: OPTION_SELECTED    → Submit ENABLED (shows ● + blue border)
State: SUBMITTED_CORRECT  → Options DISABLED, correct green ✓, feedback text, "Continue →" button
State: SUBMITTED_WRONG    → Options DISABLED, wrong red ✗, correct green, feedback text, "Continue →"
```

### Active Vocabulary (per word)
```
State: ALL_UNANSWERED          → Submit DISABLED
State: PARTIALLY_ANSWERED      → Submit DISABLED
State: ALL_4_ANSWERED          → Submit ENABLED
State: SUBMITTED_PERFECT       → All disabled, green ✓, "Perfect!" feedback
State: SUBMITTED_PARTIAL       → All disabled, correct green / wrong red, score feedback
```

### Written Production
```
State: TEXT_EMPTY      → Submit DISABLED
State: TEXT_SHORT (<10 chars) → Submit DISABLED
State: TEXT_READY      → Submit ENABLED
State: SUBMITTED       → TextInput disabled, word/char count feedback
```

### Narrative Coherence
```
State: NONE_PLACED      → "Complete Diagnostic" DISABLED
State: PARTIALLY_PLACED → "Complete Diagnostic" DISABLED
State: ALL_5_PLACED     → "Complete Diagnostic" ENABLED
State: SUBMITTED        → All events DISABLED, order feedback, "Continue →" button
```

## Enable/Disable Triggers

| Condition | Effect |
|-----------|--------|
| Grammar: no option selected | Submit DISABLED |
| Grammar: option selected | Submit ENABLED |
| Vocabulary: < 4 words answered | Submit DISABLED |
| Vocabulary: 4 words answered | Submit ENABLED |
| Writing: < 10 chars | Submit DISABLED |
| Writing: ≥ 10 chars | Submit ENABLED |
| Narrative: < 5 events placed | Submit DISABLED |
| Narrative: 5 events placed | Submit ENABLED |
| After any submission | All inputs DISABLED; "Continue →" shown |

## Code Implementation
The interaction model is implemented via:
- React state: `selectedGrammarOption`, `vocabularyAnswers`, `textInput`, `narrativeOrder`
- Derived state: `canSubmit` IIFE checking each step's completion
- Feedback state: `lastFeedback` with `{ stepKey, correct, text }`
- `showingFeedback` computed from `lastFeedback?.stepKey === currentStep.key`
