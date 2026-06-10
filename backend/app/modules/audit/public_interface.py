"""Public interface for the audit module."""

from app.modules.audit.services import get_events, record_event

__all__ = ["record_event", "get_events"]
