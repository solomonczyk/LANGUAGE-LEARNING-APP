# Decision Log — Language Learning App

**Status:** Approved  
**Version:** 1.0.0  
**Last updated:** 2026-06-09

---

## Decision record format

Each entry:

| Field | Description |
|-------|-------------|
| `ID` | Unique sequential identifier |
| `Date` | ISO date of decision |
| `Title` | Concise statement |
| `Context` | Background and constraints |
| `Decision` | What was decided |
| `Alternatives` | Options considered and why rejected |
| `Consequences` | Expected impact |
| `Status` | Proposed | Accepted | Deprecated | Superseded |
| `Superseded by` | ID if applicable |

---

## DCL-001 — Documentation-only vertical-layer approach

| Field | Value |
|-------|-------|
| **Date** | 2026-06-09 |
| **Title** | Begin with complete canonical documentation before any implementation |
| **Context** | The product scope is complex (language learning with AI, multiple lesson modes, security requirements). Starting implementation without full documentation risks inconsistent architecture, missed requirements, and contradictory design decisions. |
| **Decision** | Create a complete documentation suite covering product, methodology, diagnostics, lessons, skill modes, memory/engagement, architecture, security, and validation before any application code is written. |
| **Alternatives** | 1. **Agile documentation** — document incrementally alongside implementation. Rejected: risk of architectural inconsistency across a complex multi-engine system. 2. **MVP-only documentation** — document only what's needed for first build. Rejected: would miss security, anti-cheat, and reward-economy constraints that must be designed upfront. |
| **Consequences** | All implementation is deferred until documentation is accepted. The documentation serves as the single source of truth for all subsequent development. |
| **Status** | Accepted |

## DCL-002 — CEFR as primary progression framework

| Field | Value |
|-------|-------|
| **Date** | 2026-06-09 |
| **Title** | Adopt CEFR as the core progression framework |
| **Context** | The app needs a standardized, internationally recognized framework for language ability levels. CEFR is the most widely adopted standard. |
| **Decision** | Progression is defined using CEFR levels (A1–C2). All curriculum items, assessments, and content are mapped to CEFR descriptors. The CEFR Companion Volume (2020) is the reference edition, incorporating mediation, online interaction, and plurilingualism. |
| **Alternatives** | 1. **ACTFL** — US-centric, less international recognition for the target market. 2. **Custom framework** — would require extensive validation and lacks external recognition. |
| **Consequences** | Materials and assessments align with CEFR descriptors. Learners receive internationally interpretable level certifications (where applicable). Curriculum mapping must accommodate the non-linear nature of CEFR levels across skills. |
| **Status** | Accepted |

## DCL-003 — Communicative goal over grammar goal

| Field | Value |
|-------|-------|
| **Date** | 2026-06-09 |
| **Title** | Every lesson is anchored by a communicative goal, not a grammar point |
| **Context** | Traditional language apps (Duolingo, Babbel) organize lessons around grammatical structures. Research in task-based language teaching (TBLT) and the CEFR communicative approach prioritizes real-world tasks. |
| **Decision** | Every lesson contract MUST specify a communicative goal (real-world task) as the primary organizing principle. Grammar, vocabulary, and discourse foci support the communicative goal, not the reverse. |
| **Alternatives** | 1. **Grammar-first** — organize by tense/structure. Rejected: leads to decontextualized practice. 2. **Hybrid** — mix of grammar and communicative units. Rejected: risk of reverting to grammar-primary in practice. |
| **Consequences** | Lesson design always starts with "what will the learner DO?" Curriculum design requires authentic task analysis. Assessment criteria focus on communicative effectiveness, not just grammatical accuracy. |
| **Status** | Accepted |

## DCL-004 — LLM as constrained assistant, not authority

| Field | Value |
|-------|-------|
| **Date** | 2026-06-09 |
| **Title** | LLM operates within strict boundaries; deterministic engines hold authority |
| **Context** | LLMs are powerful for language analysis, content generation, and dialogue. However, they are unreliable for state mutations, reward decisions, and curriculum progression. |
| **Decision** | LLM is limited to: response analysis, draft content generation, educational dialogue. LLM CANNOT directly: change mastery, award XP, modify curriculum, alter grammar KB, access other users' data, perform admin actions. All LLM outputs must pass pipeline: schema validation → linguistic validation → pedagogical validation → policy engine → deterministic state transition → audit log. |
| **Alternatives** | 1. **LLM-authoritative** — let LLM decide progression and rewards. Rejected: unreliable, unaccountable, vulnerable to injection. 2. **No LLM** — rule-based only. Rejected: cannot provide personalized, contextual feedback at scale. |
| **Consequences** | All state mutations are deterministic. LLM quality affects learning experience but cannot compromise system integrity. Architecture requires validation pipeline. |
| **Status** | Accepted |

