from typing import Annotated, List, TypedDict, Literal, Optional
from pydantic import BaseModel, Field
from uuid import uuid4
from utilities.states.research_state import QueryState,OutputState

class Section(BaseModel):
    section_id: str = Field(description="The ID of the section", default_factory=lambda: str(uuid4()))
    name: str = Field(description="The title of the section within the report.")
    description: str = Field(description="A concise overview of the topics and concepts covered in this section.")
    research: bool = Field(description="Indicates whether web research is required for this section of the report.")
    content: str = Field(description="The main content or body of the section." )

class DetailedSection(BaseModel):
    name:str= Field(description="The name of the section")
    description:str= Field(description="A concise overview of the topics and concepts covered in this section")
    content:str= Field(description="The main content or body of the section.")
    
class Sections(BaseModel):
    sections: List[Section] = Field(
        description="A collection of sections that make up the report."
    )

class Header(BaseModel):
    title: Optional[str] = Field(default=None, description="The title of the report.")
    summary: Optional[str] = Field(default=None,description="A brief summary or abstract of the report's content and findings.",)

class Footer(BaseModel):
    conclusion: str = Field(description="The concluding section of the report, summarizing key takeaways and final thoughts.")


class Reference(BaseModel):
    section_name: str = Field(description="The name of the section where the referenced information was sourced from.")
    section_id: str = Field(description="A unique identifier for the section within the report.")
    source_url: List[str] = Field(description="A list of URLs or sources where additional information can be found related to this reference.")


class ReportState(BaseModel):
    query: Optional[str] = Field(default=None, description="Query of the user")
    type_of_query: Optional[
        Literal[
            "factual_query",
            "comparative_evaluative_query",
            "research_oriented_query",
            "execution_programming_query",
            "idea_generation",
        ]
    ] = Field(default=None, description="Type of the query")
    header: Optional[Header] = Field(
        default=None, description="The header of the report"
    )
    sections: Optional[Sections] = Field(
        default=None, description="All sections of the report"
    )
    footer: Optional[Footer] = Field(
        default=None, description="The footer of the report"
    )
    user_feedback: Optional[str] = Field(
        default=None, description="User feedback on the report structure"
    )
    report_framework: Optional[bool] = Field(
        default=None,
        description="A flag indicating whether the report framework is structured well.",
    )


class WriterState(BaseModel):
    query:str= Field(description="The query by the user")
    type_of_query: Literal[
        "factual_query",
        "comparative_evaluative_query",
        "research_oriented_query",
        "execution_programming_query",
        "idea_generation",
    ] = Field(
        description="The type of the query being asked, which determines the specific set of tools"
    )
    outputs: Optional[List[OutputState]] = Field(
        default=None, description="Output of the tools"
    )
    header: Optional[Header] = Field(
        default=None, description="The header of the report"
    )
    sections: Optional[Sections] = Field(
        default=None, description="All sections of the report"
    )
    footer: Optional[Footer] = Field(
        default=None, description="The footer of the report"
    )
    references: Optional[List[Reference]] = Field(default=None, description="List of reference")