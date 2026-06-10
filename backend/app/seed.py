"""Seed data for local development — one learner, one diagnostic, one lesson."""

from __future__ import annotations

import asyncio
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_factory, engine
from app.models import (
    LessonDefinition,
    User,
)


async def seed_database() -> None:
    """Seed the database with initial development data."""
    async with async_session_factory() as db:
        # Check if seed data already exists
        result = await db.execute(select(User).where(User.username == "local_learner"))
        existing = result.scalar_one_or_none()
        if existing:
            print("Seed data already exists, skipping.")
            return

        # 1. Create local learner user
        local_learner_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
        learner = User(
            id=local_learner_id,
            username="local_learner",
            display_name="Local Learner",
            email="learner@local.dev",
            is_active=True,
            is_operator=False,
        )
        db.add(learner)

        # 2. Create operator user
        operator_id = uuid.UUID("00000000-0000-0000-0000-000000000002")
        operator = User(
            id=operator_id,
            username="local_operator",
            display_name="Local Operator",
            email="operator@local.dev",
            is_active=True,
            is_operator=True,
        )
        db.add(operator)

        # 3. Create personal narrative lesson definition
        lesson = LessonDefinition(
            id=uuid.UUID("00000000-0000-0000-0000-000000000010"),
            lesson_type="personal_narrative",
            title="My Morning with My Pet",
            description="Describe how your morning started and what happened with your pet.",
            communicative_goal="Describe a personal daily routine with a focus on sequence of events and interaction with a pet.",
            grammar_focus=[
                {"feature": "Past tense", "priority": "high"},
                {"feature": "Subject-verb agreement", "priority": "medium"},
            ],
            vocabulary_focus=[
                {"word": "morning", "category": "time"},
                {"word": "pet", "category": "animals"},
                {"word": "breakfast", "category": "food"},
                {"word": "walk", "category": "routine"},
            ],
            narrative_focus="Sequence of events with time markers (first, then, after that)",
            scaffolding_mode="moderate",
            cognitive_budget="low",
            assessment_criteria={
                "min_length": 30,
                "required_elements": ["time_markers", "sequence_of_events"],
                "focus_skills": ["past_tense", "vocabulary_range"],
            },
            allowed_attempts=3,
            version="1.0.0",
            is_active=True,
        )
        db.add(lesson)

        await db.commit()
        print("Database seeded successfully!")
        print(f"  - Local learner: {learner.username} (ID: {learner.id})")
        print(f"  - Local operator: {operator.username} (ID: {operator.id})")
        print(f"  - Lesson: {lesson.title} (ID: {lesson.id})")


async def main() -> None:
    try:
        await seed_database()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
