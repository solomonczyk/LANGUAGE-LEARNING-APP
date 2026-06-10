"""Identity module API router."""

from __future__ import annotations

from fastapi import APIRouter

from app.dependencies import CurrentUserId, DbSession
from app.modules.identity.schemas import LoginRequest, RegisterRequest, UserResponse
from app.modules.identity.services import get_user_by_id, register_user

router = APIRouter(prefix="/identity", tags=["identity"])


@router.post("/register", response_model=UserResponse)
async def register(body: RegisterRequest, db: DbSession):
    """Register a new local user."""
    user = await register_user(db, body.username, body.display_name, body.email)
    return UserResponse(
        id=str(user.id),
        username=user.username,
        display_name=user.display_name,
        email=user.email,
        is_active=user.is_active,
        is_operator=user.is_operator,
    )


@router.post("/login", response_model=UserResponse)
async def login(body: LoginRequest, db: DbSession):
    """Stub login — returns user by username."""
    from sqlalchemy import select

    from app.models import User as UserModel

    stmt = select(UserModel).where(UserModel.username == body.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        from app.shared.exceptions.domain import NotFoundError

        raise NotFoundError(f"User '{body.username}' not found. Register first.")

    return UserResponse(
        id=str(user.id),
        username=user.username,
        display_name=user.display_name,
        email=user.email,
        is_active=user.is_active,
        is_operator=user.is_operator,
    )


@router.get("/me", response_model=UserResponse)
async def get_me(user_id: CurrentUserId, db: DbSession):
    """Get current user info."""
    user = await get_user_by_id(db, user_id)
    return UserResponse(
        id=str(user.id),
        username=user.username,
        display_name=user.display_name,
        email=user.email,
        is_active=user.is_active,
        is_operator=user.is_operator,
    )
