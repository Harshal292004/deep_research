from config import settings
from langchain_together import ChatTogether
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer


class LLMProvider:
    _api_key = settings.TOGETHER_API_KEY
    _default_text_model = settings.TEXT_MODEL_NAME
    _default_embedding_model = settings.EMBEDDING_MODEL

    @classmethod
    def _init_chat_model(cls, model_name: str = None):
        return ChatTogether(
            api_key=cls._api_key, model=model_name or cls._default_text_model
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
