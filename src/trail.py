from utilities.states.tool_state import TavilyQuery,DuckDuckGoQuery, ExaQuery
from components.tools import tavily_search,duckduckgo_search, exa_search
import asyncio


async def main():
    duckduckgo_query=DuckDuckGoQuery(query='current American tariffs', max_results=3)
    d_output=await  duckduckgo_search(input=duckduckgo_query)
    print(f"DuckDuck output : {type(d_output)} | Content: {d_output} ")
    
asyncio.run(main())