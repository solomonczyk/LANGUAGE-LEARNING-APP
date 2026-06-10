"""Public interface for the identity module."""

from app.modules.identity.services import register_user, get_user_by_id

__all__ = ["register_user", "get_user_by_id"]
