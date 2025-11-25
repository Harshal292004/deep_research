"""Search tool implementations"""
import json
import aiohttp
import http.client
from typing import List
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.utilities.arxiv import ArxivAPIWrapper
from src.models.tools import (
    DuckDuckGoQuery, ExaQuery, SerperQuery, ArxivQuery, TavilyQuery,
    DuckDuckGoOutput, ExaOutput, SerperQueryOutput, TavilyQueryOutput, ArxivOutput,
    SearchResult, LocationOutput, TavilyItem
)
from exa_py import Exa
from src.config import settings
from tavily import AsyncTavilyClient
from src.helpers.parsers import parse_arxiv_text
from src.helpers.logger import log

async def duckduckgo_search(input: DuckDuckGoQuery) -> List[DuckDuckGoOutput]:
    wrapper = DuckDuckGoSearchAPIWrapper(max_results=input.max_results)
    search = DuckDuckGoSearchResults(
        output_format="list", api_wrapper=wrapper
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
        {
            "q": input.query,
            "gl": country,
            "num": input.num_results,
            "tbs": input.tbs,
        }
    )
    headers = {"X-API-KEY": settings.SERPER_API_KEY, "Content-Type": "application/json"}
    try:
        log.info(f"Serper search: {input.query}")
        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        data = json.loads(res.read())
        organic_items = [
            SearchResult(
                title=item.get("title", ""),
                link=item.get("link", ""),
                snippet=item.get("snippet", ""),
            )
            for item in data.get("organic", [])
        ]
        log.info(f"Serper search completed: {len(organic_items)} results")
        return SerperQueryOutput(organic_results=organic_items)
    except Exception as e:
        log.error(f"Serper search failed: {e}")
        return SerperQueryOutput(organic_results=[])

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

async def arxiv_search(input: ArxivQuery) -> ArxivOutput:
    wrapper = ArxivAPIWrapper(
        top_k_results=input.top_k_results,
        ARXIV_MAX_QUERY_LENGTH=input.max_query_length,
        load_max_docs=input.load_max_docs,
        load_all_available_meta=input.load_all_available_meta,
        doc_content_chars_max=input.doc_content_chars_max,
        arxiv_exceptions=None,
        arxiv_search=None
    )
    try:
        log.info(f"Arxiv search: {input.query}")
        docs = wrapper.run(input.query)
        parsed = parse_arxiv_text(raw_text=docs)
        log.info(f"Arxiv search completed: {len(parsed.results) if isinstance(parsed.results, list) else 0} results")
        return parsed
    except Exception as e:
        log.error(f"Arxiv search failed: {e}")
        return ArxivOutput(results=[])
