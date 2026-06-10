# LLM Gateway Architecture

**Status:** Draft  
**Version:** 1.0.0  
**Last updated:** 2026-06-10

---

## Architecture Overview

The AI Gateway is a provider-independent abstraction layer that sits between the backend business logic and external LLM providers. It enforces structured output, manages provider failover, tracks costs, and ensures every LLM interaction is auditable.

```
┌─────────────────────────────────────────────────┐
│               Backend Module                     │
│  (lesson_engine, submission, etc.)               │
└──────────────────┬──────────────────────────────┘
                   │ call (Python internal)
                   ▼
┌─────────────────────────────────────────────────┐
│                AI Gateway                        │
│                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────┐ │
│  │ Text        │  │ Transcript  │  │ Dialogue │ │
│  │ Analysis    │  │ Analysis    │  │ Turn     │ │
│  └──────┬──────┘  └──────┬──────┘  └────┬─────┘ │
│         │                │               │        │
│  ┌──────┴────────────────┴───────────────┴─────┐ │
│  │         Structured Output Layer              │ │
│  │  (Schema enforcement, validation, retry)     │ │
│  └──────┬──────────────────────────────────────┘ │
│         │                                         │
│  ┌──────┴──────────────────────────────────────┐  │
│  │      Provider Router                        │  │
│  │  (primary → fallback → error)               │  │
│  └──────┬──────────────────────────────────────┘  │
└─────────┼─────────────────────────────────────────┘
          │ HTTPS
          ▼
┌─────────────────────┐  ┌─────────────────────┐
│  Provider A         │  │  Provider B         │
│  (Primary)          │  │  (Fallback)         │
└─────────────────────┘  └─────────────────────┘
```

---

## Provider-Independent Interface

### generate_structured_response()

**Purpose:** Generic structured LLM call with schema validation
| Property | Value |
|----------|-------|
| **Input** | prompt_template (str), context (dict), output_schema (JSON Schema), model_class (str) |
| **Output** | Validated structured data matching output_schema |
| **Provider Policy** | Primary → fallback → error |
| **Model Class** | "capable" (Claude Sonnet 4 / GPT-4o equivalent) |
| **Timeout** | 15 seconds |
| **Retry Eligibility** | Yes — max 2 retries, classified cause |
| **Cost Budget** | Tracked per request |
| **Fallback** | Alternate provider on 2nd retry |
| **Validation** | Post-generation schema validation; retry on failure |
| **Audit** | prompt_version, provider, model, tokens, latency, result |

### analyze_text()

**Purpose:** Analyze learner's written text for grammar, vocabulary, coherence, fluency
| Property | Value |
|----------|-------|
| **Input** | submission_text (str), lesson_context (dict), learner_level (str) |
| **Output** | Structured analysis: corrections[], vocabulary_suggestions[], grammar_notes[], coherence_score, fluency_score |
| **Model Class** | "capable" |
| **Timeout** | 12 seconds |
| **Retry Eligibility** | Yes — max 2 |
| **Audit** | Full audit fields |

### analyze_transcript()

**Purpose:** Analyze learner's audio transcript for comprehension accuracy and language quality
| Property | Value |
|----------|-------|
| **Input** | transcript (str), original_text (str), lesson_context (dict), learner_level (str) |
| **Output** | Structured analysis: comprehension_score, accuracy_notes[], pronunciation_notes[], language_quality_score |
| **Model Class** | "capable" |
| **Timeout** | 12 seconds |
| **Retry Eligibility** | Yes — max 2 |
| **Audit** | Full audit fields |

### generate_dialogue_turn()

**Purpose:** Generate next turn in an AI-learner dialogue
| Property | Value |
|----------|-------|
| **Input** | dialogue_history (list), scenario_context (dict), learner_level (str), learner_utterance (str) |
| **Output** | Structured response: ai_utterance (str), expected_response_type (str), scaffolding_hint (str or null) |
| **Model Class** | "fast" (Claude Haiku / GPT-4o-mini equivalent) |
| **Timeout** | 8 seconds |
| **Retry Eligibility** | Yes — max 1 |
| **Audit** | Full audit fields |

### generate_feedback()

