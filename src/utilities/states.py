from pydantic import BaseModel, Field
from typing import List,Optional


class DuckDuckGoOutput(BaseModel):
    snippet: str = Field(description="The snippet extracted from the whole page")
    title: str = Field(description="The title of the search")
    link: str = Field(description="The refrence")


class LocationOutput(BaseModel):
    country: str = Field(description="The country the results are to searched in")


class OrganicItem(BaseModel):
    title: str = Field(description="The title of the search")
    link: str = Field(description="The source of the search")
    snippet: str = Field(description="The snippet of the webpage")


class SereprSearchOutput(BaseModel):
    organic: List[OrganicItem] = Field(description="the list of organic items")

class FireScrapeOutput(BaseModel):
    markdown: str=  Field(description="The output of the fire scrape ")
    
    
class TavilySearchItem(BaseModel):
    title:str = Field(description="The title of the search")
    url:str = Field(description="The source of the search")
    content:str = Field(description="The content of the webpage")
    
class TavilySearchOutput(BaseModel):
    results:List[TavilySearchItem] = Field(description="The output list of the tavily search")
    
    

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
    results: List[GitHubRepoSearchItem] = Field(description="List of repositories matching the language search")


class ArxivDoc(BaseModel):
    title: str = Field(description="Title of the arXiv paper")
    authors: List[str] = Field(description="List of authors")
    summary: str = Field(description="Abstract of the paper")
    published: str = Field(description="Date of publication")
    
class ArxivSearchOutput(BaseModel):
    results: Union[List[ArxivDoc],str] = Field(description="List of arXiv search results")
    