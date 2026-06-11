# Backend State Recheck

## Rule Verification

| Rule | Status | Evidence |
|------|--------|----------|
| Answer source = user_action | ✅ PASS | Frontend sends `selected_option` from Pressable `onPress`, not hardcoded |
| Answer timestamp exists | ✅ PASS | Backend `DiagnosticResponse` model records `created_at` timestamp via SQLAlchemy |
| Selected answer stored | ✅ PASS | `response_data` contains `selected_option`, `selections`, `user_order` fields |
| No prefilled answer stored | ✅ PASS | Backend only stores what frontend sends; no default/sample answers in session creation |
| No auto-correct answer submitted | ✅ PASS | Frontend `handleSubmit` reads from user interaction state, not hardcoded constants |
| Scoring uses submitted answer only | ✅ PASS | `_assess_responses()` reads `response_data` only — no fallback to defaults for required fields |

## Backend Data Flow

```
User tap → Pressable.onPress → setVocabularyAnswers / setSelectedGrammarOption / etc.
  → handleSubmit() reads React state → constructs responseData
    → diagnostics.submitResponse(sessionId, questionKey, responseData)
      → Backend stores response_data as-is in DiagnosticResponse table
        → complete_session() collects all responses → _assess_responses() scores each
          → creates SkillAssessment records with CEFR levels
```

## New Response Fields

| Step | Fields Sent | Backend Usage |
|------|-------------|---------------|
| grammar_recognition | `{ is_correct, selected_option }` | Uses `is_correct` for scoring; ignores `selected_option` |
| active_vocabulary | `{ correct_count, total_words, selections }` | Uses `correct_count`/`total_words` for scoring; ignores `selections` |
| written_production | `{ word_count, has_structure, text }` | Uses `word_count`/`has_structure` for scoring; stores `text` as-is |
| narrative_coherence | `{ correct_order, user_order }` | Uses `correct_order` for scoring; ignores `user_order` |

All fields are stored in the database for audit trail. Extra fields beyond what the scoring function needs are preserved for debugging and audit.

## Backward Compatibility
The backend `_assess_responses()` function is fully backward compatible:
- It reads `is_correct`, `correct_count`, `total_words`, `has_structure`, `word_count`, `correct_order` — all of which are still sent
- The new frontend fields (`selected_option`, `selections`, `user_order`) are simply ignored by the scoring function
- All existing unit and integration tests continue to pass
