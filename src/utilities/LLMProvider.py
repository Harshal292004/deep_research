from config import settings
from langchain_together import ChatTogether

class LLMProvider:
    @staticmethod
    def structuredtextclient(model, model_name=settings.TEXT_MODEL_NAME):
        model = ChatTogether(api_key=settings.TOGETHER_API_KEY, model=model_name)
        return model.with_structured_output(model)

    @staticmethod
    def textclient(model_name):
        model = ChatTogether(api_key=settings.TOGETHER_API_KEY, model=model_name)
        return model

    @staticmethod
    def embeddingsclient(model=settings.EMBEDDING_MODEL):
        return SentenceTransformer(model)
