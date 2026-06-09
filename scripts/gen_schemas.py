#!/usr/bin/env python3
"""Generate all JSON Schema files for the Language Learning App."""
import json, os

SCHEMA_DIR = "f:/Dev/Projects/LANGUAGE-LEARNING-APP/documents/language_learning_app/schemas"
os.makedirs(SCHEMA_DIR, exist_ok=True)

schemas = {}

# Shared definitions
schemas["diagnostic_session.schema.json"] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://language-learning.app/schemas/diagnostic_session.json",
    "title": "Diagnostic Session",
    "description": "A complete initial diagnostic assessment session",
    "type": "object",
    "required": ["learner_id", "session_id", "dimensions", "started_at", "status"],
    "additionalProperties": False,
    "properties": {
        "learner_id": {"type": "string", "format": "uuid"},
        "session_id": {"type": "string", "format": "uuid"},
        "dimensions": {
            "type": "array",
            "items": {"$ref": "#/definitions/dimension_assessment"},
            "minItems": 14
        },
        "started_at": {"type": "string", "format": "date-time"},
        "completed_at": {"type": "string", "format": "date-time"},
        "status": {"type": "string", "enum": ["in_progress", "completed", "abandoned"]},
        "version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"}
    },
    "definitions": {
        "dimension_assessment": {
            "type": "object",
            "required": ["dimension", "level", "confidence"],
            "properties": {
                "dimension": {"type": "string", "enum": ["reading", "listening", "passive_vocabulary", "active_vocabulary", "grammar_recognition", "productive_grammar", "spoken_production", "spoken_interaction", "pronunciation_intelligibility", "narrative_coherence", "writing", "mediation", "communication_strategies"]},
                "level": {"type": "string", "pattern": "^(A1|A2|B1|B2|C1|C2)(_entering|_developing|_consolidating)?$"},
                "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                "observations": {"type": "integer", "minimum": 0},
                "evidence_ids": {"type": "array", "items": {"type": "string"}}
            }
        }
    }
}

schemas["diagnostic_evidence.schema.json"] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://language-learning.app/schemas/diagnostic_evidence.json",
    "title": "Diagnostic Evidence",
    "description": "A single piece of evidence from a diagnostic task",
    "type": "object",
    "required": ["evidence_id", "session_id", "dimension", "task_type", "score", "timestamp"],
    "additionalProperties": False,
    "properties": {
        "evidence_id": {"type": "string", "format": "uuid"},
        "session_id": {"type": "string", "format": "uuid"},
        "dimension": {"type": "string"},
        "task_type": {"type": "string"},
        "score": {"type": "number", "minimum": 0, "maximum": 1},
        "confidence_weight": {"type": "number", "minimum": 0.1, "maximum": 2.0},
        "timestamp": {"type": "string", "format": "date-time"},
        "response_data": {"type": "object"}
    }
}

schemas["skill_assessment.schema.json"] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://language-learning.app/schemas/skill_assessment.json",
    "title": "Skill Assessment",
    "description": "Assessment of a single skill dimension",
    "type": "object",
    "required": ["learner_id", "dimension", "assessed_level", "confidence"],
    "additionalProperties": False,
    "properties": {
        "learner_id": {"type": "string"},
        "dimension": {"type": "string"},
        "assessed_level": {"type": "string"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "evidence_count": {"type": "integer", "minimum": 0},
        "last_updated": {"type": "string", "format": "date-time"},
        "trend": {"type": "string", "enum": ["improving", "stable", "declining", "insufficient_data"]}
    }
}

