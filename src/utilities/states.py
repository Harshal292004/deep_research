from pydantic import BaseModel, Field
from typing import List


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
    organic: List[OrganicItem]
