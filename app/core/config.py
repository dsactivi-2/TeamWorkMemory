import os
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Telesales Shared Memory Server"
    app_env: str = "development"
    log_level: str = "INFO"
    memory_api_key: str = Field(default="local-dev-memory-key", alias="MEMORY_API_KEY")
    database_url: str | None = Field(default=None, alias="DATABASE_URL")
    redis_url: str | None = Field(default=None, alias="REDIS_URL")
    allowed_namespace_prefix: str = Field(
        default="telesales-builder:", alias="ALLOWED_NAMESPACE_PREFIX"
    )
    allow_inmemory_store: bool = Field(default=True, alias="ALLOW_INMEMORY_STORE")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def is_production_like(self) -> bool:
        return self.app_env.lower() in {"staging", "production"}

    @property
    def has_non_default_api_key(self) -> bool:
        return self.memory_api_key != "local-dev-memory-key"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def clear_settings_cache() -> None:
    get_settings.cache_clear()
    os.environ.pop("PYDANTIC_SKIP_VALIDATION", None)