## DCL-005 — Multidimensional diagnostic, not single-level placement

| Field | Value |
|-------|-------|
| **Date** | 2026-06-09 |
| **Title** | Diagnostic evaluates 13 separate dimensions, not one overall level |
| **Context** | Language ability is not monolithic. A learner may be B1 in reading but A2 in speaking. Single-level placement leads to inappropriate content. |
| **Decision** | The initial diagnostic separately assesses: reading, listening, passive vocabulary, active vocabulary, grammar recognition, productive grammar, spoken production, spoken interaction, pronunciation intelligibility, narrative coherence, writing, mediation, communication strategies. Each dimension receives a level estimate with confidence interval. |
| **Alternatives** | 1. **Single placement test** — faster but inaccurate. 2. **Self-assessment** — unreliable for objective placement. |
| **Consequences** | Longer onboarding (estimated 30–45 min for full diagnostic). More complex learner model. Significantly better personalization. |
| **Status** | Accepted |

## DCL-006 — Dynamic scaffolding by skill and construction

| Field | Value |
|-------|-------|
| **Date** | 2026-06-09 |
| **Title** | Scaffolding level is determined per skill and per target construction |
| **Context** | A learner may need full scaffolding for spoken production of a new tense but can handle independent output for familiar vocabulary. A single scaffolding level across all dimensions is inappropriate. |
| **Decision** | Support graduated scaffolding modes: native_formulation, target_fragments, mixed_construction, guided_target_output, independent_target_output, interactive_target_use. The level for each lesson dimension is selected based on the specific skill × construction combination. |
| **Alternatives** | 1. **Global scaffolding level** — simpler but ignores skill asymmetry. 2. **Per-lesson scaffolding** — better but still too coarse. |
| **Consequences** | More complex lesson orchestration. Better learner experience with appropriate challenge. Scaffolding engine required in architecture. |
| **Status** | Accepted |

## DCL-007 — Mastery lifecycle with delayed retention check

| Field | Value |
|-------|-------|
| **Date** | 2026-06-09 |
| **Title** | Retained status requires a delayed, spaced-repetition verification |
| **Context** | Immediate post-lesson performance does not predict long-term retention. The system must distinguish between short-term recall and consolidated knowledge. |
| **Decision** | Mastery lifecycle: introduced → recognized → reconstructed → guided_use → independent_use → interactive_use → transferred → retained. The `retained` state is reachable only after successful delayed review (minimum 7 days after last practice, verified via spaced repetition). |
| **Alternatives** | 1. **Single mastery threshold** — simpler but conflates short-term and long-term knowledge. 2. **Time-based decay** — automatic demotion without verification. |
| **Consequences** | Mastery engine must track review history. Learner sees "in progress" for items not yet retained. Reporting distinguishes practiced vs. retained. |
| **Status** | Accepted |

## DCL-008 — Reward economy is fully deterministic

| Field | Value |
|-------|-------|
| **Date** | 2026-06-09 |
| **Title** | All XP and rewards are awarded by a deterministic Reward Engine |
| **Context** | LLMs cannot reliably compute rewards. Inconsistent or exploitable reward systems undermine motivation and economy integrity. |
| **Decision** | LLM NEVER awards XP, currency, or unlocks. The Reward Engine deterministically computes rewards based on verifiable events (lesson completion, review success, streak milestones, retention achievements). Rewards are awarded via atomic transactions with idempotency keys. |
| **Alternatives** | 1. **LLM-awarded rewards** — allows more nuanced assessment but unreliable and exploitable. 2. **Hybrid** — LLM recommends, engine approves. Adds complexity without solving the trust issue. |
| **Consequences** | Reward system is secure and auditable. Some nuanced achievements (e.g., "creative language use") cannot be directly rewarded unless deterministically measurable. |
| **Status** | Accepted |

## DCL-009 — Grammar Knowledge Base as version-controlled source of truth

