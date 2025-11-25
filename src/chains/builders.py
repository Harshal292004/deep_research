from typing import Optional, Type

from langchain_core.runnables import Runnable
from pydantic import BaseModel

from src.helpers.llm import LLMProvider
from src.helpers.logger import log
from src.models.report import DetailedSection, Header, Sections
from src.prompts.templates import Prompts


def get_router_chain() -> Optional[Runnable]:
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


def get_header_chain() -> Optional[Runnable]:
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


def get_section_writer_chain() -> Optional[Runnable]:
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


def get_footer_writer_chain() -> Optional[Runnable]:
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


def get_search_queries_chain(schema: Type[BaseModel]) -> Optional[Runnable]:
    try:
        log.debug("Starting get_search_queries_chain...")
        prompt = Prompts.get_search_queries_prompt()
        log.debug("Search queries prompt fetched successfully.")
        llm = LLMProvider.structuredtextclient(schema=schema)
        log.debug("LLM client for search queries created successfully.")
        return prompt | llm
    except Exception as e:
        log.error(f"Error in get_search_queries_chain: {e}")
        return None


def get_detailed_section_writer_chain() -> Optional[Runnable]:
    try:
        prompt = Prompts.get_detailed_section_writer_prompt()
        llm = LLMProvider.structuredtextclient(schema=DetailedSection)
        return prompt | llm
    except Exception as e:
        log.error(f"Error in get_detailed_section_writer_chain: {e}")
        return None


def get_detailed_header_writer_chain() -> Optional[Runnable]:
    try:
        log.debug("Starting get_detailed_header_writer_chain...")
        prompt = Prompts.get_detailed_header_writer_prompt()
        llm = LLMProvider.textclient()
        return prompt | llm
    except Exception as e:
        log.error(f"Error in get_detailed_header_writer_chain: {e}")
        return None


def get_detailed_footer_write_chain() -> Optional[Runnable]:
    try:
        log.debug("Starting get_detailed_footer_writer_chain...")
        prompt = Prompts.get_detailed_footer_write_prompt()
        log.debug("Search queries prompt fetched successfully.")
        llm = LLMProvider.textclient()
        log.debug("LLM client for section schema successfully.")
        return prompt | llm
    except Exception as e:
        log.error(f"Error in get_detailed_footer_writer_chain: {e}")
        return None


def get_report_formator_chain() -> Optional[Runnable]:
    try:
        log.debug("Starting get_report_formator_chain...")
        prompt = Prompts.get_report_formator_prompt()
        llm = LLMProvider.textclient()
        return prompt | llm
    except Exception as e:
        log.error(f"Error in get_report_formator_chain: {e}")
        return None