schemas["placement_result.schema.json"] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://language-learning.app/schemas/placement_result.json",
    "title": "Placement Result",
    "description": "Recommended starting point derived from diagnostic",
    "type": "object",
    "required": ["learner_id", "diagnostic_session_id", "recommended_start_range"],
    "additionalProperties": False,
    "properties": {
        "learner_id": {"type": "string"},
        "diagnostic_session_id": {"type": "string"},
        "recommended_start_range": {
            "type": "object",
            "required": ["low", "high"],
            "properties": {
                "low": {"type": "string"},
                "high": {"type": "string"}
            }
        },
        "weakest_dimensions": {"type": "array", "items": {"type": "string"}},
        "strongest_dimensions": {"type": "array", "items": {"type": "string"}},
        "notes": {"type": "string"}
    }
}

schemas["learner_profile.schema.json"] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://language-learning.app/schemas/learner_profile.json",
    "title": "Learner Profile",
    "description": "Multidimensional learner profile with ability estimates and preferences",
    "type": "object",
    "required": ["learner_id", "profiles", "preferences"],
    "additionalProperties": False,
    "properties": {
        "learner_id": {"type": "string"},
        "version": {"type": "integer"},
        "profiles": {
            "type": "object",
            "additionalProperties": {"$ref": "#/definitions/dimension_profile"}
        },
        "preferences": {
            "type": "object",
            "properties": {
                "learning_style": {"type": "string", "enum": ["inductive", "deductive", "mixed"]},
                "preferred_modes": {"type": "array", "items": {"type": "string"}},
                "session_duration_min": {"type": "integer"}
            }
        },
        "interests": {"type": "array", "items": {"type": "string"}},
        "languages": {"type": "object"},
        "created_at": {"type": "string", "format": "date-time"},
        "updated_at": {"type": "string", "format": "date-time"}
    },
    "definitions": {
        "dimension_profile": {
            "type": "object",
            "required": ["level", "confidence"],
            "properties": {
                "level": {"type": "string"},
                "confidence": {"type": "number"},
                "observations": {"type": "integer"},
                "trend": {"type": "string"}
            }
        }
    }
}

schemas["learning_entry_contract.schema.json"] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://language-learning.app/schemas/learning_entry_contract.json",
    "title": "Learning Entry Contract",
    "description": "Agreement between system and learner at onboarding",
    "type": "object",
    "required": ["learner_id", "goals", "time_commitment"],
    "additionalProperties": False,
    "properties": {
        "learner_id": {"type": "string"},
        "goals": {"type": "array", "items": {"type": "string"}, "minItems": 1},
        "time_commitment": {
            "type": "object",
            "required": ["minutes_per_day", "days_per_week"],
            "properties": {
                "minutes_per_day": {"type": "integer", "minimum": 5},
                "days_per_week": {"type": "integer", "minimum": 1, "maximum": 7},
                "preferred_time": {"type": "string"}
            }
        },
        "interests": {"type": "array", "items": {"type": "string"}},
        "language_background": {"type": "object"},
        "consent": {"type": "boolean"},
        "created_at": {"type": "string", "format": "date-time"}
    }
}

schemas["lesson_contract.schema.json"] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://language-learning.app/schemas/lesson_contract.json",
    "title": "Lesson Contract",
    "description": "Complete specification for a single lesson session",
    "type": "object",
    "required": ["lesson_id", "communicative_goal", "mode", "cognitive_budget"],
    "additionalProperties": False,
    "properties": {
        "lesson_id": {"type": "string", "format": "uuid"},
        "communicative_goal": {"type": "string"},
        "mode": {"type": "string"},
        "grammar_focus": {"type": "array", "items": {"type": "string"}},
        "vocabulary_focus": {"type": "array", "items": {"type": "string"}},
        "narrative_focus": {"type": "string"},
        "receptive_skill_focus": {"type": "string"},
        "productive_skill_focus": {"type": "string"},
        "interaction_focus": {"type": "string"},
        "strategy_focus": {"type": "string"},
        "scaffolding_mode": {"type": "string"},
        "cognitive_budget": {
            "type": "object",
            "required": ["max_duration_minutes"],
            "properties": {
                "max_duration_minutes": {"type": "integer"},
                "max_new_vocabulary": {"type": "integer"},
                "max_new_constructions": {"type": "integer"},
                "max_corrections": {"type": "integer"},
                "audio_max_seconds": {"type": "integer"},
                "interaction_turns": {"type": "integer"}
            }
        },
        "assessment_criteria": {"type": "object"}
    }
}

