"""SQLAlchemy ORM models for all database entities."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.shared.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class User(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_operator: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    learner_profile = relationship("LearnerProfile", back_populates="user", uselist=False)
    diagnostic_sessions = relationship("DiagnosticSession", back_populates="user")
    lesson_sessions = relationship("LessonSession", back_populates="user")


class LearnerProfile(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "learner_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    target_language: Mapped[str] = mapped_column(String(50), nullable=False)
    native_language: Mapped[str] = mapped_column(String(50), nullable=False)
    learning_goal: Mapped[str] = mapped_column(String(255), nullable=True)
    preferred_lesson_duration: Mapped[int] = mapped_column(Integer, default=10)
    self_reported_level: Mapped[str] = mapped_column(String(10), default="A1")
    profile_status: Mapped[str] = mapped_column(String(50), default="created")

    user = relationship("User", back_populates="learner_profile")


class DiagnosticSession(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "diagnostic_sessions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(String(50), default="CREATED", nullable=False)
    current_step: Mapped[int] = mapped_column(Integer, default=0)

    user = relationship("User", back_populates="diagnostic_sessions")
    responses = relationship("DiagnosticResponse", back_populates="session", cascade="all, delete-orphan")
    skill_assessments = relationship("SkillAssessment", back_populates="session", cascade="all, delete-orphan")


class DiagnosticResponse(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "diagnostic_responses"

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("diagnostic_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    question_key: Mapped[str] = mapped_column(String(100), nullable=False)
    response_data: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    session = relationship("DiagnosticSession", back_populates="responses")


class SkillAssessment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "skill_assessments"

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("diagnostic_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    skill_name: Mapped[str] = mapped_column(String(100), nullable=False)
    cefr_level: Mapped[str] = mapped_column(String(10), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    evidence: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    session = relationship("DiagnosticSession", back_populates="skill_assessments")


class LearningEntryContract(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "learning_entry_contracts"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    target_language: Mapped[str] = mapped_column(String(50), nullable=False)
    support_language: Mapped[str] = mapped_column(String(50), nullable=False)
    lesson_duration_minutes: Mapped[int] = mapped_column(Integer, default=10)
    active_vocabulary_budget: Mapped[int] = mapped_column(Integer, default=5)
    grammar_focus_count: Mapped[int] = mapped_column(Integer, default=2)
    max_primary_corrections: Mapped[int] = mapped_column(Integer, default=3)
    scaffolding_mode: Mapped[str] = mapped_column(String(50), default="moderate")
    lesson_complexity: Mapped[str] = mapped_column(String(20), default="simple")
    diagnostic_profile_snapshot: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    version: Mapped[str] = mapped_column(String(20), default="1.0.0")
    status: Mapped[str] = mapped_column(String(50), default="active")

    __table_args__ = (
        UniqueConstraint("user_id", "version", name="uq_user_contract_version"),
    )


class LessonDefinition(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "lesson_definitions"

    lesson_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    communicative_goal: Mapped[str] = mapped_column(String(500), nullable=False)
    grammar_focus: Mapped[dict] = mapped_column(JSONB, nullable=False, default=list)
    vocabulary_focus: Mapped[dict] = mapped_column(JSONB, nullable=False, default=list)
    narrative_focus: Mapped[str] = mapped_column(String(500), nullable=True)
    scaffolding_mode: Mapped[str] = mapped_column(String(50), default="moderate")
    cognitive_budget: Mapped[str] = mapped_column(String(20), default="low")
    assessment_criteria: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    allowed_attempts: Mapped[int] = mapped_column(Integer, default=3)
    version: Mapped[str] = mapped_column(String(20), default="1.0.0")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class LessonSession(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "lesson_sessions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    lesson_definition_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("lesson_definitions.id", ondelete="CASCADE"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(String(50), default="CREATED", nullable=False)
    current_attempt: Mapped[int] = mapped_column(Integer, default=0)

    user = relationship("User", back_populates="lesson_sessions")
    lesson_definition = relationship("LessonDefinition")
    submissions = relationship("Submission", back_populates="lesson_session", cascade="all, delete-orphan")
    attempts = relationship("LessonAttempt", back_populates="session", cascade="all, delete-orphan")


class LessonAttempt(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "lesson_attempts"

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("lesson_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="in_progress")

    session = relationship("LessonSession", back_populates="attempts")

    __table_args__ = (
        UniqueConstraint("session_id", "attempt_number", name="uq_session_attempt"),
    )


class Submission(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "submissions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    lesson_session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("lesson_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    lesson_definition_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("lesson_definitions.id", ondelete="CASCADE"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(String(50), default="RECEIVED", nullable=False)
    source_text: Mapped[str] = mapped_column(Text, nullable=False)
    normalized_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    idempotency_key: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)

    lesson_session = relationship("LessonSession", back_populates="submissions")
    analysis_requests = relationship("AIAnalysisRequest", back_populates="submission", cascade="all, delete-orphan")
    analysis_results = relationship("AIAnalysisResult", back_populates="submission", cascade="all, delete-orphan")
    validation_results = relationship("ValidationResult", back_populates="submission", cascade="all, delete-orphan")


class AIAnalysisRequest(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "ai_analysis_requests"

    submission_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("submissions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[str] = mapped_column(String(50), default="CREATED", nullable=False)
    analysis_type: Mapped[str] = mapped_column(String(100), default="text_analysis")
    request_data: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)

    submission = relationship("Submission", back_populates="analysis_requests")
    results = relationship("AIAnalysisResult", back_populates="request", cascade="all, delete-orphan")


class AIAnalysisResult(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "ai_analysis_results"

    submission_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("submissions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("ai_analysis_requests.id", ondelete="CASCADE"),
        nullable=False,
    )
    analysis_version: Mapped[str] = mapped_column(String(50), nullable=False)
    raw_output: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    output_schema_valid: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(50), default="raw")

    submission = relationship("Submission", back_populates="analysis_results")
    request = relationship("AIAnalysisRequest", back_populates="results")


class ValidationResult(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "validation_results"

    submission_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("submissions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    validation_type: Mapped[str] = mapped_column(String(100), nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    details: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    submission = relationship("Submission", back_populates="validation_results")


class MasteryRecord(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "mastery_records"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    skill_name: Mapped[str] = mapped_column(String(100), nullable=False)
    cefr_level: Mapped[str] = mapped_column(String(10), nullable=False)
    current_state: Mapped[str] = mapped_column(String(50), default="introduced")

    __table_args__ = (
        UniqueConstraint("user_id", "skill_name", "cefr_level", name="uq_user_skill_cefr"),
    )


class MasteryEvidence(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "mastery_evidence"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    submission_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False
    )
    lesson_session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("lesson_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    skill_name: Mapped[str] = mapped_column(String(100), nullable=False)
    evidence_type: Mapped[str] = mapped_column(String(50), nullable=False)
    evidence_data: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), default="PENDING")


class AuditEvent(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "audit_events"

    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    module: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    data: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    trace_id: Mapped[str] = mapped_column(String(255), nullable=True)
    event_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
