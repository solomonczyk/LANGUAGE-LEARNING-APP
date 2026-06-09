# Glossary — Language Learning App

**Status:** Approved  
**Version:** 1.0.0  
**Last updated:** 2026-06-09

---

## A

**Active vocabulary** — words and phrases the learner can produce spontaneously without prompting or retrieval cues.

**Assessment engine** — system component that evaluates learner responses against criteria, produces evidence records, and determines proficiency estimates with confidence intervals.

**Audio narrative** — lesson mode where the primary stimulus is an audio recording (monologue or dialogue) used for listening comprehension, retelling, and language production tasks.

**Audiovisual comprehension** — receptive skill combining audio and visual channels (video with sound, image with narration) for meaning-making.

## B

**Backward building** — scaffolding technique where the learner completes increasingly longer segments of a target utterance, starting from the final word or phrase.

## C

**CEFR (Common European Framework of Reference for Languages)** — international standard for describing language ability across six levels (A1, A2, B1, B2, C1, C2), used as the progression framework.

**Cognitive budget** — the planned cognitive load for a single lesson session, measured in time, number of new items, complexity of operations, and expected mental effort.

**Collocation** — a habitual combination of words that commonly occur together (e.g., "make a decision," "heavy rain"). Distinct from free combination.

**Communicative competence** — the ability to use language effectively and appropriately in real communication, encompassing linguistic, sociolinguistic, discourse, and strategic competences (per CEFR).

**Communicative goal** — the real-world purpose of a lesson (e.g., "describe a problem to a service representative") as distinct from a grammatical objective.

**Corrective feedback** — pedagogically framed response to learner error, ranging from explicit correction through recast, clarification request, metalinguistic clue, elicitation, and repetition.

**Curriculum engine** — system component that manages the ordered progression of learning content, adapting sequence and emphasis based on learner state.

## D

**Decision log** — living document recording architectural, methodological, and product decisions with rationale, alternatives considered, and date.

**Diagnostic session** — initial or periodic assessment battery that evaluates the learner across multiple dimensions to produce a skill profile.

**Dynamic scaffolding** — adaptive support system that adjusts the level of linguistic assistance based on real-time learner performance and the specific target construction.

## E

**Error evidence model** — data structure that records learner errors with context, type, frequency, pattern, and remediation history.

## F

**Fluency task** — activity prioritizing smooth, real-time production over accuracy, with error treatment deferred.

**Functional communication** — language use for practical real-world purposes (ordering, requesting, explaining, apologizing, etc.).

## G

**Gamification** — application of game-design elements (points, levels, streaks, achievements, leaderboards) to non-game contexts to increase motivation and engagement.

**Grammar knowledge base** — version-controlled repository of grammatical rules, patterns, and exceptions serving as the authoritative source for instruction and feedback, independent of any LLM.

## I

**Idempotency key** — unique identifier ensuring that a state-changing operation (e.g., XP award, lesson completion) can be applied only once, preventing duplicate rewards.

**Initial diagnostic** — multidimensional assessment performed at learner onboarding, covering all skill areas to establish baseline and placement.

**Intercultural competence** — ability to navigate and mediate between cultures, including awareness of norms, taboos, politeness conventions, and discourse patterns.

## L

**Language Knowledge Base (LKB)** — version-controlled structured repository of all canonical linguistic content: grammar rules, vocabulary items, collocations, phonology, pragmatics, and curriculum mappings.

**Learner model** — the system's structured representation of a single user's language abilities, preferences, history, error patterns, and learning state across all dimensions.

**Learner profile** — output of the multidimensional diagnostic, containing skill-level estimates, confidence scores, learning style indicators, and interest data.

**Lesson contract** — structured specification of a single lesson including communicative goal, grammar focus, vocabulary targets, receptive and productive skill foci, scaffolding mode, cognitive budget, and assessment criteria. See `lesson_contract.schema.json`.

**Lesson mode** — one of the fourteen content-delivery paradigms (personal narrative, suggested situation, visual single scene, visual sequence, etc.).

## M

**Mastery** — the system's assessment that a learner can reliably use a specific language item (word, construction, function) at a defined level of proficiency.

