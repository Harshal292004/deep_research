from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Any, Union
from utilities.states.tool_states import (
    DuckDuckGoOutput,
    LocationOutput,
    SereprSearchOutput,
    OrganicItem,
    TavilySearchItem,
    TavilySearchOutput,
    GitHubOrgOutput,
    GitHubRepoOutput,
    GitHubRepoSearchItem,
    GitHubRepoSearchOutput,
    GitHubUserOutput,
    ArxivSearchOutput,
    DuckDuckGoSearch,
    ExaSearch,
    SerperSearch,
    GitHubUserQuery,
    GitHubRepoQuery,
    GitHubOrgQuery,
    GitHubLanguageSearchQuery,
    ArxivSearchQuery,
    TavilySearchQuery,
)
from utilities.states.report_state import Sectio
from exa_py import api


class QueryState(BaseModel):
    idx: str
    query_set: Any


class ResearchState(BaseModel):
    query: str = Field(description="The query given by the user")
    type_of_query: Literal[
        "factual_query",
        "comparative_evaluative_query",
        "research_oriented_query",
        "execution_programming_query",
        "idea_generation",
    ] = Field(
        description="The type of the query being asked, which determines the specific set of tools"
    )
    sections: List[Section] = Field(description="All sections of the report")
    queries: Optional[List[QueryState]] = Field(
        default=None, description="All of the query states"
    )
    output_list: Optional[List[QueryState]] = Field(
        default=None, description="Output of the tools"
    )


class FactualQuerySet(BaseModel):
    tavily_search: Optional[TavilySearchQuery] = Field(
        default=None, description="The TavilySearch input"
    )
    duckduckgo_search: Optional[DuckDuckGoSearch] = Field(
        default=None, description="The DuckDuckGoSearch inputs"
    )
    exa_search: Optional[ExaSearch] = Field(
        default=None, description="The ExaSearch input"
    )


class ComparativeQuerySet(BaseModel):
    serper_search: Optional[SerperSearch] = Field(
        default=None, description="The SerperSearch input"
    )
    tavily_search: Optional[TavilySearchQuery] = Field(
        default=None, description="The TavilySearch input"
    )
    exa_search: Optional[ExaSearch] = Field(
        default=None, description="The ExaSearch input"
    )
    duckduckgo_search: Optional[DuckDuckGoSearch] = Field(
        default=None, description="The DuckDuckGoSearch inputs"
    )


class ResearchQuerySet(BaseModel):
    arxiv_search_query: Optional[ArxivSearchQuery] = Field(
        default=None, description="The ArxivSearch Query"
    )
    exa_search: Optional[ExaSearch] = Field(
        default=None, description="The ExaSearch input"
    )
    tavily_search: Optional[TavilySearchQuery] = Field(
        default=None, description="The TavilySearch input"
    )
    serper_search: Optional[SerperSearch] = Field(
        default=None, description="The SerperSearch input"
    )


class ProgrammingQuerySet(BaseModel):
    tavily_search: Optional[TavilySearchQuery] = Field(
        default=None, description="The TavilySearch input"
    )
    duckduckgo_search: Optional[DuckDuckGoSearch] = Field(
        default=None, description="The DuckDuckGoSearch inputs"
    )
    exa_search: Optional[ExaSearch] = Field(
        default=None, description="The ExaSearch input"
    )
    get_user_by_name: Optional[GitHubUserQuery] = Field(
        default=None, description="The GithubUserQuery input"
    )
    get_repo_by_name: Optional[GitHubRepoQuery] = Field(
        default=None, description="The GithubRepoQuery input"
    )
    get_org_by_name: Optional[GitHubOrgQuery] = Field(
        default=None, description="The GithubOrgQuery input"
    )
    search_repos_by_language: Optional[GitHubLanguageSearchQuery] = Field(
        default=None, description="The GithubLanguageQuery input"
    )


class IdeaQuerySet(BaseModel):
    exa_search: Optional[ExaSearch] = Field(
        default=None, description="The ExaSearch input"
    )
    duckduckgo_search: Optional[DuckDuckGoSearch] = Field(
        default=None, description="The DuckDuckGoSearch inputs"
    )


class FactualOutput(BaseModel):
    duckduckgo_output: Optional[List[DuckDuckGoOutput]] = None
    exa_output: Optional[
        List[Union[api.ResultWithTextAndHighlights, api.ResultWithText]]
    ] = None
    tav_output: Optional[List[TavilySearchOutput]] = None


class ComparativeOutput(BaseModel):
    duckduckgo_output: Optional[DuckDuckGoOutput] = None
    exa_output: Optional[
        List[Union[api.ResultWithTextAndHighlights, api.ResultWithText]]
    ] = None
    tav_output: Optional[TavilySearchOutput] = None
    serper_output: Optional[SereprSearchOutput] = None


class ResearchOutput(BaseModel):
    arxiv_output: Optional[ArxivSearchOutput] = None
    exa_output: Optional[List[Union[api.ResultWithTextAndHighlights, api.ResultWithText]]] = None
    tav_output: Optional[TavilySearchOutput] = None
    serper_output: Optional[SereprSearchOutput] = None


class ProgrammingOutput(BaseModel):
    duckduckgo_output: Optional[DuckDuckGoOutput] = None
    exa_output: Optional[List[Union[api.ResultWithTextAndHighlights, api.ResultWithText]]] = None
    tav_output: Optional[TavilySearchOutput] = None
    gh_user_output: Optional[GitHubUserOutput] = None
    gh_repo_output: Optional[GitHubRepoOutput] = None
    gh_org_output: Optional[GitHubOrgOutput] = None
    gh_lang_output: Optional[GitHubRepoSearchOutput] = None


class IdeaOutput(BaseModel):
    duckduckgo_output: Optional[DuckDuckGoOutput] = None
    exa_output: Optional[List[Union[api.ResultWithTextAndHighlights, api.ResultWithText]]] = None


query_tool_map = {
    "factual_query": FactualQuerySet,
    "comparative_evaluative_query": ComparativeQuerySet,
    "research_oriented_query": ResearchQuerySet,
    "execution_programming_query": ProgrammingQuerySet,
    "idea_generation": IdeaQuerySet,
}

query_tool_output = {
    "factual_query": FactualOutput,
    "comparative_evaluative_query": ComparativeOutput,
    "research_oriented_query": ResearchOutput,
    "execution_programming_query": ProgrammingOutput,
    "idea_generation": IdeaOutput,
}