| Field | Value |
|-------|-------|
| **Date** | 2026-06-09 |
| **Title** | Grammar rules are stored in a version-controlled Language Knowledge Base, not derived from LLM |
| **Context** | LLMs can generate plausible but incorrect grammar explanations. Consistent instruction requires an authoritative, reviewed source of grammar rules. |
| **Decision** | All grammar rules, exceptions, and pedagogical sequences are stored in a version-controlled Language Knowledge Base (LKB). LLM may reference the LKB for instruction but cannot invent rules. The LKB is authored and reviewed by linguists and language teachers. |
| **Alternatives** | 1. **LLM-as-grammar-authority** — flexible but unreliable. 2. **Static textbook rules** — authoritative but limited and hard to update. |
| **Consequences** | LKB requires authoring tooling and review workflow. LLM prompts must reference LKB IDs. Grammar instruction is consistent and auditable. |
| **Status** | Accepted |

## DCL-010 — Visual scenes without forced emotional interpretation

| Field | Value |
|-------|-------|
| **Date** | 2026-06-09 |
| **Title** | Ambiguous visual scenes should not enforce a single correct emotional reading |
| **Context** | Images used for emotion and perspective tasks may be ambiguous. Forcing a single "correct" interpretation undermines authentic language use and stifles learner creativity. |
| **Decision** | Visual emotion/perspective tasks accept any well-supported interpretation. The assessment criteria focus on the quality of justification (vocabulary, coherence, reasoning) rather than correctness of emotional reading. |
| **Alternatives** | 1. **Single correct answer** — simpler to assess but pedagogically limiting. 2. **Only unambiguous images** — narrows the available image pool. |
| **Consequences** | Assessment rubrics must evaluate justification quality, not interpretation accuracy. More authentic language practice. |
| **Status** | Accepted |

## DCL-011 — Writing cycle before full AI correction

| Field | Value |
|-------|-------|
| **Date** | 2026-06-09 |
| **Title** | AI must not immediately rewrite learner text; use scaffolded self-correction cycle |
| **Context** | Immediate full AI correction deprives the learner of self-correction opportunities and can create dependency. Research supports guided self-correction for deeper learning. |
| **Decision** | The writing cycle is: draft → problem identification → hint → self-correction → recheck → natural model → transfer task. AI provides hints and identifies problems but only produces a full model after the learner has attempted self-correction. |
| **Alternatives** | 1. **Immediate full correction** — faster but reduces learning. 2. **No correction** — learner may reinforce errors. |
| **Consequences** | Writing lessons require more interaction turns. Implementations must track each stage of the cycle. More effective long-term learning. |
| **Status** | Accepted |

## DCL-012 — Anti-cheat with server-authoritative state

| Field | Value |
|-------|-------|
| **Date** | 2026-06-09 |
| **Title** | All learning state is server-authoritative with idempotency and replay protection |
| **Context** | Client-side trust for XP, streaks, mastery, and rewards invites manipulation. A language learning app with real educational value must have trustworthy records. |
| **Decision** | All state mutations require: server-authoritative processing, idempotency keys per operation, unique attempt IDs per exercise, replay protection via nonce/expiry, atomic reward transactions, anti-farm rate limits, anomaly detection on suspicious patterns, practical revalidation on contradictory evidence. |
| **Alternatives** | 1. **Client-authoritative** — simpler but easily exploited. 2. **Trust-but-verify** — weaker guarantees, harder to audit. |
| **Consequences** | Higher implementation complexity. Must design for offline → sync with conflict resolution. Learning records are trustworthy for credentialing purposes. |
| **Status** | Accepted |

## DCL-013 — Prompt injection defense as architectural requirement

| Field | Value |
|-------|-------|
| **Date** | 2026-06-09 |
| **Title** | All user-supplied content is untrusted; injection defense is built into the architecture |
| **Context** | The app uses LLMs that process user text, speech transcripts, images, and uploaded documents. Each of these channels is a potential prompt injection vector. |
| **Decision** | All user data is treated as untrusted content. Injection defense measures include: input sanitization and boundary tokens in prompts, output schema validation, separation between user context and system instructions, instruction override detection, rate limiting on injection attempts, and regular red-team testing. User instructions must never alter system logic. |
| **Alternatives** | 1. **Prompt-only defense** — rely on instructing the LLM to ignore user commands. Insufficient for determined attacks. 2. **No LLM** — avoid the problem but lose core product value. |
| **Consequences** | All LLM interactions require defense layers. Additional latency and cost for validation. Security is a continuous investment, not a one-time implementation. |
| **Status** | Accepted |

## DCL-014 — Adaptive load with single-dimension increments

