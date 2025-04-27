from utilities.app_state import RouterResponse

from utilities.report_state import (
    Header,
    Sections,
    Footer,
    Reference,
    References,
    VerifyReport
)
from utilities.LLMProvider import LLMProvider
from prompts import (
    get_router_prompt,
    get_header_prompt,
    get_section_writer_prompt,
    get_verify_report_framework_prompt,
    get_footer_writer_prompt,
    get_references_writer_prompt
)


def get_router_chain():
    prompt = get_router_prompt()
    llm = LLMProvider.structuredtextclient(model=RouterResponse)
    return prompt | llm


def get_header_chain():
    prompt = get_header_prompt()
    llm=LLMProvider.structuredtextclient(model= Header)
    return prompt| llm

def get_section_writer_chain():
    prompt=get_section_writer_prompt()
    llm= LLMProvider.structuredtextclient(model =Sections)
    return prompt |llm 

def get_footer_writer_chain():
    prompt= get_footer_writer_prompt()
    llm=LLMProvider.structuredtextclient(model=Footer)
    return prompt|llm

def get_verify_report_framework_chain():
    prompt= get_verify_report_framework_prompt()
    llm= LLMProvider.structuredtextclient(model=VerifyReport)
    return prompt|llm

def get_refrences_writter_chain():
    prompt=get_references_writer_prompt()
    llm= LLMProvider.structuredtextclient(model= References)
    return prompt|llm
