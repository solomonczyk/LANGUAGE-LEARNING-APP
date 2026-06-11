# Level Adaptation Design

## Purpose

Document the design of level-aware wording variants implemented in Alpha 006 for A1, A2, B1, and B2 learners across diagnostic, contract, lesson, and feedback surfaces.

## Design Principles

1. **A1**: Maximum scaffolding — short instructions, native language support allowed, simple examples, smaller tasks, lower pressure, encouraging tone.
2. **A2**: Simple English with some support, short personal answers, basic grammar guidance, slightly more independence than A1.
3. **B1**: Clearer communicative goals, longer answers expected, more independence, less step-by-step guidance.
4. **B2**: More nuanced prompts, focus on style and precision, minimal scaffolding, natural phrasing emphasis.

## Surface-level Changes

### 1. Diagnostic Demo Responses

| Element | A1 | A2 | B1/B2 |
|---------|-----|-----|--------|
| Label | "Example only" | "Example only" | "Example only" |
| Helper text | "This is an example. Just read it — we'll use this as your answer." | "This is a sample answer. You don't need to do anything — we'll submit it for you." | "The example below shows a correct answer." |

### 2. Learning Contract

| Element | A1 | A2+ |
|---------|-----|-----|
| Title | "Your Personal Learning Plan" | "Learning Entry Contract" |
| Subtitle | "Based on your answers, we made a plan just for you." | Standard technical explanation |
| Term labels | Plain-language inline explanations | Brief hint text below terms |
| Active Vocabulary Budget | "New words you will learn in each lesson" | "Number of new vocabulary items introduced per lesson" |
| Max Corrections | "How many small fixes we suggest (gentle feedback)" | "Maximum number of primary corrections shown per submission" |
| Scaffolding | "How much help and support you get" | "Amount of structural support provided during lessons" |
| Summary box | Green card with 4 bullet points in simple language | Not shown |

### 3. Lesson Content

| Element | A1 | A2 | B1 | B2 |
|---------|-----|-----|-----|-----|
| Goal label | "Goal" | "Communicative Goal" | "Communicative Goal" | "Communicative Goal" |
| Goal text | "Tell a short story about your morning with your pet." | "Write about your morning routine with your pet." | "Describe a personal daily routine..." | "Craft a concise narrative..." |
| Task | 2-3 short sentences, simple words | 3-4 sentences | 3-5 sentences with time markers | 4-6 sentences, varied tenses |
| Example sentence | Yes | No | No | No |
| Support hint | "Use your own language if you need to check a word." | "Try using 'first', 'then', 'after'..." | Not shown | Not shown |
| Grammar focus | Simple explanation: "'I played', 'I ate'" | "Past tense" | "Past tense — narrative consistency" | "Past tense variation..." |
| Submit button | "Send my answer" | "Submit" | "Submit" | "Submit" |

### 4. Mock AI Feedback

| Element | A1 | A2 | B1 | B2 |
|---------|-----|-----|-----|-----|
| Intro | "Good effort! Here is some helpful feedback." | "You did well! Here are some small corrections." | Standard | "Here are some refinements..." |
| Strengths | 1, very supportive | 2, encouraging | 2, specific | 2, detailed |
| Max corrections | 1 (all minor) | 2 | 2+ | 2+ |
| Correction detail | Simple rewrite | Past tense explanation | Grammar + vocabulary | Nuance, collocation |
| Feedback style | Gentle, encouraging | Clear, direct | More precise | Style-focused |

## Level Detection

Learner level is determined by the lowest CEFR level across all diagnostic skill assessments. This is the same logic used by the learning contract system.

**Implementation locations**:
- `learning-contract.tsx` — reads from `diagnostic_profile_snapshot.assessments`
- `lesson/[id].tsx` — reads from learning contract via TanStack Query
- `result/[id].tsx` — reads from learning contract via TanStack Query
- `backend/lesson_engine/services.py` — reads `self_reported_level` from `LearnerProfile` model
- `backend/ai_gateway/services.py` — receives `learner_level` parameter from lesson engine

## Fallback

If no assessment data is available, all screens default to A2 (for lesson, result) or A1 (for diagnostic) as the safest fallback.

A2 is chosen as the default lesson level because:
- A2 is the most common CEFR self-assessment
- A2 feedback is supportive but not over-simplified
- A2 ensures comprehensible input for both A1 (slightly above) and A2-B1 learners
