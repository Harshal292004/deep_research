from typing import Annotated, List, TypedDict, Literal, Optional
from pydantic import BaseModel, Field
from uuid import uuid4


class RouterResponse(BaseModel):
    type_of_query: Literal[
        "factual_query",
        "comparative_evaluative_query",
        "research_oriented_query",
        "execution_programming_query",
        "idea_generation",
    ] = Field(
        description="The type of the query being asked, which determines the specific set of tools"
    )


class Section(BaseModel):
    section_id: str = Field(description="The ID of the section", default=str(uuid4()))
    name: str = Field(description="The title of the section within the report.")
    description: str = Field(
        description="A concise overview of the topics and concepts covered in this section."
    )
    research: bool = Field(
        description="Indicates whether web research is required for this section of the report."
    )
    content: str = Field(description="The main content or body of the section.")


class Sections(BaseModel):
    sections: List[Section] = Field(
        description="A collection of sections that make up the report."
    )


class Header(BaseModel):
    title: str = Field(description="The title of the report.")
    summary: str = Field(
        description="A brief summary or abstract of the report's content and findings."
    )


class VerifyReport(BaseModel):
    verified: bool = Field(
        description="Whether or not the report structure is well-designed"
    )


class Footer(BaseModel):
    conclusion: str = Field(
        description="The concluding section of the report, summarizing key takeaways and final thoughts."
    )


class Reference(BaseModel):
    section_name: str = Field(
        description="The name of the section where the referenced information was sourced from."
    )
    section_id: int = Field(
        description="A unique identifier for the section within the report."
    )
    source_url: List[str] = Field(
        description="A list of URLs or sources where additional information can be found related to this reference."
    )


class References(BaseModel):
    references: Optional[List[Reference]] = Field(
        description="A list of references used in the report, linking back to the relevant sections from where the data was sourced."
    )


class ReportState(BaseModel):
    query: str = Field(description="Query of the user")
    type_of_query: Literal[
        "factual_query",
        "comparative_evaluative_query",
        "research_oriented_query",
        "execution_programming_query",
        "idea_generation",
    ] = Field(description="Type of the query")
    header: Header = Field(description="The header of the report")
    sections: Sections = Field(description="All sections of the report")
    footer: Footer = Field(description="The footer of the report")
    user_feedback: str = Field(description="User feedback on the report structure")
    report_framework: bool = Field(description="A flag indicating whether the report framework is structured well.")
    references: References = Field(description="List of references")
