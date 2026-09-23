import os
from pydantic import Field

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore
except ImportError:
    # Graceful fallback when viewed in an editor using global interpreter without pydantic-settings
    from pydantic import BaseModel as BaseSettings  # type: ignore

    def SettingsConfigDict(**kwargs):  # type: ignore
        return kwargs


class MLSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ENVIRONMENT: str = Field(default="local")
    LOG_LEVEL: str = Field(default="INFO")

    ML_HOST: str = Field(default="0.0.0.0")
    ML_PORT: int = Field(default=8001)

    MODEL_ARTIFACTS_DIR: str = Field(default="./models")
    FEATURE_CONFIG_PATH: str = Field(default="./config/features.json")
    SCORING_CONFIG_PATH: str = Field(default="./config/scoring_rules.json")
    ENABLE_SHAP_EXPLANATIONS: bool = Field(default=True)
    RETRAIN_INTERVAL_HOURS: int = Field(default=12)
    ENABLE_AUTO_RETRAINING: bool = Field(default=True)


ml_settings = MLSettings()