schemas["lesson_session.schema.json"] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://language-learning.app/schemas/lesson_session.json",
    "title": "Lesson Session",
    "description": "Record of an actual lesson session execution",
    "type": "object",
    "required": ["session_id", "lesson_id", "learner_id", "started_at", "status"],
    "additionalProperties": False,
    "properties": {
        "session_id": {"type": "string", "format": "uuid"},
        "lesson_id": {"type": "string", "format": "uuid"},
        "learner_id": {"type": "string"},
        "started_at": {"type": "string", "format": "date-time"},
        "completed_at": {"type": "string", "format": "date-time"},
        "status": {"type": "string", "enum": ["in_progress", "completed", "abandoned"]},
        "completion_percentage": {"type": "number", "minimum": 0, "maximum": 100},
        "quiz_score": {"type": "number", "minimum": 0, "maximum": 100},
        "activities": {"type": "array", "items": {"type": "object"}},
        "scaffolding_levels_used": {"type": "array", "items": {"type": "string"}},
        "errors_treated": {"type": "array", "items": {"type": "object"}}
    }
}

schemas["narrative_analysis.schema.json"] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://language-learning.app/schemas/narrative_analysis.json",
    "title": "Narrative Analysis",
    "description": "Analysis of a learner's spoken or written narrative",
    "type": "object",
    "required": ["narrative_id", "learner_id", "analysis_dimensions"],
    "additionalProperties": False,
    "properties": {
        "narrative_id": {"type": "string", "format": "uuid"},
        "learner_id": {"type": "string"},
        "source_text": {"type": "string"},
        "analysis_dimensions": {
            "type": "object",
            "required": ["grammatical_accuracy", "lexical_range", "narrative_coherence", "pragmatic_appropriateness"],
            "properties": {
                "grammatical_accuracy": {"$ref": "#/definitions/dimension_score"},
                "lexical_range": {"$ref": "#/definitions/dimension_score"},
                "narrative_coherence": {"$ref": "#/definitions/dimension_score"},
                "pragmatic_appropriateness": {"$ref": "#/definitions/dimension_score"}
            }
        },
        "errors_detected": {"type": "array", "items": {"$ref": "#/definitions/error_entry"}},
        "strengths": {"type": "array", "items": {"type": "string"}},
        "recommended_focus": {"type": "array", "items": {"type": "string"}}
    },
    "definitions": {
        "dimension_score": {
            "type": "object",
            "required": ["score", "level"],
            "properties": {
                "score": {"type": "number", "minimum": 0, "maximum": 1},
                "level": {"type": "string"},
                "notes": {"type": "string"}
            }
        },
        "error_entry": {
            "type": "object",
            "required": ["type", "target_form", "learner_form", "context"],
            "properties": {
                "type": {"type": "string"},
                "target_form": {"type": "string"},
                "learner_form": {"type": "string"},
                "context": {"type": "string"},
                "l1_influence": {"type": "boolean"},
                "severity": {"type": "string", "enum": ["global", "local"]}
            }
        }
    }
}

schemas["visual_scenario.schema.json"] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://language-learning.app/schemas/visual_scenario.json",
    "title": "Visual Scenario",
    "description": "A visual scenario (single image or sequence) used as lesson stimulus",
    "type": "object",
    "required": ["scenario_id", "image_count", "task_types"],
    "additionalProperties": False,
    "properties": {
        "scenario_id": {"type": "string", "format": "uuid"},
        "image_count": {"type": "integer", "minimum": 1, "maximum": 6},
        "images": {"type": "array", "items": {"type": "object"}},
        "task_types": {"type": "array", "items": {"type": "string"}},
        "scene_description": {"type": "string"},
        "detected_elements": {"type": "array", "items": {"type": "string"}},
        "emotional_interpretations": {"type": "array", "items": {"type": "string"}},
        "cefr_level": {"type": "string"}
    }
}

