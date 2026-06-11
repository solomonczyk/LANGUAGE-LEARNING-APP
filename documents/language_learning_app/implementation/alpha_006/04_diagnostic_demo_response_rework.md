# Diagnostic Demo Response Rework

## Problem

The diagnostic screen displayed pre-filled responses (e.g., "✓ Sentence B is correct") that looked like they should be interactive but were actually demo/informational placeholders. This could confuse learners into thinking they can select different options when the actual behavior is auto-advancing.

## Changes Applied

### 1. "Example only" Badge

Added a blue chip/badge labeled "Example only" at the top of each demo-only step (grammar recognition, vocabulary, narrative coherence) to clearly separate example content from user input.

### 2. Corrected Labels

Replaced italic hint text like "✓ Sentence B is correct (we'll use this as your response)" with a prominent green "✓ Sentence B is correct" label that clearly indicates the selected answer.

### 3. Level-Specific Helper Text

Added `getLevelHelperText()` function that provides different helper text per learner level:

- **A1**: "This is an example. Just read it — we'll use this as your answer."
- **A2**: "This is a sample answer. You don't need to do anything — we'll submit it for you."
- **B1/B2**: "The example below shows a correct answer. It will be submitted as your response."

### 4. Vocabulary Step Clarification

Added clear "Example only" badge to vocabulary step. Changed generic hint "We'll test active vocabulary..." to "Here are some example word matches:" to make it clearer the content is a demo.

### 5. Narrative Coherence Step Clarification

Added clear "Example only" badge to narrative step. Changed "The events below are in the correct order:" to "The events are already in the right order:" to remove ambiguity.

## Files Changed

- `mobile/app/diagnostic.tsx` — added demo badges, level-aware helper text, corrected labels, new styles

## Before/After

| Element | Before | After |
|---------|--------|-------|
| Grammar step | Options with hint text | "Example only" badge + options + green correct label + level-aware helper |
| Vocabulary step | Hint + demo text + checkmark | "Example only" badge + clearer label + green checkmark + helper |
| Narrative step | Hint + ordered list | "Example only" badge + "already in the right order" + helper |
| Writing step | (no change — this is the only interactive step) | (unchanged) |
