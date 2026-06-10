"""Application configuration via Pydantic Settings."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "Language Learning App"
    debug: bool = False
    api_prefix: str = "/api/v1"

    # Database
    database_url: str = "postgresql+asyncpg://llapp:llapp_dev@localhost:5432/llapp"
    database_echo: bool = False
    database_pool_size: int = 10
    database_max_overflow: int = 20

    # Auth stub (local development only)
    auth_stub_enabled: bool = True
    auth_stub_user_id: str = "00000000-0000-0000-0000-000000000001"
    auth_stub_user_name: str = "local_learner"

    # Security
    secret_key: str = "dev-secret-key-not-for-production"
    idempotency_key_expiry_hours: int = 24

    # Observability
    log_level: str = "INFO"
    structured_logging: bool = True

    # Mock AI
    mock_ai_enabled: bool = True
    mock_ai_fixture_mode: str = "valid"  # "valid" or "malformed"

    # CORS
    cors_origins: list[str] = ["*"]


settings = Settings()
