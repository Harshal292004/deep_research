from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.utilities.arxiv import ArxivAPIWrapper
from pydantic import BaseModel, Field
from typing import List, Literal, Union
from langchain_core.tools import tool

from utilities.states.tool_states import (
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
    ArxivSearchOutput,
    DuckDuckGoSearch,
    ExaSearch,
    SereprSearch,
    GitHubUserQuery,
    GitHubRepoQuery,
    GitHubOrgQuery,
    GitHubLanguageSearchQuery,
    ArxivSearchQuery,
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


@tool
def duckduckgo_search(input: DuckDuckGoSearch) -> List[DuckDuckGoOutput]:
    wrapper = DuckDuckGoSearchAPIWrapper(max_results=input.max_results)
    search = DuckDuckGoSearchResults(api_wrapper=wrapper, source="news")
    results = search.invoke(input.query)
    return results


@tool
def exa_search(
    input: ExaSearch,
) -> List[Union[api.ResultWithTextAndHighlights, api.ResultWithText]]:
    exa = Exa(api_key=settings.EXA_API_KEY)
    results = exa.search_and_contents(
        query=input.query,
        num_results=input.num_results,
        start_published_date=input.start_published_date,
        end_published_date=input.end_published_date,
        category=input.category,
        highlights=input.highlights,
        text=True,
    )
    return results


@tool
def get_location() -> LocationOutput:
    response = requests.get("https://ipinfo.io/json")
    result = response.json()
    country = str(result["country"])
    location_reuslt = LocationOutput(country=country.lower())
    return location_reuslt


@tool
def serper_search(input: SereprSearch) -> SereprSearchOutput:
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps(
        {"q": input.query, "gl": input.country, "num": input.num, "tbs": input.tbs}
    )
    headers = {"X-API-KEY": settings.SERPER_API_KEY, "Content-Type": "application/json"}
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read())
    organic = [OrganicItem(**item) for item in data["organic"]]
    return SereprSearchOutput(organic=organic)


def fire_scrape_web_page():
    app = FirecrawlApp(api_key=settings.FIRE_CRAWL_API_KEY)
    # scrape a website:
    response = app.scrape_url(url, formats=["markdown"])
    result = response["data"]["markdown"]
    scraped_output = FireScrapeOutput(markdown=result)
    return FireScrapeOutput


@tool
def tavily_search(input: TavilySearchOutput) -> TavilySearchOutput:
    tavily_client = TavilyClient(api_key=settings.TAVLIY_API_KEY)
    response = tavily_client.search(
        query=input.query,
        topic=input.topic,
        time_range=input.time_range,
        max_results=input.max_results,
    )
    items = [
        TavilySearchItem(
            title=entry["title"], url=entry["url"], content=entry["content"]
        )
        for entry in response["results"]
    ]
    return TavilySearchOutput(results=items)


class GitHubInspector:
    def __init__(self, token: str = settings.GITHUB_ACCESS_TOKEN):
        self.g = Github(token)

    @tool
    def get_user_by_name(self, input: GitHubUserQuery) -> GitHubUserOutput:
        user = self.g.get_user(input.username)
        return GitHubUserOutput(
            login=user.login,
            name=user.name,
            public_repos=user.public_repos,
            followers=user.followers,
            bio=user.bio,
            location=user.location,
        )

    @tool
    def get_repo_by_name(self, input: GitHubRepoQuery) -> GitHubRepoOutput:
        repo = self.g.get_repo(input.full_name)
        return GitHubRepoOutput(
            name=repo.name,
            full_name=repo.full_name,
            description=repo.description,
            stars=repo.stargazers_count,
            forks=repo.forks_count,
            language=repo.language,
            topics=repo.get_topics(),
        )

    @tool
    def get_org_by_name(self, input: GitHubOrgQuery) -> GitHubOrgOutput:
        org = self.g.get_organization(input.org_name)
        members = [member.login for member in org.get_members()][: input.member_limit]
        return GitHubOrgOutput(
            login=org.login,
            name=org.name,
            description=org.description,
            public_repos=org.public_repos,
            members=members,
        )

    @tool
    def search_repos_by_language(
        self, input: GitHubLanguageSearchQuery
    ) -> GitHubRepoSearchOutput:
        result = self.g.search_repositories(query=f"language:{input.language}")
        repos = [
            GitHubRepoSearchItem(
                name=repo.name,
                full_name=repo.full_name,
                stars=repo.stargazers_count,
                url=repo.html_url,
            )
            for repo in result[: input.limit]
        ]
        return GitHubRepoSearchOutput(results=repos)


@tool
def arxiv_search(input: ArxivSearchQuery) -> ArxivSearchOutput:
    wrapper = ArxivAPIWrapper(
        top_k_results=input.top_k_results,
        ARXIV_MAX_QUERY_LENGTH=input.ARXIV_MAX_QUERY_LENGTH,
        load_max_docs=input.load_max_docs,
        load_all_available_meta=input.load_all_available_meta,
        doc_content_chars_max=input.doc_content_chars_max,
    )
    docs = wrapper.run(input.query)
    parsed = parse_arxiv_text(raw_text=docs)
    return ArxivSearchOutput(results=parsed)
