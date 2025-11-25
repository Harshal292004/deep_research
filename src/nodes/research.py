"""Research nodes (query generation, tool output)"""
from src.models.state import ResearchState, QueryState, OutputState, ToolQueryState, ToolOutputState
from src.chains.builders import get_search_queries_chain
from src.tools.orchestrator import get_tool_output
from src.helpers.logger import log

async def query_generation_node(state: ResearchState):
    try:
        log.debug("Starting query generation...")
        query = state.query
        type_of_query = state.type_of_query
        schema_of_tools = ToolQueryState
        input_list = []
        if state.sections:    
            for section in state.sections:
                if section.research:
                    section_string = f"Section: {section.name}\nDescription: {section.description}\nContent: {section.content}\n\n"
                    chain = get_search_queries_chain(schema=schema_of_tools)
                    if chain:        
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

async def tool_output_node(state: ResearchState):
    try:
        log.debug("Starting tool_output_node...")
        queries = state.queries
        type_of_query = state.type_of_query
        schema_of_output = ToolOutputState
        output_list = []
        if queries:     
            for query in queries:
                # Extract queries from unified ToolQueryState
                duckduckgo_query = query.query_state.duckduckgo_query
                exa_query = query.query_state.exa_query
                serper_query = query.query_state.serper_query
                github_user_query = query.query_state.github_user_query
                github_repo_query = query.query_state.github_repo_query
                github_org_query = query.query_state.github_org_query
                github_language_query = query.query_state.github_language_query
                arxiv_query = query.query_state.arxiv_query
                tavily_query = query.query_state.tavily_query

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
                    output_schema=schema_of_output,
                    type_of_query=type_of_query,
                )

                output_list.append(
                    OutputState(section_id=query.section_id, output_state=output)
                )

        return {"outputs": output_list}
    except Exception as e:
        log.error(f"Error in tool_output_node: {e}")
        return {"outputs": None}

