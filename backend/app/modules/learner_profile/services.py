"""Learner profile services."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import LearnerProfile
from app.shared.exceptions.domain import NotFoundError


async def create_or_update_profile(
    db: AsyncSession,
    user_id: str,
    target_language: str,
    native_language: str,
    learning_goal: str | None = None,
    preferred_lesson_duration: int = 10,
    self_reported_level: str = "A1",
) -> LearnerProfile:
    """Create or update a learner profile."""
    uid = UUID(user_id)
    stmt = select(LearnerProfile).where(LearnerProfile.user_id == uid)
    result = await db.execute(stmt)
    profile = result.scalar_one_or_none()

    if profile:
        profile.target_language = target_language
        profile.native_language = native_language
        profile.learning_goal = learning_goal
        profile.preferred_lesson_duration = preferred_lesson_duration
        profile.self_reported_level = self_reported_level
    else:
        profile = LearnerProfile(
            user_id=uid,
            target_language=target_language,
            native_language=native_language,
            learning_goal=learning_goal,
            preferred_lesson_duration=preferred_lesson_duration,
            self_reported_level=self_reported_level,
        )
        db.add(profile)

    await db.flush()
    await db.refresh(profile)
    return profile


async def get_profile(db: AsyncSession, user_id: str) -> LearnerProfile:
    """Get learner profile by user ID."""
    uid = UUID(user_id)
    stmt = select(LearnerProfile).where(LearnerProfile.user_id == uid)
    result = await db.execute(stmt)
    profile = result.scalar_one_or_none()
    if not profile:
        raise NotFoundError("Learner profile not found. Complete onboarding first.")
    return profile
