import json
import aiohttp
import asyncio
import requests
import http.client
from typing import List, Union
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.utilities.arxiv import ArxivAPIWrapper
from pydantic import BaseModel, Field
from utilities.states.tool_states import (
   DuckDuckGoQuery,
   ExaQuery,
   SerperQuery,
   GitHubUserQuery,
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
from exa_py import Exa, api
from config import settings
from tavily import TavilyClient
from github import Github
from utilities.helpers.parsers import parse_arxiv_text
from utilities.helpers.logger import log

async def duckduckgo_search(input:DuckDuckGoQuery) -> List[DuckDuckGoOutput]:
    wrapper = DuckDuckGoSearchAPIWrapper(max_results=input.max_results)
    search = DuckDuckGoSearchResults(api_wrapper=wrapper, source="news")
    try:
        log.debug(f"Starting DuckDuckGo search with query: {input.query}")
        results = await search.ainvoke(input.query)
        log.info(f"Search completed with {len(results)} results.")
        return results
    except Exception as e:
        log.error(f"Error during DuckDuckGo search: {e}")
        return []


async def exa_search(input: ExaQuery) -> List[ExaOutput]:
    exa = Exa(api_key=settings.EXA_API_KEY)
    exa_output= []
    try:
        log.debug(f"Starting Exa search with query: {input.query}")
        results = await exa.search_and_contents(
            query=input.query,
            num_results=input.num_results,
            start_published_date=input.start_published_date,
            end_published_date=input.end_published_date,
            category=input.category,
            text=True,
        )
        log.info(f"Exa search completed with {len(results)} results.")
        for result in results:
            exa_output.append(ExaOutput(text=result.text, url= result.url))
        return exa_output
    except Exception as e:
        log.error(f"Error during Exa search: {e}")
        return []


async def get_location() -> LocationOutput:
    try:
        log.debug("Fetching location information...")
        async with aiohttp.ClientSession() as session:
            async with session.get("https://ipinfo.io/json") as response:
                result = await response.json()
                country = str(result.get("country", ""))
                location_result = LocationOutput(country=country.lower())
                log.info(f"Location found: {country.lower()}")
                return location_result
    except Exception as e:
        log.error(f"Error fetching location: {e}")
        return LocationOutput(country="")
    
async def serper_search(input: SerperQuery) -> SerperQueryOutput:
    conn = http.client.HTTPSConnection("google.serper.dev")
    country= await get_location()
    country= country.country
    payload = json.dumps(
        {"q": input.query, "gl": country, "num": input.num, "tbs": input.tbs}
    )
    headers = {"X-API-KEY": settings.SERPER_API_KEY, "Content-Type": "application/json"}
    try:
        log.debug(f"Starting Serper search for query: {input.query}")
        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        data = json.loads(res.read())
        organic = [OrganicItem(**item) for item in data.get("organic", [])]
        log.info(f"Serper search returned {len(organic)} results.")
        return SereprSearchOutput(organic=organic)
    except Exception as e:
        log.error(f"Error during Serper search: {e}")
        return SereprSearchOutput(organic=[])

async def tavily_search(input: TavilyQuery) -> TavilyQueryOutput:
    tavily_client = TavilyClient(api_key=settings.TAVLIY_API_KEY)
    try:
        log.debug(f"Starting Tavily search with query: {input.query}")
        response = await tavily_client.search(
            query=input.query,
            topic=input.topic,
            time_range=input.time_range,
            max_results=input.max_results,
        )
        items = [
            TavilyItem(
                title=entry["title"], url=entry["url"], content=entry["content"]
            )
            for entry in response.get("results", [])
        ]
        log.info(f"Tavily search returned {len(items)} results.")
        return TavilyQueryOutput(results=items)
    except Exception as e:
        log.error(f"Error during Tavily search: {e}")
        return TavilyQueryOutput(results=[])

class GitHubInspector:
    def __init__(self, token: str = settings.GITHUB_ACCESS_TOKEN):
        self.g = Github(token)

    async def get_user_by_name(self, input: GitHubUserQuery) -> GitHubUserOutput:
        try:
            log.debug(f"Fetching GitHub user with username: {input.username}")
            user = await self.g.get_user(input.username)
            log.info(f"GitHub user found: {user.login}")
            return GitHubUserOutput(
                login=user.login,
                name=user.name,
                public_repos=user.public_repos,
                followers=user.followers,
                bio=user.bio,
                location=user.location,
            )
        except Exception as e:
            log.error(f"Error fetching GitHub user {input.username}: {e}")
            return GitHubUserOutput(
                login="", name="", public_repos=0, followers=0, bio="", location=""
            )

    async def get_repo_by_name(self, input: GitHubRepoQuery) -> GitHubRepoOutput:
        try:
            log.debug(f"Fetching GitHub repo with name: {input.full_name}")
            repo = await self.g.get_repo(input.full_name)
            log.info(f"GitHub repo found: {repo.name}")
            return GitHubRepoOutput(
                name=repo.name,
                full_name=repo.full_name,
                description=repo.description,
                stars=repo.stargazers_count,
                forks=repo.forks_count,
                language=repo.language,
                topics=repo.get_topics(),
            )
        except Exception as e:
            log.error(f"Error fetching GitHub repo {input.full_name}: {e}")
            return GitHubRepoOutput(
                name="",
                full_name="",
                description="",
                stars=0,
                forks=0,
                language="",
                topics=[],
            )

    async def get_org_by_name(self, input: GitHubOrgQuery) -> GitHubOrgOutput:
        try:
            log.debug(f"Fetching GitHub organization with name: {input.org_name}")
            org = await self.g.get_organization(input.org_name)
            members = [member.login for member in org.get_members()][
                : input.member_limit
            ]
            log.info(f"GitHub org found: {org.name}, members: {len(members)}")
            return GitHubOrgOutput(
                login=org.login,
                name=org.name,
                description=org.description,
                public_repos=org.public_repos,
                members=members,
            )
        except Exception as e:
            log.error(f"Error fetching GitHub org {input.org_name}: {e}")
            return GitHubOrgOutput(
                login="", name="", description="", public_repos=0, members=[]
            )

    async def search_repos_by_language(self, input: GitHubLanguageQuery) -> GitHubLanguageOutput:
        try:
            log.debug(f"Searching GitHub repos by language: {input.language}")
            result = await self.g.search_repositories(
                query=f"language:{input.language}"
            )
            repos = [
                GitHubLanguageItem(
                    name=repo.name,
                    full_name=repo.full_name,
                    stars=repo.stargazers_count,
                    url=repo.html_url,
                )
                for repo in result[: input.limit]
            ]
            log.info(f"Found {len(repos)} repos matching language {input.language}")
            return GitHubLanguageOutput(results=repos)
        except Exception as e:
            log.error(f"Error searching GitHub repos by language {input.language}: {e}")
            return GitHubLanguageOutput(results=[])


async def arxiv_search(input: ArxivQuery) -> ArxivOutput:
    wrapper = ArxivAPIWrapper(
        top_k_results=input.top_k_results,
        ARXIV_MAX_QUERY_LENGTH=input.max_query_length,
        load_max_docs=input.load_max_docs,
        load_all_available_meta=input.load_all_available_meta,
        doc_content_chars_max=input.doc_content_chars_max,
    )
    try:
        log.debug(f"Starting Arxiv search for query: {input.query}")
        docs = await wrapper.run(input.query)
        parsed = parse_arxiv_text(raw_text=docs)
        log.info(f"Arxiv search returned {len(parsed)} results.")
        return ArxivSearchOutput(results=parsed)
    except Exception as e:
        log.error(f"Error during Arxiv search: {e}")
        return ArxivSearchOutput(results=[])
