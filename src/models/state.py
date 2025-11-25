"""Unified state models for the research pipeline"""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from src.models.report import Footer, Header, Reference, Section, Sections
from src.models.tools import (
    ArxivOutput,
    ArxivQuery,
    DuckDuckGoOutput,
    DuckDuckGoQuery,
    ExaOutput,
    ExaQuery,
    GitHubLanguageOutput,
    GitHubLanguageQuery,
    GitHubOrgOutput,
    GitHubOrgQuery,
    GitHubRepoOutput,
    GitHubRepoQuery,
    GitHubUserOutput,
    GitHubUserQuery,
    SerperQuery,
    SerperQueryOutput,
    TavilyQuery,
    TavilyQueryOutput,
)


# Query State Models (unified with optional fields)
class ToolQueryState(BaseModel):
    """Unified query state with all tools as optional fields"""

    duckduckgo_query: Optional[DuckDuckGoQuery] = None
    exa_query: Optional[ExaQuery] = None
    serper_query: Optional[SerperQuery] = None
    github_user_query: Optional[GitHubUserQuery] = None
    github_repo_query: Optional[GitHubRepoQuery] = None
    github_org_query: Optional[GitHubOrgQuery] = None
    github_language_query: Optional[GitHubLanguageQuery] = None
    arxiv_query: Optional[ArxivQuery] = None
    tavily_query: Optional[TavilyQuery] = None


# Output State Models (unified with optional fields)
class ToolOutputState(BaseModel):
    """Unified output state with all tools as optional fields"""

    duckduckgo_output: Optional[List[DuckDuckGoOutput]] = None
    exa_output: Optional[List[ExaOutput]] = None
    serper_output: Optional[SerperQueryOutput] = None
    tavily_output: Optional[TavilyQueryOutput] = None
    github_user_output: Optional[GitHubUserOutput] = None
    github_repo_output: Optional[GitHubRepoOutput] = None
    github_org_output: Optional[GitHubOrgOutput] = None
    github_language_output: Optional[GitHubLanguageOutput] = None
    arxiv_output: Optional[ArxivOutput] = None


# Query and Output State wrappers
class QueryState(BaseModel):
    """Represents a specific query state with section identifier."""

    section_id: str
    query_state: ToolQueryState


class OutputState(BaseModel):
    """Represents an output state with section identifier."""

    section_id: str
    output_state: ToolOutputState


# Main State Models
class ReportState(BaseModel):
    query: Optional[str] = Field(default=None, description="Query of the user")
    type_of_query: Optional[
        Literal[
            "factual_query",
            "comparative_evaluative_query",
            "research_oriented_query",
            "execution_programming_query",
            "idea_generation",
        ]
    ] = Field(default=None, description="Type of the query")
    header: Optional[Header] = Field(
        default=None, description="The header of the report"
    )
    sections: Optional[Sections] = Field(
        default=None, description="All sections of the report"
    )
    footer: Optional[Footer] = Field(
        default=None, description="The footer of the report"
    )


class ResearchState(BaseModel):
    """Main research state containing query information, sections and results."""

    query: str = Field(description="The query given by the user")
    type_of_query: Literal[
        "factual_query",
        "comparative_evaluative_query",
        "research_oriented_query",
        "execution_programming_query",
        "idea_generation",
    ] = Field(
        description="The type of the query being asked, which determines the specific State of tools"
    )
    sections: Optional[List[Section]] = Field(
        default=None, description="All sections of the report"
    )
    queries: Optional[List[QueryState]] = Field(
        default=None, description="All of the query states"
    )
    outputs: Optional[List[OutputState]] = Field(
        default=None, description="Output of the tools"
    )


class WriterState(BaseModel):
    query: str = Field(description="The query by the user")
    type_of_query: Literal[
        "factual_query",
        "comparative_evaluative_query",
        "research_oriented_query",
        "execution_programming_query",
        "idea_generation",
    ] = Field(
        description="The type of the query being asked, which determines the specific set of tools"
    )
    outputs: Optional[List[OutputState]] = Field(
        default=None, description="Output of the tools"
    )
    header: Optional[Header] = Field(
        default=None, description="The header of the report"
    )
    sections: Optional[Sections] = Field(
        default=None, description="All sections of the report"
    )
    footer: Optional[Footer] = Field(
        default=None, description="The footer of the report"
    )
    references: Optional[List[Reference]] = Field(
        default=None, description="List of reference"
    )
    markdown: Optional[str] = Field(
        default=None, description="The actual formatted report"
    )


# Tool registry mapping
QUERY_TYPE_TOOLS = {
    "factual_query": ["duckduckgo", "exa", "tavily"],
    "comparative_evaluative_query": ["duckduckgo", "exa", "tavily", "serper"],
    "research_oriented_query": ["arxiv", "exa", "tavily", "serper"],
    "execution_programming_query": [
        "duckduckgo",
        "exa",
        "tavily",
        "github_user",
        "github_repo",
        "github_org",
        "github_language",
    ],
    "idea_generation": ["duckduckgo", "exa"],
}
