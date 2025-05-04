from utilities.states.tool_state import TavilyQuery,DuckDuckGoQuery, ExaQuery
from components.tools import tavily_search,duckduckgo_search, exa_search
import asyncio


async def main():
    tavily_query=TavilyQuery(query='American tariffs updates', topic='news', time_range='month',             
                             max_results=2) 


    duckduckgo_query=DuckDuckGoQuery(query='current American tariffs status', max_results=3)              

    exa_query=ExaQuery(query='recent changes American tariffs', num_results=2,                                             
                                start_published_date='2022-01-01', end_published_date='2024-12-31', category='news') 

    # t_output= await tavily_search(input=tavily_query)
    # d_output=await  duckduckgo_search(input=duckduckgo_query)
    e_output= exa_search(input=exa_query)


    # print("Tavily output :  ",t_output)
    # print("DuckDuck output :  ",d_output)
    print("Exa output : ",e_output)

asyncio.run(main())

final_output=[
    {
        'section_id':'f1db5681-0404-4b69-8201-67e06c2cb278',
        'output_state': <class 'utilities.states.research_state.FactualOutput'>
    },
    {
        'section_id': 'd9c1d715-a32b-4047-8a29-f78311769c9a',              
        'output_state': <class 'utilities.states.research_state.FactualOutput'>
    },
    {   
        'section_id': '30e030e1-076e-4b40-a2ec-c06db75b72c7', 
        'output_state': <class 'utilities.states.research_state.FactualOutput'>
    }
]  
