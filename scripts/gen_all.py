#!/usr/bin/env python3
"""Generate ALL documentation documents for the Language Learning App."""

import os, json

BASE = "f:/Dev/Projects/LANGUAGE-LEARNING-APP/documents/language_learning_app"

# Section: In scope / Out of scope / Core decisions / Acceptance criteria
IN_OUT = {
    "methodology": ("- Pedagogical framework definition\n- Curriculum structure and progression design\n- Assessment and competence model specifications\n- Learning strategy and learner autonomy frameworks",
                     "- Detailed lesson plans\n- Specific curriculum item specifications\n- Assessment rubric details\n- Tutor training materials",
                     "1. Methodology is grounded in established SLA research\n2. Task-Based Language Teaching is the core approach\n3. Personal narrative is the primary content source\n4. CEFR 2020 is the reference framework",
                     "1. Methodology is clearly articulated and internally consistent\n2. Research foundations are cited\n3. Methodology directly informs product design\n4. All recommendations are actionable"),
    "diagnostics": ("- Initial diagnostic design and placement\n- Multidimensional learner profiling\n- Entry contract and onboarding\n- Continuous recalibration and assessment confidence\n- Error evidence tracking",
                     "- Individual diagnostic items\n- Norm-referenced scoring\n- Certification decision logic\n- Third-party assessment integration",
                     "1. Diagnostic must evaluate 14+ separate dimensions\n2. No single-level placement is allowed\n3. Confidence intervals accompany every estimate\n4. Continuous recalibration updates the profile",
                     "1. All diagnostic dimensions are defined with assessment methods\n2. Confidence model is mathematically specified\n3. Error evidence model is structured and actionable\n4. Recalibration policy is defined"),
    "lessons": ("- Lesson type taxonomy (14 modes)\n- Runtime contract structure\n- Topic orchestration and format selection\n- Scaffolding, cognitive load, and feedback policies\n- Completion and mastery criteria",
                 "- Specific lesson content\n- UI/UX implementation\n- Teacher-facing tools\n- Real-time execution logic",
                 "1. Communicative goal drives every lesson\n2. Scaffolding is per-skill and per-construction\n3. Cognitive load increases one dimension at a time\n4. Feedback is selective and prioritized",
                 "1. All 14 lesson modes are defined with purpose and structure\n2. Lesson contract has all required fields\n3. Scaffolding policy covers 6 levels with fading rules\n4. Cognitive load limits are specified per CEFR level"),
    "skill_modes": ("- Personal narrative lesson system\n- Suggested situation lesson system\n- Visual narrative and emotion/perspective systems\n- Audio narrative and listening comprehension\n- Reading, writing, and spoken dialogue systems\n- Quiz and controlled practice system",
                     "- Implementation code\n- UI specifications\n- Third-party integration details\n- Production deployment configuration",
                     "1. Each skill mode has a defined pedagogical purpose\n2. Writing follows scaffolded self-correction cycle\n3. Visual scenes accept multiple emotional interpretations\n4. Quiz is a checkpoint, not mastery assessment",
                     "1. All 13 skill mode documents exist with substantive content\n2. Writing cycle is specified (draft through transfer)\n3. Visual narrative includes all required task types\n4. Quiz specifications include length and item types"),
    "memory": ("- Spaced repetition system design\n- Adaptive review scheduling\n- Review task variation policy\n- Adaptive learning load specifications\n- Gamification and engagement system\n- Reward economy and streaks\n- Content personalization and notifications",
                "- Implementation of SRS algorithm\n- UI for review sessions\n- Push notification infrastructure\n- Leaderboard implementation",
                "1. SRS covers vocabulary, collocations, constructions, errors, stories, functions\n2. Reward engine is fully deterministic, no LLM involvement\n3. Learning load increases one dimension at a time\n4. Streaks have recovery paths, not hard punishment",
                "1. SRS interval chain is specified\n2. Review task types match item types\n3. Reward catalog is complete with deterministic rules\n4. Notification policy includes frequency caps and opt-out"),
    "architecture": ("- Overall system architecture\n- AI agent architecture and validation pipeline\n- Narrative, Visual, Audio scenario engines\n- Curriculum, Learner Model, Assessment, Mastery, Reward engines\n- Review scheduler and LQA services\n- Model provider fallback and observability",
                      "- Implementation code\n- Infrastructure configuration\n- CI/CD pipeline\n- Third-party service integrations",
                      "1. LLM cannot directly change mastery, XP, curriculum, or LKB\n2. Required pipeline: LLM -> schema validation -> linguistic validation -> pedagogical validation -> policy engine -> state transition -> audit\n3. Deterministic engines hold state authority\n4. All state changes are auditable",
                      "1. All 14 architecture documents exist\n2. LLM boundaries are clearly defined\n3. Pipeline specification is complete\n4. Each engine has defined responsibilities and interfaces"),
    "security": ("- AI security and prompt injection defense\n- Anti-cheat and learning integrity\n- Authorization and tool access policy\n- Reward economy integrity\n- Untrusted content handling\n- User data isolation and privacy\n- Rate limiting, logging, red team testing\n- Sensitive content and data retention",
                  "- Implementation of security controls\n- Specific encryption libraries\n- Production security configuration\n- Penetration testing reports",
                  "1. All user content is untrusted\n2. State is server-authoritative with idempotency\n3. Cross-user isolation prevents data access\n4. Structured output with JSON Schema validation on all LLM outputs\n5. No secrets in prompts",
                  "1. All 11 security documents exist\n2. Prompt injection defense has multiple layers\n3. Anti-cheat covers all reward and progression mechanisms\n4. Data retention and deletion policy is specified"),
    "validation": ("- MVP scope and roadmap\n- Validation and experiment plan\n- Product and learning metrics\n- Accessibility and inclusive learning\n- Content authoring and editorial workflow\n- Human linguist review and AI calibration\n- Risk register, traceability matrix, acceptance criteria\n- Language variants, licensing, offline learning, state repair",
                    "- Implementation of validation infrastructure\n- Specific A/B test configurations\n- Marketing collateral\n- User research recruitment",
                    "1. MVP scope is clearly defined with phased rollout\n2. Validation plan includes A/B testing and user studies\n3. Traceability matrix covers all requirements\n4. Risk register is comprehensive with mitigations",
                    "1. All 15 validation documents exist\n2. MVP scope is specific and actionable\n3. Risk register has probability, impact, and mitigation for each risk\n4. Acceptance criteria are testable")
}

