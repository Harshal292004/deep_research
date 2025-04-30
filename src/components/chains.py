from utilities.states.report_state import (
    Header,
    Sections,
    Footer,
    Reference,
    References,
)
from components.prompts import Prompts
from utilities.helpers.LLMProvider import LLMProvider
from utilities.helpers.logger import log


def get_router_chain():
    try:
        log.debug("Starting get_router_chain...")
        prompt = Prompts.get_router_prompt()
        log.debug("Router prompt fetched successfully.")
        llm = LLMProvider.textclient()
        log.debug("LLM client for RouterResponse created successfully.")
        return prompt | llm
    except Exception as e:
        log.error(f"Error in get_router_chain: {e}")
        return None


def get_header_chain():
    try:
        log.debug("Starting get_header_chain...")
        prompt = Prompts.get_header_prompt()
        log.debug("Header prompt fetched successfully.")
        llm = LLMProvider.structuredtextclient(schema=Header)
        log.debug("LLM client for Header created successfully.")
        return prompt | llm
    except Exception as e:
        log.error(f"Error in get_header_chain: {e}")
        return None


def get_section_writer_chain():
    try:
        log.debug("Starting get_section_writer_chain...")
        prompt = Prompts.get_section_writer_prompt()
        log.debug("Section writer prompt fetched successfully.")
        llm = LLMProvider.structuredtextclient(schema=Sections)
        log.debug("LLM client for Sections created successfully.")
        return prompt | llm
    except Exception as e:
        log.error(f"Error in get_section_writer_chain: {e}")
        return None


def get_footer_writer_chain():
    try:
        log.debug("Starting get_footer_writer_chain...")
        prompt = Prompts.get_footer_writer_prompt()
        log.debug("Footer prompt fetched successfully.")
        llm = LLMProvider.textclient()
        log.debug("LLM text client created successfully.")
        return prompt | llm
    except Exception as e:
        log.error(f"Error in get_footer_writer_chain: {e}")
        return None


def get_references_writer_chain():
    try:
        log.debug("Starting get_references_writer_chain...")
        prompt = Prompts.get_references_writer_prompt()
        log.debug("References writer prompt fetched successfully.")
        llm = LLMProvider.structuredtextclient(schema=References)
        log.debug("LLM client for References created successfully.")
        return prompt | llm
    except Exception as e:
        log.error(f"Error in get_references_writer_chain: {e}")
        return None
