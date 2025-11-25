"""Structure nodes (header, section, footer)"""
from backend.src.models.state import ReportState
from backend.src.chains.builders import (
    get_header_chain,
    get_section_writer_chain,
    get_footer_writer_chain
)
from backend.src.helpers.logger import log

async def header_writer_node(state: ReportState):
    try:
        log.debug("Starting header_writer_node...")
        query = state.query
        type_of_query = state.type_of_query
        chain = get_header_chain()
        response = await chain.ainvoke(
            {
                "query": query,
                "type_of_query": type_of_query,
                "user_feedback": state.user_feedback,
            }
        )
        return {
            "header": {
                "title": response.title,
                "summary": response.summary,
            }
        }
    except Exception as e:
        log.error(f"Error in header_writer_node: {e}")
        return {"header": {"title": "", "summary": ""}}

async def section_writer_node(state: ReportState):
    try:
        log.debug("Starting section_writer_node...")
        query = state.query
        type_of_query = state.type_of_query
        title = state.header.title
        summary = state.header.summary
        chain = get_section_writer_chain()
        response = await chain.ainvoke(
            {
                "query": query,
                "type_of_query": type_of_query,
                "title": title,
                "summary": summary,
            }
        )
        return {"sections": response.dict()}
    except Exception as e:
        log.error(f"Error in section_writer_node: {e}")
        return {"sections": {"sections": []}}

async def footer_writer_node(state: ReportState):
    try:
        log.debug("Starting footer_writer_node...")
        query = state.query
        type_of_query = state.type_of_query
        sections = state.sections.sections
        chain = get_footer_writer_chain()
        section_string = ""
        for sec in sections:
            section_string += (
                f"name: {sec.name} "
                f"description: {sec.description} "
                f"content: {sec.content}"
            )

        response = await chain.ainvoke(
            {
                "query": query,
                "type_of_query": type_of_query,
                "section": section_string,
            }
        )

        return {"footer": {"conclusion": response.content}}
    except Exception as e:
        log.error(f"Error in footer_writer_node: {e}")
        return {"footer": {"conclusion": ""}}

