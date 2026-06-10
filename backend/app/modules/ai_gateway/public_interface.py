"""Public interface for the ai_gateway module."""

from app.modules.ai_gateway.services import analyze_submission, get_analysis_result

__all__ = ["analyze_submission", "get_analysis_result"]
