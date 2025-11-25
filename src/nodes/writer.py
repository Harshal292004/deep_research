"""Writer nodes (detailed section, header, footer, formatter)"""
from src.models.state import WriterState
from src.models.report import Reference
from src.chains.builders import (
    get_detailed_section_writer_chain,
    get_detailed_header_writer_chain,
    get_detailed_footer_write_chain,
    get_report_formator_chain
)
from src.tools.formatter import roll_out_output
from src.helpers.logger import log

async def detailed_section_writer_node(state: WriterState):
    try:
        log.debug("Starting detailed section writer...")
        log.debug("State: %s", state)
        outputs = state.outputs
        sections = state.sections.sections
        log.debug("Sections: %s", sections)
        ref_list = []
        section_written = None

        for section in sections:
            section_string = (
                f"name: {section.name} "
                f"description: {section.description} "
                f"content: {section.content}"
            )

            if not section.research:
                section_written = await get_detailed_section_writer_chain().ainvoke(
                    {
                        "query": state.query,
                        "type_of_query": state.type_of_query,
                        "section": section_string,
                        "research_data": "",
                    }
                )
                continue

            for output in outputs:
                if output.section_id == section.section_id:
                    roll_out_str, refrence = roll_out_output(
                        output.output_state, refrence=Reference(), section=section
                    )
                    ref_list.append(refrence.dict())

                    section_written = await get_detailed_section_writer_chain().ainvoke(
                        {
                            "query": state.query,
                            "type_of_query": state.type_of_query,
                            "section": section_string,
                            "research_data": roll_out_str,
                        }
                    )

            section.name = section_written.name
            section.description = section_written.description
            section.content = section_written.content

        return {
            "sections": {"sections": [sec.dict() for sec in state.sections.sections]},
            "references": ref_list,
        }
    except Exception as e:
        log.error(f"Error in detailed_section_writer_node: {e}")
        existing_sections = (
            [sec.dict() for sec in getattr(getattr(state, "sections", None), "sections", [])]
            if getattr(state, "sections", None) is not None
            else []
        )
        return {"sections": {"sections": existing_sections}}

async def detailed_header_writer_node(state: WriterState):
    try:
        log.debug("Starting detailed header writer...")
        query = state.query
        type_of_query = state.type_of_query
        sections = state.sections.sections
        title = state.header.title
        summary = state.header.summary

        section_string = ""
        for sec in sections:
            section_string += (
                f"name: {sec.name} "
                f"description: {sec.description} "
                f"research: {sec.research} "
                f"content: {sec.content} "
            )

        summary = await get_detailed_header_writer_chain().ainvoke(
            {
                "query": query,
                "type_of_query": type_of_query,
                "section": section_string,
                "introduction": summary,
                "title": title,
            }
        )

        return {"header": {"summary": summary.content}}
    except Exception as e:
        log.error(f"Error in detailed_header_writer_node: {e}")
        return {"header": {"summary": None}}

async def detailed_footer_writer_node(state: WriterState):
    try:
        log.debug("Starting detailed footer writer...")
        query = state.query
        sections = state.sections.sections

        section_string = ""
        for sec in sections:
            section_string += (
                f"name: {sec.name} "
                f"description: {sec.description} "
                f"research: {sec.research} "
                f"content: {sec.content} "
            )

        conclusion = await get_detailed_footer_write_chain().ainvoke(
            {
                "query": query,
                "section": section_string,
            }
        )

        return {"footer": {"conclusion": conclusion.content}}
    except Exception as e:
        log.error(f"Error in detailed_footer_writer_node: {e}")
        return {"footer": {"conclusion": None}}

async def report_formatter_node(state: WriterState):
    try:
        log.debug("Starting report formatter...")

        header = getattr(state, "header", None)
        header_title = getattr(header, "title", "") if header else ""
        header_summary = getattr(header, "summary", "") if header else ""
        header_str = f"Title: {header_title}\n\nSummary: {header_summary}\n\n"

        sections_container = getattr(state, "sections", None)
        sections_list = getattr(sections_container, "sections", []) if sections_container else []
        section_str = ""
        for sec in sections_list:
            sec_str = (
                f"Section {sec.section_id}: {sec.name}\n"
                f"Description: {sec.description}\n"
                f"Content: {sec.content}\n\n"
            )
            section_str += sec_str

        footer = getattr(state, "footer", None)
        conclusion_text = getattr(footer, "conclusion", "") if footer else ""
        conclusion_str = f"Conclusion: {conclusion_text}\n"

        references_list = getattr(state, "references", []) or []
        reference_str = ""
        for reference in references_list:
            url_str = ""
            for url in getattr(reference, "source_url", []) or []:
                url_str += f"{url} \n"
            ref_str = f"Refrence: {getattr(reference, 'section_id', '')} Name: {getattr(reference, 'section_name', '')} url: {url_str} "
            reference_str += ref_str

        response = await get_report_formator_chain().ainvoke(
            {
                "header": header_str,
                "section": section_str,
                "conclusion": conclusion_str,
                "reference": reference_str,
            }
        )

        return {"markdown": response.content}
    except Exception as e:
        log.error(f"Error in report_formatter_node: {e}")
        return {"markdown": None}

