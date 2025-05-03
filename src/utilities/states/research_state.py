from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Any, Union

from utilities.states.tool_states import (
    DuckDuckGoQuery,
    ExaQuery,
    SerperQuery,
    GitHubUserQuery,
    GitHubRepoQuery,
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
from utilities.states.report_state import Section


class QueryState(BaseModel):
    """Represents a specific query state with section identifier."""
    section_id: str
    query_state: Any


class OutputState(BaseModel):
    """Represents an output state with section identifier."""
    section_id: str
    output_state: Any


class ResearchState(BaseModel):
    """Main research state containing query information, sections and results."""
    query: str = Field(description="The query given by the user")
    type_of_query: Literal[
        "factual_query",
        "comparative_evaluative_query",
        "research_oriented_query",
        "execution_programming_query",
        "idea_generation",
    ] = Field(description="The type of the query being asked, which determines the specific State of tools")
    sections: List[Section] = Field(default=None, description="All sections of the report")
    queries: Optional[List[QueryState]] = Field(default=None, description="All of the query states")
    outputs: Optional[List[OutputState]] = Field(default=None, description="Output of the tools")


class FactualQueryState(BaseModel):
    """State of query tools used for factual queries."""
    tavily_query: Optional[TavilyQuery] = Field(
        default=None, description="The Tavily query input"
    )
    duckduckgo_query: Optional[DuckDuckGoQuery] = Field(
        default=None, description="The DuckDuckGo query input"
    )
    exa_query: Optional[ExaQuery] = Field(
        default=None, description="The Exa query input"
    )


class ComparativeQueryState(BaseModel):
    """State of query tools used for comparative evaluative queries."""
    serper_query: Optional[SerperQuery] = Field(
        default=None, description="The Serper query input"
    )
    tavily_query: Optional[TavilyQuery] = Field(
        default=None, description="The Tavily query input"
    )
    exa_query: Optional[ExaQuery] = Field(
        default=None, description="The Exa query input"
    )
    duckduckgo_query: Optional[DuckDuckGoQuery] = Field(
        default=None, description="The DuckDuckGo query input"
    )


class ResearchQueryState(BaseModel):
    """State of query tools used for research oriented queries."""
    arxiv_query: Optional[ArxivQuery] = Field(
        default=None, description="The Arxiv query input"
    )
    exa_query: Optional[ExaQuery] = Field(
        default=None, description="The Exa query input"
    )
    tavily_query: Optional[TavilyQuery] = Field(
        default=None, description="The Tavily query input"
    )
    serper_query: Optional[SerperQuery] = Field(
        default=None, description="The Serper query input"
    )


class ProgrammingQueryState(BaseModel):
    """State of query tools used for execution and programming queries."""
    tavily_query: Optional[TavilyQuery] = Field(
        default=None, description="The Tavily query input"
    )
    duckduckgo_query: Optional[DuckDuckGoQuery] = Field(
        default=None, description="The DuckDuckGo query input"
    )
    exa_query: Optional[ExaQuery] = Field(
        default=None, description="The Exa query input"
    )
    github_user_query: Optional[GitHubUserQuery] = Field(
        default=None, description="The GitHub user query input"
    )
    github_repo_query: Optional[GitHubRepoQuery] = Field(
        default=None, description="The GitHub repo query input"
    )
    github_org_query: Optional[GitHubOrgQuery] = Field(
        default=None, description="The GitHub organization query input"
    )
    github_language_query: Optional[GitHubLanguageQuery] = Field(
        default=None, description="The GitHub language query input"
    )


class IdeaQueryState(BaseModel):
    """State of query tools used for idea generation queries."""
    exa_query: Optional[ExaQuery] = Field(
        default=None, description="The Exa query input"
    )
    duckduckgo_query: Optional[DuckDuckGoQuery] = Field(
        default=None, description="The DuckDuckGo query input"
    )


class FactualOutput(BaseModel):
    """Output model for factual queries."""
    duckduckgo_output: Optional[List[DuckDuckGoOutput]] = None
    exa_output: Optional[List[ExaOutput]] = None
    tavily_output: Optional[TavilyQueryOutput] = None


class ComparativeOutput(BaseModel):
    """Output model for comparative evaluative queries."""
    duckduckgo_output: Optional[List[DuckDuckGoOutput]] = None
    exa_output: Optional[List[ExaOutput]] = None
    tavily_output: Optional[TavilyQueryOutput] = None
    serper_output: Optional[SerperQueryOutput] = None


class ResearchOutput(BaseModel):
    """Output model for research oriented queries."""
    arxiv_output: Optional[ArxivOutput] = None
    exa_output: Optional[List[ExaOutput]] = None
    tavily_output: Optional[TavilyQueryOutput] = None
    serper_output: Optional[SerperQueryOutput] = None


class ProgrammingOutput(BaseModel):
    """Output model for execution and programming queries."""
    duckduckgo_output: Optional[List[DuckDuckGoOutput]] = None
    exa_output: Optional[List[ExaOutput]] = None
    tavily_output: Optional[TavilyQueryOutput] = None
    github_user_output: Optional[GitHubUserOutput] = None
    github_repo_output: Optional[GitHubRepoOutput] = None
    github_org_output: Optional[GitHubOrgOutput] = None
    github_language_output: Optional[GitHubLanguageOutput] = None


class IdeaOutput(BaseModel):
    """Output model for idea generation queries."""
    duckduckgo_output: Optional[List[DuckDuckGoOutput]] = None
    exa_output: Optional[List[ExaOutput]] = None


# Mapping dictionaries to link query types with their respective models
tool_input_map = {
    "factual_query": FactualQueryState,
    "comparative_evaluative_query": ComparativeQueryState,
    "research_oriented_query": ResearchQueryState,
    "execution_programming_query": ProgrammingQueryState,
    "idea_generation": IdeaQueryState,
}

tool_output_map = {
    "factual_query": FactualOutput,
    "comparative_evaluative_query": ComparativeOutput,
    "research_oriented_query": ResearchOutput,
    "execution_programming_query": ProgrammingOutput,
    "idea_generation": IdeaOutput,
}