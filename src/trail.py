import asyncio
from components.prompts import Prompts
from components.chains import get_header_chain
from utilities.states.report_state import Header,Sections
from utilities.helpers.LLMProvider import LLMProvider
async def get_output():    
    prompt= Prompts.get_section_writer_prompt().invoke({
        "query": "What is the current status of the american tariffs?",
        "type_of_query": "factual_query",
        "title":"Current Status of American Tariffs.",
        "summary":"""
            This report provides an overview of the current American tariffs, including definitions,
            key characteristics, and essential details.
            The summary structure will cover: 
            1. Definition of Tariffs, 
            2. Recent Developments and Updates, 
            3. Impact on International Trade, and
            4. Future Outlook and Potential Changes.
            """
    })
    llm = LLMProvider.structuredtextclient(schema=Sections)
    output= await llm.ainvoke(prompt)
    print(output)
    return output

if __name__ == "__main__":
    asyncio.run(get_output())
