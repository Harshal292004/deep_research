from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.utilities.arxiv import ArxivAPIWrapper
from pydantic import BaseModel, Field
from typing import List, Literal, Union
from utilities.states import (
    DuckDuckGoOutput,
    LocationOutput,
    SereprSearchOutput,
    OrganicItem,
    FireScrapeOutput,
    TavilySearchItem,
    TavilySearchOutput,
    GitHubOrgOutput,
    GitHubRepoOutput,
    GitHubRepoSearchItem,
    GitHubRepoSearchOutput,
    GitHubUserOutput,
    ArxivSearchOutput
)
from exa_py import Exa, api
from utilities.config import settings
import requests
import http.client
import json
from firecrawl import FirecrawlApp
from tavily import TavilyClient
from github import Github 
from utilities.parsers import parse_arxiv_text
def duckduckgo_search(query: str, max_results: int = 2) -> List[DuckDuckGoOutput]:
    wrapper = DuckDuckGoSearchAPIWrapper(max_results=max_results)
    search = DuckDuckGoSearchResults(api_wrapper=wrapper, source="news")
    results = search.invoke(query)
    return results


def exa_search(
    query: str,
    highlights: bool,
    num_results: int,
    start_published_date: str,
    end_published_date: str,
    category: str,
) -> List[Union[api.ResultWithTextAndHighlights, api.ResultWithText]]:
    exa = Exa(api_key=settings.EXA_API_KEY)
    results = exa.search_and_contents(
        query=query,
        num_results=num_results,
        start_published_date=start_published_date,
        end_published_date=end_published_date,
        category=category,
        highlights=highlights,
        text=True,
    )
    return results


def get_location() -> LocationOutput:
    response = requests.get("https://ipinfo.io/json")
    result = response.json()
    country = str(result["country"])
    location_reuslt = LocationOutput(country=country.lower())
    return location_reuslt


def serper_search(
    query: str,
    country: str,
    num: int,
    tbs: Literal["qdr:h", "qdr:d", "qdr:w", "qdr:m", "qdr:y"],
):
    conn = http.client.HTTPSConnection("google.serper.dev")
    if country:
        payload = json.dumps({"q": query, "gl": country, "num": num, "tbs": tbs})
    else:
        payload = json.dumps({"q": query, "num": num, "tbs": tbs})

    headers = {"X-API-KEY": settings.SERPER_API_KEY, "Content-Type": "application/json"}
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = res.read()
    result = data["organic"]
    serper_output = []
    for item in result:
        organic_item = OrganicItem(
            title=item["title"], link=item["link"], snippet=item["snippet"]
        )
        serper_output.append(organic_item)

    serper_output_list = SereprSearchOutput(organic=serper_output)
    return serper_output_list


def fire_scrape_web_page():
    app = FirecrawlApp(api_key=settings.FIRE_CRAWL_API_KEY)
    # scrape a website:
    response= app.scrape_url(url, formats=["markdown"])
    result= response["data"]["markdown"]
    scraped_output= FireScrapeOutput(markdown=result)
    return  FireScrapeOutput

def tavily_search(query:str,topic:Literal['general','news'],time_range:Literal['week','day','month','year'],max_results:int):

    tavily_client = TavilyClient(api_key=settings.TAVLIY_API_KEY)
    response = tavily_client.search(query=query,topic=topic,time_range=time_range,max_results=max_results)
    results=response["results"]
    tavily_item_list=[]
    
    for res in results:
        tavily_item_list.append(
            TavilySearchItem(
                title= res["title"],
                url=res["url"],
                content=res["content"]
            )
        )
    
    tavily_search_output= TavilySearchOutput(results= tavily_search)
    return tavily_search_output
