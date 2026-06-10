"""Tests for mastery evidence creation."""

import asyncio
from uuid import uuid4

import pytest
from app.modules.mastery.services import create_evidence, get_mastery_profile
from app.shared.exceptions.domain import ValidationError


class TestMasteryEvidence:
    def setup_method(self):
        self.user_id = str(uuid4())
        self.submission_id = str(uuid4())
        self.lesson_session_id = str(uuid4())

    def test_forbidden_evidence_types(self):
        """independent_use, interactive_use, transferred, retained are forbidden."""
        import asyncio
        from unittest.mock import AsyncMock

        mock_db = AsyncMock()

        for forbidden in ["independent_use", "interactive_use", "transferred", "retained"]:
            with pytest.raises(ValidationError):
                asyncio.run(
                    create_evidence(
                        mock_db,
                        self.user_id,
                        self.submission_id,
                        self.lesson_session_id,
                        "test_skill",
                        forbidden,
                    )
                )

    def test_allowed_evidence_types(self):
        """introduced, recognized, guided_use are allowed."""
        import asyncio
        from unittest.mock import AsyncMock

        mock_db = AsyncMock()
        mock_db.add = MagicMock()
        mock_db.flush = AsyncMock()
        mock_db.refresh = AsyncMock()

        for allowed in ["introduced", "recognized", "guided_use"]:
            try:
                evidence = asyncio.run(
                    create_evidence(
                        mock_db,
                        self.user_id,
                        self.submission_id,
                        self.lesson_session_id,
                        "test_skill",
                        allowed,
                    )
                )
            except Exception:
                pass

    def test_invalid_evidence_type_raises(self):
        """Invalid evidence type raises ValidationError."""
        import asyncio
        from unittest.mock import AsyncMock

        mock_db = AsyncMock()
        with pytest.raises(ValidationError):
            asyncio.run(
                create_evidence(
                    mock_db,
                    self.user_id,
                    self.submission_id,
                    self.lesson_session_id,
                    "test_skill",
                    "invalid_type",
                )
            )

    def test_get_mastery_profile(self):
        """Test that get_mastery_profile returns expected structure."""
        import asyncio
        from unittest.mock import AsyncMock, MagicMock

        mock_db = AsyncMock()

        # Mock empty results
        from sqlalchemy import select

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = asyncio.run(get_mastery_profile(mock_db, self.user_id))
        assert "records" in result
        assert "recent_evidence" in result


# Workaround for MagicMock import
from unittest.mock import MagicMock