schemas["audio_scenario.schema.json"] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://language-learning.app/schemas/audio_scenario.json",
    "title": "Audio Scenario",
    "description": "An audio scenario used as lesson stimulus",
    "type": "object",
    "required": ["scenario_id", "duration_seconds", "transcript"],
    "additionalProperties": False,
    "properties": {
        "scenario_id": {"type": "string"},
        "duration_seconds": {"type": "number", "minimum": 5},
        "transcript": {"type": "string"},
        "speaker_count": {"type": "integer", "minimum": 1},
        "cefr_level": {"type": "string"},
        "vocabulary_items": {"type": "array", "items": {"type": "string"}},
        "comprehension_questions": {"type": "array", "items": {"type": "object"}}
    }
}

schemas["performance_task.schema.json"] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://language-learning.app/schemas/performance_task.json",
    "title": "Performance Task",
    "description": "A performance-based assessment task",
    "type": "object",
    "required": ["task_id", "task_type", "prompt", "assessment_criteria"],
    "additionalProperties": False,
    "properties": {
        "task_id": {"type": "string", "format": "uuid"},
        "task_type": {"type": "string"},
        "prompt": {"type": "string"},
        "stimulus": {"type": "object"},
        "scaffolding_level": {"type": "string"},
        "assessment_criteria": {
            "type": "object",
            "required": ["dimensions"],
            "properties": {
                "dimensions": {"type": "array", "items": {"type": "string"}},
                "pass_threshold": {"type": "number", "minimum": 0, "maximum": 1}
            }
        },
        "cefr_level": {"type": "string"}
    }
}

schemas["quiz_package.schema.json"] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://language-learning.app/schemas/quiz_package.json",
    "title": "Quiz Package",
    "description": "A short controlled-practice quiz (4-7 items, 2-4 minutes)",
    "type": "object",
    "required": ["quiz_id", "items", "time_limit_minutes"],
    "additionalProperties": False,
    "properties": {
        "quiz_id": {"type": "string", "format": "uuid"},
        "lesson_id": {"type": "string", "format": "uuid"},
        "items": {
            "type": "array",
            "items": {"$ref": "#/definitions/quiz_item"},
            "minItems": 4,
            "maxItems": 7
        },
        "time_limit_minutes": {"type": "integer", "minimum": 2, "maximum": 4},
        "passing_score": {"type": "number", "minimum": 0, "maximum": 100}
    },
    "definitions": {
        "quiz_item": {
            "type": "object",
            "required": ["item_id", "type", "prompt", "correct_answer"],
            "properties": {
                "item_id": {"type": "string"},
                "type": {"type": "string", "enum": ["multiple_choice", "gap_fill", "matching", "ordering", "short_answer"]},
                "prompt": {"type": "string"},
                "options": {"type": "array", "items": {"type": "string"}},
                "correct_answer": {"type": "string"},
                "points": {"type": "integer", "minimum": 1}
            }
        }
    }
}

schemas["dialogue_assessment.schema.json"] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://language-learning.app/schemas/dialogue_assessment.json",
    "title": "Dialogue Assessment",
    "description": "Assessment of learner performance in a spoken dialogue task",
    "type": "object",
    "required": ["assessment_id", "learner_id", "dialogue_turns", "scores"],
    "additionalProperties": False,
    "properties": {
        "assessment_id": {"type": "string"},
        "learner_id": {"type": "string"},
        "dialogue_turns": {"type": "array", "items": {"type": "object"}},
        "scores": {
            "type": "object",
            "properties": {
                "fluency": {"type": "number"},
                "appropriateness": {"type": "number"},
                "effectiveness": {"type": "number"},
                "range": {"type": "number"}
            }
        },
        "errors": {"type": "array", "items": {"type": "object"}},
        "overall_level": {"type": "string"}
    }
}

