from pydantic import BaseModel,Field

class DuckDuckGoOutput(BaseModel):
    snippet:str=Field(description="The snippet extracted from the whole page")
    title:str=Field(description="The title of the search")
    link:str= Field(description="The refrence")
    

class LocationOutput(BaseModel):
    country:str = Field(description="The country the results are to searched in")
