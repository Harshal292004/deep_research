import os
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: str = "*"

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    # Task Management
    MAX_CONCURRENT_TASKS: int = 10
    TASK_TIMEOUT: int = 3600  # 1 hour

    # API Keys (optional defaults, can be overridden per request)
    EXA_API_KEY: str = ""
    SERPER_API_KEY: str = ""
    TAVLIY_API_KEY: str = ""
    GITHUB_ACCESS_TOKEN: str = ""
    GROQ_API_KEY: str = ""
    # Langfuse (optional)
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_HOST: str = "https://cloud.langfuse.com"
    # Model Configuration
    TEXT_GROQ_MODEL_NAME: str = "llama-3.3-70b-versatile"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Read PORT from environment (Render sets this dynamically)
        port_env = os.getenv("PORT")
        if port_env:
            self.PORT = int(port_env)


settings = Settings()


def set_api_keys(api_keys: dict):
    """Set API keys in environment for use by business logic"""
    import os

    for key, value in api_keys.items():
        if value:
            os.environ[key] = value
