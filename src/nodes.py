from utilities.helpers.LLMProvider import LLMProvider
from components.chains import (
    get_router_chain,
    get_header_chain,
    get_section_writer_chain,
    get_footer_writer_chain,
    get_search_queries_chain,
    get_detailed_footer_write_chain,
    get_detailed_header_writer_chain,
    get_detailed_section_writer_chain,
    get_report_formator_chain
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
    duckduckgo_search,
    exa_search,
    tavily_search,
    serper_search,
    GitHubInspector,
    arxiv_search,
)
from utilities.states.tool_state import (
   DuckDuckGoQuery,
   ExaQuery,
   SerperQuery,
   GitHubRepoQuery,
   GitHubUserQuery,
   GitHubOrgQuery,
   GitHubLanguageQuery,
   ArxivQuery,
   TavilyQuery,
   LocationOutput,
   DuckDuckGoOutput,
   SerperQueryOutput,
   TavilyQueryOutput,
   GitHubUserOutput,
   GitHubRepoOutput,
   GitHubOrgOutput,
   GitHubLanguageOutput,
   GitHubLanguageItem,
   ArxivOutput,
   ExaOutput,
   TavilyItem
)
from utilities.states.research_state import ResearchState, QueryState,OutputState, tool_input_map,tool_output_map
from utilities.helpers.logger import log
import traceback
from typing import Any
from pydantic import BaseModel

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
        log.error(f"Error in header_writer_node: {e}")
        return {"header": {"title": "", "summary": ""}}


async def section_writer_node(state: ReportState):
    try:
        log.debug("Starting section_writer_node...")
        query = state.query
        type_of_query = state.type_of_query
        title = state.header.title
        summary= state.header.summary
        chain = get_section_writer_chain()
        response = await chain.ainvoke(
            {
                "query": query,
                "type_of_query": type_of_query,
                "title": title,
                "summary": summary
            }
        )
        return {"sections":response.dict()}
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

        log.debug(f"Footer generated successfully: {response.content}")
        return {"footer": {"conclusion": response.content}}
    except Exception as e:
        log.error(f"Error in footer_writer_node: {e}")
        return {"footer": {"conclusion": ""}}

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
        
        print("Generated Report:\n")
        print(report_display)
        
        user_input = input(
            "Is the report structure satisfactory? (True/False): "
        ).strip()

        while user_input not in ["True", "False"]:
            user_input = input("Please enter 'True' or 'False': ").strip()

        verified = user_input == "True"
        user_feedback = ""

        if not verified:
            user_feedback = input("Please provide feedback to improve the report structure: ").strip()

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
        schema_of_tools = tool_input_map.get(type_of_query)
        input_list = []
        for section in state.sections:
            if section.research:
                section_string = f"Section: {section.name}\nDescription: {section.description}\nContent: {section.content}\n\n"
                chain = get_search_queries_chain(schema=schema_of_tools)
                output = await chain.ainvoke(
                    {
                        "type_of_query": type_of_query,
                        "query": query,
                        "section": section_string,
                    }
                )
                log.debug(f"The type and the output is {type(output)} \n\n\n The Output:  {output}")
                input_list.append(QueryState(section_id=section.section_id, query_state= output))
        return {"queries": input_list}

    except Exception as e:
        log.error(f"Error in query_generation_node: {e}")
        return {"queries": None}


