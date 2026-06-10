"""Initial database schema — all tables for vertical slice 003

Revision ID: 001
Revises:
Create Date: 2026-06-10
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Users
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("username", sa.String(255), unique=True, nullable=False),
        sa.Column("display_name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), unique=True, nullable=True),
        sa.Column("is_active", sa.Boolean(), default=True, nullable=False),
        sa.Column("is_operator", sa.Boolean(), default=False, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_users_username", "users", ["username"])
    op.create_index("ix_users_email", "users", ["email"])

    # Learner profiles
    op.create_table(
        "learner_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False),
        sa.Column("target_language", sa.String(50), nullable=False),
        sa.Column("native_language", sa.String(50), nullable=False),
        sa.Column("learning_goal", sa.String(255), nullable=True),
        sa.Column("preferred_lesson_duration", sa.Integer(), default=10),
        sa.Column("self_reported_level", sa.String(10), default="A1"),
        sa.Column("profile_status", sa.String(50), default="created"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_learner_profiles_user_id", "learner_profiles", ["user_id"])

    # Diagnostic sessions
    op.create_table(
        "diagnostic_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(50), default="CREATED", nullable=False),
        sa.Column("current_step", sa.Integer(), default=0),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_diagnostic_sessions_user_id", "diagnostic_sessions", ["user_id"])
    op.create_index("ix_diagnostic_sessions_status", "diagnostic_sessions", ["status"])

    # Diagnostic responses
    op.create_table(
        "diagnostic_responses",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("diagnostic_sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("question_key", sa.String(100), nullable=False),
        sa.Column("response_data", postgresql.JSONB(), nullable=False, default=dict),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_diagnostic_responses_session_id", "diagnostic_responses", ["session_id"])

    # Skill assessments
    op.create_table(
        "skill_assessments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("diagnostic_sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("skill_name", sa.String(100), nullable=False),
        sa.Column("cefr_level", sa.String(10), nullable=False),
        sa.Column("confidence", sa.Float(), default=0.0),
        sa.Column("evidence", postgresql.JSONB(), nullable=False, default=dict),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_skill_assessments_session_id", "skill_assessments", ["session_id"])

    # Learning entry contracts
    op.create_table(
        "learning_entry_contracts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("target_language", sa.String(50), nullable=False),
        sa.Column("support_language", sa.String(50), nullable=False),
        sa.Column("lesson_duration_minutes", sa.Integer(), default=10),
        sa.Column("active_vocabulary_budget", sa.Integer(), default=5),
        sa.Column("grammar_focus_count", sa.Integer(), default=2),
        sa.Column("max_primary_corrections", sa.Integer(), default=3),
        sa.Column("scaffolding_mode", sa.String(50), default="moderate"),
        sa.Column("lesson_complexity", sa.String(20), default="simple"),
        sa.Column("diagnostic_profile_snapshot", postgresql.JSONB(), nullable=False, default=dict),
        sa.Column("version", sa.String(20), default="1.0.0"),
        sa.Column("status", sa.String(50), default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_learning_entry_contracts_user_id", "learning_entry_contracts", ["user_id"])
    op.create_unique_constraint("uq_user_contract_version", "learning_entry_contracts", ["user_id", "version"])

    # Lesson definitions
    op.create_table(
        "lesson_definitions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("lesson_type", sa.String(100), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("communicative_goal", sa.String(500), nullable=False),
        sa.Column("grammar_focus", postgresql.JSONB(), nullable=False, default=list),
        sa.Column("vocabulary_focus", postgresql.JSONB(), nullable=False, default=list),
        sa.Column("narrative_focus", sa.String(500), nullable=True),
        sa.Column("scaffolding_mode", sa.String(50), default="moderate"),
        sa.Column("cognitive_budget", sa.String(20), default="low"),
        sa.Column("assessment_criteria", postgresql.JSONB(), nullable=False, default=dict),
        sa.Column("allowed_attempts", sa.Integer(), default=3),
        sa.Column("version", sa.String(20), default="1.0.0"),
        sa.Column("is_active", sa.Boolean(), default=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_lesson_definitions_lesson_type", "lesson_definitions", ["lesson_type"])

    # Lesson sessions
    op.create_table(
        "lesson_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("lesson_definition_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("lesson_definitions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(50), default="CREATED", nullable=False),
        sa.Column("current_attempt", sa.Integer(), default=0),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_lesson_sessions_user_id", "lesson_sessions", ["user_id"])
    op.create_index("ix_lesson_sessions_status", "lesson_sessions", ["status"])

    # Lesson attempts
    op.create_table(
        "lesson_attempts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("lesson_sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("attempt_number", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(50), default="in_progress"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_lesson_attempts_session_id", "lesson_attempts", ["session_id"])
    op.create_unique_constraint("uq_session_attempt", "lesson_attempts", ["session_id", "attempt_number"])

    # Submissions
    op.create_table(
        "submissions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("lesson_session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("lesson_sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("lesson_definition_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("lesson_definitions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(50), default="RECEIVED", nullable=False),
        sa.Column("source_text", sa.Text(), nullable=False),
        sa.Column("normalized_text", sa.Text(), nullable=True),
        sa.Column("idempotency_key", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_submissions_user_id", "submissions", ["user_id"])
    op.create_index("ix_submissions_lesson_session_id", "submissions", ["lesson_session_id"])
    op.create_index("ix_submissions_idempotency_key", "submissions", ["idempotency_key"])

    # AI analysis requests
    op.create_table(
        "ai_analysis_requests",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("submission_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(50), default="CREATED", nullable=False),
        sa.Column("analysis_type", sa.String(100), default="text_analysis"),
        sa.Column("request_data", postgresql.JSONB(), nullable=False, default=dict),
        sa.Column("retry_count", sa.Integer(), default=0),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_ai_analysis_requests_submission_id", "ai_analysis_requests", ["submission_id"])

    # AI analysis results
    op.create_table(
        "ai_analysis_results",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("submission_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("request_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("ai_analysis_requests.id", ondelete="CASCADE"), nullable=False),
        sa.Column("analysis_version", sa.String(50), nullable=False),
        sa.Column("raw_output", postgresql.JSONB(), nullable=False, default=dict),
        sa.Column("output_schema_valid", sa.Boolean(), default=False),
        sa.Column("status", sa.String(50), default="raw"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_ai_analysis_results_submission_id", "ai_analysis_results", ["submission_id"])

    # Validation results
    op.create_table(
        "validation_results",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("submission_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("validation_type", sa.String(100), nullable=False),
        sa.Column("passed", sa.Boolean(), nullable=False),
        sa.Column("details", postgresql.JSONB(), nullable=False, default=dict),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_validation_results_submission_id", "validation_results", ["submission_id"])

    # Mastery records
    op.create_table(
        "mastery_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("skill_name", sa.String(100), nullable=False),
        sa.Column("cefr_level", sa.String(10), nullable=False),
        sa.Column("current_state", sa.String(50), default="introduced"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_mastery_records_user_id", "mastery_records", ["user_id"])
    op.create_unique_constraint("uq_user_skill_cefr", "mastery_records", ["user_id", "skill_name", "cefr_level"])

    # Mastery evidence
    op.create_table(
        "mastery_evidence",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("submission_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("lesson_session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("lesson_sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("skill_name", sa.String(100), nullable=False),
        sa.Column("evidence_type", sa.String(50), nullable=False),
        sa.Column("evidence_data", postgresql.JSONB(), nullable=False, default=dict),
        sa.Column("status", sa.String(50), default="PENDING"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_mastery_evidence_user_id", "mastery_evidence", ["user_id"])

    # Audit events
    op.create_table(
        "audit_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("event_type", sa.String(100), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("module", sa.String(100), nullable=False),
        sa.Column("entity_type", sa.String(100), nullable=False),
        sa.Column("entity_id", sa.String(255), nullable=False),
        sa.Column("data", postgresql.JSONB(), nullable=False, default=dict),
        sa.Column("trace_id", sa.String(255), nullable=True),
        sa.Column("event_timestamp", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_audit_events_event_type", "audit_events", ["event_type"])
    op.create_index("ix_audit_events_user_id", "audit_events", ["user_id"])
    op.create_index("ix_audit_events_entity_id", "audit_events", ["entity_id"])


def downgrade() -> None:
    op.drop_table("audit_events")
    op.drop_table("mastery_evidence")
    op.drop_table("mastery_records")
    op.drop_table("validation_results")
    op.drop_table("ai_analysis_results")
    op.drop_table("ai_analysis_requests")
    op.drop_table("submissions")
    op.drop_table("lesson_attempts")
    op.drop_table("lesson_sessions")
    op.drop_table("lesson_definitions")
    op.drop_table("learning_entry_contracts")
    op.drop_table("skill_assessments")
    op.drop_table("diagnostic_responses")
    op.drop_table("diagnostic_sessions")
    op.drop_table("learner_profiles")
    op.drop_table("users")
