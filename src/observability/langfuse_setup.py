import os
from langfuse.langchain import CallbackHandler
from config import settings

langfuse_handler = CallbackHandler(
    public_key=settings.LANGFUSE_PUBLIC_KEY
)
