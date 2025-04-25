from pydantic import BaseModel, Field
from typing import List, Literal


class RouterResponse(BaseModel):
    type_of_query: Literal[
        "factual_query",
        "comparative_evaluative_query",
        "research_oriented_query",
        "execution_programming_query",
        "idea_generation",
    ] = Field(
        description=" The type of tje qiery being asked on which you get a specific set of tools"
    )


class AppState(BaseModel):
    query:str= Field(description="the query given by the user")
    type_of_query: Literal[
        "factual_query",
        "comparative_evaluative_query",
        "research_oriented_query",
        "execution_programming_query",
        "idea_generation",
    ] = Field(
        description=" The type of tje qiery being asked on which you get a specific set of tools"
    )