# Document content - organized by section
CONTENT = {}

CONTENT["methodology"] = {
    "24_grammar_instruction_system.md": (
        "Grammar Instruction System",
        "How grammar is taught within the communicative framework — rule-based instruction from the LKB, inductive and deductive approaches.",
        """## Grammar in service of communication

Grammar is never taught as an isolated system. It always arises from and feeds back into communicative tasks.

## Sources of grammar content

Grammar rules come exclusively from the LKB. The LLM may:
- Present rules from the LKB in learner-friendly language
- Generate examples based on LKB rules
- Create practice activities targeting specific rules

The LLM may NOT:
- Invent grammatical rules
- Contradict LKB content
- Present alternative analyses without marking them as such

## Inductive vs deductive presentation

| Approach | Description | When used |
|----------|-------------|-----------|
| Inductive | Learner discovers pattern from examples | Preferred for simple, regular patterns; learners who enjoy puzzle-solving |
| Deductive | Rule is presented, then practiced | Preferred for complex rules; learners who want explicit explanation |

## Grammar in the lesson flow

1. **Task performance** — Learner attempts communicative task
2. **Noticing** — Attention is drawn to a grammatical feature
3. **Brief explanation** — Rule presented inductively or deductively
4. **Controlled practice** — 2-3 targeted exercises
5. **Task replay** — Learner repeats the task, applying the rule
6. **Transfer** — New context requiring the same rule

## Error selection for grammar focus

Not every error is treated. Selection criteria:
1. Global vs local — Errors affecting meaning take priority
2. Teachable moment — Is the learner ready for this rule?
3. Frequency — Persistent errors take priority over one-off slips
4. L1 influence — Errors from L1 transfer need contrastive explanation

## Grammar review in SRS

Grammatical constructions enter the spaced repetition system alongside vocabulary. Review tasks require production in new contexts."""
    ),
    "25_vocabulary_collocation_and_phraseology.md": (
        "Vocabulary, Collocation and Phraseology",
        "The vocabulary acquisition system — selection, presentation, practice, and retention of words, collocations, and multi-word units.",
        """## Vocabulary selection principles

1. **Frequency** — High-frequency words appear first (per corpus data)
2. **Relevance** — Learner's personal topics and needs influence selection
3. **CEFR alignment** — Words appropriate to the learner's level
4. **Learnability** — Cognates and transparent words may be introduced earlier
5. **Usefulness** — Words with broad applicability prioritized over narrow ones

## Active vs passive vocabulary

The system tracks two states for each vocabulary item:

| State | Definition | Assessment |
|-------|------------|------------|
| Passive | Recognizes and understands meaning | Recognition tasks (multiple choice, matching) |
| Active | Can produce in appropriate context | Production tasks (sentence completion, description) |

Transition from passive to active requires:
- Multiple exposures in varied contexts
- Productive practice opportunities
- Successful recall in spaced repetition

## Collocation teaching

Collocations are taught as units, not as individual words. Examples:
- make + decision (not *do a decision)
- heavy + rain (not *strong rain)
- take + break (not *make a break)

## Phraseological competence

Learners need:
- Social formulae — How are you? Nice to meet you
- Discourse markers — First of all, on the other hand
- Lexical chunks — I was wondering if, the thing is
- Idioms and fixed expressions — Level-appropriate

## Personal vocabulary tracking

Each learner has a personal vocabulary repository with items from lessons, self-added words, words from stories, mastery status per item, and SRS schedule.

The learner can view vocabulary inventory, filter by level/topic, and see progress."""
    ),
    "26_phonological_competence_and_pronunciation.md": (
        "Phonological Competence and Pronunciation",
        "The pronunciation teaching framework — intelligibility-based approach, segmental and suprasegmental features.",
        """## Pronunciation philosophy: intelligibility over nativeness

The goal is comprehensible pronunciation, not native-like accent. Target: pronunciation that can be understood without effort by a sympathetic native speaker.

## Components of phonological competence

### Segmental (individual sounds)
- Consonants and vowels of the target language
- Sound distinctions that affect meaning (minimal pairs)
- Sounds that do not exist in the learner's L1

### Suprasegmental (beyond individual sounds)
- Word stress and sentence stress
- Intonation patterns (questions, emotions, emphasis)
- Rhythm and connected speech
- Pausing and phrasing

## Assessment dimensions

| Dimension | What is assessed |
|-----------|-----------------|
| Segment accuracy | Individual sound production |
| Word stress | Correct syllable emphasis |
| Sentence stress | Focus on key content words |
| Intonation | Rising/falling patterns for meaning |
| Connected speech | Linking, elision, reduction |
| Overall intelligibility | Can a listener understand? |

## Integration with lessons

Pronunciation is addressed:
1. Diagnostically — Initial assessment identifies issues
2. In lessons — When error affects intelligibility, brief practice is inserted
3. In review — Pronunciation items enter SRS
4. Through audio — Audio narratives provide models for shadowing and repetition

## L1-specific pronunciation profiles

The system maintains L1-specific pronunciation difficulty profiles for common L1-L2 pairs."""
    ),
    "27_pragmatics_register_and_politeness.md": (
        "Pragmatics, Register and Politeness",
        "Teaching contextually appropriate language use including speech acts, register variation, and politeness strategies.",
        """## Pragmatic competence in communication

Pragmatic competence is the ability to use language appropriately in social contexts. It is often more important for successful communication than grammatical accuracy.

## Speech acts

Each speech act has multiple linguistic realizations depending on context:

| Speech act | Formal | Informal | Very casual |
|------------|--------|----------|-------------|
| Request | Would you mind... | Can you... | Got a sec to... |
| Apology | I sincerely apologize | Sorry about that | My bad |
| Refusal | I regret that I cannot | Sorry, no can do | Nah |

## Register variation

The system teaches register awareness:
- Formal — Official, academic, professional contexts
- Neutral — Standard polite interaction
- Informal — Friends, family, casual settings
- Very casual — Close relationships, slang

Learners practice producing the same message in different registers.

## Politeness strategies

Positive politeness (showing solidarity), negative politeness (showing deference, not imposing), off-record politeness (hints, indirectness).

## Cultural variation

Directness vs indirectness, formality expectations, addressing conventions, turn-taking norms, compliment responses vary significantly across cultures.

## Integration

Pragmatics is integrated through functional communication lessons, role-play, error correction for inappropriate language, and cultural notes."""
    ),
    "28_intercultural_competence.md": (
        "Intercultural Competence",
        "Developing learners' ability to navigate and mediate between cultures.",
        """## What is intercultural competence?

Intercultural competence involves: awareness of one's own cultural lens, knowledge of other cultural norms, skills in interpreting across cultures, and attitudes of curiosity and openness.

## Cultural dimensions

### High-context vs low-context communication
- High-context (Japan, Arab countries): Meaning is implicit, relies on shared knowledge
- Low-context (Germany, USA): Meaning is explicit, stated directly

### Individualism vs collectivism
- Individualist (USA, Western Europe): Direct speech, personal achievement
- Collectivist (East Asia, Latin America): Indirect speech, group harmony

### Power distance
- High (Mexico, Russia): Clear hierarchy, formal address
- Low (Denmark, Israel): Informal, egalitarian

## Cultural content principles

Cultural content is:
1. Integrated — Embedded in language use, not separate lessons
2. Contrastive — Comparing target culture with learner's L1 culture
3. Non-stereotyping — Patterns as tendencies, not absolutes
4. Practical — Relevant to situations the learner will encounter

## Topics covered

Greetings and address, time and punctuality, gift-giving, food and dining, business culture, taboo topics. Each with cross-cultural comparisons and practical guidance."""
    ),
    "29_plurilingual_and_language_transfer_model.md": (
        "Plurilingual and Language Transfer Model",
        "Leveraging learner's existing linguistic repertoire and addressing cross-linguistic transfer.",
        """## Plurilingual competence (CEFR 2018)

Plurilingual competence is the ability to draw on a repertoire of linguistic and cultural resources from multiple languages as an integrated, holistic ability.

## Leveraging the learner's L1

The app:
1. Uses L1 strategically for grammar explanations, cultural notes, translations
2. Acknowledges positive transfer (cognates, similar structures) and negative transfer (false friends)
3. Provides contrastive information between L1 and target language

## Language transfer awareness

| Transfer type | Example (Spanish speaker learning English) |
|--------------|--------------------------------------------|
| Positive | Information (cognate) |
| Negative | I have 30 years instead of I am 30 |
| Null transfer | No article system in L1, struggling with articles |

The system maintains L1-specific transfer profiles to anticipate common errors.

## Plurilingual teaching strategies

1. Cross-linguistic comparison tasks
2. Strategic translation and back-translation
3. Code-switching awareness
4. Third language transfer for multilingual learners

## Learner plurilingual profile

The profile includes all languages known with levels, language family relationships, known transfer patterns, and preferred language for metalinguistic explanations."""
    ),
    "30_mediation_and_information_transfer.md": (
        "Mediation and Information Transfer",
        "The mediation framework per CEFR 2018 — relaying information, explaining data, facilitating communication.",
        """## Mediation in CEFR 2018

The CEFR Companion Volume introduced mediation as a core language activity alongside reception, production, and interaction.

## Types of mediation

### Mediating a text
- Relaying specific information
- Explaining data (charts, infographics)
- Processing text (summarizing, paraphrasing)
- Translating a written text
- Note-taking while listening

### Mediating concepts
- Collaborating in a group
- Leading group work
- Managing interaction

### Mediating communication
- Facilitating between parties
- Managing sensitive topics
- Cultural mediation

## Mediation tasks in the app

| CEFR mediation activity | App task type |
|-------------------------|--------------|
| Relaying information | Read a text and tell someone what it says |
| Explaining data | Describe a chart or infographic |
| Summarizing | Condense a narrative into key points |
| Interpreting | Act as go-between in a dialogue |
| Facilitating | Help two parties reach agreement |

## Progression

A1-A2: Relay very simple, concrete information
A2-B1: Summarize short texts, explain simple data
B1-B2: Mediate detailed information, facilitate routine situations
B2+: Mediate complex information, manage sensitive cross-cultural situations"""
    ),
    "31_communication_strategy_and_repair.md": (
        "Communication Strategy and Repair",
        "Explicit teaching of communication strategies for managing real-world interactions.",
        """## Why teach communication strategies?

Even with limited linguistic resources, learners can communicate effectively if they have strategies to compensate for unknown vocabulary, clarify misunderstanding, and repair breakdowns.

## Strategy categories

### Achievement strategies (keep communicating)
- Paraphrasing — Describing the concept when the word is unknown
- Approximation — Using a similar word
- Word coinage — Creating a term from known elements
- Non-linguistic means — Gestures, drawing, pointing
- Restructuring — Starting the utterance differently

### Reduction strategies (simplify message)
- Message abandonment
- Topic avoidance
- Message replacement

### Interaction strategies
- Clarification requests — Could you repeat that?
- Confirmation checks — Do you mean X?
- Comprehension checks — Do you understand?
- Self-repair — Correcting own error
- Appeals for help — How do you say X?

## Repair strategy teaching

Repair strategies are taught explicitly in focused lessons, in context when breakdowns occur, and in SRS for strategy phrases.

## Strategy assessment

Learners are assessed on range of strategies, appropriate selection, and effectiveness in maintaining communication."""
    ),
    "32_learner_autonomy_and_learning_strategies.md": (
        "Learner Autonomy and Learning Strategies",
        "Fostering independent learning skills for continued improvement beyond the app.",
        """## Why learner autonomy matters

The ultimate goal is not just language proficiency but the ability to continue learning independently. The app should progressively make itself less necessary.

## Learning strategy categories

### Metacognitive strategies (planning and monitoring)
- Goal-setting — Setting specific, achievable language goals
- Planning — Organizing learning time and resources
- Self-monitoring — Tracking progress and identifying weaknesses
- Self-evaluation — Assessing learning outcomes

### Cognitive strategies (processing and retaining)
- Rehearsal — Repeating to remember
- Elaboration — Connecting new information to existing knowledge
- Organization — Grouping, categorizing, diagramming
- Inferencing — Guessing meaning from context

### Social and affective strategies
- Cooperation — Learning with others
- Questioning for clarification — Asking for help
- Self-talk — Managing anxiety and motivation

## Integration into the app

1. Explicit instruction — Lessons that teach learning strategies
2. Prompted use — The app suggests strategies at appropriate moments
3. Reflection prompts — Brief reflection on strategies after lessons
4. Progress visualization — Tools for the learner to see their own progress

## Autonomy progression

A1-A2: Guided — app suggests goals, strategies, reflection
B1: Supported — app prompts but learner chooses
B2: Independent — learner sets goals, app provides resources
C1+: Autonomous — learner uses app as one of many tools"""
    )
}

