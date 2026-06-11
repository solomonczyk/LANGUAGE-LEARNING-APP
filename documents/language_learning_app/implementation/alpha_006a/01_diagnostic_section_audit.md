# Diagnostic Section Audit — All Item Types

## Audit Result Summary
| Item Type | Current Interaction | Clickable/Editable | Prefills Correct Answer | Shows Feedback Before Action | Backend Receives User Answer | Status |
|-----------|-------------------|-------------------|------------------------|---------------------------|-----------------------------|--------|
| grammar_recognition | Tap to select 1 of 3 options | ✅ Yes | ✅ No | ✅ No — after submit only | ✅ Yes: `{ is_correct, selected_option }` | PASS |
| active_vocabulary | Tap to select 1 of 4 definitions per word | ✅ Yes | ✅ No | ✅ No — after submit only | ✅ Yes: `{ correct_count, total_words, selections }` | PASS |
| written_production | Free-text TextInput | ✅ Yes | ✅ No | ✅ No — after submit only | ✅ Yes: `{ word_count, has_structure, text }` | PASS |
| narrative_coherence | Tap events to build order | ✅ Yes | ✅ No | ✅ No — after submit only | ✅ Yes: `{ correct_order, user_order }` | PASS |

## Item Type Detail

### Grammar Recognition
- **UI**: 3 sentence options rendered as `<Pressable>` with radio-button style indicator
- **Flow**: User taps one option → option highlighted with blue border + ● → "Submit" button enabled → user taps Submit → feedback shown → "Continue →" appears
- **Visual before selection**: ○ He go to school every day. / ○ He goes to school every day. / ○ He going to school every day.
- **Visual after selection**: ○ He go to school every day. / ● He goes to school every day. / ○ He going to school every day.
- **Visual after submit (correct)**: Option highlighted green ✓; feedback text shown
- **Visual after submit (incorrect)**: Wrong option highlighted red ✗, correct option highlighted green
- **Backend data**: `{ is_correct: boolean, selected_option: "a"|"b"|"c" }`

### Active Vocabulary
- **UI**: 4 words, each with 4 definition options as `<Pressable>` items
- **Flow**: User taps definition for each word → each selection highlighted → "Submit" enabled when all 4 answered → feedback after submit
- **Backend data**: `{ correct_count: number, total_words: 4, selections: { [word]: optionId } }`

### Written Production
- **UI**: `<TextInput>` multiline with character counter
- **Flow**: User types response → "Submit" enabled at ≥10 chars → feedback after submit
- **Backend data**: `{ word_count: number, has_structure: boolean, text: string }`

### Narrative Coherence
- **UI**: 5 events displayed in scrambled order; tap to add to "Your order" list; tap ordered item to undo
- **Flow**: User taps events in correct sequence → each moves from available to ordered → "Complete Diagnostic" enabled when all 5 placed → feedback after submit
- **Backend data**: `{ correct_order: boolean, user_order: string[] }`

## Before/After Comparison

| Aspect | Before (Alpha 006) | After (Alpha 006A) |
|--------|-------------------|-------------------|
| Option rendering | `<View>` with `<Text>` — not clickable | `<Pressable>` with `onPress` — interactive |
| Selection indicator | None | ○ / ● with border highlight |
| Correct answer display | Always visible (`✓ Sentence B is correct`) | Hidden until user submits |
| Feedback timing | Always visible alongside content | Only after user submits answer |
| Submit button state | Always enabled | Disabled until required input provided |
| Backend data source | Hardcoded `{ is_correct: true }` | Actual user `selected_option` |
