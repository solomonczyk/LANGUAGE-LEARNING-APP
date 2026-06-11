"""Database engine and session management."""

from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=settings.database_echo,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
)

async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for all models."""


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that yields a database session.

    Session commit is delegated to route handlers to ensure
    data is committed before the HTTP response is sent.
    FastAPI yields dependency cleanup runs AFTER response delivery,
    so committing here would create a race condition where the
    next request cannot find data the previous request wrote.
    """
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
