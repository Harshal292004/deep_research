from typing import Annotated, List, TypedDict, Literal, Optional
from pydantic import BaseModel, Field

class Section(BaseModel):
    name: str = Field(
        description="The title of the section within the report."
    )
    description: str = Field(
        description="A concise overview of the topics and concepts covered in this section."
    )
    research: bool = Field(
        description="Indicates whether web research is required for this section of the report."
    )
    content: str = Field(
        description="The main content or body of the section."
    )

class Sections(BaseModel):
    sections: List[Section] = Field(
        description="A collection of sections that make up the report."
    )

class Header(BaseModel):
    title: str = Field(
        description="The title of the report."
    )
    summary: str = Field(
        description="A brief summary or abstract of the report's content and findings."
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

class ReportState(BaseModel):
    type_of_query: Literal[
        "factual_query",
        "comparative_evaluative_query",
        "research_oriented_query",
        "execution_programming_query",
        "idea_generation",
    ] 
    header: Header
    sections: Sections
    footer: Footer
    report_framework_good: bool = Field(
        description="A flag indicating whether the report framework is structured well."
    )
    references: Optional[List[Reference]] = Field(
        description="A list of references used in the report, linking back to the relevant sections from where the data was sourced."
    )
