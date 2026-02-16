from typing import Annotated

from pydantic import Field, HttpUrl, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = f"{ENV_FILE}",
        env_file_encoding="utf-8",
        extra="ignore", 
    )

    port: Annotated[int, Field(default=8000)]
    app_secret: Annotated[
        str,
        Field(alias="APP_SECRET", min_length=32),
    ]
    pg_dsn: Annotated[
        PostgresDsn,
        Field(
            alias="DATABASE_URL",
            default="postgres://user:pass@localhost:5432/database",
        ),
    ]
    cors_whitelist_domains: Annotated[
        set[HttpUrl],
        Field(alias="CORS_WHITELIST", default=["http://localhost:3000"]),
    ]

settings = AppSettings()

print(settings.model_dump())