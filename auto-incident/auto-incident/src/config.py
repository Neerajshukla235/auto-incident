"""Application configuration."""
from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    openai_api_key: str = ""
    anthropic_api_key: str = ""
    log_level: str = "INFO"
    alert_webhook_secret: str = ""
    llm_provider: Literal["openai", "anthropic", "ollama"] = "ollama"
    llm_model: str = "mistral:latest"
    ollama_base_url: str = "http://localhost:11434"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
