# Participant Matrix

## Overview

| Tester ID | Profile Type | Target Language | Native Language | Self-Reported Level | Completed Flow | Steps Passed | Total Steps | Completion Time (est.) |
|-----------|-------------|----------------|-----------------|---------------------|---------------|-------------|-------------|----------------------|
| ALPHA-001 | returning_learner | English | Synthetic | A2 | ✓ | 17 | 17 | ~2 min |
| ALPHA-002 | beginner | English | Synthetic | A1 | ✓ | 17 | 17 | ~2 min |
| ALPHA-003 | work_focused | English | Synthetic | B1 | ✓ | 17 | 17 | ~2 min |
| ALPHA-004 | low_confidence | English | Synthetic | A1 | ✓ | 17 | 17 | ~2 min |
| ALPHA-005 | returning_learner_advanced | English | Synthetic | B2 | ✓ | 17 | 17 | ~2 min |

## Aggregate Results

| Metric | Value |
|--------|-------|
| Total participants | 5 |
| Completed flow | 5 |
| Dropped or blocked | 0 |
| Real personal data used | false |
| All consent recorded | true |

## Per-participant Details

### ALPHA-001 (returning_learner)

```json
{
  "tester_id": "ALPHA-001",
  "profile_type": "returning_learner",
  "target_language": "English",
  "native_language": "Synthetic",
  "learning_goal": "B1 conversational fluency",
  "self_reported_level": "A2",
  "preferred_duration": 15,
  "flow_completed": true,
  "steps_passed": "17/17",
  "blockers_found": [],
  "ux_issues": ["Diagnostic writing step shows pre-filled response option without explicit instruction to the learner"],
  "learning_clarity_issues": [],
  "trust_safety_issues": [],
  "operator_notes": "All API calls succeeded. The diagnostic screen displays response options that look like they should be interactive but are informational/demo placeholders. The mock AI correctly detected verb form issues in 'wanted to play'.",
  "tester_feedback_summary": "Clear flow. The communicative goal on the lesson screen helps understand the task."
}
```

### ALPHA-002 (beginner)

```json
{
  "tester_id": "ALPHA-002",
  "profile_type": "beginner",
  "target_language": "English",
  "native_language": "Synthetic",
  "learning_goal": "Basic conversation",
  "self_reported_level": "A1",
  "preferred_duration": 10,
  "flow_completed": true,
  "steps_passed": "17/17",
  "blockers_found": [],
  "ux_issues": ["Level descriptions (A1-A2-B1) may need more beginner-friendly labels for absolute beginners"],
  "learning_clarity_issues": [],
  "trust_safety_issues": [],
  "operator_notes": "Beginner A1 profile created successfully. The lesson scaffolding correctly matched the level. AI analysis detected simple grammar patterns in the submission text.",
  "tester_feedback_summary": "The steps were easy to follow. I knew what to do at each screen."
}
```

### ALPHA-003 (work_focused)

```json
{
  "tester_id": "ALPHA-003",
  "profile_type": "work_focused",
  "target_language": "English",
  "native_language": "Synthetic",
  "learning_goal": "Work",
  "self_reported_level": "B1",
  "preferred_duration": 20,
  "flow_completed": true,
  "steps_passed": "17/17",
  "blockers_found": [],
  "ux_issues": ["Lesson duration preference not reflected in lesson card (always shows ~15 min)"],
  "learning_clarity_issues": [],
  "trust_safety_issues": [],
  "operator_notes": "Work-focused goal selected. The contract was created with appropriate parameters for an intermediate learner. Processing pipeline completed with decision=COMPLETE.",
  "tester_feedback_summary": "Quick to complete. I would appreciate seeing my preferred duration reflected in the lesson estimates."
}
```

### ALPHA-004 (low_confidence)

```json
{
  "tester_id": "ALPHA-004",
  "profile_type": "low_confidence",
  "target_language": "English",
  "native_language": "Synthetic",
  "learning_goal": "Study",
  "self_reported_level": "A1",
  "preferred_duration": 10,
  "flow_completed": true,
  "steps_passed": "17/17",
  "blockers_found": [],
  "ux_issues": ["A1 level shown as 'Beginner' but more encouraging messaging would help low-confidence learners"],
  "learning_clarity_issues": ["Learning contract may be dense for A1 learners — some terms like 'scaffolding mode' might not be intuitive"],
  "trust_safety_issues": [],
  "operator_notes": "Low-confidence A1 learner was given moderate scaffolding and simple lesson complexity as expected. The mock AI corrections were supportive rather than punitive.",
  "tester_feedback_summary": "I understood what to do. The feedback was helpful and not scary."
}
```

### ALPHA-005 (returning_learner_advanced)

```json
{
  "tester_id": "ALPHA-005",
  "profile_type": "returning_learner_advanced",
  "target_language": "English",
  "native_language": "Synthetic",
  "learning_goal": "Study",
  "self_reported_level": "B2",
  "preferred_duration": 20,
  "flow_completed": true,
  "steps_passed": "17/17",
  "blockers_found": [],
  "ux_issues": ["No visible difference in experience between A1 and B2 learners beyond contract parameters"],
  "learning_clarity_issues": [],
  "trust_safety_issues": [],
  "operator_notes": "Advanced learner still receives same lesson content as others (no differentiation in lesson topics). The mock AI currently treats all levels similarly since it's a deterministic fixture system.",
  "tester_feedback_summary": "The technical flow works well. For a more advanced learner, the lesson content should scale in complexity."
}
```
