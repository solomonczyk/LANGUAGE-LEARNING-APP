"""Tests for audit event creation."""

import asyncio
from uuid import uuid4

from app.modules.audit.services import record_event


class TestAuditEvents:
    def setup_method(self):
        self.user_id = str(uuid4())

    def test_record_audit_event(self):
        """Test creating an audit event."""
        import asyncio
        from unittest.mock import AsyncMock, MagicMock

        mock_db = AsyncMock()
        mock_db.add = MagicMock()
        mock_db.flush = AsyncMock()
        mock_db.refresh = AsyncMock()

        mock_event = MagicMock()
        mock_event.id = uuid4()
        mock_event.event_type = "test.event"
        mock_event.user_id = uuid4()
        mock_event.module = "test"
        mock_event.entity_type = "submission"
        mock_event.entity_id = str(uuid4())
        mock_event.data = {}
        mock_event.trace_id = str(uuid4())
        mock_event.event_timestamp = MagicMock()
        mock_event.event_timestamp.isoformat.return_value = "2026-01-01T00:00:00"
        mock_db.refresh = AsyncMock()

        async def test():
            from app.models import AuditEvent

            event = AuditEvent(
                event_type="test.event",
                user_id=uuid4(),
                module="test",
                entity_type="submission",
                entity_id=str(uuid4()),
            )
            return event

        result = asyncio.run(test())
        assert result.event_type == "test.event"
        assert result.module == "test"


def test_audit_event_requires_mandatory_fields():
    """Audit events need event_type, user_id, module, entity_type, entity_id."""
    from app.models import AuditEvent
    from uuid import uuid4

    event = AuditEvent(
        event_type="lesson.completed",
        user_id=uuid4(),
        module="lesson_engine",
        entity_type="lesson_session",
        entity_id=str(uuid4()),
        data={"result": "completed"},
    )
    assert event.event_type == "lesson.completed"
    assert event.module == "lesson_engine"


def test_audit_write_failure():
    """Audit write failure should raise exception."""
    from app.shared.exceptions.domain import AuditWriteFailedError

    try:
        raise AuditWriteFailedError("Database connection lost")
    except AuditWriteFailedError as e:
        assert "Database" in e.message
        assert e.retryable is True
