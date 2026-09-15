from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    gemini_api_key: str
    redis_url: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(env_file=str(ENV_PATH), extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()