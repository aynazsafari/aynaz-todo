from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Aynaz To-Do"
    api_v1_prefix: str = "/api/v1"

    mongo_url: str = "mongodb://localhost:27017"
    mongo_db: str = "todo"

    # comma-separated in env; parsed below
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    @classmethod
    def model_validate_settings(cls, values):
        return super().model_validate(values)

settings = Settings()

# Support CORS_ORIGINS as comma-separated string
import os
_raw = os.getenv("CORS_ORIGINS")
if _raw:
    settings.cors_origins = [x.strip() for x in _raw.split(",") if x.strip()]
