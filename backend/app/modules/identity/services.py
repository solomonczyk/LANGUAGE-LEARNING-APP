"""Identity services — local auth stub."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.shared.exceptions.domain import ConflictError, NotFoundError


async def register_user(
    db: AsyncSession,
    username: str,
    display_name: str,
    email: str | None = None,
) -> User:
    """Register a new local user (auth stub)."""
    existing = await db.scalar(select(User).where(User.username == username))
    if existing:
        raise ConflictError(f"User '{username}' already exists.")

    user = User(
        username=username,
        display_name=display_name,
        email=email,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


async def get_user_by_id(db: AsyncSession, user_id: str) -> User:
    """Get a user by ID."""
    from uuid import UUID

    user = await db.get(User, UUID(user_id))
    if not user:
        raise NotFoundError(f"User not found: {user_id}")
    return user
