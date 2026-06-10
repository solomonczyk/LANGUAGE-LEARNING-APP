# AI Gateway Runtime Canon

**Status:** Accepted  
**Version:** 1.0.0  
**Last updated:** 2026-06-10  
**ADR:** ADR-008, ADR-009

---

## 1. Provider-Independent Interface

All LLM operations go through the AI Gateway abstraction layer. Direct provider SDK calls are FORBIDDEN.

```
ai_gateway.generate_structured_response(schema, prompt_context)
ai_gateway.analyze_text(submission_text, learner_level)
ai_gateway.analyze_transcript(audio_transcript, lesson_context)
ai_gateway.generate_dialogue_turn(dialogue_history, scenario)
ai_gateway.generate_feedback(analysis_result, learner_profile)
```

---

## 2. Operation Specifications

### 2.1 generate_structured_response(prompt_schema, prompt_context)
| Field | Specification |
|-------|--------------|
| Input schema | Pydantic model defining expected JSON structure |
| Output schema | Pydantic model (validated before return) |
| Prompt version | Git-tracked, hash in audit (prompt_templates/prompts/*.j2) |
| Model class | Fast (claude-haiku or equivalent tier) |
| Timeout | 30s |
| Token budget | 4,096 output tokens max |
| Cost budget | Tracked per request, alert at threshold |
| Retry eligibility | Retryable causes: timeout, 5xx, rate limit; NON-retryable: schema validation fail |
| Fallback | Fallback provider on 2nd consecutive failure |
| Audit fields | request_id, prompt_version, model, tokens, cost, latency, result_code |

### 2.2 analyze_text(submission_text, learner_level)
| Field | Specification |
|-------|--------------|
| Input schema | `{ text: string, learner_level: string, lesson_type: string }` |
| Output schema | Analysis result with corrections, feedback, score |
| Prompt version | `analysis/v1` |
| Model class | Medium (claude-sonnet or equivalent) |
| Timeout | 60s |
| Token budget | 8,192 output tokens |
| Retry | 2 retries on timeout/5xx; fallback on 3rd |
| Audit | Full input/output (lesson data) |

### 2.3 analyze_transcript(audio_transcript, lesson_context)
| Field | Specification |
|-------|--------------|
| Input schema | `{ transcript: string, lesson_context: object }` |
| Output schema | Transcript analysis with accuracy, fluency, pronunciation feedback |
| Prompt version | `transcript/v1` |
| Model class | Medium |
| Timeout | 60s |
| Retry | 2 retries; fallback on 3rd |

### 2.4 generate_dialogue_turn(dialogue_history, scenario)
| Field | Specification |
|-------|--------------|
| Input schema | `{ history: array, scenario: object, learner_level: string }` |
| Output schema | Next dialogue turn with alternatives |
| Prompt version | `dialogue/v1` |
| Model class | Medium |
| Timeout | 30s |
| Retry | 1 retry (dialogue is interactive, latency matters) |

### 2.5 generate_feedback(analysis_result, learner_profile)
| Field | Specification |
|-------|--------------|
| Input schema | `{ analysis: object, learner_level: string, personality: object }` |
| Output schema | Feedback message with encouragement and improvement tips |
| Prompt version | `feedback/v1` |
| Model class | Fast (haiku class) |
| Timeout | 15s |
| Retry | 1 retry |

---

## 3. Mock AI Gateway (MVP Only)

For the first vertical slice (`003`), the AI Gateway operates in **mock mode only**.

```
config.ai_mock_mode = True  # default for all environments until staging
```

**Mock behaviour:**
- `analyze_text()` returns pre-defined structured analysis matching the output schema
- Configurable response delay (500ms–2000ms, default 1000ms)
- Configurable failure modes: timeout, invalid JSON, schema mismatch (for testing)
- Mock responses are schema-validated via Pydantic (same as real mode)
- Mock responses are NOT used for training or evaluation

**Transition to real provider:** New task, new ADR, requires:
- Provider API key in staging config
- Provider-independent fallback tested
- Prompt evaluation suite passing
- Cost tracking verified
- Schema validation confirmed working with real provider output

---

## 4. Authority Restrictions

**LLM can only propose. LLM cannot:**

| Forbidden Action | Enforcement Mechanism |
|-----------------|----------------------|
| Complete a lesson | `lesson_engine.complete_session()` is deterministic; LLM output is input only |
| Change mastery | `mastery` module uses deterministic rules; LLM output is evidence only |
| Award rewards | `reward_engine.award_xp()` has no LLM code path |
| Schedule reviews | `review_scheduler.schedule()` is deterministic algorithm |
| Modify curriculum | `curriculum` module does not expose mutation from AI Gateway |
| Execute authorization | Auth decisions are JWT-based, never AI-influenced |
| Make security decisions | Security is hard-coded policy, never AI-influenced |
| Send notifications | `notifications.send()` requires explicit module call from policy engine |

---

## 5. Validation Chain

```
LLM Response
  → Schema Validation (Pydantic)          → fail → reject
    → Linguistic Validation                → fail → reject
      → Pedagogical Validation             → fail → reject
        → Policy Engine Decision           → fail → reject
          → State Transition (deterministic)
```

Each stage must pass before the next executes. No stage can be skipped.

---

## 6. Audit Requirements

Every AI Gateway operation records:

| Field | Source |
|-------|--------|
| `trace_id` | From incoming request |
| `request_id` | AI Gateway internal ID |
| `prompt_version` | From prompt template registry |
| `model` | Provider model used |
| `input_tokens` | Token count |
| `output_tokens` | Token count |
| `cost` | Computed from token counts |
| `latency_ms` | Provider response time |
| `schema_valid` | Boolean |
| `linguistic_valid` | Boolean |
| `pedagogical_valid` | Boolean |
| `accepted` | Boolean (all gates passed) |
| `retry_count` | Number of retries |
| `error_code` | If failed |
