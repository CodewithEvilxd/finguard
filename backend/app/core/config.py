import os
from typing import List, Optional
from pydantic import Field, field_validator

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore
except ImportError:
    # Graceful fallback when viewed in an editor using global interpreter without pydantic-settings
    from pydantic import BaseModel as BaseSettings  # type: ignore

    def SettingsConfigDict(**kwargs):  # type: ignore
        return kwargs


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ENVIRONMENT: str = Field(default="local", description="Runtime environment: local, staging, production")
    LOG_LEVEL: str = Field(default="INFO", description="Log level: DEBUG, INFO, WARNING, ERROR")
    DEBUG: bool = Field(default=False, description="Debug mode flag")

    BACKEND_HOST: str = Field(default="0.0.0.0", description="FastAPI bind host")
    BACKEND_PORT: int = Field(default=8000, description="FastAPI bind port")
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000",
        description="Comma-separated list of allowed origins",
    )

    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./finguard_local.db",
        description="PostgreSQL async connection string or SQLite for local dev",
    )

    SUPABASE_URL: Optional[str] = Field(default=None, description="Supabase project URL")
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = Field(default=None, description="Supabase service role secret key")
    SUPABASE_JWT_SECRET: Optional[str] = Field(default=None, description="JWT verification secret")

    ML_SERVICE_URL: str = Field(
        default="http://localhost:8001",
        description="URL to the independent ML Backend inference service",
    )

    LLM_PROVIDER: str = Field(default="openai", description="AI provider: openai, anthropic, groq, local")
    LLM_API_KEY: Optional[str] = Field(default=None, description="LLM API secret key")
    LLM_MODEL: str = Field(default="gpt-4o-mini", description="LLM model identifier")

    EMBEDDING_PROVIDER: str = Field(default="local", description="Embedding provider: local, openai")
    EMBEDDING_MODEL: str = Field(default="all-MiniLM-L6-v2", description="Embedding model name")

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        valid_envs = {"local", "staging", "production", "test"}
        if v.lower() not in valid_envs:
            raise ValueError(f"Invalid ENVIRONMENT: {v}. Must be one of {valid_envs}")
        return v.lower()


settings = Settings()
