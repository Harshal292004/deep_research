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
from utilities.states.tool_state import (
    DuckDuckGoQuery,
    ExaQuery,
    SerperQuery,
    GitHubRepoQuery,
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
    TavilyItem,
)
from exa_py import Exa, api
from config import settings
from tavily import AsyncTavilyClient
from github import Github
from utilities.helpers.parsers import parse_arxiv_text
from utilities.helpers.logger import log


async def duckduckgo_search(input: DuckDuckGoQuery) -> List[DuckDuckGoOutput]:
    wrapper = DuckDuckGoSearchAPIWrapper(max_results=input.max_results)
    search = DuckDuckGoSearchResults(
        output_format="list", api_wrapper=wrapper, source="news"
    )
    try:
        log.info(f"DuckDuckGo search: {input.query}")
        results = await search.ainvoke(input.query)
        log.info(f"DuckDuckGo search completed: {len(results)} results")

        items = [
            DuckDuckGoOutput(
                title=result["title"], link=result["link"], snippet=result["snippet"]
            )
            for result in results
        ]

        return items
    except Exception as e:
        log.error(f"DuckDuckGo search failed: {e}")
        return []


def exa_search(input: ExaQuery) -> List[ExaOutput]:
    exa = Exa(api_key=settings.EXA_API_KEY)
    exa_output = []
    try:
        log.info(f"Exa search: {input.query}")
        results = exa.search_and_contents(
            query=input.query,
            num_results=input.num_results,
            start_published_date=input.start_published_date,
            end_published_date=input.end_published_date,
            category=input.category,
            text=False,
            highlights=True,
        )

        for result in results.results:
            exa_output.append(ExaOutput(highlights=result.highlights, url=result.url))
        log.info(f"Exa search completed: {len(exa_output)} results")
        return exa_output
    except Exception as e:
        log.error(f"Exa search failed: {e}")
        return []


async def get_location() -> LocationOutput:
    try:
        log.info("Fetching location")
        async with aiohttp.ClientSession() as session:
            async with session.get("https://ipinfo.io/json") as response:
                result = await response.json()
                country = str(result.get("country", ""))
                location_result = LocationOutput(country=country.lower())
                log.info(f"Location found: {country.lower()}")
                return location_result
    except Exception as e:
        log.error(f"Location fetch failed: {e}")
        return LocationOutput(country="")


async def serper_search(input: SerperQuery) -> SerperQueryOutput:
    conn = http.client.HTTPSConnection("google.serper.dev")
    country = await get_location()
    country = country.country
    payload = json.dumps(
        {"q": input.query, "gl": country, "num": input.num, "tbs": input.tbs}
    )
    headers = {"X-API-KEY": settings.SERPER_API_KEY, "Content-Type": "application/json"}
    try:
        log.info(f"Serper search: {input.query}")
        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        data = json.loads(res.read())
        organic = [OrganicItem(**item) for item in data.get("organic", [])]
        log.info(f"Serper search completed: {len(organic)} results")
        return SereprSearchOutput(organic=organic)
    except Exception as e:
        log.error(f"Serper search failed: {e}")
        return SereprSearchOutput(organic=[])


async def tavily_search(input: TavilyQuery) -> TavilyQueryOutput:
    tavily_client = AsyncTavilyClient(api_key=settings.TAVLIY_API_KEY)
    try:
        log.info(f"Tavily search: {input.query}")
        response = await tavily_client.search(
            query=input.query,
            topic=input.topic,
            time_range=input.time_range,
            max_results=input.max_results,
        )
        items = [
            TavilyItem(title=entry["title"], url=entry["url"], content=entry["content"])
            for entry in response.get("results", [])
        ]
        log.info(f"Tavily search completed: {len(items)} results")
        return TavilyQueryOutput(results=items)
    except Exception as e:
        log.error(f"Tavily search failed: {e}")
        return TavilyQueryOutput(results=[])


class GitHubInspector:
    def __init__(self, token: str = settings.GITHUB_ACCESS_TOKEN):
        self.g = Github(token)

    async def get_user_by_name(self, input: GitHubUserQuery) -> GitHubUserOutput:
        try:
            log.info(f"GitHub user lookup: {input.username}")
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
            log.error(f"GitHub user lookup failed: {e}")
            return GitHubUserOutput(
                login="", name="", public_repos=0, followers=0, bio="", location=""
            )

    async def get_repo_by_name(self, input: GitHubRepoQuery) -> GitHubRepoOutput:
        try:
            log.info(f"GitHub repo lookup: {input.full_name}")
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
            log.error(f"GitHub repo lookup failed: {e}")
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
            log.info(f"GitHub org lookup: {input.org_name}")
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
            log.error(f"GitHub org lookup failed: {e}")
            return GitHubOrgOutput(
                login="", name="", description="", public_repos=0, members=[]
            )

    async def search_repos_by_language(
        self, input: GitHubLanguageQuery
    ) -> GitHubLanguageOutput:
        try:
            log.info(f"GitHub language search: {input.language}")
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
            log.info(f"GitHub language search completed: {len(repos)} repos")
            return GitHubLanguageOutput(results=repos)
        except Exception as e:
            log.error(f"GitHub language search failed: {e}")
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
        log.info(f"Arxiv search: {input.query}")
        docs = await wrapper.run(input.query)
        parsed = parse_arxiv_text(raw_text=docs)
        log.info(f"Arxiv search completed: {len(parsed)} results")
        return ArxivSearchOutput(results=parsed)
    except Exception as e:
        log.error(f"Arxiv search failed: {e}")
        return ArxivSearchOutput(results=[])
