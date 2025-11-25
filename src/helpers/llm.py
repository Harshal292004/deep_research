"""LLM Provider"""
from src.config import settings
from pydantic import BaseModel ,SecretStr
from typing import Optional, Type
from langchain_groq import ChatGroq
from langchain_core.language_models import BaseChatModel

class LLMProvider:
    _groq_api_key = settings.GROQ_API_KEY
    _default_groq_text_model = settings.TEXT_GROQ_MODEL_NAME

    @classmethod
    def _init_chat_model(cls, model_name: Optional[str] = None) -> BaseChatModel:
        return ChatGroq(
            api_key=SecretStr(cls._groq_api_key),
            model=model_name or cls._default_groq_text_model,
        )

    @classmethod
    def structuredtextclient(cls, schema: Type[BaseModel], model_name: Optional[str] = None):
        model = cls._init_chat_model(model_name)
        return model.with_structured_output(schema)

    @classmethod
    def textclient(cls, model_name: Optional[str] = None):
        return cls._init_chat_model(model_name)
