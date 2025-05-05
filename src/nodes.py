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
    get_report_formator_chain,
)
from utilities.states.report_state import (
    Section,
    Sections,
    Footer,
    Header,
    Reference,
    ReportState,
    WriterState,
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
    TavilyItem,
)
from utilities.states.research_state import (
    ResearchState,
    QueryState,
    OutputState,
    tool_input_map,
    tool_output_map,
)
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
        response = await chain.ainvoke({"query": query})
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


async def query_generation_node(state: ResearchState):
    try:
        log.debug("Starting query generation...")
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
                input_list.append(
                    QueryState(section_id=section.section_id, query_state=output)
                )
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

    if exa_query:
        exa_output = exa_search(input=exa_query)

    if serper_query:
        serper_output = await serper_search(input=serper_query)
    if github_user_query:
        github_user_output = await GitHubInspector.get_user_by_name(
            input=github_user_query
        )

    if github_repo_query:
        github_repo_output = await GitHubInspector.get_repo_by_name(
            input=github_repo_query
        )

    if github_org_query:
        github_org_output = await GitHubInspector.get_org_by_name(
            input=github_org_query
        )

    if github_language_query:
        github_language_output = await GitHubInspector.search_repos_by_language(
            input=github_language_query
        )

    if arxiv_query:
        arxiv_output = await arxiv_search(input=arxiv_query)

    if tavily_query:
        tavily_output = await tavily_search(input=tavily_query)

    # Populate output based on query type
    output = output_schema()

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
        output.github_language_output = github_language_output

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
            github_language_query = getattr(
                query.query_state, "github_language_query", None
            )
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

            output_list.append(
                OutputState(section_id=query.section_id, output_state=output)
            )

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

        if duckduckgo_output:
            rolled_out_str += "DUCK DUCK GO SEARCH:\n\n\n"
            for duck in duckduckgo_output:
                duck_string = f"{duck.title} {duck.snippet}\n\n"
                duck_string = duck_string[:1000]
                rolled_out_str += f"{duck_string}\n\n"
                refrence.source_url.append(duck.link)

        if exa_output:
            rolled_out_str += "EXA SEARCH:\n\n\n"
            for exa in exa_output:
                highlight_string = "".join(exa.highlights)
                highlight_string = highlight_string[:1000]
                rolled_out_str += f"{highlight_string} \n\n"
                refrence.source_url.append(exa.url)

        if serper_output:
            rolled_out_str += "SERPER SEARCH:\n\n\n"
            for organic in serper_output:
                organic_string = f"{organic.title} {organic.snippet} \n\n"
                organic_string = organic_string[:2000]
                rolled_out_str += organic_string
                refrence.source_url.append(organic.link)

        if github_user_output:
            rolled_out_str += "GITHUB USER:\n\n\n"
            for gh in github_user_output:
                rolled_out_str += f"Github username: {gh.login} User's full name: {gh.name} Number of public repos: {gh.public_repos} Number of followers: {gh.followers} Bio of the user: {gh.bio} Location of the user: {gh.location}\n\n"
                refrence.source_url.append(f"https://github.com/{gh.login}")

        if github_repo_output:
            rolled_out_str += "GITHUB REPO:\n\n"
            for gh in github_repo_output:
                topic_str = "\n".join(gh.topics)
                rolled_out_str += f"Github Repo name: {gh.name} Repo's full name: {gh.full_name} Description of repo: {gh.description} Number of stars: {gh.stars} Number of forks: {gh.forks} Language used: {gh.language} Topics:\n{topic_str}\n\n"
                refrence.source_url.append(gh.html_url)

        if github_org_output:
            rolled_out_str += "GITHUB ORG:\n\n"
            for gh in github_org_output:
                member_list = "".join(gh.members)
                rolled_out_str += f"Github Org login: {gh.login} Org's full name: {gh.name} Org's description: {gh.description} Number of public_repo: {gh.public_repos} Member of repo: {member_list}\n\n"
                refrence.source_url.append(f"https://github.com/{gh.login}")

        if github_language_output:
            rolled_out_str += "GITHUB REPO Based on language:\n\n"
            for gh in github_language_output.results:
                rolled_out_str += f"Github repo's name: {gh.name} Repo's full name: {gh.full_name} Number of stars: {gh.stars} URL of the repo: {gh.url}\n\n"
                refrence.source_url.append(gh.url)

        if arxiv_output:
            rolled_out_str += "ARXIV Output:\n\n"
            for axv in arxiv_output.results:
                author_str = "  ".join(axv.authors[:4])
                arxiv_string = f"Paper Title: {axv.title} Authors: {author_str} Summary: {axv.summary[:200]} Published: {axv.published}\n\n"
                rolled_out_str += arxiv_string
                refrence.source_url.append(axv.url)

        if tavily_output:
            rolled_out_str += "TAVILY Output:\n\n"
            for tav in tavily_output.results:
                tavily_string = f"Title: {tav.title} Content: {tav.content} \n\n"
                tavily_string = tavily_string[:500]
                rolled_out_str += tavily_string
                refrence.source_url.append(tav.url)

        return rolled_out_str, refrence
    except Exception as e:
        log.error(f"Error occurred: {e}")
        return None, None


async def detailed_section_writer_node(state: WriterState):
    try:
        log.debug("Starting detailed section writer...")

        schema_output = tool_output_map.get(state.type_of_query)
        outputs = state.outputs
        sections = state.sections.sections
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
        return {"sections": {"sections": None}}


async def detailed_header_writer_node(state: WriterState):
    try:
        log.debug("Starting detailed header writer...")
        query = state.query
        type_of_query = state.type_of_query
        output = state.outputs
        sections = state.sections.sections
        title = state.header.title
        summary = state.header.summary

        section_written = None
        for sec in sections:
            section_string = (
                f"name: {sec.name} "
                f"description: {sec.description} "
                f"research: {sec.research} "
                f"content: {sec.content}"
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
        type_of_query = state.type_of_query
        sections = state.sections.sections

        for sec in sections:
            section_string = (
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

        header_str = (
            f"Title: {state.header.title}\n\nSummary: {state.header.summary}\n\n"
        )

        section_str = ""
        for sec in state.sections.sections:
            sec_str = (
                f"Section {sec.section_id}: {sec.name}\n"
                f"Description: {sec.description}\n"
                f"Content: {sec.content}\n\n"
            )
            section_str += sec_str

        conclusion_str = f"Conclusion: {state.footer.conclusion}\n"

        reference_str = ""
        for reference in state.references:
            url_str = ""
            for url in reference.source_url:
                url_str += f"{url} \n"
            ref_str = f"Refrence: {reference.section_id} Name: {reference.section_name} url: {url_str} "
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