CONTENT["diagnostics"] = {
    "40_initial_diagnostic_and_placement_system.md": (
        "Initial Diagnostic and Placement System",
        "The multidimensional initial assessment that evaluates learners across 14+ separate dimensions with confidence intervals.",
        """## Purpose of the initial diagnostic

To create a detailed, multi-dimensional profile of the learner's current language abilities — not a single level. This profile drives lesson personalization, curriculum starting point, and scaffolding level.

## Dimensions assessed

| Dimension | Assessment method | What is measured |
|-----------|------------------|-----------------|
| Reading | Text comprehension questions | Understanding written texts |
| Listening | Audio comprehension | Understanding spoken language |
| Passive vocabulary | Recognition tasks | Vocabulary breadth |
| Active vocabulary | Production tasks | Vocabulary available for use |
| Grammar recognition | Grammaticality judgments | Explicit grammar knowledge |
| Productive grammar | Error analysis in production | Grammar in use |
| Spoken production | Monologue task | Extended speech |
| Spoken interaction | Dialogue task | Interactive communication |
| Pronunciation intelligibility | Reading aloud, free speech | Sound production |
| Narrative coherence | Story retelling | Discourse organization |
| Writing | Written prompt response | Written production |
| Mediation | Information transfer task | Relaying information |
| Communication strategies | Problem-solving scenario | Strategy use |

## Adaptive diagnostic flow

The diagnostic uses adaptive difficulty within each dimension to efficiently find the learner's level:
1. Start at estimated level (or A1 if unknown)
2. Present task at that level
3. If correct, move up; if incorrect, move down
4. Converge on level estimate after 3-5 items per dimension

## Confidence intervals

Each dimension estimate includes a confidence interval. The system requires minimum confidence before making placement decisions. Low-confidence dimensions are flagged for early reassessment.

## Duration

Estimated 30-45 minutes for full diagnostic. Learners can pause and resume. If full diagnostic is too long, a short-form version (15 min) provides initial estimates with wider confidence intervals."""
    ),
    "41_diagnostic_task_bank_contract.md": (
        "Diagnostic Task Bank Contract",
        "Structure and requirements for the diagnostic task item bank.",
        """## Purpose

To define the structure, formats, and quality requirements for diagnostic task items used across all assessment dimensions.

## Task types

| Task type | Used for | Item count per dimension |
|-----------|----------|-------------------------|
| Multiple choice | Reading, Listening, Grammar recognition | 10-20 |
| Matching | Vocabulary recognition | 10-15 |
| Gap-fill | Grammar, Vocabulary | 8-12 |
| Sentence completion | Productive grammar | 5-8 |
| Short answer | Writing | 2-3 |
| Read aloud | Pronunciation | 3-5 |
| Monologue (30-60s) | Spoken production | 1-2 |
| Dialogue response | Spoken interaction | 3-5 |
| Retelling | Narrative coherence | 1 |
| Information transfer | Mediation | 1-2 |

## Item requirements

Each item must include:
- Stimulus (text, audio, image, prompt)
- Correct answer / expected response
- Scoring criteria (for open-ended items)
- Difficulty level (CEFR sub-level)
- Dimension(s) assessed
- Time limit
- Instructions (learner-facing)
- L1 translation support where appropriate

## Item pool requirements

Minimum 50 items per dimension to support adaptive testing and prevent memorization. Items tagged by CEFR level, sub-skill, and topic domain.

## Quality assurance

All items reviewed by linguist and methodologist. Pilot-tested with minimum 30 learners per CEFR level. Item analysis for discrimination, difficulty, and reliability."""
    ),
    "42_multidimensional_learner_profile.md": (
        "Multidimensional Learner Profile",
        "The structured representation of a learner's abilities across all assessed dimensions.",
        """## Profile structure

The learner profile captures ability estimates across all 14+ dimensions, plus metadata, preferences, and history.

## Per-dimension data

For each dimension:
- CEFR level estimate (A1-C2 with sub-level)
- Confidence interval
- Number of observations
- Date of last assessment
- Trend (improving, stable, declining)

## Profile sections

### Ability estimates
Per-dimension CEFR levels with confidence. This is the core data driving personalization.

### Skill asymmetry visualization
Visual comparison of strongest and weakest dimensions. Example: Reading B1 vs Speaking A2. This helps learners understand their profile and motivates targeted practice.

### Learning style indicators
Preferences for: inductive vs deductive, visual vs auditory, individual vs interactive, fast vs thorough.

### Interest inventory
Topics the learner has engaged with: personal stories, suggested preferences, content engagement history.

### Error profile
Most common error types, persistent patterns, L1-specific issues.

### Versioning

The profile is versioned. Each update creates a new version. Previous versions are retained for analysis. Major updates (e.g., new diagnostic) create a new baseline."""
    ),
    "43_learning_entry_contract.md": (
        "Learning Entry Contract",
        "The agreement between system and learner established at onboarding, including goals, commitments, and privacy consent.",
        """## Purpose

To establish shared expectations between the system and the learner at the start of their journey. The contract is periodically revisited and updated.

## Contract components

### Learning goals
Learner states their primary motivation and goals:
- Why are you learning this language?
- What do you want to be able to do? (travel, work, family, etc.)
- What level are you aiming for?
- How much time can you commit?

### Time commitment
- Daily/weekly practice target
- Preferred time of day
- Session length preference

### Language background
- L1 and other languages
- Previous learning experience
- What has/hasn't worked before

### Interest profile
- Topics the learner enjoys discussing
- Hobbies, work, life domains
- Cultural interests

### Consent and privacy
- Data usage consent
- Understanding of how personal stories are used
- Right to access, export, delete data
- Opt-in for optional features

## Contract review

The contract is reviewed:
- After initial diagnostic (goals realistic?)
- Every 3 months (goals changed?)
- On learner request
- When behavior suggests mismatch (e.g., consistently skipping certain modes)"""
    ),
    "44_continuous_recalibration_policy.md": (
        "Continuous Recalibration Policy",
        "How the learner model is updated based on ongoing performance evidence, not just the initial diagnostic.",
        """## Why continuous recalibration?

Language ability changes with learning. The initial diagnostic is a snapshot. Ongoing performance provides richer, more current evidence.

## Evidence sources

| Source | Evidence value | Update frequency |
|--------|---------------|-----------------|
| Lesson performance | High — direct observation | Per lesson |
| Quiz results | High — controlled condition | Per quiz |
| Review sessions | Medium — recall under schedule | Per review |
| Spontaneous production | High — naturalistic use | Per occurrence |
| Error correction patterns | Medium — indirect evidence | Per correction |

## Recalibration algorithm

Bayesian updating approach:
1. Prior: current estimate with confidence
2. Evidence: new observation with reliability weight
3. Posterior: updated estimate with adjusted confidence

Confidence increases with consistent evidence and decreases with contradictory evidence.

## Reassessment triggers

Full reassessment is triggered when:
- Confidence drops below threshold for any key dimension
- Significant time gap (3+ months with low activity)
- Learner reports feeling overplaced or underplaced
- Major change in learning context (new job, new country)
- Performance patterns strongly contradict current profile

## Handling contradictions

When new evidence contradicts current estimates:
1. Log the contradiction
2. Lower confidence in affected dimension(s)
3. Request additional evidence (specific tasks)
4. Update estimate only after sufficient contradictory evidence"""
    ),
    "45_assessment_confidence_and_evidence_model.md": (
        "Assessment Confidence and Evidence Model",
        "How the system determines confidence in its ability estimates and what constitutes sufficient evidence.",
        """## Confidence model

Every ability estimate includes a confidence level: Low, Medium, High, or Very High.

| Confidence | Meaning | Evidence required |
|------------|---------|------------------|
| Low | Preliminary estimate, may be inaccurate | 1-3 observations |
| Medium | Reasonably confident, may shift | 4-8 observations across contexts |
| High | Stable estimate, unlikely to change | 9-15 observations across multiple contexts |
| Very High | Highly reliable estimate | 15+ observations, confirmed by delayed testing |

## Evidence weighting

Not all observations are equal. Weight factors:

| Factor | Weight adjustment |
|--------|-----------------|
| Task type (production > recognition) | Production: 1.5x, Recognition: 1.0x |
| Context variety (multiple contexts > single) | Per new context: +0.2x |
| Time span (distributed > massed) | Per day apart: +0.05x |
| Spontaneity (spontaneous > rehearsed) | Spontaneous: 1.3x |
| Delayed performance (1+ week) | 2.0x |

## Minimum evidence requirements

- Lesson placement: Minimum Medium confidence in relevant dimensions
- Mastery transition: Minimum 3 observations at target level
- Level advancement: Minimum High confidence across production dimensions
- Certificate readiness: Minimum Very High confidence in all relevant dimensions

## Handling insufficient evidence

When confidence is too low for a decision:
- The system transparently explains what additional evidence is needed
- Suggests specific tasks or activities to gather evidence
- Does not make premature advancement decisions"""
    ),
    "46_learner_error_evidence_model.md": (
        "Learner Error Evidence Model",
        "Structured tracking of learner errors for remediation, SRS, and profile refinement.",
        """## Purpose

To systematically track, categorize, and act on learner errors. Errors are valuable data points for personalization, not just failures to be corrected.

## Error type taxonomy

### Grammatical errors
- Article misuse
- Tense/aspect errors
- Agreement errors
- Word order
- Preposition errors
- Pronoun errors

### Lexical errors
- Wrong word choice
- False cognate
- Collocation error
- Overgeneralization

### Phonological errors
- Segment substitution
- Stress shift
- Intonation pattern

### Pragmatic errors
- Register mismatch
- Inappropriate directness
- Speech act error

### Discourse errors
- Coherence breakdown
- Reference ambiguity
- Missing discourse markers

## Error tracking per event

Each recorded error includes:
- Error type (from taxonomy)
- Target form (correct version)
- Learner form (what was produced)
- Context (the utterance/sentence)
- L1 influence flag
- Frequency count
- Pattern detection (isolated error or systematic?)
- Remediation attempts and outcomes

## Error to mastery link

Persistent errors indicate items that are introduced but not mastered. The error evidence model feeds into:
1. Mastery engine — errors block mastery advancement
2. SRS — error items scheduled for focused review
3. Lesson selection — repair lessons built around error patterns
4. Scaffolding level — errors may indicate need for more support

## Privacy consideration

Error data is personally identifiable (reveals specific learner weaknesses). Protected accordingly. Aggregate error data (anonymized) used for improving LKB and pedagogy."""
    )
}

# Generate all documents
def generate(section, data):
    in_scope, out_scope, core_decisions, acceptance = IN_OUT[section]
    base_path = os.path.join(BASE, section)
    os.makedirs(base_path, exist_ok=True)

    for filename, (title, purpose, content) in data.items():
        doc = f"""# {title}

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

{purpose}

## In scope

{in_scope}

## Out of scope

{out_scope}

## Core decisions

{core_decisions}

## Acceptance criteria

{acceptance}

---

{content}
"""
        path = os.path.join(base_path, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(doc)
        print(f"Created: {section}/{filename}")

# Run methodology first
print("=== Generating Methodology ===")
generate("methodology", CONTENT["methodology"])

print("=== Generating Diagnostics ===")
generate("diagnostics", CONTENT["diagnostics"])

print("\nDone! This script generates methodology and diagnostics only.")
print("Run with additional content sections for more documents.")