**Mastery lifecycle** — progression through states: introduced → recognized → reconstructed → guided_use → independent_use → interactive_use → transferred → retained.

**Mastery engine** — deterministic system component that updates mastery status based on evidence, without LLM involvement.

**Mediation** — language activity where the learner acts as an intermediary, conveying meaning between parties who cannot communicate directly (CEFR 2018).

**Multidimensional learner profile** — structured representation of learner abilities across all assessed dimensions, not reducible to a single CEFR level.

## N

**Narrative coherence** — the logical and temporal organization of a spoken or written story, including sequence, causality, reference maintenance, and discourse markers.

**Narrative Learning Engine (NLE)** — AI agent responsible for managing personal-narrative-based lessons: eliciting, analyzing, and building activities around user stories.

## P

**Passive vocabulary** — words and phrases the learner can recognize and understand but cannot yet produce spontaneously.

**Pedagogical validation** — verification that LLM-generated content meets instructional quality, level-appropriateness, and scaffolding policy requirements.

**Personal narrative** — lesson mode where the primary content is a story or experience from the learner's own life, used as material for language practice and development.

**Phonological competence** — ability to perceive and produce the sound system, intonation, stress, and rhythm patterns of the target language at an intelligible level.

**Placement result** — recommended starting point in the curriculum derived from the initial diagnostic, expressed as a range rather than a single point.

**Plurilingualism** — an individual's ability to draw on a repertoire of linguistic and cultural resources from multiple languages, rather than maintaining separate, isolated competences.

**Pragmatic competence** — ability to use language appropriately in context, including speech acts, implicature, register, and politeness strategies.

**Prompt injection** — security attack where user-supplied content contains instructions that attempt to override or manipulate the LLM's system behavior.

## Q

**Quiz** — short controlled-practice assessment (4–7 items, 2–4 minutes) serving as a checkpoint within a lesson, distinct from comprehensive mastery assessment.

## R

**Recast** — corrective feedback type where the teacher/ system rephrases the learner's erroneous utterance in correct form without explicit error marking.

**Repair strategy** — communication strategy used by the learner to address breakdowns in understanding or production (clarification request, self-correction, paraphrasing, etc.).

**Review scheduler** — service that determines optimal timing for spaced-repetition review of each language item, adapting intervals based on recall success.

**Reward economy** — the system of points, currency, and rewards earned through learning activities, with deterministic awarding rules excluding LLM discretion.

**Reward Engine** — deterministic service that calculates and distributes rewards based on verifiable learner actions, with no LLM involvement in reward decisions.

## S

**Scaffolding** — temporary support structures that enable the learner to perform at a level beyond independent ability, progressively removed as competence develops.

**Schema validation** — structural verification of data against a predefined JSON Schema, applied to all LLM outputs before any state mutation occurs.

**Spaced repetition** — scheduling technique that distributes review of previously learned material across expanding intervals to optimize long-term retention.

**Structured output** — LLM response constrained to a predefined JSON Schema, enforced at the application layer.

**Suggested situation** — lesson mode where the learner is given a realistic scenario (not from personal experience) and asked to respond communicatively.

## T

**Traceability matrix** — document mapping every requirement to its source, canonical document location, schema, example, validation test, and implementation status.

**Transfer task** — activity requiring the learner to apply recently practiced language to a novel context, confirming the ability to generalize.

## U

**Untrusted content** — any user-supplied input (text, voice transcription, images, OCR, documents, external materials) treated as potentially containing prompt injection or other malicious payloads.

## V

**Visual narrative** — lesson mode using images (single or sequential) as the primary stimulus for language production, description, storytelling, and inference.

**Vocabulary depth** — quality of word knowledge including collocational, grammatical, and register properties beyond basic meaning.

## W

**Writing cycle** — structured process: draft → problem identification → hint → self-correction → recheck → natural model → transfer task. AI does not rewrite the entire learner text upfront.

## X

**XP (Experience Points)** — deterministic reward currency earned through verifiable learning activities, awarded only by the Reward Engine, never by an LLM.
