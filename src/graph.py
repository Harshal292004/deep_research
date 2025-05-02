# section writer first but with the same grah but with differnet agents
from nodes import (
    router_node,
    header_writer_node,
    section_writer_node,
    footer_writer_node,
    reference_writer_node,
    verify_report_node,
    query_generation_node,
    tool_output_node
)
from edges import verify_conditional_edge
from observability.langfuse_setup import langfuse_handler
from utilities.states.report_state import ReportState
from utilities.states.research_state import ResearchState
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
import asyncio
from langgraph.checkpoint.memory import MemorySaver

section_builder = StateGraph(ReportState)
# register nodes
section_builder.add_node("router_node", router_node)
section_builder.add_node("header_writer_node", header_writer_node)
section_builder.add_node("section_writer_node", section_writer_node)
section_builder.add_node("footer_writer_node", footer_writer_node)
section_builder.add_node("reference_writer_node", reference_writer_node)
section_builder.add_node("verify_report_node", verify_report_node)
# edges
section_builder.add_edge(START, "router_node")
section_builder.add_edge("router_node", "header_writer_node")
section_builder.add_edge("header_writer_node", "section_writer_node")
section_builder.add_edge("section_writer_node", "footer_writer_node")
section_builder.add_edge("footer_writer_node", "reference_writer_node")
section_builder.add_edge("reference_writer_node", "verify_report_node")
section_builder.add_conditional_edges("verify_report_node", verify_conditional_edge)

memory = MemorySaver()
graph = section_builder.compile(checkpointer=memory)


# section writer first but with the same grah but with differnet agents
from nodes import (
    router_node,
    header_writer_node,
    section_writer_node,
    footer_writer_node,
    reference_writer_node,
    verify_report_node,
)
from edges import verify_conditional_edge
from observability.langfuse_setup import langfuse_handler
from utilities.states.report_state import ReportState
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
import asyncio
from langgraph.checkpoint.memory import MemorySaver


# Section Builder

section_builder = StateGraph(ReportState)
# register nodes
section_builder.add_node("router_node", router_node)
section_builder.add_node("header_writer_node", header_writer_node)
section_builder.add_node("section_writer_node", section_writer_node)
section_builder.add_node("footer_writer_node", footer_writer_node)
section_builder.add_node("reference_writer_node", reference_writer_node)
section_builder.add_node("verify_report_node", verify_report_node)
# edges
section_builder.add_edge(START, "router_node")
section_builder.add_edge("router_node", "header_writer_node")
section_builder.add_edge("header_writer_node", "section_writer_node")
section_builder.add_edge("section_writer_node", "footer_writer_node")
section_builder.add_edge("footer_writer_node", "reference_writer_node")
section_builder.add_edge("reference_writer_node", "verify_report_node")
section_builder.add_conditional_edges("verify_report_node", verify_conditional_edge)

memory = MemorySaver()
section_graph = section_builder.compile(checkpointer=memory)



# Research Agent

research_builder= StateGraph(ResearchState)

research_builder.add_node("query_generation_node",query_generation_node)
research_builder.add_node("tool_output_node",tool_output_node)

research_builder.add_edge(START,"query_generation_node")
research_builder.add_edge("query_generation_node","tool_output_node")
research_builder.add_edge("tool_output_node",END)

research_graph= research_builder.compile(checkpointer=memory)

async def main():
    final_report_state = None
    final_research_state=None
    
    async for state in section_graph.astream(
        {
            "query": "What is the current status of the american tariffs?",
            "user_feedback": " ",
        },
        config={
            "callbacks": [langfuse_handler],
            "configurable": {"thread_id": "abc123"},
        },
    ):
        final_report_state = state 
    print("Final Output:", final_report_state)
    
    async for state in research_graph.astream(
        {
            "query":final_report_state.query,
            "type_query":final_report_state.type_of_query,
            "sections":final_report_state.sections.sections
        },
        config={
            "callbacks":[langfuse_handler],
            "configurable":{"thread_id":"abc123"}
        }
    ):
        final_research_state= state
    
    print("Final research output:",final_research_state)
        

asyncio.run(main())
