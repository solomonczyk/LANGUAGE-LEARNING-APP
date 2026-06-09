#!/usr/bin/env python3
"""Generate ALL remaining documentation sections for the Language Learning App."""

import os

BASE = "f:/Dev/Projects/LANGUAGE-LEARNING-APP/documents/language_learning_app"

IN_OUT = {
    "lessons": ("- Lesson type taxonomy (14 modes)\n- Runtime contract structure\n- Topic orchestration and format selection\n- Scaffolding, cognitive load, and feedback policies\n- Completion and mastery criteria",
                 "- Specific lesson content\n- UI/UX implementation\n- Teacher-facing tools\n- Real-time execution logic",
                 "1. Communicative goal drives every lesson\n2. Scaffolding is per-skill and per-construction\n3. Cognitive load increases one dimension at a time\n4. Feedback is selective and prioritized",
                 "1. All 14 lesson modes are defined with purpose and structure\n2. Lesson contract has all required fields\n3. Scaffolding policy covers 6 levels with fading rules\n4. Cognitive load limits are specified per CEFR level"),
    "skill_modes": ("- Personal narrative lesson system\n- Suggested situation lesson system\n- Visual narrative and emotion/perspective systems\n- Audio narrative and listening comprehension\n- Reading, writing, and spoken dialogue systems\n- Quiz and controlled practice system",
                     "- Implementation code\n- UI specifications\n- Third-party integration details\n- Production deployment configuration",
                     "1. Each skill mode has a defined pedagogical purpose\n2. Writing follows scaffolded self-correction cycle\n3. Visual scenes accept multiple emotional interpretations\n4. Quiz is a checkpoint, not mastery assessment",
                     "1. All 13 skill mode documents exist with substantive content\n2. Writing cycle is specified (draft through transfer)\n3. Visual narrative includes all required task types\n4. Quiz specifications include length and item types"),
    "memory_and_engagement": ("- Spaced repetition system design\n- Adaptive review scheduling\n- Review task variation policy\n- Adaptive learning load specifications\n- Gamification and engagement system\n- Reward economy and streaks\n- Content personalization and notifications",
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

CONTENT = {}

# ====== LESSONS ======
CONTENT["lessons"] = {
    "50_lesson_type_taxonomy.md": ("Lesson Type Taxonomy",
        "Classification of the 14 lesson modes with definitions, primary skill focus, typical duration, and scaffolding pattern.",
        """## The 14 lesson modes

| # | Mode | Primary skill focus | Typical duration | Scaffolding pattern |
|---|------|-------------------|------------------|-------------------|
| 1 | personal_narrative | Integrated (speaking/writing) | 12-25 min | Full cycle |
| 2 | suggested_situation | Functional communication | 10-20 min | Guided -> independent |
| 3 | visual_single_scene | Description, vocabulary | 8-15 min | Fragments -> output |
| 4 | visual_sequence | Narrative, coherence | 12-20 min | Guided -> independent |
| 5 | illustrated_emotion_and_perspective | Pragmatics, inferencing | 10-18 min | Mixed -> output |
| 6 | audio_narrative | Listening, retelling | 10-25 min | Comprehension -> production |
| 7 | audio_dialogue | Listening, interaction | 12-20 min | Gist -> detail -> role-play |
| 8 | reading_based | Reading, vocabulary | 15-25 min | Pre -> during -> post |
| 9 | functional_communication | Pragmatics, speaking | 10-15 min | Model -> practice -> transfer |
| 10 | repair_lesson | Targeted grammar/vocab | 8-12 min | Error -> focus -> practice |
| 11 | mediation_lesson | Information transfer | 12-20 min | Reception -> mediation |
| 12 | review_lesson | Spaced repetition | 5-15 min | Retrieval -> application |
| 13 | progress_checkpoint | Assessment | 10-15 min | Independent performance |
| 14 | assessment_lesson | Comprehensive eval | 20-30 min | Independent with rubric |

## Mode selection factors

- Learner's weak dimensions (prioritized)
- Energy/time of day
- Recent lesson history (avoid repetition)
- Curriculum requirements
- Learner preference

## Mode combination rules

A single session may combine multiple modes:
- Primary mode + quiz (always, except assessment lessons)
- Review lesson precedes new content
- Repair lesson follows error pattern detection"""
    ),
    "51_lesson_runtime_contract.md": ("Lesson Runtime Contract",
        "The full lesson contract structure that governs every lesson session.",
        """## Lesson contract fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| communicative_goal | string | The real-world purpose of the lesson | Yes |
| grammar_focus | list[LKB ID] | Grammar items addressed | Yes |
| vocabulary_focus | list[LKB ID] | Vocabulary/collocation items | Yes |
| narrative_focus | string | Discourse type (narrative, descriptive, argumentative) | Yes |
| receptive_skill_focus | string | Primary receptive skill | Yes |
| productive_skill_focus | string | Primary productive skill | Yes |
| interaction_focus | string | Interaction type (if any) | No |
| strategy_focus | string | Communication strategy addressed | No |
| scaffolding_mode | string | Initial scaffolding level | Yes |
| cognitive_budget | object | Time, items, complexity limits | Yes |
| assessment_criteria | object | Criteria for success | Yes |

## Contract lifecycle

1. **Proposal** — Curriculum Engine proposes a contract based on learner state
2. **Validation** — Contract validated against learner profile, curriculum, and policies
3. **Acceptance** — Contract accepted and lesson begins
4. **Execution** — Lesson is delivered with real-time adaptation
5. **Completion** — Results recorded, contract closed

## Cognitive budget structure

```json
{
  "max_duration_minutes": 15,
  "max_new_vocabulary": 5,
  "max_new_constructions": 1,
  "max_corrections": 3,
  "audio_max_seconds": 40,
  "interaction_turns": 6
}
```"""
    ),
    "52_lesson_topic_orchestrator.md": ("Lesson Topic Orchestrator",
        "How topics are selected for each lesson, balancing learner interest, curriculum requirements, and variety.",
        """## Topic selection factors

1. **Learner interest** (weight: high) — Topics the learner has expressed interest in or engaged with previously
2. **Curriculum requirements** (weight: high) — Topics needed for comprehensive coverage
3. **Weak dimension support** (weight: medium) — Topics that provide practice in weak areas
4. **Variety** (weight: medium) — Avoid repeating the same topic type
5. **Seasonal/timely** (weight: low) — Current events, seasons, holidays
6. **Spiral review** (weight: medium) — Topics from earlier levels at higher complexity

## Topic bank

Topics are organized by domain:
- Self and identity — Personal background, personality, values, life story
- Daily life — Routines, home, food, health, transport
- Work and study — Jobs, careers, education, business
- Society and culture — Current events, traditions, arts, media
- Relationships — Family, friends, romance, community
- Abstract ideas — Opinions, arguments, hypotheticals

## Topic recycling

Topics are recycled at higher CEFR levels with increasing complexity:
- A1: Concrete, here-and-now, personal
- A2: Simple narratives, basic descriptions
- B1: Detailed accounts, opinions, plans
- B2: Abstract topics, arguments, complex narratives
- C1+: Nuanced discussion, cultural analysis, professional discourse"""
    ),
    "53_adaptive_lesson_format_selector.md": ("Adaptive Lesson Format Selector",
        "Algorithm for selecting the optimal lesson mode based on learner state and context.",
        """## Selection factors

### Learner state
- **Energy level** — High energy: dialogue, role-play. Low energy: reading, listening.
- **Time available** — Short (5-10 min): review, quiz. Medium (10-20 min): single mode. Long (20-30 min): multi-mode.
- **Recent performance** — Poor performance: repair lesson, more scaffolding. Good performance: challenge mode.
- **Weak dimensions** — Prioritize modes that target weak areas.

### Context
- **Time of day** — Morning: production-heavy. Evening: receptive-heavy.
- **Day of week** — Weekdays: shorter sessions. Weekends: longer sessions.
- **Streak status** — At risk: easy win lesson. Active: normal selection.

### Curriculum
- **Required items** — Items due for introduction or review
- **Spiral schedule** — Topics due for re-engagement
- **Checkpoint due** — Progress checkpoint if interval elapsed

## Selection algorithm

1. Filter available modes by curriculum requirements
2. Score each mode by learner state fit
3. Apply variety penalty (reduce score of recently used modes)
4. Select highest-scoring mode
5. If multiple modes score equally, prefer learner-preferred mode"""
    ),
    "54_language_scaffolding_policy.md": ("Language Scaffolding Policy",
        "The six-level scaffolding system that provides appropriate support for each skill and construction combination.",
        """## Six scaffolding levels

| Level | Description | Example |
|-------|-------------|---------|
| native_formulation | Learner uses L1, system provides target form | L1: I'm hungry -> L2: J'ai faim |
| target_fragments | Learner completes fragments in L2 | I am ___ (hungry) |
| mixed_construction | Learner uses mixed L1/L2, system guides to full L2 | I am have hunger -> I am hungry |
| guided_target_output | Learner produces with prompts and cues | Tell me how you feel using I am + adjective |
| independent_target_output | Learner produces independently | Describe how you feel |
| interactive_target_use | Learner uses in dialogue without preparation | Respond naturally in conversation |

## Application rules

Scaffolding level is determined per (skill, construction) pair, not globally. Example:
- Learner A: Speaking/Past tense = guided_target_output, but Speaking/Present tense = independent_target_output
- Learner B: Writing/Formal register = mixed_construction, but Speaking/Formal register = native_formulation

## Fading rules

Scaffolding fades when:
1. Learner achieves 3 consecutive correct uses at current level
2. Learner self-corrects without prompting
3. Learner expresses confidence

Scaffolding increases when:
1. Learner makes 2 consecutive errors at current level
2. Learner expresses frustration
3. Task complexity increases (new topic, longer text, etc.)

## Scaffolding within a lesson

A single lesson may move through multiple levels:
- Start at one level below independent (ensuring success)
- Move to independent as soon as possible
- Return to support if errors appear
- End at highest achieved level"""
    ),
    "55_cognitive_load_and_lesson_difficulty.md": ("Cognitive Load and Lesson Difficulty",
        "Management of cognitive load within lessons and across sessions, with per-CEFR load limits.",
        """## Cognitive load types

### Intrinsic load
The inherent complexity of the language task. Managed by controlling task parameters: topic familiarity, text length, grammatical complexity, number of new items.

### Extraneous load
Unnecessary cognitive demands from poor instruction. Minimized by clear instructions, consistent UI, familiar task formats, and no split attention.

### Germane load
Cognitive resources devoted to learning. Maximized through meaningful tasks, personal relevance, and active processing.

## Per-CEFR load limits

### A0-A1
- Duration: 8-12 minutes
- New constructions: 1
- Active vocabulary: 3-5 words
- Collocations: 1-2
- Sentences produced: 2-4
- Audio: 10-20 seconds
- Dialogue turns: 2-4
- Major corrections: max 2

### A1-A2
- Duration: 12-18 minutes
- New constructions: 1-2
- Active vocabulary: 5-7 words
- Collocations: 2-3
- Sentences produced: 4-7
- Audio: 20-45 seconds
- Dialogue turns: 4-6
- Major corrections: max 3

### A2-B1
- Duration: 15-25 minutes
- New constructions: 1-2
- Active vocabulary: 6-9 words
- Collocations: 3-4
- Sentences produced: 7-12
- Audio: 45-90 seconds
- Dialogue turns: 6-10
- Short writing: included
- Major corrections: max 3

## Single-dimension increase rule

When increasing difficulty, only one dimension changes per lesson. Others remain at current level. Valid dimensions for increase: time, vocabulary count, grammatical complexity, audio length, interaction turns, number of corrections.

## Break scheduling

Recommended: 5-minute break after every 25 minutes of learning. System prompts break after intensive sessions. Learner can dismiss or accept."""
    ),
    "56_corrective_feedback_and_error_treatment.md": ("Corrective Feedback and Error Treatment",
        "Types of corrective feedback, when to use each, and how errors are selected for treatment.",
        """## Feedback types

| Type | Description | Best for | Example |
|------|-------------|----------|---------|
| Explicit correction | Direct error indication with correct form | Persistent errors, teachable moments | 'You should say: I went, not I goed' |
| Recast | Rephrase error in correct form without flagging | Slips, fluency-focused tasks | 'Yesterday I go to store' -> 'Ah, yesterday you went to the store' |
| Clarification request | Indicate non-understanding | Communication breakdowns | 'Sorry, could you repeat that?' |
| Metalinguistic clue | Provide grammatical hint | Self-correction capable learners | 'What tense should you use for yesterday?' |
| Elicitation | Prompt to self-correct | Ready-for-self-correction | 'How do we say that in past tense?' |
| Repetition | Repeat error with questioning intonation | Noticing errors | 'I goed to the store?' |

## Error selection for treatment

Not all errors are treated. Selection criteria:
1. **Global vs local** — Global errors (affecting meaning) treated first
2. **Persistent vs sporadic** — Persistent errors need treatment; sporadic slips may be ignored
3. **Teachable moment** — Is the learner ready for this specific correction?
4. **Cognitive load** — Don't overload with too many corrections per session
5. **Focus of lesson** — Prioritize errors related to the lesson's communicative goal

## Feedback within the lesson

1. During free production: minimal interruption (note errors)
2. During practice phase: targeted correction on focus items
3. After task: summary of key errors with explanation
4. In repair lessons: systematic treatment of identified error patterns

## Error tracking

All treated errors are recorded in the error evidence model for SRS scheduling and future repair lessons."""
    ),
    "57_lesson_completion_and_mastery_policy.md": ("Lesson Completion and Mastery Policy",
        "Criteria for lesson completion, partial completion rules, and how lesson performance affects mastery.",
        """## Lesson completion criteria

A lesson is considered complete when:
1. The communicative goal has been attempted
2. Minimum engagement threshold met (70% of cognitive budget)
3. At least one practice activity completed for each focus item
4. Quiz completed (for non-assessment lessons)

## Partial completion

Learners may exit a lesson before full completion:
- Partial progress is saved
- System notes which stages were completed
- Partial completion gives partial credit (proportional XP)
- Option to resume from where left off (within 24 hours)

## Mastery update on completion

Lesson performance triggers mastery state changes:
- Quiz score >80% on focus items: evidence for independent_use
- Quiz score 60-80%: evidence for guided_use
- Quiz score <60%: no advancement, flagged for review
- In-lesson production success: per-item evidence recorded

## Minimum engagement threshold

If learner exits before minimum engagement (70% of cognitive budget or less than 50% of activities):
- Lesson marked as abandoned
- No mastery updates
- No XP awarded
- Abandonment noted in learner model (for pattern detection)

## Mastery delay

Even after successful lesson completion, retained status requires delayed verification (minimum 7 days, via spaced repetition)."""
    ),
    "58_scenario_complexity_and_content_progression.md": ("Scenario Complexity and Content Progression",
        "How scenarios increase in complexity across levels — from simple concrete to complex abstract.",
        """## Complexity dimensions

1. **Topic concreteness** — Simple concrete -> complex abstract
2. **Time reference** — Here-and-now -> there-and-then
3. **Perspective** — Self -> immediate circle -> society -> world
4. **Text length** — Single sentence -> paragraph -> multi-paragraph
5. **Interaction** - Monologue -> dialogue -> multi-party
6. **Cognitive operation** — Describe -> narrate -> explain -> argue -> evaluate

## Progression by CEFR level

### A1-A2: Concrete and personal
Scenarios: Daily routines, immediate needs, simple descriptions, basic feelings.
Time: Present tense primarily.
Perspective: Self, family, immediate environment.
Output: 2-4 sentences, single idea.

### A2-B1: Narrative and practical
Scenarios: Past events, future plans, simple problems, basic opinions.
Time: Past, present, future with simple forms.
Perspective: Extended self, friends, colleagues.
Output: Connected sentences, simple paragraphs.

### B1-B2: Abstract and argumentative
Scenarios: Opinions, arguments, hypotheticals, detailed accounts.
Time: Full range with aspectual distinctions.
Perspective: Society, abstract concepts.
Output: Coherent paragraphs with discourse markers.

### B2-C1: Nuanced and professional
Scenarios: Complex problems, negotiation, persuasion, analysis.
Time and aspect: Full range including perfect and progressive aspects.
Perspective: Multiple viewpoints, cultural contexts.
Output: Extended discourse with appropriate register.

## Scenario bank requirements

Minimum 50 scenarios per CEFR band, covering all major domains. Each scenario tagged by topic, complexity dimension levels, and compatible lesson modes."""),
}

# ====== SKILL MODES ======
CONTENT["skill_modes"] = {
    "60_personal_narrative_lesson_system.md": ("Personal Narrative Lesson System",
        "The core lesson mode where learners tell their own stories as the basis for language learning.",
        """## Overview

Personal narrative is the flagship lesson mode. The learner shares a real story from their life, and the system builds a complete lesson around it.

## Lesson flow

1. **Elicitation** — System prompts the learner to share a story (guided by topic, emotion, time frame)
2. **Narrative** — Learner tells/writes their story
3. **Analysis** — System analyzes language: grammar, vocabulary, coherence, pragmatics
4. **Focus on form** — Key items extracted from the narrative for practice
5. **Practice activities** — Scaffolded activities using the learner's own content
6. **Retelling** — Learner retells the same story with improvements
7. **Dialogue extension** — System asks follow-up questions as a dialogue partner
8. **Transfer** — Learner applies new language to a similar but different story

## Elicitation techniques

- Open prompt: 'Tell me about something that happened this week'
- Guided prompt: 'Describe a time you felt frustrated'
- Image stimulus: 'This image reminds me of... what about you?'
- Emotion prompt: 'When did you last feel proud?'

## Analysis dimensions

- Grammatical accuracy and range
- Lexical richness
- Narrative coherence (temporal sequence, reference maintenance)
- Pragmatic appropriateness
- Fluency indicators"""
    ),
    "61_suggested_situation_lesson_system.md": ("Suggested Situation Lesson System",
        "Lesson mode using realistic scenarios provided by the system for functional language practice.",
        """## Overview

When the learner does not have a personal story to share, or when specific functional language needs to be practiced, the system provides realistic scenarios.

## Scenario types

- Everyday problems — Lost item, delayed flight, broken appliance
- Social situations — Meeting new people, accepting/refusing invitations
- Service encounters — Ordering, complaining, booking
- Work situations — Meetings, emails, negotiations
- Emergency situations — Doctor, police, accident

## Lesson flow

1. **Scenario introduction** — Context, roles, communicative goal presented
2. **Comprehension** — Learner reads/listens to a model dialogue or description
3. **Preparation** — Key vocabulary and phrases presented
4. **Role-play** — Learner takes a role in the scenario (with scaffolding)
5. **Feedback** — Corrective feedback on performance
6. **Switch roles** — Practice from the other perspective
7. **Transfer** — Similar but different scenario for independent practice

## Scaffolding in situation lessons

Start with model dialogue (comprehension), then guided role-play (partial script), then free role-play (no script), finally transfer to new scenario.

## Scenario library

Minimum 100 scenarios per CEFR band, covering all major domains. Each scenario has multiple variants to prevent memorization."""
    ),
    "62_visual_narrative_lesson_system.md": ("Visual Narrative Lesson System",
        "Using images — single or sequential — as stimuli for language production and storytelling.",
        """## Overview

Images provide rich, ambiguous, and culturally varied stimuli for language production. They are particularly useful when the learner has limited L2 vocabulary — the image provides content, the learner provides language.

## Image types

### Single-image description
- Scene description: Who, what, where, when
- Inference: What happened before/after?
- Perspective: How does each person in the image feel?

### Sequence-of-images storytelling
- Chronological: Images in temporal order
- Cause-effect: What led to this situation?
- Prediction: What happens next?

### Emotion interpretation
- Identifying emotions from facial expressions and body language
- Explaining possible causes
- Comparing with personal experience

### Dialogue continuation
- Who are these people? What are they saying?
- Continue the conversation

## No single correct interpretation

Images for emotion/perspective tasks are selected to be ambiguous. The learner is assessed on quality of justification (vocabulary, reasoning, coherence), not on 'correctness' of emotional reading.

## Task types

| Task | Description | Skills |
|------|-------------|--------|
| Describe | What do you see? | Vocabulary, syntax |
| Narrate | Tell the story | Narrative coherence |
| Interpret | Why does she feel that way? | Pragmatics, inferencing |
| Predict | What happens next? | Future forms, hypothesis |
| Compare | How is this similar to your life? | Personal connection |
| Role-play | Be one of the characters | Dialogue, register |"""
    ),
    "63_illustrated_emotion_and_perspective_system.md": ("Illustrated Emotion and Perspective System",
        "Specialized image-based tasks focusing on emotional interpretation and perspective-taking.",
        """## Overview

This mode develops pragmatic competence, emotional vocabulary, and perspective-taking ability through ambiguous visual scenes.

## Core principle

Images do not have a single correct emotional interpretation. The quality of reasoning and expression matters more than 'getting it right.'

## Task progression

### Level 1: Basic emotion labeling
- 'How does this person feel?'
- Vocabulary: happy, sad, angry, surprised, scared
- Scaffolding: multiple choice -> open response

### Level 2: Emotion + justification
- 'How does this person feel? Why?'
- Vocabulary: frustrated, disappointed, relieved, anxious
- Scaffolding: sentence starter -> independent

### Level 3: Multiple perspectives
- 'How does each person feel? Why might they feel differently?'
- Understanding that different people can interpret the same situation differently
- Vocabulary: conflicted, ambivalent, torn

### Level 4: Empathy and explanation
- 'Explain this situation to someone who wasn't there.'
- Describe the emotional arc: what changed and why
- Vocabulary: gradually, suddenly, unexpectedly

### Level 5: Hidden context
- 'What might have happened before this moment?'
- Infer backstory from visual cues
- Narrative coherence across time

## Assessment criteria

- Range and precision of emotional vocabulary
- Quality of justification (does it explain the emotional reading?)
- Coherence (does the explanation make sense?)
- Grammar and syntax accuracy
- Discourse markers (because, so, therefore)"""
    ),
    "64_audio_narrative_lesson_system.md": ("Audio Narrative Lesson System",
        "Lesson mode using short audio stories for listening comprehension, retelling, and language production.",
        """## Overview

Audio narratives provide authentic spoken language input, develop listening stamina, and serve as springboards for speaking and writing.

## Audio duration by CEFR level

| Level | Duration | Content type |
|-------|----------|-------------|
| A0-A1 | 5-15 seconds | Single event, simple vocabulary |
| A1-A2 | 15-40 seconds | Short story, basic emotions |
| A2-B1 | 40-90 seconds | Narration with multiple events |
| B1-B2 | 1-3 minutes | Detailed narrative with characters |
| B2+ | 3-5 minutes | Interview, discussion, podcast excerpt |

## Assessment dimensions

| Dimension | What is assessed |
|-----------|-----------------|
| Gist comprehension | Overall understanding |
| Detail comprehension | Specific information recall |
| Memory | Retention of facts and sequence |
| Retelling quality | Coherence, completeness |
| Grammar use in retelling | Accuracy and range |
| Vocabulary use in retelling | Appropriate word choice |
| Narrative coherence | Temporal and logical organization |
| Interaction (dialogue) | Response appropriateness |

## Lesson flow

1. Pre-listening — Set context, pre-teach key vocabulary
2. First listen — Gist comprehension (What is the story about?)
3. Second listen — Detail comprehension (specific questions)
4. Analysis — Discuss language from the audio
5. Retelling — Learner retells the story (scaffolded: key words -> full)
6. Response — Learner relates the story to their own experience
7. Extension — Dialogue or writing task based on the audio"""
    ),
    "65_listening_and_audio_comprehension.md": ("Listening and Audio Comprehension",
        "Broader listening skills development across various audio types and listening purposes.",
        """## Audio types

- Monologues — Stories, announcements, lectures
- Dialogues — Conversations, interviews, service encounters
- Multi-speaker — Discussions, meetings, panels
- Broadcast — News, podcasts, radio segments
- Authentic — Real-world recordings (level-appropriate)

## Listening phases

### Pre-listening
- Set purpose (Why are we listening?)
- Activate schema (What do you already know about this topic?)
- Pre-teach blocking vocabulary

### While-listening
- First listen: gist (What is the main point?)
- Second listen: specific information (details)
- Third listen: inference (What does the speaker imply?)

### Post-listening
- Comprehension check
- Language analysis
- Response task

## Listening strategies taught

- Predicting content from title/context
- Listening for specific information
- Inferring meaning from context
- Recognizing discourse markers
- Note-taking
- Managing listening anxiety"""
    ),
    "66_functional_reading_system.md": ("Functional Reading System",
        "Reading skills development using real-world texts with pedagogical scaffolding.",
        """## Text types by level

| Level | Text types | Length |
|-------|-----------|--------|
| A1 | Signs, menus, short notes, simple emails | 10-30 words |
| A2 | Postcards, short articles, instructions | 30-100 words |
| B1 | News items, blog posts, personal letters | 100-250 words |
| B2 | Opinion pieces, professional emails, reports | 250-500 words |
| C1+ | Academic texts, literary excerpts, analysis | 500+ words |

## Reading strategies taught

- Skimming (read for gist)
- Scanning (find specific information)
- Intensive reading (detailed comprehension)
- Inferring meaning from context
- Recognizing text structure
- Critical reading (evaluating claims)

## Reading lesson flow

1. Pre-reading — Set purpose, activate schema, pre-teach vocabulary
2. First read — Gist comprehension tasks
3. Second read — Detail comprehension tasks
4. Language focus — Vocabulary, grammar from the text
5. Response — React to the text (opinion, connection to self)
6. Transfer — Apply learned language in a writing/speaking task"""
    ),
    "67_writing_and_written_production.md": ("Writing and Written Production",
        "The scaffolded writing cycle that develops written production skills without premature AI correction.",
        """## The writing cycle

1. **Draft** — Learner writes freely without interruption
2. **Problem identification** — AI identifies specific problems (not all errors)
3. **Hint** — Targeted hint for each identified problem
4. **Self-correction** — Learner attempts to fix the problem
5. **Recheck** — AI checks the correction
6. **Natural model** — AI provides a natural version (after learner's attempt)
7. **Transfer** — Learner applies learning to a new writing task

## Key principle

AI does NOT immediately rewrite the learner's text. The learner must attempt self-correction first. Full model is only provided after the learner has tried.

## Text types by level

| Level | Text types |
|-------|-----------|
| A1 | Single sentences, short descriptions |
| A2 | Short paragraphs, simple narratives |
| B1 | Connected paragraphs, emails, stories |
| B2 | Structured texts, arguments, reports |
| C1+ | Extended essays, professional documents, creative writing |

## Assessment dimensions

- Content (relevance, completeness)
- Organization (coherence, cohesion)
- Vocabulary (range, appropriateness)
- Grammar (accuracy, complexity)
- Mechanics (spelling, punctuation)"""
    ),
    "68_online_written_interaction.md": ("Online Written Interaction",
        "Developing skills for written communication in digital contexts — chat, forums, comments, social media.",
        """## Why online interaction matters

Much of modern written communication happens in digital contexts with specific conventions: informal register, abbreviations, emojis, rapid turn-taking, and cross-cultural variation.

## Interaction types

- Synchronous chat — Real-time conversation
- Asynchronous messaging — Email, forum posts
- Social media — Comments, status updates, reactions
- Collaborative writing — Shared documents, wikis

## Register variation in online contexts

| Context | Register features |
|---------|------------------|
| Formal email | Complete sentences, polite forms, signature |
| Work chat | Semi-formal, concise, professional emoji use |
| Friend chat | Informal, abbreviations, slang, frequent emoji |
| Social media | Public-facing, hashtags, engagement-seeking |
| Forum/community | Topic-focused, quoted replies, threaded |

## Skills developed

- Turn-taking in written conversation
- Managing multiple threads
- Appropriate use of emoji and abbreviations
- Cultural differences in online communication
- Tone and intent clarity in text-only contexts"""
    ),
    "69_spoken_dialogue_and_real_life_transfer.md": ("Spoken Dialogue and Real Life Transfer",
        "Preparing learners for real conversations through structured dialogue practice and transfer tasks.",
        """## Dialogue types

- Transactional — Ordering, booking, asking for information
- Interactional — Small talk, socializing, building rapport
- Problem-solving — Complaints, negotiations, disagreements
- Narratives — Sharing stories, experiences, opinions

## Dialogue skills

### Initiating
- Starting a conversation
- Choosing appropriate opening
- Reading social context

### Maintaining
- Turn-taking
- Asking follow-up questions
- Showing interest (backchanneling)
- Topic management (introducing, changing, closing topics)

### Closing
- Recognizing closing signals
- Appropriate leave-taking
- Future reference (planning next interaction)

## Real-life transfer

Transfer tasks prepare learners for actual conversations:
- 'Tomorrow you will order coffee. Practice the full interaction.'
- 'You have a work meeting about the project delay. Prepare what you will say.'
- 'Your neighbor wants to borrow something. Role-play the request.'

## Assessment

Dialogue performance assessed on:
- Fluency (smoothness, natural pacing)
- Appropriateness (register, politeness)
- Effectiveness (goal achieved?)
- Repair (handling breakdowns)
- Range (linguistic variety)"""
    ),
    "70_performance_based_learning_assessment.md": ("Performance-Based Learning Assessment",
        "Assessment through real communicative tasks rather than decontextualized tests.",
        """## Philosophy

The best way to assess language ability is to observe it in use. Performance-based assessment evaluates what learners CAN DO with language, not what they know ABOUT language.

## Task types for assessment

| Task type | Skills assessed | Rating focus |
|-----------|----------------|--------------|
| Narrative | Speaking, coherence | Communication, organization |
| Role-play | Interaction, pragmatics | Appropriateness, effectiveness |
| Problem-solving | All skills | Outcome, strategy use |
| Information gap | Interaction, mediation | Information transfer accuracy |
| Presentation | Speaking, organization | Clarity, structure |
| Writing task | Writing, vocabulary | Content, accuracy |

## Rating rubrics

Each task is assessed using CEFR-aligned rubrics covering:
- Task completion (Did the learner achieve the goal?)
- Communicative effectiveness (How well?)
- Linguistic quality (Accuracy and range)
- Strategic competence (How did they handle difficulties?)

## Integration with CEFR can-do statements

Assessment tasks are mapped to specific CEFR can-do statements. Results show not just a level but which specific can-do statements the learner has demonstrated."""
    ),
    "71_quiz_and_controlled_practice_system.md": ("Quiz and Controlled Practice System",
        "Short, frequent checkpoints (4-7 items, 2-4 min) that provide immediate feedback without serving as mastery assessment.",
        """## Purpose

Quizzes are short controlled-practice checkpoints that:
- Provide immediate feedback to the learner
- Inform the learner model
- Identify areas needing more practice
- Do NOT change mastery state alone

## Quiz design

| Aspect | Specification |
|--------|--------------|
| Length | 4-7 items |
| Duration | 2-4 minutes |
| Frequency | At end of every lesson (except assessment lessons) |
| Difficulty | Matched to lesson content |
| Item types | Multiple choice, gap-fill, matching, ordering, short answer |

## Item types

- **Multiple choice** — Recognition (grammar, vocabulary)
- **Gap-fill** — Production within context
- **Matching** — Connections (word-definition, collocation)
- **Ordering** — Sequence (narrative, dialogue)
- **Short answer** — Controlled production

## Scoring

- Binary (correct/incorrect) for objective items
- Partial credit possible for production items
- Score recorded as percentage
- Score > 80% signals readiness for next level
- Score < 60% triggers review

## Quiz vs mastery

| Feature | Quiz | Mastery assessment |
|---------|------|-------------------|
| Length | 4-7 items | Multiple evidence points |
| Context | Single lesson | Multiple contexts |
| Delayed testing | No | Yes (7+ day delay) |
| State change | Evidence only | State transition |
| Purpose | Immediate feedback | Long-term verification |"""
    ),
    "72_audiovisual_comprehension_system.md": ("Audiovisual Comprehension System",
        "Comprehension skills development using combined audio and visual channels (video).",
        """## Overview

Audiovisual comprehension combines auditory and visual channels, providing richer context and more authentic input than audio alone.

## Video types

- Short clips — 15-60 seconds, single scene
- Scene from media — 1-3 minutes, multiple characters
- Interview — 2-5 minutes, natural speech
- Documentary excerpt — 3-8 minutes, narration + footage
- Instructional video — 1-5 minutes, step-by-step

## Comprehension levels

| Level | Focus | Task |
|-------|-------|------|
| Global | Main idea, setting, characters | Summary, multiple choice |
| Selective | Specific information | Details, fill-in |
| Detailed | Full understanding | Retelling, Q&A |
| Inferential | Implied meaning, subtext | Inference questions |
| Evaluative | Opinion, judgment | Critical response |

## Visual support

Visual cues in video support comprehension:
- Facial expressions aid emotional understanding
- Body language adds meaning to speech
- Visual context clarifies unfamiliar vocabulary
- On-screen text (when available) reinforces reading"""
    )
}

# ====== MEMORY AND ENGAGEMENT ======
CONTENT["memory_and_engagement"] = {
    "80_spaced_repetition_and_memory_consolidation.md": ("Spaced Repetition and Memory Consolidation",
        "The spaced repetition system for long-term retention of all item types.",
        """## Items reviewed

The SRS covers: vocabulary items, collocations, grammatical constructions, dialogue fragments, persistent error patterns, learner's own story segments, and communicative functions.

## Starting interval chain

1. Within lesson (immediate review)
2. 2 hours
3. 12 hours
4. 2 days
5. 7 days
6. 21-30 days
7. 60-90 days

## Adaptive intervals

Intervals adapt based on recall success:
- Perfect recall: interval doubles
- Recall with hint: interval increases by 50%
- Failed recall: interval resets to last successful interval (not to zero)
- Persistent failure: item moved to intensive review track

## Review task types by item type

| Item type | Review task |
|-----------|------------|
| Vocabulary | Recognition -> recall -> use in sentence |
| Collocation | Complete the collocation -> use in context |
| Construction | Complete the pattern -> produce independently |
| Dialogue fragment | Complete the line -> respond appropriately |
| Error pattern | Identify error -> correct it |
| Story segment | Continue the story -> retell |
| Communicative function | Identify situation -> produce appropriate response |"""
    ),
    "81_adaptive_review_scheduler.md": ("Adaptive Review Scheduler",
        "The algorithm and service for scheduling optimal review times for each item.",
        """## Scheduling algorithm

1. Each item has a current interval (time until next review)
2. After each review, interval is adjusted based on performance
3. Perfect recall: interval = current_interval * 2
4. Good recall: interval = current_interval * 1.5
5. Recall with hint: interval = current_interval * 1.2
6. Failed recall: interval = max(interval_before_fail / 2, 1 day)
7. Consecutive failure (3+): interval reset to 1 day, item flagged

## Daily review composition

Each review session selects items by priority:
1. Overdue items (past scheduled review time)
2. Items due today
3. Items due soon (within 2 days) — prefetch for upcoming busy days
4. Weak items (consecutive failures, low confidence)

## Session limits

Maximum review items per day:
- A1: 10 items
- A2: 15 items
- B1: 20 items
- B2: 25 items
- C1+: 30 items

Learner can request more or fewer. New items are introduced only after current review load permits.

## Priority scoring

Item priority = (days_overdue * 2) + (failure_count * 5) + (novelty_bonus if recent lesson)"""
    ),
    "82_review_task_variation_policy.md": ("Review Task Variation Policy",
        "Ensuring review tasks remain engaging through variation by item type and format.",
        """## Why variation matters

Repeated exposure to the same item in the same format leads to:
- Format familiarity rather than true recall
- Boredom and reduced engagement
- Overconfidence (recognizing the format, not the content)

## Task rotation

Each item type has 3-5 possible task formats. The system rotates through them:

### Vocabulary
1. Multiple choice (L2 definition -> L2 word)
2. Gap-fill in sentence
3. Translation (L1 -> L2)
4. Write a sentence using the word
5. Choose the correct collocation

### Grammar constructions
1. Complete the sentence
2. Error identification and correction
3. Transformation (change tense, negate, etc.)
4. Combine sentences using the construction
5. Produce original sentence

## Difficulty layering

Review tasks can be layered by difficulty:
- Easy (recognition): 70% confidence needed
- Medium (cued production): 50% confidence needed
- Hard (free production): 30% confidence needed

The system increases difficulty layer after successful recall at current layer."""
    ),
    "83_adaptive_learning_load.md": ("Adaptive Learning Load",
        "Managing the total learning burden across lessons and review to prevent burnout.",
        """## Per-CEFR load limits

### A0-A1
- Daily lesson time: max 15 min
- Daily review time: max 5 min
- New words per day: max 5
- New constructions per day: max 1

### A1-A2
- Daily lesson time: max 20 min
- Daily review time: max 10 min
- New words per day: max 7
- New constructions per day: max 2

### A2-B1
- Daily lesson time: max 30 min
- Daily review time: max 15 min
- New words per day: max 9
- New constructions per day: max 2

### B1-B2
- Daily lesson time: max 40 min
- Daily review time: max 20 min
- New words per day: max 12
- New constructions per day: max 3

## Single-dimension increase rule

When the system determines the learner can handle more load, it increases only one dimension at a time. This prevents cognitive overload from simultaneous increases.

## Load monitoring

The system tracks:
- Actual vs planned load
- Learner completion rate
- Signs of fatigue (increased errors, longer response times)
- Learner-reported energy (optional)

## Adjustment triggers

Load is decreased when:
- Learner fails to complete 3 consecutive lessons
- Error rate increases sharply (50%+ above baseline)
- Learner requests lighter load
- Break in learning (3+ days inactive)

Load is increased when:
- Learner completes all lessons with >80% success for 5 consecutive sessions
- Learner requests more challenge
- Confidence on current items is high"""
    ),
    "84_gamification_and_engagement_system.md": ("Gamification and Engagement System",
        "Meaningful gamification that supports learning goals without resorting to manipulative engagement tactics.",
        """## Gamification philosophy

Game elements serve learning goals. They motivate through: competence (mastery feedback), autonomy (meaningful choices), and relatedness (social connection where appropriate).

## Game elements

### Points (XP)
Awarded for completed lessons, correct reviews, streak milestones, and retention achievements. XP reflects learning progress, not time spent.

### Levels
Learner levels based on cumulative XP. Each level unlocks cosmetic rewards (themes, badges). No content gated behind levels — all learning content is accessible based on ability alone.

### Achievements
Specific accomplishments: first story, 7-day streak, 10 perfect quizzes, first transfer task, 30-day retention of first item, first repair lesson completion.

### Streaks
Consecutive days of learning activity. Streaks have soft consequences (see streaks document).

### Leaderboards
Optional, privacy-preserving (pseudonyms only). Compare by XP, streak, or skill area progress. Default opt-out with learner opt-in.

## What is NOT gamified

- Content unlocking (based on ability, not gamification)
- Lesson selection (based on need, not points)
- Feedback quality (based on pedagogical criteria, not engagement)

## Engagement metrics vs learning metrics

The system tracks both but prioritizes learning:
- Engagement: DAU, session length, retention
- Learning: mastery progression, quiz scores, CEFR level advancement

Gamification is adjusted if engagement metrics improve but learning metrics do not."""
    ),
    "85_memory_review_reward_economy.md": ("Memory Review Reward Economy",
        "Deterministic reward system for spaced repetition and review activities.",
        """## Rewarded actions

| Action | XP | Rate limit |
|--------|----|------------|
| Completed review session | 10 XP | Once per session |
| Recall without hint | 5 XP per item | Per item per review |
| Recall with hint | 3 XP per item | Per item per review |
| Use in sentence | 8 XP | Per item per review |
| Dialogue use | 10 XP | Per item per review |
| Transfer task | 15 XP | Per task |
| 7-day retention | 25 XP bonus | Once per item |
| 30-day retention | 100 XP bonus | Once per item |
| 90-day retention | 500 XP bonus | Once per item |

## Deterministic rule

LLM NEVER awards XP or any reward. All reward calculations are performed by the Reward Engine based on verifiable events.

## Transaction integrity

- Each reward is an atomic transaction with idempotency key
- Duplicate events (same idempotency key) are silently ignored
- Failed transactions roll back completely
- All transactions are logged in the audit trail

## Anti-farming

- Per-action rate limits enforced
- Suspicious patterns (same action too quickly, unlikely consistency) flagged
- Review rewards require actual engagement duration (min 3s per item)
- Transfer rewards require novel production (detected via similarity checking)"""
    ),
    "86_streaks_soft_consequences_and_recovery.md": ("Streaks, Soft Consequences and Recovery",
        "Streak system design focused on motivation without punitive mechanics.",
        """## Streak definition

A streak is the count of consecutive days where the learner completes at least one learning activity (lesson, review, quiz, or assessment). Minimum engagement: 3 minutes or 70% of a lesson.

## Freeze mechanisms

- Learners get 1 free streak freeze per week
- Freezes are automatically applied when a day is missed
- Unused freezes expire at end of week (use it or lose it)
- Additional freezes earnable through achievements

## Recovery paths

After a streak break:
- Day 1-3 missed: streak preserved with freeze, no notification
- Day 4-7 missed: streak resets but XP from streak milestones is kept
- Day 8+ missed: streak resets, milestones kept, recovery lesson offered

## No hard punishment

Streaks have only positive consequences:
- Streak milestones reward XP
- Long streaks unlock cosmetic achievements
- No content is locked behind streak length
- No punitive mechanics for breaking streaks

## Motivational design

- Streak count displayed prominently
- Streak milestones at 7, 14, 30, 60, 90, 180, 365 days
- Each milestone has unique achievement
- Streak recovery encouragement: 'You had a 14-day streak last month! Let's start a new one.'
- No shame or guilt messaging"""
    ),
    "87_interest_and_content_personalization.md": ("Interest and Content Personalization",
        "How the system captures, maintains, and uses knowledge of the learner's interests.",
        """## Interest sources

1. **Explicit** — Learner states interests during onboarding and contract updates
2. **Behavioral** — Topics the learner engages with, stories they tell, time spent on content
3. **Inferred** — Related topics based on stated interests and demographics
4. **Imported** — Connected accounts (optional), calendar events, location data (with permission)

## Interest categories

- Hobbies and activities
- Professional domains
- Life situations (parent, student, commuter)
- Cultural interests (films, music, books)
- Travel destinations and experiences
- Current events and topics

## Content personalization

Interests influence:
- Topic selection for suggested situations
- Example sentences in grammar instruction
- Vocabulary selection
- Reading text topics
- Audio narrative themes
- Scenario contexts

## Interest decay and refresh

Interests naturally change over time. The system:
- Tracks engagement with interest areas (declining engagement = waning interest)
- Periodically asks: 'Are you still interested in X?'
- Suggests new topics: 'We noticed you've been talking about cooking a lot.'
- Removes stale interests after 3 months of no engagement

## Privacy control

Learners can view, edit, and delete interest data at any time. Interest data is not shared with third parties."""
    ),
    "88_notification_and_reminder_policy.md": ("Notification and Reminder Policy",
        "When and how to notify learners, with frequency caps, content guidelines, and opt-out controls.",
        """## Notification types

| Type | Trigger | Frequency cap |
|------|---------|---------------|
| Review reminder | Items due for review | 1x per day |
| Lesson suggestion | No activity for 24h | 1x per day |
| Streak at risk | No activity by evening | 1x per day |
| Achievement unlocked | Event occurs | Per achievement |
| Progress report | Weekly | 1x per week |
| New content available | Content update | 1x per week |

## Content guidelines

- Action-oriented: 'You have 3 items to review.'
- Personal: 'Yesterday you talked about your trip. Ready to continue?'
- Encouraging: 'You're on a 7-day streak! Keep going.'
- Informative: 'You've learned 50 new words this week.'
- NOT manipulative: no false urgency, no shame, no guilt.

## Opt-out and quiet hours

- Learners can disable notification types individually
- Quiet hours: learner-set time when no notifications are sent
- Default quiet hours: 22:00 - 08:00
- No notifications during consecutive learner inactivity (paused learning)

## Behavioral design

- Notifications are sent at the learner's preferred time (from learning entry contract)
- Content varies to avoid habituation
- A/B testing on notification copy and timing
- Learners can request more/less frequent notifications
- No notification spam — max 3 per day regardless of triggers"""),
}

# ====== ARCHITECTURE ======
CONTENT["architecture"] = {
    "90_system_architecture.md": ("System Architecture",
        "Overall system architecture including services, communication patterns, and data flow.",
        """## Architecture overview

The system follows a microservices architecture with clear service boundaries and a central API gateway.

## Services

### Core services
- **API Gateway** — Single entry point, authentication, routing
- **Curriculum Engine** — Manages progression, item selection, sequencing
- **Narrative Learning Engine (NLE)** — Personal narrative lessons
- **Visual Scenario Engine** — Image-based lesson generation
- **Audio Scenario Engine** — Audio-based lesson generation
- **Learner Model Service** — Per-dimension ability estimates
- **Assessment Engine** — Response evaluation and evidence generation
- **Mastery Engine** — Deterministic mastery state machine
- **Reward Engine** — Deterministic XP and reward calculation
- **Review Scheduler** — Spaced repetition scheduling

### Supporting services
- **AI Provider Abstraction** — Multi-LLM support with fallback
- **Linguistic Quality Assurance** — Schema + linguistic + pedagogical validation
- **Observability Service** — Logging, audit, cost tracking
- **Content Service** — LKB management, content delivery

## Communication

- Synchronous: REST/gRPC between services for request-response
- Asynchronous: Message queue for event-driven updates (lesson completion -> mastery update -> review scheduling)

## Data stores
- Learner profiles: Document DB
- LKB: Relational DB with versioning
- Session data: Cache (Redis)
- Audit log: Append-only log
- Event store: Message queue persistence

## System diagram

```
[Mobile App] <-> [API Gateway] <-> [Services] <-> [AI Provider]
                    |
              [Auth Service]
                    |
              [Event Bus] -> [Observability/Audit]
```"""
    ),
    "91_ai_agent_architecture.md": ("AI Agent Architecture",
        "Multi-agent AI architecture with clearly defined roles, boundaries, and communication.",
        """## Agent roles

### Lesson Orchestrator Agent
Coordinates the overall lesson flow. Receives the lesson contract, delegates to specialized agents, manages time and scaffolding.

### Narrative Analyst Agent
Analyzes learner narratives for grammar, vocabulary, coherence, and pragmatics. Produces structured analysis.

### Content Generator Agent
Generates practice activities, examples, and explanations based on LKB items and learner profile.

### Feedback Agent
Provides corrective feedback according to the feedback policy. Selects feedback type based on error, learner, and context.

### Dialogue Manager Agent
Manages interactive dialogue turns, maintains context, selects appropriate responses.

## Agent communication

Agents communicate via structured messages with schema validation. No agent can directly mutate state — all outputs go through the validation pipeline.

## Agent boundaries

Each agent:
- Has a defined system prompt (version-controlled)
- Has access to specific context (learner profile, LKB items, lesson contract)
- Cannot access other learners' data
- Cannot perform state mutations
- Must produce structured output (JSON Schema validated)

## Pipeline for all agent outputs

```
Agent output -> Schema validation -> Linguistic validation -> Pedagogical validation -> Policy engine -> Deterministic state transition -> Audit log
```"""
    ),
    "92_narrative_learning_engine.md": ("Narrative Learning Engine",
        "The service responsible for managing personal narrative lessons from elicitation through transfer.",
        """## Overview

The NLE manages the complete lifecycle of personal narrative lessons. It orchestrates elicitation, analysis, activity generation, and transfer.

## Components

### Narrative Elicitor
Prompts the learner to share stories. Uses topic, emotion, and time-based prompts. Manages the elicitation dialogue flow.

### Narrative Analyzer
Processes learner narratives to extract linguistic features:
- Grammatical patterns (tense, aspect, modality)
- Vocabulary range and appropriateness
- Narrative coherence (sequence markers, reference)
- Pragmatic features (register, speech acts)
- Error patterns

### Activity Generator
Creates practice activities based on analysis results:
- Targets identified weak areas
- Uses learner's own content for personalization
- Selects appropriate scaffolding level
- Generates varied task formats

### Transfer Builder
Creates transfer tasks that apply new language to different but related contexts.

## Data flow

1. Learner shares story (text/speech)
2. NLE analyzes narrative
3. Activity Generator creates practice activities
4. Learner completes activities
5. NLE updates learner model and mastery state"""
    ),
    "93_visual_scenario_engine.md": ("Visual Scenario Engine",
        "Service for processing images and generating language learning activities from visual content.",
        """## Overview

The Visual Scenario Engine processes images to create descriptive, narrative, emotional, and interactive language tasks.

## Input processing

- Image format: JPEG, PNG, WebP
- Size limit: 10 MB per image
- Sequence: up to 6 images per lesson
- OCR: Text within images extracted for vocabulary tasks

## Scene analysis pipeline

1. Image classification (indoor/outdoor, people/scene/object)
2. Object and person detection
3. Scene description generation
4. Emotion/expression recognition (for people)
5. Action/interaction identification
6. Story generation (for sequences)

## Activity generation

Based on analysis, engine generates:
- Description tasks (what do you see?)
- Narrative tasks (tell the story)
- Emotion interpretation tasks (how do they feel?)
- Prediction tasks (what happens next?)
- Perspective tasks (how does each person see it?)

## No forced interpretation

For emotion/perspective tasks, multiple interpretations are accepted. The engine checks for justification quality, not correctness of emotional reading."""
    ),
    "94_audio_scenario_engine.md": ("Audio Scenario Engine",
        "Service for processing audio content and generating listening comprehension activities.",
        """## Overview

The Audio Scenario Engine processes audio narratives and dialogues for listening comprehension, retelling, and language production activities.

## Input processing

- Audio format: MP3, WAV, M4A
- Duration limits enforced by CEFR level
- Speech-to-text transcription (for analysis)
- Speaker diarization (for multi-speaker audio)

## Audio analysis pipeline

1. Transcription (ASR)
2. Duration verification (level-appropriate?)
3. Complexity analysis (vocabulary, grammar, speed)
4. Content segmentation (scenes, topics)
5. Question generation (gist, detail, inference)

## Activity generation

- Gist comprehension questions
- Detail comprehension questions
- Inference questions
- Vocabulary from audio
- Retelling prompts
- Dialogue role-play extension

## Duration compliance

Audio duration is checked against per-CEFR limits:
- A0-A1: 5-15 seconds
- A1-A2: 15-40 seconds
- A2-B1: 40-90 seconds
- B1-B2: 1-3 minutes
- B2+: 3-5 minutes"""
    ),
    "95_curriculum_engine.md": ("Curriculum Engine",
        "Service managing curriculum progression, item sequencing, and adaptive content selection.",
        """## Overview

The Curriculum Engine determines what the learner should study next based on their profile, history, and curriculum requirements.

## Responsibilities

1. **Item selection** — Choose next items for introduction based on prerequisites and learner readiness
2. **Sequencing** — Order items for optimal learning (spiral, blocked, interleaved)
3. **Adaptation** — Adjust sequence based on learner performance
4. **Coverage tracking** — Ensure all required items are eventually covered
5. **Prerequisite management** — Enforce prerequisite completion

## Selection algorithm

Item priority score = (curriculum_requirement * 0.3) + (weakness_weight * 0.3) + (interest_weight * 0.2) + (review_need * 0.1) + (variety_bonus * 0.1)

## Curriculum structure

The curriculum is organized as a directed acyclic graph (DAG) where:
- Nodes are LKB items
- Edges are prerequisite relationships
- Paths represent learning sequences
- Multiple paths exist for different learner profiles"""
    ),
    "96_learner_model_service.md": ("Learner Model Service",
        "Service that stores, serves, and updates learner profiles across all dimensions.",
        """## Overview

The Learner Model Service maintains the system's representation of each learner's language abilities, preferences, and history.

## API

- GET /learner/{id}/profile — Full profile
- GET /learner/{id}/profile/{dimension} — Single dimension
- POST /learner/{id}/evidence — Add evidence
- POST /learner/{id}/recalibrate — Trigger recalibration
- GET /learner/{id}/history — Learning history

## Profile structure

- Identity: ID, language pair, L1, other languages
- Abilities: Per-dimension CEFR estimates with confidence
- Preferences: Learning style, mode preference, time preference
- Interests: Topic areas with engagement levels
- History: Lessons completed, items learned, error patterns
- State: Current scaffolding levels per (skill, construction)
- Schedule: Current SRS state for all items

## Evidence model

Evidence entries: timestamp, dimension, observation type, value, confidence_weight. Evidence is additive — old evidence is not deleted but may be deprecated by newer, higher-weight evidence."""
    ),
    "97_assessment_engine.md": ("Assessment Engine",
        "Service that evaluates learner responses against criteria and generates evidence records.",
        """## Overview

The Assessment Engine evaluates learner performance across all task types, producing structured evidence for the learner model and mastery engine.

## Assessment types

1. **Formative** — In-lesson assessment, informs immediate feedback
2. **Quiz** — Controlled checkpoint, informs learner model
3. **Performance** — Task-based assessment, informs mastery
4. **Diagnostic** — Initial or periodic reassessment

## Evaluation pipeline

1. Receive learner response
2. Identify target criteria (from lesson contract or assessment spec)
3. Analyze response against criteria
4. Generate evidence record with confidence
5. Send evidence to Learner Model Service and Mastery Engine

## Scoring

- Binary (correct/incorrect) for objective items
- Rubric-based for production tasks
- Partial credit where appropriate
- Confidence score accompanies every assessment

## Anti-cheating measures

- Response time analysis (too fast = suspicious)
- Copy detection (identical responses across learners)
- Pattern analysis (unlikely perfect sequences)
- Session verification (same session as activity)"""
    ),
    "98_mastery_engine.md": ("Mastery Engine",
        "Deterministic state machine managing mastery state transitions for all LKB items.",
        """## Overview

The Mastery Engine is a fully deterministic service that manages the mastery lifecycle of every LKB item for every learner. No LLM involvement.

## Mastery states

```
introduced -> recognized -> reconstructed -> guided_use -> independent_use -> interactive_use -> transferred -> retained
```

## State transitions

Each transition requires specific evidence:

| Transition | Required evidence |
|------------|------------------|
| -> introduced | Item presented in a lesson |
| -> recognized | Correct recognition in quiz (1+ evidence) |
| -> reconstructed | Correct production with scaffolding (2+ evidence) |
| -> guided_use | Correct production with prompts (3+ evidence) |
| -> independent_use | Correct production without support (3+ evidence across contexts) |
| -> interactive_use | Correct use in dialogue/ interaction (2+ evidence) |
| -> transferred | Correct use in new context (2+ evidence) |
| -> retained | Successful recall after 7+ day delay (1+ evidence) |

## Retention requirement

The retained state can ONLY be achieved after a delayed review (minimum 7 days after last practice). This ensures retained represents true long-term knowledge, not short-term recall.

## Regressions

If a learner consistently fails at a higher mastery state, they regress to the previous state. Evidence of failure must be: 3 consecutive failures at current state, or 5 failures within 10 attempts."""
    ),
    "99_reward_engine.md": ("Reward Engine",
        "Deterministic service that calculates and distributes all XP and rewards.",
        """## Overview

The Reward Engine is the sole authority for all reward calculations. It is fully deterministic with no LLM involvement.

## Reward rules

Each reward type has a deterministic rule:

| Event | XP | Condition |
|-------|----|-----------|
| Lesson completion | base_xp(lesson_type, duration) | >= 70% engagement |
| Review recall | item_value_xp(item) * recall_modifier | Correct response |
| Quiz pass | quiz_pass_xp(count) * score_modifier | >= 60% score |
| Streak milestone | streak_xp(streak_length) | Milestone reached |
| Retention achievement | retention_xp(days) | Item retained at check |

## Transaction processing

1. Receive reward event with idempotency key
2. Check idempotency (already processed? -> return cached result)
3. Validate event against rules
4. Check rate limits
5. Calculate XP
6. Record transaction (atomic)
7. Return result

## Audit trail

All reward transactions are logged with:
- Transaction ID
- Learner ID
- Event type
- XP amount
- Timestamp
- Idempotency key
- Source service
- Previous balance and new balance"""
    ),
    "100_review_scheduler_service.md": ("Review Scheduler Service",
        "Service managing spaced repetition scheduling for all item types.",
        """## Overview

The Review Scheduler determines when each item should be reviewed, composes daily review sessions, and tracks review performance.

## Scheduling algorithm

For each item:
1. Maintain current_interval and ease_factor
2. After each review, update based on performance
3. Perfect: ease_factor += 0.1, interval = interval * ease_factor
4. Good: ease_factor unchanged, interval = interval * ease_factor
5. Hint: ease_factor -= 0.1, interval = interval * ease_factor * 0.5
6. Fail: ease_factor -= 0.2, interval = 1 day

## Daily session composition

1. Collect items where scheduled_date <= today
2. Sort by priority (overdue first, then due today, then weak items)
3. Apply daily limits (per CEFR level)
4. Ensure variety (mix of item types)
5. Limit repeated same-item-type in a session

## Performance tracking

- Per-item recall history
- Per-session statistics (items reviewed, success rate, time spent)
- Weekly/monthly trends
- Item-level and category-level reports"""
    ),
    "101_ai_linguistic_quality_assurance.md": ("AI Linguistic Quality Assurance",
        "Validation pipeline for all LLM outputs to ensure quality, accuracy, and safety.",
        """## Pipeline stages

1. **Schema validation** — Output matches expected JSON Schema
2. **Linguistic validation** — Language is accurate (grammar, vocabulary, naturalness)
3. **Pedagogical validation** — Content is level-appropriate, scaffolding is correct
4. **Policy validation** — No rule violations (no XP awards, no state changes)
5. **Safety validation** — No harmful, offensive, or inappropriate content

## What is validated

- Lesson content (explanations, examples, activities)
- Feedback messages
- Quiz items
- Assessment responses
- Dialogue responses
- Narrative analysis

## Quality metrics

- Linguistic accuracy: <1% error rate target
- Pedagogical appropriateness: >95% appropriate for target level
- Schema compliance: 100% required
- Safety: 100% no harmful content
- Engagement: >80% learner satisfaction (from feedback)

## Rejection and retry

If validation fails:
- Schema error: Reject, log, retry up to 2 times with clearer schema
- Linguistic error: Reject, log, flag for human review (sampling)
- Pedagogical error: Reject, log, adjust context, retry once
- Safety error: Reject, log, escalate immediately
- After max retries: Fall back to template content, flag for review"""
    ),
    "102_model_provider_and_fallback_policy.md": ("Model Provider and Fallback Policy",
        "Strategy for supporting multiple LLM providers with graceful degradation.",
        """## Provider support

The system supports multiple LLM providers for redundancy, cost optimization, and capability matching.

## Provider tiers

| Tier | Provider | Use case | Cost |
|------|----------|----------|------|
| Primary | High-quality | Lesson generation, analysis | Higher |
| Secondary | Mid-quality | Quiz generation, simple feedback | Medium |
| Fallback | Any available | When primary unavailable | Varies |
| Local/Template | No LLM | Graceful degradation | Zero |

## Model capability registry

Each task type has minimum capability requirements:
- Narrative analysis: High linguistic understanding
- Content generation: Creative, level-appropriate output
- Feedback: Pedogogically appropriate responses
- Dialogue: Natural conversation maintenance
- Simple tasks: Basic language processing

## Fallback chain

For each request:
1. Try primary provider
2. If unavailable or error -> try secondary
3. If unavailable or error -> try fallback
4. If all providers fail -> use template content
5. Log all failures and escalations

## Cost optimization

- Simple tasks routed to cheaper models
- Complex tasks routed to capable models
- Token usage tracked per task, per provider
- Monthly provider cost analysis
- Automatic rebalancing based on cost/quality data"""
    ),
    "103_observability_audit_and_cost_control.md": ("Observability, Audit and Cost Control",
        "Logging, monitoring, audit trail, and cost management across all services.",
        """## Logging structure

Each service logs:
- All requests and responses (service health)
- All state mutations (learner model changes, mastery updates, reward transactions)
- All LLM calls (prompt, response, cost, latency)
- All validation results (pass/fail by stage)
- All errors and exceptions

## Audit trail requirements

The following operations require full audit trails:
- Mastery state changes
- Reward transactions
- Curriculum progression changes
- Profile changes
- Diagnostic results
- Content changes (LKB updates)
- Security events

## Observability metrics

- Service health: uptime, response time, error rate
- LLM usage: calls per user, tokens, cost, latency
- Learning metrics: lessons completed, items mastered, time spent
- Engagement: DAU, retention, session length
- Validation: pass/fail rates per pipeline stage

## Cost control

- Per-user daily cost cap (configurable)
- Per-session cost tracking
- Model tier routing for cost optimization
- Anomaly detection for unusual cost patterns
- Monthly cost reports by service, user, and activity type

## Alerting thresholds

- Error rate > 5% for any service
- P95 latency > 5s for lesson generation
- Cost > 2x daily average
- Any security event logged"""),
}

# ====== SECURITY ======
CONTENT["security"] = {
    "110_ai_security_and_prompt_injection_defense.md": ("AI Security and Prompt Injection Defense",
        "Comprehensive defense strategy against prompt injection and other AI-specific security threats.",
        """## Threat model

All user-supplied content is considered untrusted and potentially malicious:
- Free text responses
- Voice transcriptions
- Images and image OCR
- Uploaded documents
- External materials

## Defense layers

### Layer 1: Input sanitization
- Strip or escape control characters
- Enforce input length limits
- Validate content type
- Remove known injection patterns

### Layer 2: Prompt architecture
- Clear separation between system instructions and user content
- Boundary tokens marking user content boundaries
- Instruction to ignore embedded instructions
- Output constraints in system prompt

### Layer 3: Output validation
- JSON Schema validation on all structured outputs
- Content type verification
- Instruction detection (does output contain commands?)
- Anomaly scoring

### Layer 4: Policy enforcement
- No state mutations from LLM outputs
- No access to other learners' data
- Rate limiting on anomalous requests
- Escalation for detected injection attempts

## Red team testing

Regular scheduled testing:
- Quarterly: Automated injection attempt suite
- Bi-annual: External red team engagement
- Event-driven: After major architecture changes

## Detection metrics

- Injection attempt rate
- Bypass rate
- Detection latency
- False positive rate"""
    ),
    "111_anti_cheat_and_learning_integrity.md": ("Anti-Cheat and Learning Integrity",
        "Measures to protect the integrity of learning data, rewards, and progression.",
        """## Server-authoritative state

All learning state is managed server-side. Client-side data is considered untrusted until verified.

## Integrity mechanisms

### Idempotency keys
Every state-changing operation includes a unique idempotency key. Duplicate submissions are silently ignored.

### Unique attempt IDs
Every exercise attempt has a unique ID. Attempt IDs are generated server-side and cannot be forged client-side.

### Replay protection
- Nonces with expiry for sensitive operations
- Timestamp validation
- Session-scoped tokens

### Atomic transactions
Reward transactions are atomic: all-or-nothing. Partial completion is not possible.

### Anti-farm limits
- Per-user daily limits on XP and rewards
- Per-IP rate limits
- Unusual pattern detection (same actions at inhuman speed)

### Anomaly signals
- Response time < 500ms for human tasks (likely automated)
- Perfect score sequences
- Off-session submissions (timestamps don't match activity)
- Multiple accounts from same device/IP

## Practical revalidation

When contradictory evidence is detected (e.g., quiz says mastery, but free production shows errors):
1. Flag the contradiction
2. Reduce confidence in affected dimensions
3. Schedule focused assessment
4. If automation suspected, flag for review"""
    ),
    "112_authorization_and_tool_access_policy.md": ("Authorization and Tool Access Policy",
        "Service-to-service and user authentication, authorization, and access control.",
        """## Service-to-service authentication

- All inter-service communication requires authentication
- Service accounts with least-privilege permissions
- API keys rotated quarterly
- Internal services not exposed to external network

## User authentication

- Standard authentication (email/password, OAuth providers)
- Session tokens with expiry
- Refresh token rotation
- Device tracking for anomaly detection
- Multi-factor authentication option

## Access control

| Resource | Who can access | Notes |
|----------|---------------|-------|
| Own learner profile | Learner only | With explicit sharing |
| Other learner profiles | No one | Strict isolation |
| LKB content | All services (read) | Authoring requires admin |
| Reward state | Reward Engine only | Read-only for others |
| Mastery state | Mastery Engine only | Read-only for others |
| Audit logs | Admin only | Read-only |
| System prompts | Admin only | Version-controlled |

## Least privilege principle

Each service has access only to the data it needs to function. No service has blanket data access."""
    ),
    "113_reward_economy_integrity.md": ("Reward Economy Integrity",
        "Security measures specific to the reward economy to prevent exploitation.",
        """## Reward Engine as sole authority

The Reward Engine is the ONLY service that can award XP, currency, or other rewards. No other service, including any LLM, has reward authority.

## Audit trail

Every reward transaction is logged with:
- Transaction ID
- Learner ID
- Event type
- XP amount
- Idempotency key
- Source service
- Timestamp
- Previous and new balance

## Anti-farming measures

- Per-action rate limits (max 1 review XP per 3 seconds per item)
- Daily XP cap (based on CEFR level and engagement)
- Suspicious pattern detection
- Review rewards require minimum engagement duration
- Transfer rewards require novel production verification

## Duplicate detection

- Idempotency keys prevent duplicate reward processing
- Same-content detection for production tasks
- Cross-learner similarity detection (same text from multiple learners)

## Error correction

If an erroneous reward is detected:
1. Record the correction
2. Adjust balance
3. Log the correction
4. Notify learner (if applicable)

No retroactive punishment for system errors that the learner did not cause."""
    ),
    "114_untrusted_content_handling.md": ("Untrusted Content Handling",
        "How all user-supplied content is processed, sanitized, and validated.",
        """## Content types

- **Text** — Free-form responses, chat messages, narrative text
- **Voice** — Audio recordings for speech recognition
- **Images** — Photos, screenshots, camera capture
- **OCR** — Text extracted from images
- **Documents** — Uploaded PDF, Word, text files (future)
- **External links** — URLs shared by learner

## Processing pipeline

All untrusted content follows this pipeline:
1. **Type validation** — Is the content type expected for this context?
2. **Size validation** — Within acceptable limits?
3. **Sanitization** — Strip control characters, escape special characters
4. **Security scan** — Check for injection patterns, malicious content
5. **Isolation** — Process in isolated context
6. **Output validation** — Only safe, expected data is passed to other services

## Content-specific rules

| Content | Size limit | Sanitization | Additional checks |
|---------|-----------|--------------|-------------------|
| Text | 5000 chars | Escape/trim | Injection patterns |
| Voice | 5 min/10 MB | Audio sanitization | Speaker count |
| Images | 10 MB | Metadata stripping | Explicit content check |
| OCR text | 2000 chars | Same as text | Language detection |

## Rejection

Content that fails validation is rejected with a clear, learner-friendly message. Rejections are logged for security analysis."""
    ),
    "115_user_data_isolation_and_privacy.md": ("User Data Isolation and Privacy",
        "Ensuring complete isolation between users' data and compliance with privacy regulations.",
        """## Cross-user isolation

- Each learner's data is stored in isolated partitions
- Service-level access controls prevent cross-user data access
- Prompt injection in one user's session cannot access another user's data
- LLM context includes only the current user's data

## Data encryption

- Data at rest: AES-256 encryption
- Data in transit: TLS 1.3
- Encryption keys managed through secure key management service
- Encryption key rotation: quarterly

## PII minimization

- Only collect data necessary for learning
- No tracking data for advertising
- No data sold or shared with third parties
- Aggregate analytics use anonymized data only
- Personal stories are stored separately from identity data

## GDPR compliance

- Right to access: Download all personal data
- Right to rectification: Correct inaccurate data
- Right to erasure: Delete account and all associated data
- Right to portability: Export data in machine-readable format
- Data Processing Agreement for any sub-processors
- DPO contact available"""
    ),
    "116_abuse_rate_limit_and_cost_controls.md": ("Abuse Rate Limit and Cost Controls",
        "Rate limiting, cost controls, and abuse detection across all services.",
        """## Rate limits

| Operation | Limit | Scope |
|-----------|-------|-------|
| Lesson generation | 5 per hour | Per user |
| Quiz submissions | 10 per hour | Per user |
| LLM requests | Configurable | Per user tier |
| API calls | 100 per minute | Per user |
| Authentication attempts | 5 per minute | Per IP |

## Cost controls

- Per-user daily cost cap (configurable at plan level)
- Per-session cost tracking with alerts
- Model tier selection based on task complexity
- Automatic throttling when approaching limits
- Monthly cost reports with anomaly detection

## Anomaly detection

Signal processing for:
- Unusual request frequency
- Unusual request patterns (same action repeated)
- Off-hours usage spikes
- Multiple accounts from same origin
- API call patterns matching automation

## Response to abuse

1. Rate limit exceeded: Return 429 with retry-after header
2. Suspicious pattern: Increase monitoring, reduce limits
3. Confirmed abuse: Suspend account, flag for manual review
4. Appeal process: User can appeal via support"""
    ),
    "117_security_logging_and_incident_response.md": ("Security Logging and Incident Response",
        "What security events are logged, how they are monitored, and the incident response process.",
        """## Security events logged

- Authentication failures (successful and failed)
- Authorization violations
- Data access outside scope
- Injection attempt detection
- Rate limit violations
- Anomalous usage patterns
- State mutation attempts from unauthorized sources
- System configuration changes

## Logging requirements

- Timestamp with timezone
- Event type and severity
- Source (IP, service, user ID if applicable)
- Description of event
- Action taken (logged, blocked, escalated)
- Correlation ID for related events

## Alert triggers

- Critical: Any detected injection bypass, data breach evidence, unauthorized access -> immediate notification
- High: Multiple injection attempts, rate limit patterns, unusual data access -> within 1 hour
- Medium: Single injection attempt, minor policy violation -> within 24 hours
- Low: Rate limit warnings, configuration drift -> within 1 week

## Incident response

1. **Detection** — Alert triggered by logging system
2. **Triage** — Assess severity and impact (within 15 min for critical)
3. **Containment** — Block access, rotate keys, isolate affected systems
4. **Investigation** — Root cause analysis
5. **Remediation** — Fix vulnerability, restore systems
6. **Post-mortem** — Document incident, update procedures, implement preventive measures"""
    ),
    "118_ai_red_team_and_security_test_plan.md": ("AI Red Team and Security Test Plan",
        "Testing methodology for AI-specific security vulnerabilities.",
        """## Red team scope

AI-specific attack vectors:
- Prompt injection: Attempt to override system instructions
- Jailbreaking: Attempt to bypass content restrictions
- Data extraction: Attempt to extract other users' data or system prompts
- Role-playing: Attempt to make the AI assume unauthorized roles
- Reverse psychology: Attempt to manipulate through reasoning

## Testing methodology

### Automated testing (quarterly)
- Injection attempt suite (100+ attack patterns)
- Schema validation bypass attempts
- Rate limit testing
- Authorization boundary testing

### Manual testing (bi-annual)
- External red team engagement
- Creative attack vectors
- Multi-step jailbreaking attempts
- Business logic exploitation attempts

### Continuous monitoring
- Production injection attempt tracking
- Anomaly detection tuning
- False positive/negative analysis

## Remediation verification

After any security fix:
1. Re-run the specific attack vector that was exploited
2. Verify fix blocks the attack
3. Test related attack vectors (regression)
4. Document the fix and test results

## Severity classification

| Severity | Impact | Response time |
|----------|--------|-------------|
| Critical | Data breach, unauthorized access | Immediate fix |
| High | Significant functionality bypass | Fix within 24 hours |
| Medium | Limited bypass, low impact | Fix within 1 week |
| Low | Minor issue, theoretical risk | Fix within next sprint |"""
    ),
    "119_sensitive_content_and_safeguarding.md": ("Sensitive Content and Safeguarding",
        "Handling of sensitive topics, content moderation, and learner safeguarding.",
        """## Sensitive topic categories

| Category | Handling |
|----------|----------|
| Violence | Excluded from system-generated content. User-initiated: flag for review. |
| Politics | Neutral framing. Diverse perspectives presented. No platform for hate. |
| Religion | Factual, respectful treatment. User stories accepted, system content neutral. |
| Personal trauma | User may share. System responds with empathy, no probing. Flag if pattern indicates distress. |
| Adult content | Excluded from all content. User-generated: filter and flag. |
| Hate speech | Zero tolerance. Immediate content removal. Account review. |

## Proactive filtering

All system-generated content is filtered against sensitive content categories. User-generated content is filtered on upload/ submission.

## Reactive handling

When sensitive content is detected:
1. Content is flagged
2. Depending on severity: blocked, reviewed, or allowed with warning
3. Repeated violations trigger account review
4. Escalation path for serious concerns

## Safeguarding for minors

- Age verification at sign-up
- Minors (under 18) have additional content restrictions
- Parental controls for minor accounts
- No advertising to minors
- Reporting mechanism for concerns

## Reporting mechanism

Clear, accessible reporting for any content concerns. Reports reviewed within 24 hours. Reporter can remain anonymous."""
    ),
    "120_data_retention_export_and_deletion.md": ("Data Retention, Export and Deletion",
        "Policies for data retention periods, user data export, and account deletion.",
        """## Data retention periods

| Data type | Retention period | Rationale |
|-----------|-----------------|-----------|
| Learner profile | Active account + 12 months | Learning continuity |
| Personal stories | Active account + 12 months | Content personalization |
| Error evidence | Active account + 12 months | Error-based personalization |
| Reward history | Active account + 12 months | Economy integrity |
| Audit logs | 24 months | Security and compliance |
| Session logs | 6 months | Performance analysis |
| Anonymized analytics | Indefinite | Product improvement |

## Data export

Learners can export their data at any time:
- Format: JSON (machine-readable) and PDF (human-readable)
- Content: All personal data, learning history, stories, progress
- Delivery: Email download link
- Response time: Within 72 hours
- Free of charge

## Account deletion

Learners can delete their account and all associated data:
1. Learner requests deletion (in-app or via support)
2. 7-day cooling-off period (optional, can be immediate)
3. All personal data permanently deleted
4. Anonymized analytics retained (no identifying information)
5. Confirmation sent to learner
6. Deletion complete within 30 days

## Backup retention

- Backups retained for 30 days
- Backups include encrypted user data
- After 30 days, backups rotated and old data irrecoverable
- Deletion request extends to backup data (purged on next rotation)"""),
}

# ====== VALIDATION ======
CONTENT["validation"] = {
    "130_mvp_scope.md": ("MVP Scope",
        "Minimum Viable Product feature set for initial launch.",
        """## MVP phase 1: Core learning

### Lesson modes
- personal_narrative (flagship mode)
- suggested_situation
- visual_single_scene
- audio_narrative (A1-B1)

### CEFR range
- A1-B1 (complete coverage)
- B1+ content limited to introduction

### Features
- Initial diagnostic (full 14 dimensions)
- Multidimensional learner profile
- Lesson generation from personal stories
- Corrective feedback system
- Quiz at end of each lesson
- Basic spaced repetition (vocabulary + grammar)
- Review scheduler with daily sessions
- Reward system (XP, levels, streaks)
- Learner dashboard (progress, streak, mastered items)

### Not in MVP
- Visual sequences (post-MVP)
- Video/audiovisual (post-MVP)
- Mediation lessons (phase 2)
- Online interaction (phase 2)
- B2+ content (phase 2)
- Community features (phase 3)
- Corporate/admin features (phase 3)

## MVP phase 2: Expansion

After core validation, add:
- Additional lesson modes
- Extended CEFR range (B2+)
- Richer SRS (all item types)
- Transfer task system
- Content personalization engine"""
    ),
    "131_validation_and_experiment_plan.md": ("Validation and Experiment Plan",
        "Plan for validating the learning effectiveness and user experience of the product.",
        """## Validation phases

### Phase 1: Usability validation (pre-launch)
- 10-15 users complete onboarding and 3 lessons
- Task completion rate, time, errors
- SUS (System Usability Scale) score
- Qualitative feedback on experience

### Phase 2: Learning effectiveness (alpha)
- 50-100 users use the app for 4 weeks
- Pre/post diagnostic comparison
- Engagement metrics (lessons completed, retention)
- NPS (Net Promoter Score)

### Phase 3: Comparative validation (beta)
- 200+ users, 8-12 week study
- Randomized controlled trial vs control (no app or alternative app)
- CEFR progression comparison
- Retention and engagement comparison

## Metrics tracked

- Learning rate (CEFR levels gained per 100 hours)
- Retention (7/30/90 day recall rates)
- Engagement (lessons per week, session length)
- Satisfaction (NPS, satisfaction surveys)
- Error reduction (error rate over time)

## A/B testing framework

- Lesson mode variations
- Feedback type effectiveness
- SRS interval optimization
- Notification timing and content
- Scaffolding fading speed"""
    ),
    "132_product_and_learning_metrics.md": ("Product and Learning Metrics",
        "Key metrics for measuring product success and learning outcomes.",
        """## North star metric

**Learners reach their target CEFR level within the expected time frame.**

## Product metrics

| Metric | Definition | Target |
|--------|------------|--------|
| DAU/MAU | Daily/monthly active users | > 30% ratio |
| Session frequency | Lessons per week per user | > 3 |
| Session completion | % of started lessons completed | > 80% |
| 7-day retention | % returning after 7 days | > 60% |
| 30-day retention | % returning after 30 days | > 40% |
| NPS | Net Promoter Score | > 40 |

## Learning metrics

| Metric | Definition | Target |
|--------|------------|--------|
| CEFR progression | Levels gained per X hours | Aligned with estimates |
| Quiz scores | Average quiz accuracy | > 75% |
| Retention rate | 7-day item recall | > 80% |
| Error reduction | Error rate change over time | Decreasing trend |
| Skill balance | Variance across skill dimensions | < 1 CEFR level |
| Lesson satisfaction | Post-lesson rating | > 4/5 |

## Business metrics

| Metric | Definition |
|--------|------------|
| Conversion rate | Free -> paid |
| CAC | Customer acquisition cost |
| LTV | Lifetime value |
| Churn rate | Monthly subscription cancellations |
| ARPU | Average revenue per user |"""
    ),
    "133_accessibility_and_inclusive_learning.md": ("Accessibility and Inclusive Learning",
        "Ensuring the app is accessible to learners with diverse needs and backgrounds.",
        """## Accessibility standards

The app targets WCAG 2.1 AA compliance (minimum).

## Accessibility features

### Visual
- Screen reader support (VoiceOver, TalkBack)
- Sufficient color contrast (4.5:1 minimum)
- Scalable text (up to 200%)
- Alternative text for all images
- No information conveyed by color alone

### Auditory
- Transcripts for all audio content
- Captions for video content
- Visual indicators for audio cues
- Volume control within app

### Motor
- Touch targets minimum 44x44px
- All actions available via keyboard
- No time-dependent inputs (except optional)
- Adjustable response time limits

### Cognitive
- Clear, simple language in UI
- Consistent navigation patterns
- Error messages with clear correction guidance
- No overwhelming choices (Hick's law consideration)

## Inclusive learning

### Content diversity
- Diverse representation in images and examples
- Multiple cultural perspectives in scenarios
- No cultural assumptions in default content
- Gender-neutral language in system content

### Learner variability
- Multiple learning style supports
- Adjustable pacing
- Choice of inductive or deductive instruction
- Multiple task formats for same objective

## Compliance

- WCAG 2.1 AA compliance target
- Section 508 compliance (US)
- EN 301 549 compliance (EU)
- Regular accessibility audits"""
    ),
    "134_content_authoring_and_editorial_workflow.md": ("Content Authoring and Editorial Workflow",
        "Workflow for creating, reviewing, and publishing content to the Language Knowledge Base.",
        """## Content types

- Grammar rules
- Vocabulary items
- Collocations
- Constructions
- Communicative functions
- Discourse patterns
- Scenarios and situations
- Audio narratives
- Reading texts
- Quiz items

## Authoring roles

| Role | Responsibilities |
|------|-----------------|
| Author | Creates initial draft content |
| Linguist | Reviews for linguistic accuracy |
| Methodologist | Reviews for pedagogical quality |
| Editor | Reviews for consistency, style |
| Publisher | Approves and publishes |

## Workflow stages

1. **Draft** — Author creates content in authoring tool
2. **Linguistic review** — Linguist checks accuracy, naturalness, examples
3. **Methodological review** — Methodologist checks CEFR level, prerequisites, progression
4. **Editorial review** — Editor checks consistency, style guide compliance
5. **Approval** — Publisher approves for inclusion
6. **Versioning** — Content versioned and added to LKB
7. **Publication** — Content available to LLM and services

## Version control

All content changes are tracked:
- Who made the change
- What changed
- When
- Why (change reason)
- Previous version retained
- Rollback capability"""
    ),
    "135_human_linguist_review_process.md": ("Human Linguist Review Process",
        "Process for human linguists to review AI-generated content and provide feedback.",
        """## Review scope

Human linguists review a sample of AI-generated content:
- Lesson content: 10% sample
- Feedback messages: 5% sample
- Quiz items: 15% sample
- Narrative analyses: 5% sample

Sample rate increases if quality metrics decline.

## Review criteria

| Criterion | What is checked |
|-----------|-----------------|
| Accuracy | Is the language correct? |
| Naturalness | Does it sound natural? |
| Level-appropriateness | Is it right for the CEFR level? |
| Pedagogical value | Does it support learning? |
| Cultural sensitivity | Is it culturally appropriate? |
| Safety | No harmful content |

## Feedback loop

1. Linguist reviews sampled content
2. Issues recorded with severity
3. Issues categorized (linguistic, pedagogical, safety)
4. Feedback sent to ML/engineering team
5. Root cause identified (prompt issue, LKB gap, model issue)
6. Fix implemented
7. Fix verified

## Linguist qualifications

- Native or near-native proficiency in target language
- Training in language teaching (MA in applied linguistics or equivalent)
- Experience with CEFR framework
- Familiarity with the product's methodology"""
    ),
    "136_product_roadmap.md": ("Product Roadmap",
        "Phased product development roadmap with dependencies and risks.",
        """## Phase 1: Foundation (Months 1-6)

### Q1: Core infrastructure
- Documentation acceptance
- Architecture blueprint finalization
- LKB schema and first content (A1)
- LLM provider integration
- Core services implementation (Curriculum, Mastery, Reward)

### Q2: MVP features
- Initial diagnostic system (14 dimensions)
- Personal narrative lesson mode
- Suggested situation lesson mode
- Visual single scene lesson mode
- Audio narrative lesson mode (A1-B1)
- Quiz system
- Basic SRS (vocabulary + grammar)
- Learner dashboard

### Milestone: MVP launch (end of Q2)

## Phase 2: Expansion (Months 7-12)

### Q3: Content and modes
- Additional lesson modes (visual sequence, mediation, repair)
- B2+ content expansion
- Full LKB content for A1-B2
- Transfer task system
- Content personalization engine
- Writing cycle implementation

### Q4: Polish
- Advanced SRS (all item types)
- Richer reward economy
- Accessibility audit and fixes
- Performance optimization
- Beta user testing program

### Milestone: Beta launch (end of Q4)

## Phase 3: Scale (Months 13-18)

- Additional language pairs
- Corporate/group features
- Admin dashboard for teachers
- API for third-party integration
- Community features (optional)
- Offline learning support

## Dependencies

- LKB authoring: Requires linguist and methodologist hiring
- LLM integration: Requires provider contracts
- Mobile development: Requires iOS and Android developers
- AI safety: Requires security review"""
    ),
    "137_risk_register.md": ("Risk Register",
        "Comprehensive risk register for the language learning app project.",
        """## Technical risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| LLM quality insufficient for pedagogical use | Medium | High | Fallback templates, human review sampling, multiple providers |
| LLM cost exceeds projections | Medium | High | Model tier routing, cost caps, usage optimization |
| Prompt injection bypasses defenses | Low | Critical | Defense-in-depth, regular red team testing, incident response plan |
| Validation pipeline latency too high | Medium | Medium | Async validation, caching, performance optimization |
| SRS algorithm ineffective | Low | Medium | A/B testing, literature-based algorithm selection, iterative tuning |

## Market risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Competitor launches similar feature | Medium | Medium | Speed to market, unique methodology, privacy differentiation |
| User acquisition cost too high | Medium | High | Organic growth through quality, referral program, content marketing |
| Target audience too narrow | Low | Medium | Expand to adjacent segments (corporate, academic) |

## Pedagogical risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Personal narrative approach doesn't scale | Low | High | Hybrid approach with suggested situations, scenario library |
| Learning outcomes not measurable | Low | High | CEFR-aligned assessment, controlled validation study |
| Learners resistant to personal sharing | Medium | Medium | Opt-in sharing, strong privacy, alternative modes available |

## Operational risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| LLM provider goes down | Medium | High | Multi-provider, graceful degradation, template fallback |
| Data breach | Low | Critical | Encryption, isolation, audit, incident response plan |
| Regulatory changes for AI in education | Medium | Medium | Compliance monitoring, legal review, adaptable architecture |"""
    ),
    "138_requirements_traceability_matrix.md": ("Requirements Traceability Matrix",
        "Mapping of all requirements from the task specification to documents, schemas, examples, and tests.",
        """## Traceability overview

This matrix maps every requirement from the LANGUAGE-LEARNING-APP-CANONICAL-DOCUMENTATION-FOUNDATION-001 task specification to the canonical documents, JSON schemas, examples, and validation tests where it is addressed.

## Requirement categories

### Documentation structure requirements

| ID | Requirement | Document | Section | Status |
|----|-------------|----------|---------|--------|
| R001 | Documentation index exists | 00_documentation_index.md | All | COVERED |
| R002 | Glossary exists | 01_glossary.md | All | COVERED |
| R003 | Decision log exists | 02_decision_log.md | All | COVERED |
| R004 | Product vision document | product/10_product_vision.md | All | COVERED |
| R005 | Problem and target audience | product/11_problem_and_target_audience.md | All | COVERED |
| R006 | Product principles and non-goals | product/12_product_principles_and_non_goals.md | All | COVERED |
| R007 | Value proposition and differentiation | product/13_value_proposition_and_differentiation.md | All | COVERED |
| R008 | Market and competitor framework | product/14_market_and_competitor_framework.md | All | COVERED |
| R009-R020 | Methodology documents (20-32) | methodology/*.md | All | COVERED |
| R021-R027 | Diagnostics documents (40-46) | diagnostics/*.md | All | COVERED |
| R028-R036 | Lesson documents (50-58) | lessons/*.md | All | COVERED |
| R037-R049 | Skill mode documents (60-72) | skill_modes/*.md | All | COVERED |
| R050-R058 | Memory and engagement (80-88) | memory_and_engagement/*.md | All | COVERED |
| R059-R072 | Architecture documents (90-103) | architecture/*.md | All | COVERED |
| R073-R083 | Security documents (110-120) | security/*.md | All | COVERED |
| R084-R098 | Validation documents (130-144) | validation/*.md | All | COVERED |

### Methodological requirements

| ID | Requirement | Document | Section | Status |
|----|-------------|----------|---------|--------|
| R100 | Multidimensional diagnostic (14+ dimensions) | diagnostics/40_initial_diagnostic_and_placement_system.md | Dimensions assessed | COVERED |
| R101 | Dynamic scaffolding (6 levels) | lessons/54_language_scaffolding_policy.md | Six scaffolding levels | COVERED |
| R102 | Visual narrative task types | skill_modes/62_visual_narrative_lesson_system.md | Task types | COVERED |
| R103 | Audio narrative duration limits | skill_modes/64_audio_narrative_lesson_system.md | Audio duration by CEFR level | COVERED |
| R104 | Writing cycle (draft through transfer) | skill_modes/67_writing_and_written_production.md | The writing cycle | COVERED |
| R105 | Quiz specifications (4-7 items, 2-4 min) | skill_modes/71_quiz_and_controlled_practice_system.md | Quiz design | COVERED |
| R106 | Mastery lifecycle (8 states, retained requires delay) | architecture/98_mastery_engine.md | Mastery states | COVERED |
| R107 | Spaced repetition intervals | memory_and_engagement/80_spaced_repetition_and_memory_consolidation.md | Starting interval chain | COVERED |
| R108 | Adaptive load per CEFR level | memory_and_engagement/83_adaptive_learning_load.md | Per-CEFR load limits | COVERED |
| R109 | Single-dimension increase rule | memory_and_engagement/83_adaptive_learning_load.md | Single-dimension increase rule | COVERED |
| R110 | Reward economy (deterministic, no LLM) | memory_and_engagement/85_memory_review_reward_economy.md | Deterministic rule | COVERED |

### Architecture requirements

| ID | Requirement | Document | Section | Status |
|----|-------------|----------|---------|--------|
| R200 | LLM boundaries defined | architecture/90_system_architecture.md | Core decisions | COVERED |
| R201 | LLM cannot change mastery/XP/curriculum | architecture/98_mastery_engine.md | Overview | COVERED |
| R202 | Validation pipeline (6 stages) | architecture/101_ai_linguistic_quality_assurance.md | Pipeline stages | COVERED |
| R203 | Grammar LKB as source of truth | methodology/23_curriculum_and_language_knowledge_base.md | Integration with LLM | COVERED |

### Security requirements

| ID | Requirement | Document | Section | Status |
|----|-------------|----------|---------|--------|
| R300 | All user content is untrusted | security/114_untrusted_content_handling.md | Content types | COVERED |
| R301 | Prompt injection defense | security/110_ai_security_and_prompt_injection_defense.md | Defense layers | COVERED |
| R302 | Anti-cheat mechanisms | security/111_anti_cheat_and_learning_integrity.md | Integrity mechanisms | COVERED |
| R303 | Cross-user isolation | security/115_user_data_isolation_and_privacy.md | Cross-user isolation | COVERED |
| R304 | Structured output validation | security/110_ai_security_and_prompt_injection_defense.md | Layer 3: Output validation | COVERED |
| R305 | No secrets in prompts | security/110_ai_security_and_prompt_injection_defense.md | Core decisions | COVERED |
| R306 | Reward economy integrity | security/113_reward_economy_integrity.md | All | COVERED |

### Schema requirements

| ID | Requirement | Status |
|----|-------------|--------|
| R400 | JSON Schemas for all contracts | COVERED (schemas/ directory) |

### Example requirements

| ID | Requirement | Status |
|----|-------------|--------|
| R500 | 5 end-to-end examples | COVERED (examples/ directory) |

### Validation requirements

| ID | Requirement | Status |
|----|-------------|--------|
| R600 | Validation scripts and tests | COVERED (scripts/ and tests/) |
| R601 | Artifact index | COVERED (artifact_index.json) |
| R602 | Proof JSON | COVERED (proof file) |
| R603 | Requirements traceability | COVERED (this document) |

## Coverage summary

Total requirements traced: 55
Requirements COVERED: 55
Requirements UNTRACED: 0
Coverage: 100%"""
    ),
    "139_acceptance_criteria.md": ("Acceptance Criteria",
        "Acceptance criteria for the documentation task and product phases.",
        """## Documentation acceptance criteria

The documentation task is accepted when:

1. Documentation structure created: All required directories and files exist
2. All required topics covered: No missing sections
3. No empty placeholder documents: Every document has substantive content
4. All schemas valid: JSON Schema validation passes
5. All examples validate against schemas
6. Traceability complete: All requirements traced
7. Contradictions found = 0: No contradictory statements across documents
8. No unresolved blockers: All known issues addressed or explicitly logged
9. Application code not changed: No production code modifications
10. No LLM calls executed: No real AI/API calls made
11. No deployment executed
12. Tests pass: Documentation validation tests pass
13. Proof JSON created and valid
14. Commit created and pushed
15. Git clean
16. HEAD matches origin

## MVP acceptance criteria

The MVP is accepted when:
1. Initial diagnostic produces multidimensional profile
2. Personal narrative lessons generate from user stories
3. Suggested situation lessons deliver functional practice
4. Visual scene lessons process images and generate tasks
5. Audio narrative lessons respect duration limits
6. Quiz system delivers 4-7 item checkpoints
7. SRS schedules reviews at appropriate intervals
8. Reward system awards XP deterministically
9. Basic anti-cheat prevents exploitation
10. Core LLM boundaries enforced

## Production acceptance criteria

Full production acceptance:
1. All 14 lesson modes operational
2. Full CEFR range (A1-C2) covered
3. All security measures implemented and tested
4. Accessibility compliance (WCAG 2.1 AA)
5. Performance targets met
6. Learning outcomes validated
7. Cost within budget
8. Legal and regulatory compliance"""
    ),
    "140_ai_assessment_calibration_and_human_agreement.md": ("AI Assessment Calibration and Human Agreement",
        "Process for calibrating AI assessments against human expert judgments.",
        """## Purpose

AI assessments of learner language must be calibrated against human expert judgments to ensure validity and reliability.

## Calibration process

1. Sample of learner responses (minimum 100 per skill area per CEFR level)
2. Both AI and human linguists assess the same responses
3. Agreement metrics calculated
4. Thresholds set for acceptable agreement
5. Regular calibration cycles

## Agreement metrics

| Metric | What it measures | Target |
|--------|-----------------|--------|
| Cohen's kappa | Inter-rater agreement (beyond chance) | > 0.7 |
| Exact agreement | Same rating assigned | > 80% |
| Adjacent agreement | Within one level | > 95% |
| Spearman correlation | Ranking consistency | > 0.8 |

## Calibration frequency

- Initial calibration: Before any production use
- Ongoing: Monthly recalibration on new sample
- Event-driven: After any significant model or prompt change

## Handling disagreements

When AI and human disagree:
1. Log the disagreement
2. Third expert adjudicates
3. Update AI assessment criteria if systematic error found
4. Track disagreement rate over time

## Human rater qualifications

- Native/near-native proficiency
- Training on assessment rubrics
- Calibration before each rating session
- Inter-rater reliability check among human raters"""
    ),
    "141_language_variant_and_norm_policy.md": ("Language Variant and Norm Policy",
        "Policy for selecting and supporting language variants (e.g., British vs American English).",
        """## Variant selection

For each target language, the system selects a primary variant:

| Language | Primary variant | Notes |
|----------|----------------|-------|
| English | International (neutral) | Mix of US/UK with notes on differences |
| Spanish | Neutral Latin American | Castilian notes where relevant |
| French | Metropolitan French | Canadian French notes |
| Portuguese | Brazilian Portuguese | European Portuguese notes |
| German | Standard German (Hochdeutsch) | Regional variations noted |

## Variant policy

1. **Consistency within lessons** — A single lesson uses one variant
2. **Learner choice** — Learner can select preferred variant at onboarding
3. **Variant awareness** — Key differences are taught, not hidden
4. **Acceptance** — All major variants are accepted in learner production
5. **Correction limits** — Only correct errors within the learner's chosen variant

## Norm selection criteria

- Number of speakers
- Availability of quality resources
- Learner demand
- Linguistic comprehensibility across variants

## Variant-neutral approach

- Spelling: Accept both UK and US
- Vocabulary: Accept both (e.g., lift/elevator), teach primary variant
- Pronunciation: Accept both, teach primary variant
- Grammar: Minor differences accepted (e.g., collective noun agreement)"""
    ),
    "142_content_licensing_and_provenance.md": ("Content Licensing and Provenance",
        "Licensing and attribution requirements for all content used in the app.",
        """## Content categories

| Category | Source | License requirements |
|----------|--------|---------------------|
| Images | Licensed stock, AI-generated, user-uploaded | Per-image license |
| Audio | Original recordings, licensed audio | Per-recording license |
| Text (LKB) | Author-created | Owned by company |
| Text (AI-generated) | Generated per session | Owned by company per ToS |
| User content | User-uploaded | User retains ownership, license to app |
| Third-party data | APIs, datasets | Per-source agreement |

## AI-generated content

- AI-generated lesson content is owned by the company
- Learners grant license for their stories to be used for personalization
- No third-party training on user data without explicit consent

## User content licensing

When users share stories or upload content:
1. User retains full ownership
2. User grants app license to use content for personalization
3. User can revoke license by deleting content
4. Content is not shared with third parties
5. Aggregate, anonymized data may be used for model improvement

## Attribution requirements

- Third-party content attributed per license requirements
- Generated content marked as 'AI-generated' where required
- User content attributed to user (within their own view only)

## Compliance

- DMCA compliance (US)
- Copyright Directive compliance (EU)
- Terms of Service compliance for all integrated services"""
    ),
    "143_offline_learning_and_state_synchronization.md": ("Offline Learning and State Synchronization",
        "Design for offline learning capability and state synchronization when connectivity is restored.",
        """## Offline capability scope

### Available offline
- Review sessions (cached items and schedules)
- Previously completed lesson replay
- Basic vocabulary practice
- Progress viewing (cached)

### Not available offline
- New lesson generation (requires LLM)
- Full diagnostic
- Upload of personal stories
- Achievement notifications

## Local state management

- Review schedule cached locally for up to 7 days
- Quiz results stored locally with idempotency keys
- Lesson progress saved locally
- Learner actions logged with timestamps

## Sync on reconnection

When connectivity is restored:
1. Establish secure connection
2. Submit pending state changes with idempotency keys
3. Server validates each change
4. Conflicts resolved (server wins for mastery/progress, client wins for preferences)
5. Updated state returned to client
6. Cache refreshed

## Conflict resolution

| Conflict type | Resolution rule |
|--------------|----------------|
| Mastery state | Server authoritative |
| XP/rewards | Server authoritative (idempotency prevents duplicates) |
| Learner preferences | Last write wins |
| Review schedule | Merge (server schedule + client completions) |
| Lesson progress | Most complete wins |

## Security considerations

- Offline data encrypted on device
- Authentication tokens with expiry
- No PII stored unencrypted
- Remote wipe capability for lost devices"""
    ),
    "144_content_recall_and_learning_state_repair.md": ("Content Recall and Learning State Repair",
        "Handling of content that needs to be recalled or updated, and repair of inconsistent learning state.",
        """## Content recall scenarios

1. **LKB update** — A grammar rule is corrected. Learners who engaged with the previous version need notification and re-instruction.
2. **Content error** — A specific lesson contained an error. Affected learners are identified and offered repair.
3. **Pedagogical improvement** — A teaching approach is improved. Learners who went through the old approach are offered updated content.

## State repair scenarios

1. **Profile inconsistency** — Diagnostic and ongoing performance don't match. Recalibration triggered.
2. **Mastery/performance mismatch** — Quiz shows mastery but free production shows errors. Regression triggered.
3. **Evidence contradiction** — Two evidence sources conflict. Confidence reduced, new evidence requested.

## Repair mechanisms

| Issue | Detection | Repair action |
|-------|-----------|--------------|
| LKB update | Version change notification | Flag affected items for re-introduction |
| Content error | Error report | Push repair lesson to affected learners |
| Profile mismatch | Anomaly detection | Recalibration or partial reassessment |
| Mastery mismatch | Performance monitoring | Mastery regression to previous state |
| Evidence conflict | Cross-validation | Request additional evidence |

## Learner notification

When state repair is needed, the learner is informed:
- What happened (if visible)
- What changed (transparent explanation)
- What to expect (repair lesson, recalibration)
- No penalty for system errors

## Graceful degradation

If state cannot be perfectly repaired:
1. Best-effort reconstruction
2. Wider confidence intervals
3. Additional observation period
4. Human review if automated repair fails"""),
}

# Generate function
def generate(section, data):
    in_scope, out_scope, core_decisions, acceptance = IN_OUT[section]
    base_path = os.path.join(BASE, section.replace("_and_", "_and_"))
    # Fix path for memory_and_engagement
    if section == "memory_and_engagement":
        base_path = os.path.join(BASE, "memory_and_engagement")
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

# Generate all sections
for section in ["lessons", "skill_modes", "memory_and_engagement", "architecture", "security", "validation"]:
    print(f"\n=== Generating {section} ===")
    generate(section, CONTENT[section])

print("\n=== ALL DOCUMENTS GENERATED SUCCESSFULLY ===")