async def get_tool_output(
    duckduckgo_query: DuckDuckGoQuery,
    exa_query: ExaQuery,
    serper_query: SerperQuery,
    github_user_query: GitHubUserQuery,
    github_repo_query: GitHubRepoQuery,
    github_org_query: GitHubOrgQuery,
    github_language_query: GitHubLanguageQuery,
    arxiv_query: ArxivQuery,
    tavily_query: TavilyQuery,
    output_schema: Any,
    type_of_query: str,
):
    # Initialize the output variables
    duckduckgo_output = None
    exa_output = None
    serper_output = None
    github_user_output = None
    github_repo_output = None
    github_org_output = None
    github_language_output = None
    arxiv_output = None
    tavily_output = None

    # Check each query and fetch the output accordingly
    if duckduckgo_query:
        duckduckgo_output = await duckduckgo_search(input=duckduckgo_query)
        log.debug(f"duckduckgo_output type: {type(duckduckgo_output)} | Content: {duckduckgo_output}")

    if exa_query:
        exa_output = exa_search(input=exa_query)

    if serper_query:
        serper_output = await serper_search(input=serper_query)
    if github_user_query:
        github_user_output = await GitHubInspector.get_user_by_name(input=github_user_query)
        
    if github_repo_query:
        github_repo_output = await GitHubInspector.get_repo_by_name(input=github_repo_query)
        
    if github_org_query:
        github_org_output = await GitHubInspector.get_org_by_name(input=github_org_query)
        
    if github_language_query:
        github_language_output = await GitHubInspector.search_repos_by_language(input=github_language_query)
        
    if arxiv_query:
        arxiv_output = await arxiv_search(input=arxiv_query)
        
    if tavily_query:
        tavily_output = await tavily_search(input=tavily_query)
        
        
    # Log the final output schema and populate based on query type
    log.debug(f"Final type_of_query: {type_of_query}")
    output= output_schema()
    
    if type_of_query == "factual_query":
        output.duckduckgo_output = duckduckgo_output
        output.exa_output = exa_output
        output.tavily_output = tavily_output

    elif type_of_query == "comparative_evaluative_query":
        output.duckduckgo_output = duckduckgo_output
        output.exa_output = exa_output
        output.tavily_output = tavily_output
        output.serper_output = serper_output

    elif type_of_query == "research_oriented_query":
        output.arxiv_output = arxiv_output
        output.exa_output = exa_output
        output.tavily_output = tavily_output
        output.serper_output = serper_output

    elif type_of_query == "execution_programming_query":
        output.duckduckgo_output = duckduckgo_output
        output.exa_output = exa_output
        output.tavily_output = tavily_output
        output.github_user_output = github_user_output
        output.github_repo_output = github_repo_output
        output.github_org_output = github_org_output
        output.github_language_output = github_language_outpu

    elif type_of_query == "idea_generation":
        output.duckduckgo_output = duckduckgo_output
        output.exa_output = exa_output
        
    return output



async def tool_output_node(state: ResearchState):
    try:
        log.debug("Starting tool_output_node...")
        queries = state.queries
        type_of_query = state.type_of_query
        sechema_of_output = tool_output_map.get(type_of_query)
        output_list = []
        for query in queries:
            duckduckgo_query = getattr(query.query_state, "duckduckgo_query", None)
            exa_query = getattr(query.query_state, "exa_query", None)
            serper_query = getattr(query.query_state, "serper_query", None)
            github_user_query = getattr(query.query_state, "github_user_query", None)
            github_repo_query = getattr(query.query_state, "github_repo_query", None)
            github_org_query = getattr(query.query_state, "github_org_query", None)
            github_language_query = getattr(query.query_state, "github_language_query", None)
            arxiv_query = getattr(query.query_state, "arxiv_query", None)
            tavily_query = getattr(query.query_state, "tavily_query", None)

            output = await get_tool_output(
                duckduckgo_query=duckduckgo_query,
                exa_query=exa_query,
                serper_query=serper_query,
                github_user_query=github_user_query,
                github_repo_query=github_repo_query,
                github_org_query=github_org_query,
                github_language_query=github_language_query,
                arxiv_query=arxiv_query,
                tavily_query=tavily_query,
                output_schema=sechema_of_output,
                type_of_query=type_of_query,
            )

            log.debug(f"Received output: {type(output)} {output}")
            output_list.append(OutputState(section_id=query.section_id, output_state=output))
            
        return {"outputs": output_list}
    except Exception as e:
        log.error(f"Error in tool_output_node: {e}")
        return {"outputs": None}


