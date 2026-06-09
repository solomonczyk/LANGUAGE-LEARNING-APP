# Curriculum and Language Knowledge Base

**Status:** Approved
**Version:** 1.0.0
**Last updated:** 2026-06-09

---

## Purpose

Specification of the Language Knowledge Base (LKB) — the version-controlled, linguist-reviewed repository of all canonical linguistic content.

## In scope

- Pedagogical framework definition and theoretical foundations
- Curriculum structure and progression design
- Assessment and competence model specifications
- Learning strategy and learner autonomy frameworks

## Out of scope

- Detailed lesson plans
- Specific curriculum item specifications
- Assessment rubric details
- Tutor training materials

## Core decisions

1. Methodology is grounded in established SLA research (Krashen, Swain, Long, Ellis, Vygotsky)
2. Task-Based Language Teaching is the core instructional approach
3. Personal narrative is the primary content source
4. CEFR 2020 is the reference framework including mediation and plurilingualism

## Acceptance criteria

1. Methodology is clearly articulated and internally consistent
2. Research foundations are cited appropriately
3. Methodology directly informs product design decisions
4. All recommendations are actionable for implementation

---

## LKB item types

### Grammar rules
Each rule includes: name, description, form (schematic), usage conditions, exceptions, CEFR level, prerequisites, example sentences, pedagogical sequence, common errors, related rules.

### Vocabulary items
Each item includes: lemma, part of speech, CEFR level, semantic field, definition (L2), translation (L1), collocations, register information, frequency rank, prerequisites, example sentences, common errors.

### Collocations
Each includes: constituent words, type (verb+noun, adj+noun, etc.), meaning, CEFR level, example sentences, frequency.

### Constructions
Larger grammatical patterns (e.g., 'not only X but also Y'). Includes: pattern, constraints, meaning/function, CEFR level, examples.

### Communicative functions
Speech acts (requesting, apologizing, etc.) with: function name, typical realizations (by register), CEFR level, cultural notes.

### Discourse patterns
Connectors, transition phrases, organizational patterns for narratives, arguments, descriptions.

## Metadata schema per item

- id (unique, versioned)
- type (grammar_rule, vocabulary, collocation, construction, function, discourse)
- cefr_level
- prerequisites (list of LKB IDs)
- mastery_criteria (what performance constitutes mastery)
- pedagogical_sequence (order of presentation)
- common_errors (by L1 where applicable)
- related_items (cross-references)
- revision_history
- review_status (draft, reviewed, approved, deprecated)

## Integration with LLM

When generating lesson content, the LLM receives relevant LKB items as reference. It may present, explain, and create activities around these items. It may not contradict them.

## Version control

The LKB is stored in a version-controlled repository. Every change is tracked. Changes require review by a linguist and/or methodologist before approval.

## Authoring workflow

1. Author drafts new/edited item
2. Linguist reviews for accuracy
3. Methodologist reviews for pedagogical appropriateness
4. Item is approved and versioned
5. Old version remains accessible for rollback
