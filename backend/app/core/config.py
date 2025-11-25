from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: List[str] = ["http://localhost:8501", "http://localhost:3000"]
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # Task Management
    MAX_CONCURRENT_TASKS: int = 10
    TASK_TIMEOUT: int = 3600  # 1 hour
    
    # API Keys (optional defaults, can be overridden per request)
    TOGETHER_API_KEY: str = ""
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
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    TEXT_GROQ_MODEL_NAME: str = "llama-3.3-70b-versatile"
    TEXT_TOGETHER_MODEL_NAME: str = "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

def set_api_keys(api_keys: dict):
    """Set API keys in environment for use by business logic"""
    import os
    for key, value in api_keys.items():
        if value:
            os.environ[key] = value

