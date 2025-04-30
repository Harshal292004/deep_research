from utilities.helpers.LLMProvider import LLMProvider
from components.chains import (
    get_router_chain,
    get_header_chain,
    get_section_writer_chain,
    get_footer_writer_chain,
    get_references_writer_chain,
)
from utilities.states.report_state import (
    Section,
    Sections,
    Footer,
    Header,
    Reference,
    ReportState,
)
from utilities.states.research_state import ResearchState,QuerySet
from utilities.helpers.logger import log
import traceback

# Section Writer graph 

async def router_node(state: ReportState):
    try:
        log.debug("Starting router_node...")
        query = state.query
        chain = get_router_chain()
        log.debug("Router chain fetched successfully.")
        response = await chain.ainvoke({"query": query})
        log.debug(f"Type of query detected: {response.content}")
        return {"type_of_query": response.content}
    except Exception as e:
        log.error(f"Error in router_node: {e}")
        return {"type_of_query": "factual_query"}


async def header_writer_node(state: ReportState):
    try:
        log.debug("Starting header_writer_node...")
        query = state.query
        type_of_query = state.type_of_query
        chain = get_header_chain()
        log.debug("Header chain reterived successfully")
        response = await chain.ainvoke(
            {
                "query": query,
                "type_of_query": type_of_query,
                "user_feedback": state.user_feedback,
            }
        )
        log.debug(f"Header generated successfully: {response}")
        return {
            "header": {
                "title": response.title,
                "summary": response.summary,
            }
        }
    except Exception as e:
        log.error("Error in header_writer_node:")
        log.error(traceback.format_exc())
        return {"header": {"title": "", "summary": ""}}


async def section_writer_node(state: ReportState):
    try:
        log.debug("Starting section_writer_node...")
        query = state.query
        type_of_query = state.type_of_query
        title_of_report = state.header.title
        summary_of_report = state.header.summary
        chain = get_section_writer_chain()
        response = await chain.ainvoke(
            {
                "query": query,
                "type_of_query": type_of_query,
                "title": title_of_report,
                "summary": summary_of_report,
            }
        )

        sections = response.sections
        output = []
        for sec in sections:
            output.append(
                {
                    "section_id": sec.section_id,
                    "name": sec.name,
                    "description": sec.description,
                    "research": sec.research,
                    "content": sec.content,
                }
            )

        log.debug("Sections generated successfully.")
        return {"sections": {"sections": output}}
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
                f"\nsection_id: {sec.section_id} "
                f"name: {sec.name} "
                f"description: {sec.description} "
                f"research: {sec.research} "
                f"content: {sec.content}"
            )

        response = await chain.ainvoke(
            {
                "query": query,
                "type_of_query": type_of_query,
                "structure": section_string,
            }
        )

        log.debug(f"Footer generated successfully: {response.content}")
        return {"footer": {"conclusion": response.content}}
    except Exception as e:
        log.error(f"Error in footer_writer_node: {e}")
        return {"footer": {"conclusion": ""}}


async def reference_writer_node(state: ReportState):
    try:
        log.debug("Starting reference_writer_node...")
        query = state.query
        type_of_query = state.type_of_query
        chain = get_references_writer_chain()
        sections = state.sections.sections

        section_string = ""
        for sec in sections:
            section_string += (
                f"\nsection_id: {sec.section_id} "
                f"name: {sec.name} "
                f"description: {sec.description} "
                f"research: {sec.research} "
                f"content: {sec.content}"
            )

        response = await chain.ainvoke({"sections": section_string})

        output_ref = []
        for ref in response.references:
            output_ref.append(
                {
                    "section_id": ref.section_id,
                    "section_name": ref.section_name,
                    "source_url": ref.source_url,
                }
            )

        log.debug(f"References generated successfully: {output_ref}")
        return {"references": {"references": output_ref}}
    except Exception as e:
        log.error(f"Error in reference_writer_node: {e}")
        return {"references": {"references": []}}


async def verify_report_node(state: ReportState):
    try:
        log.debug("Starting verify_report_node...")

        # Display the report to the user
        report_display = (
            f"Title: {state.header.title}\n\nSummary: {state.header.summary}\n\n"
        )
        for idx, section in enumerate(state.sections.sections, start=1):
            report_display += f"Section {idx}: {section.name}\nDescription: {section.description}\nContent: {section.content}\n\n"
        report_display += f"Conclusion: {state.footer.conclusion}\n"
        for idx, reference in enumerate(state.references.references, start=1):
            report_display += f"Reference {idx}:\nSection Id: {reference.section_id}\nSection Name: {reference.section_name}\n"
            for idx, url in enumerate(reference.source_url, start=1):
                report_display += f"Source Url {idx}:{url}\n"

        print("Generated Report:\n")
        print(report_display)
        user_input = input(
            "Is the report structure satisfactory? (True/False): "
        ).strip()

        # Validate user input
        while user_input not in ["True", "False"]:
            user_input = input("Please enter 'True' or 'False': ").strip()

        verified = user_input == "True"
        user_feedback = ""

        if not verified:
            user_feedback = input(
                "Please provide feedback to improve the report structure: "
            ).strip()

        return {"report_framework": verified, "user_feedback": user_feedback}

    except Exception as e:
        log.error(f"Error in verify_report_node: {e}")
        return {
            "report_framework": False,
            "user_feedback": "Error occurred during verification.",
        }

# Researcher graph 

# Just select the set of tools with the help of the tool_dict by using the `type_of_query` when you run the graph

async def query_generation_node(state:ResearchState):
    
    pass