| Field | Value |
|-------|-------|
| **Date** | 2026-06-09 |
| **Title** | Increase lesson load one dimension at a time to avoid cognitive overload |
| **Context** | Increasing multiple difficulty dimensions simultaneously (more words + longer audio + complex grammar) can overwhelm learners, especially at lower levels. |
| **Decision** | When adapting lesson difficulty, only one dimension (time, vocabulary count, grammatical complexity, audio length, interaction turns, or correction count) may increase per lesson. Other dimensions stay at current level. |
| **Alternatives** | 1. **All-dimensions increase** — faster progression but higher dropout risk. 2. **Fixed increments** — ignores individual readiness. |
| **Consequences** | Progression may feel slower but is more sustainable. Adaptive algorithm must track each dimension separately. Better retention and lower frustration. |
| **Status** | Accepted |

## DCL-015 — Spaced repetition includes collocations, constructions, and discourse patterns

| Field | Value |
|-------|-------|
| **Date** | 2026-06-09 |
| **Title** | Spaced repetition covers more than vocabulary — includes constructions, errors, stories |
| **Context** | Most SRS systems only review isolated words. For communicative competence, learners must also consolidate collocations, grammatical constructions, repaired errors, personal story fragments, and communicative functions. |
| **Decision** | The spaced repetition system schedules reviews for: vocabulary items, collocations, grammatical constructions, dialogue fragments, persistent error patterns, learner's own story segments, and communicative functions. Each type has appropriate review task formats. |
| **Alternatives** | 1. **Vocabulary-only SRS** — simpler but insufficient for full competence. 2. **No SRS** — relies on in-lesson exposure only. |
| **Consequences** | Review scheduler must handle heterogeneous item types. Review tasks vary by item type. More comprehensive consolidation. |
| **Status** | Accepted |

## DCL-016 — Audio narrative length is level-bound

| Field | Value |
|-------|-------|
| **Date** | 2026-06-09 |
| **Title** | Audio narrative durations are capped by CEFR level |
| **Context** | Listening stamina and processing capacity grow with proficiency. Unconstrained audio length can overwhelm lower-level learners. |
| **Decision** | Audio narrative durations: A0–A1: 5–15s, A1–A2: 15–40s, A2–B1: 40–90s, B1–B2: 1–3 min, B2+: interviews/discussions/podcasts. Assessment dimensions: gist comprehension, detail comprehension, memory, retelling quality, grammar, vocabulary, coherence, interaction. |
| **Alternatives** | 1. **No length constraints** — more natural content but risks overload. 2. **Fixed length for all levels** — too short for advanced, too long for beginners. |
| **Consequences** | Audio content must be curated/created for specific level bands. Assessment captures multiple dimensions independently. |
| **Status** | Accepted |

## DCL-017 — Quiz is checkpoint, not mastery assessment

| Field | Value |
|-------|-------|
| **Date** | 2026-06-09 |
| **Title** | Quiz serves as a short controlled-practice checkpoint, distinct from mastery evaluation |
| **Context** | There is a risk of conflating short-term quiz performance with long-term mastery. The task explicitly distinguishes quiz (4–7 items, 2–4 min) from comprehensive mastery assessment. |
| **Decision** | Quizzes are short, frequent checkpoints (4–7 items, 2–4 min) that provide immediate feedback and inform the learner model but do not change mastery state alone. Mastery requires evidence across multiple contexts including delayed recall. |
| **Alternatives** | 1. **Quiz = mastery** — simpler but inaccurate. 2. **No quizzes** — less feedback for learner and system. |
| **Consequences** | Two distinct assessment mechanisms: quiz (short-term checkpoint) and mastery evaluation (multi-evidence). Different triggers, different state transitions. |
| **Status** | Accepted |

## DCL-018 — Isolated git repo for LANGUAGE-LEARNING-APP

| Field | Value |
|-------|-------|
| **Date** | 2026-06-09 |
| **Title** | The LANGUAGE-LEARNING-APP project uses its own git repository, separate from the parent gabric monorepo |
| **Context** | The project directory exists within the filesystem tree of the gabric repository. It is a conceptually independent project requiring its own version control, issue tracking, and CI/CD. |
| **Decision** | Initialize a separate git repository in the LANGUAGE-LEARNING-APP directory with remote at git@github.com:solomonczyk/LANGUAGE-LEARNING-APP.git. The parent gabric repo ignores it via nested-repo semantics. |
| **Alternatives** | 1. **Keep in gabric monorepo** — mixes unrelated projects, complicates permissions and CI. 2. **Submodule** — adds overhead without benefit for independent project. |
| **Consequences** | Clean separation of concerns. Independent commit history. No risk of affecting gabric operations. |
| **Status** | Accepted |
