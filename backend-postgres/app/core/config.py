from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List


def _split_csv(value: str) -> List[str]:
    items = [v.strip() for v in value.split(",") if v.strip()]
    return items


@dataclass(frozen=True)
class Settings:
    app_name: str = "To-Do Backend"
    api_v1_prefix: str = "/api/v1"
    database_url: str = os.getenv("DATABASE_URL", "sqlite+pysqlite:///./todo.db")
    cors_origins: List[str] = None  # set in __post_init__


    def __post_init__(self):
        object.__setattr__(
            self,
            "cors_origins",
            _split_csv(os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173")),
        )


settings = Settings()
