from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from pydantic import BaseModel, Field
from typing import List, Literal, Union
from utilities.states import (
    DuckDuckGoOutput,
    LocationOutput,
    SereprSearchOutput,
    OrganicItem,
)
from exa_py import Exa, api
from utilities.config import settings
import requests
import http.client
import json
from firecrawl import FirecrawlApp, ScrapeOptions


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


def fire_crawl_web_page():
    app = FirecrawlApp(api_key=settings.FIRE_CRAWL_API_KEY)

    # scrape a website:
    response= app.scrape_url(url, formats=["markdown"])
    result= response["data"]["markdown"]
    

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
        description="Results will only include links with a published date after this date.",
    )
    end_published_date: str = Field(
        ...,
        description="Results will only include links with a published date before this date.",
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


class FireCrawlWebScraper(BaseModel):
    pass
