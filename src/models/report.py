"""Report structure models"""

from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class Section(BaseModel):
    section_id: str = Field(
        description="The ID of the section", default_factory=lambda: str(uuid4())
    )
    name: str = Field(description="The title of the section within the report.")
    description: str = Field(
        description="A concise overview of the topics and concepts covered in this section."
    )
    research: bool = Field(
        description="Indicates whether web research is required for this section of the report."
    )
    content: str = Field(description="The main content or body of the section.")


class DetailedSection(BaseModel):
    name: str = Field(description="The name of the section")
    description: str = Field(
        description="A concise overview of the topics and concepts covered in this section"
    )
    content: str = Field(description="The main content or body of the section.")


class Sections(BaseModel):
    sections: List[Section] = Field(
        description="A collection of sections that make up the report."
    )


class Header(BaseModel):
    title: Optional[str] = Field(default=None, description="The title of the report.")
    summary: Optional[str] = Field(
        default=None,
        description="A brief summary or abstract of the report's content and findings.",
    )


class Footer(BaseModel):
    conclusion: str = Field(
        description="The concluding section of the report, summarizing key takeaways and final thoughts."
    )


class Reference(BaseModel):
    section_name: Optional[str] = Field(
        default=None,
        description="The name of the section where the referenced information was sourced from.",
    )
    section_id: Optional[str] = Field(
        default=None,
        description="A unique identifier for the section within the report.",
    )
    source_url: List[str] = Field(
        default=[],
        description="A list of URLs or sources where additional information can be found related to this reference.",
    )
