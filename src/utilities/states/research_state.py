from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from utilities.states.tool_states import (
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
    set_of_tools: List[str] = Field(
        description="The set of the tools to be used for the serch purposes"
    )
    sections: str= Field()


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


query_tool_map = {
    "factual_query": FactualQuerySet,
    "comparative_evaluative_query": ComparativeQuerySet,
    "research_oriented_query": ResearchQuerySet,
    "execution_programming_query": ProgrammingQuerySet,
    "idea_generation": IdeaQuerySet,
}
