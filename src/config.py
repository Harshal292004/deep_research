"""Configuration settings"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    EXA_API_KEY: str = ""
    SERPER_API_KEY: str = ""
    TAVLIY_API_KEY: str = ""
    GITHUB_ACCESS_TOKEN: str = ""
    GROQ_API_KEY: str = ""
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_HOST: str = "https://cloud.langfuse.com"
    TEXT_GROQ_MODEL_NAME: str = "llama-3.3-70b-versatile"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
