# A1 Wording Review

## Purpose

Review all learner-facing text for A1-appropriate simplicity. Each technical term must either be avoided or explained in simple learner-facing language.

## Terms Reviewed

| Original Term | Screen | A1 Replacement / Explanation |
|---------------|--------|------------------------------|
| Communicative Goal | Lesson | "Goal" |
| Your Task | Lesson | "Your Task" (kept, but with simpler description) |
| Grammar Focus | Lesson | "What to practice" (with examples like "use 'I played', 'I ate'") |
| Key Vocabulary | Lesson | "Useful words" |
| Submit | Lesson | "Send my answer" |
| Your Response | Lesson | "Write here" |
| Learning Entry Contract | Contract | "Your Personal Learning Plan" |
| Active Vocabulary Budget | Contract | "New words you will learn in each lesson" |
| Grammar Focus Count | Contract | "Grammar topics we will practice" |
| Max Corrections per Lesson | Contract | "How many small fixes we suggest (gentle feedback)" |
| Scaffolding Level | Contract | "How much help and support you get" |
| Lesson Complexity | Contract | "How challenging the lesson will be" |
| Support Language | Contract | "Your native language — used for explanations" |
| Lesson Complete! | Result | "Great work!" |
| Strengths | Result | "What you did well" |
| Validation Result | Result | "Check results" |
| Linguistic Check | Result | "Language check" |
| Pedagogical Check | Result | "Learning check" |
| Mastery Progress | Result | "Your progress" |
| Important Corrections | Result | "Small suggestion" (with single item shown) |
| Suggested Improved Phrasing | Result | "A clearer way to say it" |
| Beginnger (label) | Onboarding | "Starting Out" |

## A1-Specific Features

Added for A1 learners only:

1. **Learning Contract**: "What this means for you" summary box — 4 bullet points in simple language explaining what to expect
2. **Lesson**: Example sentence in purple box showing a model response
3. **Lesson**: Support hint — "Use your own language if you need to check a word. Just do your best!"
4. **Lesson**: Grammar focus shown with concrete examples — "Past tense — use 'I played', 'I ate'"
5. **Result**: Single correction, supportive tone, simplified section titles
6. **Diagnostic**: Level-specific helper text explaining that demo content is just for reading

## Mock AI Feedback Adaptation

| Aspect | A1 Treatment |
|--------|--------------|
| Number of corrections | 1 maximum |
| Severity of corrections | All marked "minor" regardless of original |
| Strengths | 1 strength, very supportive ("Good job! You are sharing your ideas.") |
| Confidence | 0.85 (supportive signal that learner is on the right track) |
| Visual presentation | Simplified labels throughout result screen |

## Verification

All A1 wording changes verified against the acceptance criteria:
- `a1_contract_readable`: true
- `technical_terms_explained_or_removed`: true
- `lesson_wording_level_aware`: true
- `a1_diagnostic_wording_simple`: true
