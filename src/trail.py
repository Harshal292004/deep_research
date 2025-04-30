import asyncio
from components.prompts import Prompts
from components.chains import get_header_chain
from utilities.states.report_state import Header, Sections, References, Section
from utilities.helpers.LLMProvider import LLMProvider


async def get_output():
    sections = [
        Section(
            section_id="57c9e273-fae8-4707-be91-8afa8e9bf6a1",
            name="Definition & Core Concept",
            description="Explanation of tariffs, their types, and impact on trade",
            research=True,
            content="Overview of tariffs, including their definition, history, and effects on international trade",
        ),
        Section(
            section_id="57c9e273-fae8-4707-be91-8afa8e8bf6a1",
            name="Scientific Basis",
            description="Underlying principles of tariffs, including economic and political considerations",
            research=True,
            content="Analysis of the economic and political factors influencing tariff policies, including protectionism and free trade",
        ),
        Section(
            section_id="57c9e273-fae8-4707-be91-8afa8e2bf6a1",
            name="Real-World Applications",
            description="Current American tariffs and their applications in various industries",
            research=True,
            content=" Examination of the current American tariffs, their applications, and effects on different industries, including manufacturing, agriculture, and services",
        ),
        Section(
            section_id="57c9e273-fae8-4707-be91-8afa8e1bf6a1",
            name="Misconceptions & Clarifications",
            description="Addressing common misconceptions about tariffs and their implications",
            research=False,
            content="Discussion of common misconceptions about tariffs, their benefits, and drawbacks, and clarification of their role in international trade",
        ),
    ]
    section_string = ""
    for sec in sections:
        section_string += (
            f"\nsection_id: {sec.section_id} "
            f"name: {sec.name} "
            f"description: {sec.description} "
            f"research: {sec.research} "
            f"content: {sec.content}"
        )

    prompt = Prompts.get_references_writer_prompt().invoke(
        {
            "sections": section_string,
        }
    )
    llm = LLMProvider.structuredtextclient(schema=References)
    output = await llm.ainvoke(prompt)
    print(output)
    return output


if __name__ == "__main__":
    asyncio.run(get_output())
