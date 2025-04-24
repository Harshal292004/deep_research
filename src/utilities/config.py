from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, Any


class Settings(BaseSettings):
    TOGETHER_API_KEY: str
    EXA_API_KEY: str
    SERPER_API_KEY: str
    FIRE_CRAWL_API_KEY: str
    TAVLIY_API_KEY:str
    GITHUB_ACCESS_TOKEN:str
    
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    LANGFUSE_SECRET_KEY: str
    LANGFUSE_PUBLIC_KEY: str
    LANGFUSE_HOST: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
print(settings.model_dump())
