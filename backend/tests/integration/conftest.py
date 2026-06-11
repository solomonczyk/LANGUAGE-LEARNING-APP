"""Integration test fixtures."""

from __future__ import annotations

import pytest
import httpx


@pytest.fixture
async def client() -> httpx.AsyncClient:
    """HTTP client for testing the running backend."""
    async with httpx.AsyncClient(timeout=30.0) as c:
        yield c
