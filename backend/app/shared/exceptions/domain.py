"""Domain exception classes with canonical error codes."""

from __future__ import annotations


class AppException(Exception):
    """Base application exception."""

    code: str = "INTERNAL_ERROR"
    message: str = "An unexpected error occurred."
    details: dict = {}
    retryable: bool = False
    status_code: int = 500

    def __init__(
        self,
        message: str | None = None,
        details: dict | None = None,
        retryable: bool | None = None,
    ) -> None:
        if message:
            self.message = message
        if details:
            self.details = details
        if retryable is not None:
            self.retryable = retryable
        super().__init__(self.message)

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details,
            "retryable": self.retryable,
        }


class ValidationError(AppException):
    code = "VALIDATION_ERROR"
    status_code = 422
    retryable = False


class UnauthorizedError(AppException):
    code = "UNAUTHORIZED"
    status_code = 401
    retryable = False


class ForbiddenError(AppException):
    code = "FORBIDDEN"
    status_code = 403
    retryable = False


class NotFoundError(AppException):
    code = "NOT_FOUND"
    status_code = 404
    retryable = False


class ConflictError(AppException):
    code = "CONFLICT"
    status_code = 409
    retryable = False


class InvalidStateTransitionError(AppException):
    code = "INVALID_STATE_TRANSITION"
    status_code = 409
    retryable = False


class IdempotencyConflictError(AppException):
    code = "IDEMPOTENCY_CONFLICT"
    status_code = 422
    retryable = False


class MockAIInvalidOutputError(AppException):
    code = "MOCK_AI_INVALID_OUTPUT"
    status_code = 502
    retryable = False


class LinguisticValidationFailedError(AppException):
    code = "LINGUISTIC_VALIDATION_FAILED"
    status_code = 422
    retryable = False


class PedagogicalValidationFailedError(AppException):
    code = "PEDAGOGICAL_VALIDATION_FAILED"
    status_code = 422
    retryable = False


class AuditWriteFailedError(AppException):
    code = "AUDIT_WRITE_FAILED"
    status_code = 500
    retryable = True