class GitHubInspector:
    def __init__(self, token: str):
        self.g = Github(token)

    def get_user_by_name(self, username: str) -> GitHubUserOutput:
        user = self.g.get_user(username)
        return GitHubUserOutput(
            login=user.login,
            name=user.name,
            public_repos=user.public_repos,
            followers=user.followers,
            bio=user.bio,
            location=user.location,
        )

    def get_repo_by_name(self, full_name: str) -> GitHubRepoOutput:
        repo = self.g.get_repo(full_name)
        return GitHubRepoOutput(
            name=repo.name,
            full_name=repo.full_name,
            description=repo.description,
            stars=repo.stargazers_count,
            forks=repo.forks_count,
            language=repo.language,
            topics=repo.get_topics()
        )

    def get_org_by_name(self, org_name: str, member_limit: int = 5) -> GitHubOrgOutput:
        org = self.g.get_organization(org_name)
        members = [member.login for member in org.get_members()][:member_limit]
        return GitHubOrgOutput(
            login=org.login,
            name=org.name,
            description=org.description,
            public_repos=org.public_repos,
            members=members
        )

    def search_repos_by_language(self, language: str, limit: int = 3) -> GitHubRepoSearchOutput:
        result = self.g.search_repositories(query=f"language:{language}")
        repos = [
            GitHubRepoSearchItem(
                name=repo.name,
                full_name=repo.full_name,
                stars=repo.stargazers_count,
                url=repo.html_url
            )
            for repo in result[:limit]
        ]
        return GitHubRepoSearchOutput(results=repos)

def arxiv_search(query: str, top_k_results: int = 3, ARXIV_MAX_QUERY_LENGTH: int = 300,
                 load_max_docs: int = 3, load_all_available_meta: bool = False,
                 doc_content_chars_max: int = 40000) -> ArxivSearchOutput:
    
    arxiv = ArxivAPIWrapper(
        top_k_results=top_k_results,
        ARXIV_MAX_QUERY_LENGTH=ARXIV_MAX_QUERY_LENGTH,
        load_max_docs=load_max_docs,
        load_all_available_meta=load_all_available_meta,
        doc_content_chars_max=doc_content_chars_max
    )
    
    docs = arxiv.run(query)
    
    output=parse_arxiv_text(raw_text= docs)
    
    return output

class DuckDuckGoSearch(BaseModel):
    """
    The Duck Duck Go search engine
    """

    query: str = Field(..., description="query to search through the engine")
    max_results: int = Field(
        ..., description="number of results desired from the engine (min:1) (max:4)"
    )


class ExaSearch(BaseModel):
    query: str = Field(..., description="The query to be provided to the exa search")
    highlights: bool = Field(
        ..., description="Includes highlights of the content in the results."
    )
    num_results: int = Field(..., description="Number of search results to return")
    start_published_date: str = Field(
        ...,
        description="Results will only include links with a published date after this date. eg. 2023-12-29(yyyy-mm-dd)",
    )
    end_published_date: str = Field(
        ...,
        description="Results will only include links with a published date before this date. eg. 2023-12-31(yyyy-mm-dd)",
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
        description="A data category to focus on when searching, with higher comprehensivity and data cleanliness.",
    )


class SereprSearch(BaseModel):
    query: str = Field(..., description="query to be searched for ")
    country: Optional[str] = Field(description="ISO 3166-1 alpha-2 naming of a country")
    num: int = Field(..., description="num of results to get")
    tbs: Literal["qdr:h", "qdr:d", "qdr:w", "qdr:m", "qdr:y"] = Field(
        ..., description="the timing to be search in"
    )


class GitHubUserQuery(BaseModel):
    username: str = Field(..., description="GitHub username to fetch details for")

class GitHubRepoQuery(BaseModel):
    full_name: str = Field(..., description="Full name of the repository (e.g. 'torvalds/linux')")

class GitHubOrgQuery(BaseModel):
    org_name: str = Field(..., description="Name of the GitHub organization")
    member_limit: int = Field(5, description="Number of members to return from the organization")

class GitHubLanguageSearchQuery(BaseModel):
    language: str = Field(..., description="Programming language to search repositories for")
    limit: int = Field(3, description="Number of repositories to return")
    
class ArxivSearchQuery(BaseModel):
    query: str = Field(..., description="The search query to be provided to the arXiv API")
    top_k_results: int = Field(3, description="Number of top-scored documents to return")
    ARXIV_MAX_QUERY_LENGTH: int = Field(300, description="Maximum allowed query length")
    load_max_docs: int = Field(3, description="Maximum number of documents to load")
    load_all_available_meta: bool = Field(False, description="Whether to load full metadata")
    doc_content_chars_max: int = Field(40000, description="Maximum character length of a document's content")
