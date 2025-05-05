from pydantic import BaseModel, Field
from typing import List, Optional, Union
from typing_extensions import Literal


class SearchResult(BaseModel):
    title: str = Field(description="The title of the search result")
    link: str = Field(description="The link to the source of the search result")
    snippet: str = Field(description="A brief description or snippet from the source")


class LocationOutput(BaseModel):
    country: str = Field(description="The country for the search query results")


class DuckDuckGoOutput(SearchResult):
    pass


class SerperQueryOutput(BaseModel):
    organic_results: List[SearchResult] = Field(
        description="The list of organic search results"
    )


class TavilyItem(BaseModel):
    title: str = Field(description="The title of the search result")
    url: str = Field(description="The source URL of the search result")
    content: str = Field(description="Content or snippet of the webpage")


class TavilyQueryOutput(BaseModel):
    results: List[TavilyItem] = Field(
        description="The output list from the Tavily search query"
    )


class ExaOutput(BaseModel):
    highlights: List[str] = Field(description="list of highlights")
    url: str = Field(description="url of the highlights")


class GitHubUserOutput(BaseModel):
    login: str = Field(description="GitHub username")
    name: Optional[str] = Field(description="User's full name")
    public_repos: int = Field(description="Number of public repositories")
    followers: int = Field(description="Number of followers")
    bio: Optional[str] = Field(description="User's bio")
    location: Optional[str] = Field(description="User's location")


class GitHubRepoOutput(BaseModel):
    name: str = Field(description="Repository name")
    full_name: str = Field(description="Full repository name")
    description: Optional[str] = Field(description="Repository description")
    stars: int = Field(description="Number of stars")
    forks: int = Field(description="Number of forks")
    language: Optional[str] = Field(description="Primary programming language used")
    topics: List[str] = Field(
        description="List of topics associated with the repository"
    )


class GitHubOrgOutput(BaseModel):
    login: str = Field(description="Organization login")
    name: Optional[str] = Field(description="Organization name")
    description: Optional[str] = Field(description="Organization description")
    public_repos: int = Field(description="Number of public repositories")
    members: List[str] = Field(description="List of member usernames")


class GitHubLanguageItem(BaseModel):
    name: str = Field(description="Repository name")
    full_name: str = Field(description="Full repository name")
    stars: int = Field(description="Number of stars")
    url: str = Field(description="URL of the repository")


class GitHubLanguageOutput(BaseModel):
    results: List[GitHubLanguageItem] = Field(
        description="List of repositories matching the  language search criteria"
    )


class ArxivDoc(BaseModel):
    title: str = Field(description="Title of the arXiv paper")
    authors: List[str] = Field(description="List of authors")
    summary: str = Field(description="Abstract of the paper")
    published: str = Field(description="Date of publication")


class ArxivOutput(BaseModel):
    results: Union[List[ArxivDoc], str] = Field(
        description="List of arXiv search results"
    )


class DuckDuckGoQuery(BaseModel):
    query: str = Field(..., description="Search query to be executed")
    max_results: int = Field(
        ..., description="Number of results to return (min: 1, max: 4)"
    )


class ExaQuery(BaseModel):
    query: str = Field(..., description="Search query for Exa")
    num_results: int = Field(..., description="Number of results to return")
    start_published_date: str = Field(..., description="Start date (yyyy-mm-dd)")
    end_published_date: str = Field(..., description="End date (yyyy-mm-dd)")
    category: Literal[
        "company",
        "research paper",
        "news",
        "linkedin profile",
        "github",
        "tweet",
        "movie",
        "song",
        "financial report",
    ] = Field(..., description="Category for search focus")


class SerperQuery(BaseModel):
    query: str = Field(..., description="Search query")
    num_results: int = Field(..., description="Number of results to retrieve")
    tbs: Literal["qdr:h", "qdr:d", "qdr:w", "qdr:m", "qdr:y"] = Field(
        ..., description="Time filter for search results"
    )


class GitHubUserQuery(BaseModel):
    username: str = Field(..., description="GitHub username for details")


class GitHubRepoQuery(BaseModel):
    full_name: str = Field(
        ..., description="Full name of the repository (e.g., 'torvalds/linux')"
    )


class GitHubOrgQuery(BaseModel):
    org_name: str = Field(..., description="Organization name")
    member_limit: int = Field(5, description="Maximum number of members to return")


class GitHubLanguageQuery(BaseModel):
    language: str = Field(..., description="Programming language for repository search")
    limit: int = Field(3, description="Maximum number of repositories to return")


class ArxivQuery(BaseModel):
    query: str = Field(..., description="Search query for arXiv")
    top_k_results: int = Field(3, description="Top k results to return")
    max_query_length: int = Field(300, description="Maximum allowed query length")
    load_max_docs: int = Field(3, description="Maximum number of documents to load")
    load_all_available_meta: bool = Field(
        False, description="Whether to load full metadata"
    )
    doc_content_chars_max: int = Field(
        40000, description="Maximum character length of document content"
    )


class TavilyQuery(BaseModel):
    query: str = Field(description="Search query for Tavily")
    topic: Literal["news", "general", "finance"] = Field(description="Topic for search")
    time_range: Literal["day", "week", "month", "year"] = Field(
        description="Time range for search results"
    )
    max_results: int = Field(
        default=3, description="Maximum number of results to return (max: 5)"
    )