schemas["writing_assessment.schema.json"] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://language-learning.app/schemas/writing_assessment.json",
    "title": "Writing Assessment",
    "description": "Assessment of learner written production",
    "type": "object",
    "required": ["assessment_id", "learner_id", "text", "scores"],
    "additionalProperties": False,
    "properties": {
        "assessment_id": {"type": "string"},
        "learner_id": {"type": "string"},
        "text": {"type": "string"},
        "scores": {
            "type": "object",
            "required": ["content", "organization", "vocabulary", "grammar", "mechanics"],
            "properties": {
                "content": {"type": "number", "minimum": 0, "maximum": 100},
                "organization": {"type": "number", "minimum": 0, "maximum": 100},
                "vocabulary": {"type": "number", "minimum": 0, "maximum": 100},
                "grammar": {"type": "number", "minimum": 0, "maximum": 100},
                "mechanics": {"type": "number", "minimum": 0, "maximum": 100}
            }
        },
        "cycle_stage": {"type": "string", "enum": ["draft", "problem_identification", "hint", "self_correction", "recheck", "natural_model", "transfer"]},
        "errors_identified": {"type": "array", "items": {"type": "object"}}
    }
}

schemas["listening_assessment.schema.json"] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://language-learning.app/schemas/listening_assessment.json",
    "title": "Listening Assessment",
    "description": "Assessment of listening comprehension",
    "type": "object",
    "required": ["assessment_id", "audio_id", "comprehension_scores"],
    "additionalProperties": False,
    "properties": {
        "assessment_id": {"type": "string"},
        "audio_id": {"type": "string"},
        "comprehension_scores": {
            "type": "object",
            "required": ["gist", "detail"],
            "properties": {
                "gist": {"type": "number", "minimum": 0, "maximum": 100},
                "detail": {"type": "number", "minimum": 0, "maximum": 100},
                "inference": {"type": "number", "minimum": 0, "maximum": 100},
                "retelling_quality": {"type": "number", "minimum": 0, "maximum": 100}
            }
        }
    }
}

schemas["mastery_evidence.schema.json"] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://language-learning.app/schemas/mastery_evidence.json",
    "title": "Mastery Evidence",
    "description": "Evidence record for mastery state transition",
    "type": "object",
    "required": ["evidence_id", "learner_id", "item_id", "current_state", "performance", "timestamp"],
    "additionalProperties": False,
    "properties": {
        "evidence_id": {"type": "string", "format": "uuid"},
        "learner_id": {"type": "string"},
        "item_id": {"type": "string"},
        "current_state": {"type": "string", "enum": ["introduced", "recognized", "reconstructed", "guided_use", "independent_use", "interactive_use", "transferred", "retained"]},
        "performance": {"type": "string", "enum": ["perfect", "good", "hint", "fail"]},
        "context": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "source": {"type": "string"}
    }
}

schemas["review_schedule.schema.json"] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://language-learning.app/schemas/review_schedule.json",
    "title": "Review Schedule",
    "description": "Spaced repetition review schedule for a learner",
    "type": "object",
    "required": ["learner_id", "scheduled_date", "items"],
    "additionalProperties": False,
    "properties": {
        "learner_id": {"type": "string"},
        "scheduled_date": {"type": "string", "format": "date"},
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["item_id", "item_type", "interval_days", "ease_factor"],
                "properties": {
                    "item_id": {"type": "string"},
                    "item_type": {"type": "string"},
                    "interval_days": {"type": "number"},
                    "ease_factor": {"type": "number"},
                    "due_date": {"type": "string", "format": "date"},
                    "last_reviewed": {"type": "string", "format": "date"},
                    "consecutive_failures": {"type": "integer"}
                }
            }
        }
    }
}

