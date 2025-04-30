from pydantic import BaseModel, Field
from typing import List, Literal,Optional
from utilities.states.tool_states import (
    DuckDuckGoSearch,
    ExaSearch,
    SerperSearch,
    GitHubUserQuery,
    GitHubRepoQuery,
    GitHubOrgQuery,
    GitHubLanguageSearchQuery,
    ArxivSearchQuery,
    TavilySearchItem
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
    set_of_tools:List[str] = Field(description="The set of the tools to be used for the serch purposes")


class FactualQuerySet(BaseModel):
    duckduck_go_search:Optional[DuckDuckGoSearch]= Field(default=None,description="The DuckDuckGo search inputs")
    exa_search:Optional[ExaSearch]= Field(default=None,description="The ExaSearch input")
    serper_search:Optional[SerperSearch] = Field(default=None,description="The SerperSearch input")
    github_user_query:Optional[GitHubUserQuery] = Field(default=None,description="The GithubUserQuery input")
    github_repo_query:Optional[GitHubRepoQuery] = Field(default=None,description="The GithubRepoQuery input")
    github_org_query:Optional[GitHubOrgQuery] = Field(default=None,description="The GithubOrgQuery input")
    github_language_search_query:Optional[GitHubLanguageSearchQuery] = Field(default=None,description="The GithubLanguageQuery input")
    arxiv_search_query:Optional[ArxivSearchQuery] = Field(default=None,description="The ArxivSearchQuery input")

class ComparativeQuerySet(BaseModel):
    serper_search:Optional[SerperSearch] = Field(default=None,description="The SerperSearch input")
    
   
    pass

class ResearchQuerySet(BaseModel):
    pass

class ProgrammingQuerySet(BaseModel):
    pass

class IdeaQuerySet(BaseModel):
    pass