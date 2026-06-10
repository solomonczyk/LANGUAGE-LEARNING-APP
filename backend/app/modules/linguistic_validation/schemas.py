"""Linguistic validation Pydantic schemas."""

from __future__ import annotations

from pydantic import BaseModel


class LinguisticValidationResult(BaseModel):
    passed: bool
    details: dict
