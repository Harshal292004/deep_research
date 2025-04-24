from utilities.app_state import  RouterResponse
from utilities.LLMProvider import  LLMProvider
from prompts import get_router_prompt

def get_router_chain():
    prompt= get_router_prompt()
    llm= LLMProvider.structuredtextclient(model=RouterResponse)
    return (
        prompt | llm
    )


