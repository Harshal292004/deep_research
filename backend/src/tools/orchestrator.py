"""Tool execution orchestrator"""
from typing import Optional, Any
from backend.src.models.tools import (
    DuckDuckGoQuery, ExaQuery, SerperQuery, GitHubUserQuery, GitHubRepoQuery,
    GitHubOrgQuery, GitHubLanguageQuery, ArxivQuery, TavilyQuery,
    ToolOutputState
)
from backend.src.tools.search import (
    duckduckgo_search, exa_search, serper_search, tavily_search, arxiv_search
)
from backend.src.tools.github import GitHubInspector as GitHubInspectorClass
from backend.src.models.state import QUERY_TYPE_TOOLS
from backend.src.helpers.logger import log

async def get_tool_output(
    duckduckgo_query: Optional[DuckDuckGoQuery],
    exa_query: Optional[ExaQuery],
    serper_query: Optional[SerperQuery],
    github_user_query: Optional[GitHubUserQuery],
    github_repo_query: Optional[GitHubRepoQuery],
    github_org_query: Optional[GitHubOrgQuery],
    github_language_query: Optional[GitHubLanguageQuery],
    arxiv_query: Optional[ArxivQuery],
    tavily_query: Optional[TavilyQuery],
    output_schema: Any,
    type_of_query: str,
):
    """Execute tools based on query type and populate output"""
    # Initialize the output
    output = output_schema()
    
    # Get tools for this query type
    tools_for_type = QUERY_TYPE_TOOLS.get(type_of_query, [])
    
    # Execute tools based on query type
    if duckduckgo_query and "duckduckgo" in tools_for_type:
        output.duckduckgo_output = await duckduckgo_search(input=duckduckgo_query)

    if exa_query and "exa" in tools_for_type:
        output.exa_output = exa_search(input=exa_query)

    if serper_query and "serper" in tools_for_type:
        output.serper_output = await serper_search(input=serper_query)
        
    if github_user_query and "github_user" in tools_for_type:
        inspector = GitHubInspectorClass()
        output.github_user_output = await inspector.get_user_by_name(
            input=github_user_query
        )

    if github_repo_query and "github_repo" in tools_for_type:
        inspector = GitHubInspectorClass()
        output.github_repo_output = await inspector.get_repo_by_name(
            input=github_repo_query
        )

    if github_org_query and "github_org" in tools_for_type:
        inspector = GitHubInspectorClass()
        output.github_org_output = await inspector.get_org_by_name(
            input=github_org_query
        )

    if github_language_query and "github_language" in tools_for_type:
        inspector = GitHubInspectorClass()
        output.github_language_output = await inspector.search_repos_by_language(
            input=github_language_query
        )

    if arxiv_query and "arxiv" in tools_for_type:
        output.arxiv_output = await arxiv_search(input=arxiv_query)

    if tavily_query and "tavily" in tools_for_type:
        output.tavily_output = await tavily_search(input=tavily_query)

    return output

