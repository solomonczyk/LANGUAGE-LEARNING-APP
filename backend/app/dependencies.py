"""FastAPI dependency injection."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

DbSession = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user_id(x_user_id: Annotated[str | None, Header()] = None) -> str:
    """Extract or stub the current user ID.

    In local development mode with auth stub enabled, the user ID comes
    from the X-User-Id header. In production this would verify a JWT.
    """
    from app.config import settings

    if settings.auth_stub_enabled:
        user_id = x_user_id or settings.auth_stub_user_id
    else:
        if not x_user_id:
            raise HTTPException(
                status_code=401,
                detail={
                    "error": {
                        "code": "UNAUTHORIZED",
                        "message": "Authentication required.",
                        "details": {},
                        "trace_id": "",
                        "retryable": False,
                    }
                },
            )
        user_id = x_user_id

    return user_id


CurrentUserId = Annotated[str, Depends(get_current_user_id)]