# Writer graph 
def roll_out_output(state, refrence: Reference, section: Section):
    try:
        duckduckgo_output = getattr(state, "duckduckgo_output", None)
        exa_output = getattr(state, "exa_output", None)
        serper_output = getattr(state, "serper_output", None)
        github_user_output = getattr(state, "github_user_output", None)
        github_repo_output = getattr(state, "github_repo_output", None)
        github_org_output = getattr(state, "github_org_output", None)
        github_language_output = getattr(state, "github_language_output", None)
        arxiv_output = getattr(state, "arxiv_output", None)
        tavily_output = getattr(state, "tavily_output", None)
        
        rolled_out_str = ""
        refrence.section_name = section.name
        refrence.section_id = section.section_id
                
        log.debug("Processing in the roll_out_output")

        log.debug(f"Type and content of duckduckgo_output: {type(duckduckgo_output)} | {duckduckgo_output}")
        log.debug(f"Type and content of exa_output: {type(exa_output)} | {exa_output}")
        log.debug(f"Type and content of serper_output: {type(serper_output)} | {serper_output}")
        log.debug(f"Type and content of github_user_output: {type(github_user_output)} | {github_user_output}")
        log.debug(f"Type and content of github_repo_output: {type(github_repo_output)} | {github_repo_output}")
        log.debug(f"Type and content of github_org_output: {type(github_org_output)} | {github_org_output}")
        log.debug(f"Type and content of github_language_output: {type(github_language_output)} | {github_language_output}")
        log.debug(f"Type and content of arxiv_output: {type(arxiv_output)} | {arxiv_output}")
        log.debug(f"Type and content of tavily_output: {type(tavily_output)} | {tavily_output}")
        
        if duckduckgo_output:
            rolled_out_str += "DUCK DUCK GO SEARCH:\n\n\n"
            for duck in duckduckgo_output:
                duck_string = f"{duck.title} {duck.snippet}\n\n"
                duck_string = duck_string[:1000]
                rolled_out_str += f"{duck_string}\n\n"
                log.debug(f"Processed DuckDuckGo result: {duck.title}")
                refrence.source_url.append(duck.link)
                log.debug(f"Added link to source_url: {duck.link}")
            log.debug(f"Processed {len(duckduckgo_output)} results from DuckDuckGo.")

        if exa_output:
            log.debug(f"Found exa_output for section {section.name}, processing.")
            rolled_out_str += "EXA SEARCH:\n\n\n"
            for exa in exa_output:
                highlight_string = "".join(exa.highlights)
                highlight_string = highlight_string[:1000]
                rolled_out_str += f"{highlight_string} \n\n"
                refrence.source_url.append(exa.url)
                log.debug(f"Added link to source_url: {exa.url}")
            log.debug(f"Processed {len(exa_output)} results from EXA.")

        if serper_output:
            log.debug(f"Found serper_output for section {section.name}, processing.")
            rolled_out_str += "SERPER SEARCH:\n\n\n"
            for organic in serper_output:
                organic_string = f"{organic.title} {organic.snippet} \n\n"
                organic_string = organic_string[:2000]
                rolled_out_str += organic_string
                refrence.source_url.append(organic.link)
                log.debug(f"Added link to source_url: {organic.link}")
            log.debug(f"Processed {len(serper_output)} results from Serper.")

        if github_user_output:
            log.debug(f"Found github_user_output for section {section.name}, processing.")
            rolled_out_str += "GITHUB USER:\n\n\n"
            for gh in github_user_output:
                rolled_out_str += f"Github username: {gh.login} User's full name: {gh.name} Number of public repos: {gh.public_repos} Number of followers: {gh.followers} Bio of the user: {gh.bio} Location of the user: {gh.location}\n\n"
                refrence.source_url.append(f"https://github.com/{gh.login}")
                log.debug(f"Added link to source_url: https://github.com/{gh.login}")
            log.debug(f"Processed {len(github_user_output)} results from GitHub User.")

        if github_repo_output:
            log.debug(f"Found github_repo_output for section {section.name}, processing.")
            rolled_out_str += "GITHUB REPO:\n\n"
            for gh in github_repo_output:
                topic_str = "\n".join(gh.topics)
                rolled_out_str += f"Github Repo name: {gh.name} Repo's full name: {gh.full_name} Description of repo: {gh.description} Number of stars: {gh.stars} Number of forks: {gh.forks} Language used: {gh.language} Topics:\n{topic_str}\n\n"
                refrence.source_url.append(gh.html_url)
                log.debug(f"Added link to source_url: {gh.html_url}")
            log.debug(f"Processed {len(github_repo_output)} results from GitHub Repo.")

        if github_org_output:
            log.debug(f"Found github_org_output for section {section.name}, processing.")
            rolled_out_str += "GITHUB ORG:\n\n"
            for gh in github_org_output:
                member_list = "".join(gh.members)
                rolled_out_str += f"Github Org login: {gh.login} Org's full name: {gh.name} Org's description: {gh.description} Number of public_repo: {gh.public_repos} Member of repo: {member_list}\n\n"
                refrence.source_url.append(f"https://github.com/{gh.login}")
                log.debug(f"Added link to source_url: https://github.com/{gh.login}")
            log.debug(f"Processed {len(github_org_output)} results from GitHub Org.")

        if github_language_output:
            log.debug(f"Found github_language_output for section {section.name}, processing.")
            rolled_out_str += "GITHUB REPO Based on language:\n\n"
            for gh in github_language_output.results:
                rolled_out_str += f"Github repo's name: {gh.name} Repo's full name: {gh.full_name} Number of stars: {gh.stars} URL of the repo: {gh.url}\n\n"
                refrence.source_url.append(gh.url)
                log.debug(f"Added link to source_url: {gh.url}")
            log.debug(f"Processed {len(github_language_output.results)} results from GitHub Repo Based on Language.")

        if arxiv_output:
            log.debug(f"Found arxiv_output for section {section.name}, processing.")
            rolled_out_str += "ARXIV Output:\n\n"
            for axv in arxiv_output.results:
                author_str = "  ".join(axv.authors[:4])
                arxiv_string = f"Paper Title: {axv.title} Authors: {author_str} Summary: {axv.summary[:200]} Published: {axv.published}\n\n"
                rolled_out_str += arxiv_string
                refrence.source_url.append(axv.url)
                log.debug(f"Added link to source_url: {axv.url}")
            log.debug(f"Processed {len(arxiv_output.results)} results from Arxiv.")

        if tavily_output:
            log.debug(f"Found tavily_output for section {section.name}, processing.")
            rolled_out_str += "TAVILY Output:\n\n"
            for tav in tavily_output.results:
                tavily_string = f"Title: {tav.title} Content: {tav.content} \n\n"
                tavily_string = tavily_string[:500]
                rolled_out_str += tavily_string
                refrence.source_url.append(tav.url)
                log.debug(f"Added link to source_url: {tav.url}")
            log.debug(f"Processed {len(tavily_output.results)} results from Tavily.")

        return rolled_out_str, refrence
    except Exception as e:
        log.error(f"Error occurred: {e}")
        return None, None

