from pydantic import BaseModel, Field
from typing import List, Optional


class DuckDuckGoOutput(BaseModel):
    snippet: str = Field(description="The snippet extracted from the whole page")
    title: str = Field(description="The title of the search")
    link: str = Field(description="The reference")


class LocationOutput(BaseModel):
    country: str = Field(description="The country the results are to be searched in")


class OrganicItem(BaseModel):
    title: str = Field(description="The title of the search")
    link: str = Field(description="The source of the search")
    snippet: str = Field(description="The snippet of the webpage")


class SerperSearchOutput(BaseModel):
    organic: List[OrganicItem] = Field(description="The list of organic items")


class FireScrapeOutput(BaseModel):
    markdown: str = Field(description="The output of the fire scrape")


class TavilySearchItem(BaseModel):
    title: str = Field(description="The title of the search")
    url: str = Field(description="The source of the search")
    content: str = Field(description="The content of the webpage")


class TavilySearchOutput(BaseModel):
    results: List[TavilySearchItem] = Field(
        description="The output list of the Tavily search"
    )


class GitHubUserOutput(BaseModel):
    login: str = Field(description="GitHub username")
    name: Optional[str] = Field(description="User's full name")
    public_repos: int = Field(description="Number of public repositories")
    followers: int = Field(description="Number of followers")
    bio: Optional[str] = Field(description="User bio")
    location: Optional[str] = Field(description="User location")


class GitHubRepoOutput(BaseModel):
    name: str = Field(description="Repository name")
    full_name: str = Field(description="Full repository name")
    description: Optional[str] = Field(description="Repository description")
    stars: int = Field(description="Number of stars")
    forks: int = Field(description="Number of forks")
    language: Optional[str] = Field(description="Main language used")
    topics: List[str] = Field(description="List of topics associated with the repo")


class GitHubOrgOutput(BaseModel):
    login: str = Field(description="Organization login")
    name: Optional[str] = Field(description="Organization name")
    description: Optional[str] = Field(description="Organization description")
    public_repos: int = Field(description="Number of public repositories")
    members: List[str] = Field(description="List of member usernames")


class GitHubRepoSearchItem(BaseModel):
    name: str = Field(description="Repository name")
    full_name: str = Field(description="Full repository name")
    stars: int = Field(description="Number of stars")
    url: str = Field(description="URL of the repository")


class GitHubRepoSearchOutput(BaseModel):
    results: List[GitHubRepoSearchItem] = Field(
        description="List of repositories matching the language search"
    )


class ArxivDoc(BaseModel):
    title: str = Field(description="Title of the arXiv paper")
    authors: List[str] = Field(description="List of authors")
    summary: str = Field(description="Abstract of the paper")
    published: str = Field(description="Date of publication")


class ArxivSearchOutput(BaseModel):
    results: Union[List[ArxivDoc], str] = Field(
        description="List of arXiv search results"
    )


class DuckDuckGoSearch(BaseModel):
    query: str = Field(..., description="Query to search through the engine")
    max_results: int = Field(
        ..., description="Number of results desired from the engine (min:1) (max:4)"
    )


class ExaSearch(BaseModel):
    query: str = Field(..., description="The query to be provided to the Exa search")
    highlights: bool = Field(
        ..., description="Includes highlights of the content in the results."
    )
    num_results: int = Field(..., description="Number of search results to return")
    start_published_date: str = Field(
        ...,
        description="Results will only include links with a published date after this date. eg. 2023-12-29 (yyyy-mm-dd)",
    )
    end_published_date: str = Field(
        ...,
        description="Results will only include links with a published date before this date. eg. 2023-12-31 (yyyy-mm-dd)",
    )
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
    ] = Field(
        ...,
        description="A data category to focus on when searching, with higher comprehensiveness and data cleanliness.",
    )


class SerperSearch(BaseModel):
    query: str = Field(..., description="Query to be searched for")
    country: Optional[str] = Field(description="ISO 3166-1 alpha-2 naming of a country")
    num: int = Field(..., description="Number of results to get")
    tbs: Literal["qdr:h", "qdr:d", "qdr:w", "qdr:m", "qdr:y"] = Field(
        ..., description="The timing to be searched in"
    )


class GitHubUserQuery(BaseModel):
    username: str = Field(..., description="GitHub username to fetch details for")


class GitHubRepoQuery(BaseModel):
    full_name: str = Field(
        ..., description="Full name of the repository (e.g. 'torvalds/linux')"
    )


class GitHubOrgQuery(BaseModel):
    org_name: str = Field(..., description="Name of the GitHub organization")
    member_limit: int = Field(
        5, description="Number of members to return from the organization"
    )


class GitHubLanguageSearchQuery(BaseModel):
    language: str = Field(
        ..., description="Programming language to search repositories for"
    )
    limit: int = Field(3, description="Number of repositories to return")


class ArxivSearchQuery(BaseModel):
    query: str = Field(
        ..., description="The search query to be provided to the arXiv API"
    )
    top_k_results: int = Field(
        3, description="Number of top-scored documents to return"
    )
    ARXIV_MAX_QUERY_LENGTH: int = Field(300, description="Maximum allowed query length")
    load_max_docs: int = Field(3, description="Maximum number of documents to load")
    load_all_available_meta: bool = Field(
        False, description="Whether to load full metadata"
    )
    doc_content_chars_max: int = Field(
        40000, description="Maximum character length of a document's content"
    )