**Purpose:** Generate pedagogical feedback based on analysis results
| Property | Value |
|----------|-------|
| **Input** | analysis_result (dict), learner_profile (dict), lesson_context (dict) |
| **Output** | Structured feedback: strengths[], improvements[], exercises[], encouragement (str) |
| **Model Class** | "fast" |
| **Timeout** | 8 seconds |
| **Retry Eligibility** | Yes — max 1 |
| **Audit** | Full audit fields |

---

## Provider Configuration

### Provider Policy

```yaml
providers:
  primary:
    provider: "anthropic"
    api_key_env: "AI_PROVIDER_PRIMARY_KEY"
    models:
      capable: "claude-sonnet-4-20250514"
      fast: "claude-haiku-4-20250514"
      analysis: "claude-sonnet-4-20250514"
    timeout: 15s
    max_retries: 2
    rate_limit: 50 requests/minute

  fallback:
    provider: "openai"
    api_key_env: "AI_PROVIDER_FALLBACK_KEY"
    models:
      capable: "gpt-4o"
      fast: "gpt-4o-mini"
      analysis: "gpt-4o"
    timeout: 15s
    max_retries: 1
    rate_limit: 50 requests/minute
```

### Model Classes

| Class | Purpose | Primary Model | Fallback Model | Cost Tier |
|-------|---------|---------------|----------------|-----------|
| capable | Text analysis, transcript analysis | Claude Sonnet 4 | GPT-4o | High |
| fast | Dialogue turns, feedback | Claude Haiku 4 | GPT-4o-mini | Low |
| analysis | Complex linguistic analysis | Claude Sonnet 4 | GPT-4o | High |

---

## LLM Authority Restrictions (CRITICAL)

These restrictions MUST be enforced at the architecture level:

1. **LLM proposes, never decides** — LLM output is always a proposal; acceptance requires passing all validation gates
2. **LLM cannot change user state** — No direct database access; no state mutation
3. **LLM cannot award rewards** — Reward decisions are 100% deterministic; LLM must not suggest XP amounts
4. **LLM cannot modify mastery** — Mastery transitions are deterministic; LLM analysis provides evidence only
5. **LLM output must pass validation gates** — Schema, linguistic, pedagogical validation required
6. **Structured output only** — Never free-text LLM responses; always schema-enforced

### Enforcement Mechanisms

| Restriction | How Enforced |
|-------------|--------------|
| No state mutation | AI Gateway has no database access; returns data to caller |
| No reward influence | Reward Engine never receives LLM output as input |
| No mastery influence | Mastery Engine uses only deterministic evidence scoring |
| Structured output | Post-LLM schema validation; non-conforming output rejected |
| No direct responses | LLM responses always pass through validation pipeline |
| Audit trail | Every LLM call logged with prompt version, output hash, result |

---

## Cost Tracking

| Metric | Implementation |
|--------|---------------|
| Per-request cost | Token count × provider rate |
| Per-lesson cost | Sum of all LLM calls in lesson pipeline |
| Per-user cost | Aggregated daily/weekly/monthly |
| Provider cost | Aggregated by provider |
| Budget alert | Threshold-based alerting (daily/weekly/monthly) |

### Token Budget

| Operation | Estimated Input Tokens | Estimated Output Tokens | Cost Estimate |
|-----------|----------------------|------------------------|---------------|
| Text analysis | 2000 | 1000 | ~$0.02 |
| Transcript analysis | 3000 | 1000 | ~$0.03 |
| Dialogue turn | 4000 | 500 | ~$0.01 |
| Feedback generation | 2000 | 500 | ~$0.01 |
| Prompt generation | 1000 | 200 | ~$0.005 |

**Target:** Cost per completed lesson < $0.10 (provisional)

---

## Audit Fields

Every AI Gateway operation records:

```json
{
  "request_id": "uuid",
  "operation": "analyze_text",
  "provider": "anthropic",
  "model": "claude-sonnet-4-20250514",
  "prompt_version": "v1.2.3",
  "prompt_hash": "sha256:abc123...",
  "request_tokens": 2150,
  "response_tokens": 980,
  "total_tokens": 3130,
  "latency_ms": 3450,
  "retry_count": 0,
  "fallback_used": false,
  "schema_valid": true,
  "linguistic_valid": true,
  "pedagogical_valid": true,
  "result": "accepted",
  "error": null,
  "estimated_cost": 0.021
}
```