async def detailed_section_writer_node(state: WriterState):
    try:
        log.debug(f"[detailed_section_writer_node] Received state: {state} | Type: {type(state)}")
        log.debug(f"[detailed_section_writer_node] Query: {state.query} | Type: {type(state.query)}")
        log.debug(f"[detailed_section_writer_node] Type of query: {state.type_of_query} | Type: {type(state.type_of_query)}")

        schema_output = tool_output_map.get(state.type_of_query)
        log.debug(f"[detailed_section_writer_node] Schema output: {schema_output} | Type: {type(schema_output)}")

        outputs = state.outputs
        log.debug(f"[detailed_section_writer_node] Outputs: {outputs} | Type: {type(outputs)}")

        sections = state.sections.sections
        log.debug(f"[detailed_section_writer_node] Sections: {sections} | Type: {type(sections)}")

        ref_list = []
        section_written = None

        for section in sections:
            log.debug(f"[detailed_section_writer_node] Processing section: {section} | Type: {type(section)}")
            section_string = (
                f"name: {section.name} "
                f"description: {section.description} "
                f"content: {section.content}"
            )
            log.debug(f"[detailed_section_writer_node] Constructed section_string: {section_string} | Type: {type(section_string)}")

            if not section.research:
                log.debug(f"[detailed_section_writer_node] Section has no research data.")
                section_written = await get_detailed_section_writer_chain().ainvoke({
                    "query": state.query,
                    "type_of_query": state.type_of_query,
                    "section": section_string,
                    "research_data": ""
                })
                log.debug(f"[detailed_section_writer_node] Section written (no research): {section_written}")
                continue

            for output in outputs:
                if output.section_id == section.section_id:
                    log.debug(f"[detailed_section_writer_node] Rolling out section: {section.name} | Section ID: {section.section_id}")
                    log.debug(f"[detailed_section_writer_node] Output: {output} | State: {output.output_state}")
                    
                    roll_out_str, refrence = roll_out_output(output.output_state, refrence=Reference(), section=section)
                    log.debug(f"[detailed_section_writer_node] Roll-out string: {roll_out_str}")
                    log.debug(f"[detailed_section_writer_node] Reference object: {refrence}")
                    ref_list.append(refrence.dict())

                    section_written = await get_detailed_section_writer_chain().ainvoke({
                        "query": state.query,
                        "type_of_query": state.type_of_query,
                        "section": section_string,
                        "research_data": roll_out_str
                    })
                    log.debug(f"[detailed_section_writer_node] Section written (with research): {section_written}")

            section.name = section_written.name
            section.description = section_written.description
            section.content = section_written.content
            log.debug(f"[detailed_section_writer_node] Updated section: {section.name} | {section.description} | {section.content}")

        log.debug(f"[detailed_section_writer_node] Returning section data and references.")
        return {
            "sections": {
                "sections": [sec.dict() for sec in state.sections.sections]
            },
            "references": ref_list
        }

    except Exception as e:
        log.exception(f"[detailed_section_writer_node] Exception: {e}", exc_info=True)
        return {
            "sections": {
                "sections": None
            }
        }