schemas["reward_transaction.schema.json"] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://language-learning.app/schemas/reward_transaction.json",
    "title": "Reward Transaction",
    "description": "A deterministic reward transaction record",
    "type": "object",
    "required": ["transaction_id", "learner_id", "event_type", "xp_amount", "idempotency_key"],
    "additionalProperties": False,
    "properties": {
        "transaction_id": {"type": "string", "format": "uuid"},
        "learner_id": {"type": "string"},
        "event_type": {"type": "string"},
        "xp_amount": {"type": "integer", "minimum": 0},
        "idempotency_key": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "source_service": {"type": "string"},
        "previous_balance": {"type": "integer"},
        "new_balance": {"type": "integer"},
        "status": {"type": "string", "enum": ["pending", "completed", "reversed"]}
    }
}

schemas["integrity_risk_signal.schema.json"] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://language-learning.app/schemas/integrity_risk_signal.json",
    "title": "Integrity Risk Signal",
    "description": "Anomaly detection signal for anti-cheat system",
    "type": "object",
    "required": ["signal_id", "learner_id", "signal_type", "severity", "timestamp"],
    "additionalProperties": False,
    "properties": {
        "signal_id": {"type": "string", "format": "uuid"},
        "learner_id": {"type": "string"},
        "signal_type": {"type": "string", "enum": ["response_time_anomaly", "perfect_sequence", "off_session_submission", "duplicate_content", "multiple_accounts", "unusual_pattern"]},
        "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
        "details": {"type": "object"},
        "timestamp": {"type": "string", "format": "date-time"},
        "action_taken": {"type": "string"}
    }
}

schemas["security_event.schema.json"] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://language-learning.app/schemas/security_event.json",
    "title": "Security Event",
    "description": "A logged security event for audit and monitoring",
    "type": "object",
    "required": ["event_id", "event_type", "severity", "timestamp"],
    "additionalProperties": False,
    "properties": {
        "event_id": {"type": "string", "format": "uuid"},
        "event_type": {"type": "string", "enum": ["injection_attempt", "auth_failure", "auth_success", "unauthorized_access", "rate_limit_exceeded", "anomalous_pattern", "state_mutation_attempt", "config_change"]},
        "severity": {"type": "string", "enum": ["critical", "high", "medium", "low"]},
        "source": {"type": "string"},
        "user_id": {"type": "string"},
        "ip_address": {"type": "string"},
        "details": {"type": "object"},
        "timestamp": {"type": "string", "format": "date-time"},
        "action_taken": {"type": "string"}
    }
}

schemas["artifact_index.schema.json"] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://language-learning.app/schemas/artifact_index.json",
    "title": "Artifact Index",
    "description": "Index of all documentation artifacts with metadata",
    "type": "object",
    "required": ["artifacts"],
    "properties": {
        "artifacts": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["path", "type", "purpose", "version", "status"],
                "properties": {
                    "path": {"type": "string"},
                    "type": {"type": "string", "enum": ["documentation", "schema", "example", "diagram", "script", "test"]},
                    "purpose": {"type": "string"},
                    "version": {"type": "string"},
                    "status": {"type": "string", "enum": ["draft", "review", "approved", "deprecated"]},
                    "sha256": {"type": "string"},
                    "related_requirements": {"type": "array", "items": {"type": "string"}},
                    "dependencies": {"type": "array", "items": {"type": "string"}}
                }
            }
        }
    }
}

