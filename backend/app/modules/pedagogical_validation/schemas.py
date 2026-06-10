"""Pedagogical validation Pydantic schemas."""

from __future__ import annotations

from pydantic import BaseModel


class PedagogicalValidationResult(BaseModel):
    passed: bool
    details: dict
