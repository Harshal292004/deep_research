from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, Any


class Settings(BaseSettings):
    TOGETHER_API_KEY: str
    EXA_API_KEY: str
    SERPER_API_KEY: str
    FIRE_CRAWL_API_KEY: str
    TAVLIY_API_KEY: str
    GITHUB_ACCESS_TOKEN: str
    GROQ_API_KEY: str

    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    LANGFUSE_SECRET_KEY: str
    LANGFUSE_PUBLIC_KEY: str
    LANGFUSE_HOST: str
    TEXT_GROQ_MODEL_NAME: str = "llama-3.3-70b-versatile"
    TEXT_TOGETHER_MODEL_NAME: str = "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