schemas["documentation_proof.schema.json"] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://language-learning.app/schemas/documentation_proof.json",
    "title": "Documentation Proof",
    "description": "Proof that the documentation task was completed according to specifications",
    "type": "object",
    "required": ["task_id", "verdict", "feature_completed", "documentation_only"],
    "additionalProperties": False,
    "properties": {
        "task_id": {"type": "string"},
        "verdict": {"type": "string", "enum": ["ACCEPTED", "REJECTED", "PENDING_REVIEW"]},
        "feature_completed": {"type": "boolean"},
        "documentation_only": {"type": "boolean"},
        "documents_created": {"type": "boolean"},
        "schemas_created": {"type": "boolean"},
        "examples_created": {"type": "boolean"},
        "artifact_index_created": {"type": "boolean"},
        "traceability_complete": {"type": "boolean"},
        "untraced_requirements": {"type": "integer", "minimum": 0},
        "contradictions_found": {"type": "integer", "minimum": 0},
        "unresolved_blockers": {"type": "array", "items": {"type": "string"}},
        "application_code_changed": {"type": "boolean"},
        "llm_calls_executed": {"type": "boolean"},
        "deployment_executed": {"type": "boolean"},
        "security_requirements_documented": {"type": "boolean"},
        "anti_cheat_documented": {"type": "boolean"},
        "prompt_injection_defense_documented": {"type": "boolean"},
        "tests": {
            "type": "object",
            "properties": {
                "documentation_tests_passed": {"type": "boolean"},
                "schema_validation_passed": {"type": "boolean"},
                "link_validation_passed": {"type": "boolean"}
            }
        },
        "git": {
            "type": "object",
            "required": ["branch", "starting_commit", "final_commit", "commit_created", "commit_pushed", "git_clean", "head_matches_origin"],
            "properties": {
                "branch": {"type": "string"},
                "starting_commit": {"type": "string"},
                "final_commit": {"type": "string"},
                "commit_created": {"type": "boolean"},
                "commit_pushed": {"type": "boolean"},
                "git_clean": {"type": "boolean"},
                "head_matches_origin": {"type": "boolean"}
            }
        }
    }
}

# Write all schemas
for filename, schema in schemas.items():
    path = os.path.join(SCHEMA_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)
    print(f"Created schema: {filename}")

# Also create example fixtures for each schema
EXAMPLES_DIR = "f:/Dev/Projects/LANGUAGE-LEARNING-APP/documents/language_learning_app/examples"
os.makedirs(EXAMPLES_DIR, exist_ok=True)

# Create a comprehensive example fixture file for each schema
for filename, schema in schemas.items():
    name = filename.replace(".schema.json", "")
    fixture_name = f"fixture_{name}.json"
    fixture_path = os.path.join(EXAMPLES_DIR, fixture_name)

    if filename == "documentation_proof.schema.json":
        continue  # Will be created separately

    # Create a minimal valid fixture by filling in required fields
    fixture = {}
    if "properties" in schema:
        for req in schema.get("required", []):
            prop = schema["properties"].get(req, {})
            if prop.get("type") == "string":
                if "format" in prop:
                    if prop["format"] == "uuid":
                        fixture[req] = "00000000-0000-0000-0000-000000000000"
                    elif prop["format"] == "date-time":
                        fixture[req] = "2026-06-09T00:00:00Z"
                    elif prop["format"] == "date":
                        fixture[req] = "2026-06-09"
                    elif "enum" in prop:
                        fixture[req] = prop["enum"][0]
                    else:
                        fixture[req] = "test_" + req
                elif "enum" in prop:
                    fixture[req] = prop["enum"][0]
                else:
                    fixture[req] = "test_" + req
            elif prop.get("type") == "integer":
                fixture[req] = 1
            elif prop.get("type") == "number":
                fixture[req] = 0.5
            elif prop.get("type") == "boolean":
                fixture[req] = True
            elif prop.get("type") == "array":
                fixture[req] = []
            elif prop.get("type") == "object":
                fixture[req] = {}

    with open(fixture_path, "w", encoding="utf-8") as f:
        json.dump(fixture, f, indent=2, ensure_ascii=False)
    print(f"Created fixture: {fixture_name}")

print(f"\nTotal schemas: {len(schemas)}")
print("Done!")