async def detailed_header_writer_node(state: WriterState):
    try:
        log.debug(f"[detailed_header_writer_node] Received state: {state} | Type: {type(state)}")
        query = state.query
        type_of_query = state.type_of_query
        output = state.outputs
        sections = state.sections.sections
        title = state.header.title
        summary = state.header.summary

        log.debug(f"[detailed_header_writer_node] Query: {query}")
        log.debug(f"[detailed_header_writer_node] Type of query: {type_of_query}")
        log.debug(f"[detailed_header_writer_node] Output: {output}")
        log.debug(f"[detailed_header_writer_node] Sections: {sections}")
        log.debug(f"[detailed_header_writer_node] Title: {title}")
        log.debug(f"[detailed_header_writer_node] Summary: {summary}")

        section_written = None
        for sec in sections:
            log.debug(f"[detailed_header_writer_node] Processing section: {sec}")
            section_string = (
                f"name: {sec.name} "
                f"description: {sec.description} "
                f"research: {sec.research} "
                f"content: {sec.content}"
            )
            log.debug(f"[detailed_header_writer_node] Constructed section_string: {section_string}")

        log.debug("[detailed_header_writer_node] Calling detailed header writer chain...")
        summary = await get_detailed_header_writer_chain().ainvoke({
            "query": query,
            "type_of_query": type_of_query,
            "section": section_string,
            "introduction": summary,
            "title": title
        })

        log.debug(f"[detailed_header_writer_node] Received summary: {summary.content}")
        return {
            "header": {
                "summary": summary.content
            }
        }

    except Exception as e:
        log.error(f"[detailed_header_writer_node] Error: {e}")
        return {
            "header": {
                "summary": None
            }
        }

