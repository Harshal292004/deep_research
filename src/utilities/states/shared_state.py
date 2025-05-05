from pydantic import BaseModel, Field
from uuid import uuid4


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
