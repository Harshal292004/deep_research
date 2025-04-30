from pydantic import BaseModel, Field
from typing import List, Literal


class AppState(BaseModel):
    query: str = Field(description="The query given by the user")
    type_of_query: Literal[
        "factual_query",
        "comparative_evaluative_query",
        "research_oriented_query",
        "execution_programming_query",
        "idea_generation",
    ] = Field(
        description="The type of the query being asked, which determines the specific set of tools"
    )