async def detailed_footer_writer_node(state: WriterState):
    try:
        log.debug(f"[detailed_footer_writer_node] Received state: {state} | Type: {type(state)}")
        query = state.query
        type_of_query = state.type_of_query
        sections = state.sections.sections

        log.debug(f"[detailed_footer_writer_node] Query: {query}")
        log.debug(f"[detailed_footer_writer_node] Type of query: {type_of_query}")
        log.debug(f"[detailed_footer_writer_node] Sections: {sections}")
        
        for sec in sections:
            log.debug(f"[detailed_footer_writer_node] Processing section: {sec}")
            section_string = (
                f"name: {sec.name} "
                f"description: {sec.description} "
                f"research: {sec.research} "
                f"content: {sec.content} "
            )
            log.debug(f"[detailed_footer_writer_node] Constructed section_string: {section_string}")

        log.debug("[detailed_footer_writer_node] Calling detailed footer writer chain...")
        conclusion = await get_detailed_footer_write_chain().ainvoke({
            "query": query,
            "section": section_string,
        })

        log.debug(f"[detailed_footer_writer_node] Received conclusion: {conclusion.content}")
        return {
            "footer": {
                "conclusion": conclusion.content
            }
        }

    except Exception as e:
        log.error(f"[detailed_footer_writer_node] Error: {e}")
        return {
            "footer": {
                "conclusion": None
            }
        }

async def report_formatter_node(state: WriterState):
    try:
        log.warning(f"[report_formatter_node] Starting formatter node")
        log.debug(f"[report_formatter_node] Received state: {state}")
        log.debug(f"[report_formatter_node] Header: {state.header}")
        log.debug(f"[report_formatter_node] Sections: {state.sections.sections}")
        log.debug(f"[report_formatter_node] Footer: {state.footer}")
        log.debug(f"[report_formatter_node] References: {state.references}")

        header_str = f"Title: {state.header.title}\n\nSummary: {state.header.summary}\n\n"
        log.debug(f"[report_formatter_node] Header string:\n{header_str}")

        section_str = ""
        for sec in state.sections.sections:
            log.debug(f"[report_formatter_node] Processing section: {sec}")
            sec_str = (
                f"Section {sec.section_id}: {sec.name}\n"
                f"Description: {sec.description}\n"
                f"Content: {sec.content}\n\n"
            )
            section_str += sec_str
            log.debug(f"[report_formatter_node] Section string:\n{sec_str}")

        conclusion_str = f"Conclusion: {state.footer.conclusion}\n"
        log.debug(f"[report_formatter_node] Conclusion string:\n{conclusion_str}")

        reference_str = ""
        for reference in state.references:
            log.debug(f"[report_formatter_node] Processing reference: {reference}")
            url_str = ""
            for url in reference.source_url:
                url_str += f"{url} \n"
                log.debug(f"[report_formatter_node] URL: {url}")
            ref_str = f"Refrence: {reference.section_id} Name: {reference.section_name} url: {url_str} "
            reference_str += ref_str
            log.debug(f"[report_formatter_node] Reference string:\n{ref_str}")

        log.debug("[report_formatter_node] Calling formatter chain...")
        response = await get_report_formator_chain().ainvoke({
            "header": header_str,
            "section": section_str,
            "conclusion": conclusion_str,
            "reference": reference_str
        })

        log.debug(f"[report_formatter_node] Formatter chain response: {response.content}")
        return {
            "markdown": response.content
        }

    except Exception as e:
        log.exception(f"[report_formatter_node] Exception: {e}", exc_info=True)
        return {
            "markdown": None
        }
