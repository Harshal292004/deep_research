from utilities.helpers.LLMProvider import LLMProvider
from components.chains import (
    get_router_chain,
    get_header_chain,
    get_section_writer_chain,
    get_footer_writer_chain,
    get_references_writer_chain,
    get_search_queries_chain,
    get_final_section_writer_chain,
    get_final_header_writer_chain,
    get_final_footer_write_chain
)
from utilities.states.report_state import (
    Section,
    Sections,
    Footer,
    Header,
    Reference,
    ReportState,
    WriterState
)
from components.tools import (
    get_location,
    duckduckgo_search,
    exa_search,
    tavily_search,
    serper_search,
    fire_scrape_web_page,
    GitHubInspector,
    arxiv_search,
)
from utilities.states.tool_states import (
    DuckDuckGoSearch,
    SerperSearch,
    TavilySearchQuery,
    ExaSearch,
    GitHubLanguageSearchQuery,
    GitHubUserQuery,
    GitHubRepoQuery,
    GitHubOrgQuery,
    ArxivSearchQuery,
)
from utilities.states.research_state import ResearchState, QueryState, query_tool_map, query_tool_output
from utilities.helpers.logger import log
import traceback
from pydantic import Any
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


async def query_generation_node(state: ResearchState):
    try:
        log.debug("Starting verify_report_node...")
        query = state.query
        type_of_query = state.type_of_query
        schema_of_tools = query_tool_map.get(state.type_of_query)
        tool_query_output = []
        for idx, section in enumerate(state.sections, start=1):
            if section.research:
                section_display = f"Section: {section.name}\nDescription: {section.description}\nContent: {section.content}\n\n"
                chain = get_search_queries_chain(schema=schema_of_tools)
                output = await chain.ainvoke(
                    {
                        "type_of_query": type_of_query,
                        "query": query,
                        "section": section_display,
                    }
                )
                tool_query_output.append(QueryState(idx=idx, query_set=output))
        return {"queries": tool_query_output}

    except Exception as e:
        log.error(f"Error in query_generation_node: {e}")
        return {"queries": None}


async def get_tool_output(
    duckduckgo_search_input: DuckDuckGoSearch,
    exa_search_input: ExaSearch,
    serper_search_input: SerperSearch,
    github_user_query_input: GitHubUserQuery,
    github_repo_query_input: GitHubRepoQuery,
    github_org_query_input: GitHubOrgQuery,
    github_language_query_input: GitHubLanguageSearchQuery,
    arxiv_search_query_input: ArxivSearchQuery,
    tavily_search_query_input: TavilySearchQuery,
    output_model: Any,
    type_of_query: str,
):
    duckduckgo_output = None
    exa_output = None
    serper_output = None
    gh_user_output = None
    gh_repo_output = None
    gh_org_output = None
    gh_lang_output = None
    axv_output = None
    tav_output = None

    if duckduckgo_search_input:
        duckduckgo_output = await duckduckgo_search(input=duckduckgo_search_input)
    if exa_search_input:
        exa_output = await exa_search(input=exa_search_input)
    if serper_search_input:
        serper_search_input.country = get_location()
        serper_output = await serper_search(input=serper_search_input)
    if github_user_query_input:
        gh_user_output = await GitHubInspector.get_user_by_name(
            input=github_user_query_input
        )
    if github_repo_query_input:
        gh_repo_output = await GitHubInspector.get_repo_by_name(
            input=github_repo_query_input
        )
    if github_org_query_input:
        gh_org_output = await GitHubInspector.get_org_by_name(
            input=github_org_query_input
        )
    if github_language_query_input:
        gh_lang_output = await GitHubInspector.search_repos_by_language(
            input=github_language_query_input
        )
    if arxiv_search_query_input:
        axv_output = await arxiv_search(arxiv_search_query_input)
    if tavily_search_query_input:
        tav_output = await tavily_search(tavily_search_query_input)

    if type_of_query == "factual_query":
        output_model.duckduckgo_output = duckduckgo_output
        output_model.exa_output = exa_output
        output_model.tav_output = tav_output

    elif type_of_query == "comparative_evaluative_query":
        output_model.duckduckgo_output = duckduckgo_output
        output_model.exa_output = exa_output
        output_model.tav_output = tav_output
        output_model.serper_output = serper_output

    elif type_of_query == "research_oriented_query":
        output_model.arxiv_output = axv_output
        output_model.exa_output = exa_output
        output_model.tav_output = tav_output
        output_model.serper_output = serper_output

    elif type_of_query == "execution_programming_query":
        output_model.duckduckgo_output = duckduckgo_output
        output_model.exa_output = exa_output
        output_model.tav_output = tav_output
        output_model.gh_user_output = gh_user_output
        output_model.gh_repo_output = gh_repo_output
        output_model.gh_org_output = gh_org_output
        output_model.gh_lang_output = gh_lang_output

    elif type_of_query == "idea_generation":
        output_model.duckduckgo_output = duckduckgo_output
        output_model.exa_output = exa_output

    return output_model


async def tool_output_node(state: ResearchState):
    try:
        log.debug("Starting tool_output_node...")
        queries = state.queries
        type_of_query = state.type_of_query
        schema_of_tool = query_tool_map.get(type_of_query)
        sechema_of_output = query_tool_output.get(type_of_query)
        output_list = []
        for query in queries:
            output = await get_tool_output(
                duckduckgo_search_input=getattr(
                    query.query_set, "duckduckgo_search", None
                ),
                exa_search_input=getattr(query.query_set, "exa_search", None),
                serper_search_input=getattr(query.query_set, "serper_search", None),
                github_user_query_input=getattr(
                    query.query_set, "get_user_by_name", None
                ),
                github_repo_query_input=getattr(
                    query.query_set, "get_repo_by_name", None
                ),
                github_org_query_input=getattr(
                    query.query_set, "get_org_by_name", None
                ),
                github_language_query_input=getattr(
                    query.query_set, "search_repos_by_language", None
                ),
                arxiv_search_query_input=getattr(
                    query.query_set, "arxiv_search_query", None
                ),
                tavily_search_query_input=getattr(
                    query.query_set, "tavily_search", None
                ),
                output_model=sechema_of_output,
                type_of_query=type_of_query,
            )
            output_list.append(QueryState(idx=query.idx, query_set=output))

        return {"tool_output": output_list}
    except Exception as e:
        log.error(f"Error in query_generation_node: {e}")
        return {"queries": None}

async def roll_out_output(state):
    pass

async def section_write_node(state:WriterState):
    try:
        type_of_query= state.type_of_query
        schema_output= query_tool_output.get(type_of_query)
        output= state.output_list
        sections= state.sections.sections
        
        section_written=None
        for section in sections:
            section_string = (
                f"\nsection_id: {sec.section_id} "
                f"name: {sec.name} "
                f"description: {sec.description} "
                f"research: {sec.research} "
                f"content: {sec.content}"
            )
            
            if not section.research:
                    section_written=await get_final_section_writer_chain().ainvoke({"query":"","type_of_query":type_of_query,"section":section_string,"research_data":""})     
                    continue
                
            for output in output:
                if output.idx == section.idx:
                    research_string= roll_out_output()
                    section_written=await get_final_section_writer_chain().ainvoke({"query":"","type_of_query":type_of_query,"section":section_string,"research_data":research_string})    
                    
            section.description= section_written.description
            section.content=section_written.content
        
        return {
            "sections":{
                "sections":state.sections.sections
            }
        }
                
        
    except Exception as e:
        log.error(f"The error is {e}")
        return {
            "sections":{
                "sections":None
            }
        }