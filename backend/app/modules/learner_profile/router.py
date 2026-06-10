"""Learner profile API router."""

from __future__ import annotations

from fastapi import APIRouter

from app.dependencies import CurrentUserId, DbSession
from app.modules.learner_profile.schemas import ProfileCreateRequest, ProfileResponse
from app.modules.learner_profile.services import create_or_update_profile, get_profile

router = APIRouter(prefix="/learner-profile", tags=["learner-profile"])


@router.post("", response_model=ProfileResponse)
async def create_profile(body: ProfileCreateRequest, user_id: CurrentUserId, db: DbSession):
    """Create or update learner profile."""
    profile = await create_or_update_profile(
        db=db,
        user_id=user_id,
        target_language=body.target_language,
        native_language=body.native_language,
        learning_goal=body.learning_goal,
        preferred_lesson_duration=body.preferred_lesson_duration,
        self_reported_level=body.self_reported_level,
    )
    return ProfileResponse(
        id=str(profile.id),
        user_id=str(profile.user_id),
        target_language=profile.target_language,
        native_language=profile.native_language,
        learning_goal=profile.learning_goal,
        preferred_lesson_duration=profile.preferred_lesson_duration,
        self_reported_level=profile.self_reported_level,
        profile_status=profile.profile_status,
        created_at=profile.created_at.isoformat(),
        updated_at=profile.updated_at.isoformat(),
    )


@router.get("/me", response_model=ProfileResponse)
async def read_profile(user_id: CurrentUserId, db: DbSession):
    """Get current user's learner profile."""
    profile = await get_profile(db, user_id)
    return ProfileResponse(
        id=str(profile.id),
        user_id=str(profile.user_id),
        target_language=profile.target_language,
        native_language=profile.native_language,
        learning_goal=profile.learning_goal,
        preferred_lesson_duration=profile.preferred_lesson_duration,
        self_reported_level=profile.self_reported_level,
        profile_status=profile.profile_status,
        created_at=profile.created_at.isoformat(),
        updated_at=profile.updated_at.isoformat(),
    )
