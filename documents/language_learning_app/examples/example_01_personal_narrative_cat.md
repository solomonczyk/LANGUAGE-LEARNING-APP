# Example 01 — Personal Narrative: The Cat Story

**Type:** End-to-end personal narrative lesson  
**CEFR Level:** A2 (developing)  
**Target language:** English (learner L1: Spanish)

---

## Learner profile

| Dimension | Level | Confidence |
|-----------|-------|------------|
| Reading | A2 | High |
| Listening | A2 | Medium |
| Passive vocabulary | A2 | High |
| Active vocabulary | A1/A2 | Medium |
| Grammar recognition | A2 | Medium |
| Productive grammar | A1 | Medium |
| Spoken production | A1/A2 | Low |
| Narrative coherence | A1 | Low |

## Lesson contract

```json
{
  "lesson_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "communicative_goal": "Describe a short morning incident using past simple",
  "mode": "personal_narrative",
  "grammar_focus": ["past_simple_regular", "past_simple_irregular_basic"],
  "vocabulary_focus": ["cat", "jump", "knock_over", "spill", "coffee"],
  "collocation_focus": ["knock_over + object", "wake_up + late"],
  "narrative_focus": "temporal_sequence",
  "receptive_skill_focus": "listening",
  "productive_skill_focus": "speaking",
  "scaffolding_mode": "mixed_construction",
  "cognitive_budget": {
    "max_duration_minutes": 15,
    "max_new_vocabulary": 4,
    "max_new_constructions": 1,
    "max_corrections": 2,
    "audio_max_seconds": 0,
    "interaction_turns": 4
  }
}
```

## Step 1: Elicitation

**System:** Tell me about something that happened this morning. What was the first thing that went wrong or surprised you?

**Learner:** This morning my cat... uh... jump on table. She... knock... my coffee. Big mess.

## Step 2: Narrative Analysis

```json
{
  "grammatical_accuracy": {
    "score": 0.45,
    "level": "A1",
    "errors": [
      {"type": "tense", "target": "jumped", "learner": "jump", "context": "my cat jumped"},
      {"type": "tense", "target": "knocked", "learner": "knock", "context": "she knocked"},
      {"type": "article", "target": "the table", "learner": "on table", "context": "on the table"}
    ]
  },
  "lexical_range": {
    "score": 0.6,
    "level": "A2",
    "strengths": ["appropriate vocabulary", "good word choice for level"]
  },
  "narrative_coherence": {
    "score": 0.5,
    "level": "A1",
    "notes": "Temporal markers missing"
  }
}
```

## Step 3: Focus on Form

**System:** Let's talk about the past. When something happened *before now*, we change the verb.

Look: Today my cat **jumps** → Yesterday my cat **jumped**.

Now you try:
1. Today I clean → Yesterday I ____ (cleaned)
2. Today she knocks → Yesterday she ____ (knocked)

**Learner:** cleaned... knocked

## Step 4: Guided Practice

**System:** Now tell me the story again, but use the past tense. I'll help you start:

"This morning, my cat..." 

**Learner:** This morning, my cat jumped on the table.

**System:** Good! "...and she..."

**Learner:** ...and she knocked over my coffee.

**System:** Excellent! "...so I..."

**Learner:** ...so I... clean the mess.

**System:** Almost! "...so I *cleaned* up the mess."

**Learner:** Ah, so I cleaned up the mess.

## Step 5: Quiz

```json
{
  "items": [
    {"type": "gap_fill", "prompt": "Yesterday, the cat _____ on the table.", "answer": "jumped"},
    {"type": "gap_fill", "prompt": "She _____ over my coffee.", "answer": "knocked"},
    {"type": "multiple_choice", "prompt": "What is the past of 'spill'?", "options": ["spilled", "spold", "spill"], "answer": "spilled"},
    {"type": "ordering", "prompt": "Order the story:", "items": ["cat jumped on table", "cat knocked coffee", "I cleaned mess"], "answer": "1-2-3"}
  ],
  "score": 75
}
```

## Step 6: Transfer Task

**System:** Now tell me about something your pet (or a friend's pet) did yesterday. Use past tense.

**Learner:** My dog... yesterday my dog opened the door. He run outside.

**System:** Almost perfect! Try: He *ran* outside.

**Learner:** He ran outside. I called him and he came back.

## Review schedule

| Item | 2h | 12h | 2d | 7d |
|------|-----|-----|----|----|
| jumped | ✓ | ✓ | | |
| knocked over | ✓ | ✓ | | |
| spilled | ✓ | | | |
| past simple -ed | ✓ | ✓ | ✓ | |
| cat story (retell) | | ✓ | | ✓ |
