from config import settings
from langchain_together import ChatTogether
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from langchain_groq import ChatGroq

class LLMProvider:
    _groq_api_key = settings.GROQ_API_KEY
    _together_api_key= settings.TOGETHER_API_KEY
    _default_groq_text_model = settings.TEXT_GROQ_MODEL_NAME
    _default_together_text_model = settings.TEXT_TOGETHER_MODEL_NAME
    _default_embedding_model = settings.EMBEDDING_MODEL

    @classmethod
    def _init_chat_model(cls, model_name: str = None, provider:str= "GROQ"):
        return  ChatGroq(
            api_key=cls._groq_api_key, model=model_name or cls._default_groq_text_model
        ) if provider == "GROQ" else ChatTogether(
            api_key=cls._together_api_key, model_name=model_name or cls._default_together_text_model
        )

    @classmethod
    def structuredtextclient(cls, schema: BaseModel, model_name: str = None):
        return cls._init_chat_model(model_name).with_structured_output(schema)

    @classmethod
    def textclient(cls, model_name: str = None):
        return cls._init_chat_model(model_name)

    @classmethod
    def embeddingsclient(cls, model: str = None):
        return SentenceTransformer(model or cls._default_embedding_model)
