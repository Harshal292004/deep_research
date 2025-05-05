# section writer first but with the same grah but with differnet agents
from nodes import (
  router_node,
  header_writer_node,
  section_writer_node,
  footer_writer_node,
  verify_report_node,
  query_generation_node,
  tool_output_node,
  detailed_footer_writer_node,
  detailed_header_writer_node,
  detailed_section_writer_node,
  report_formatter_node
)
from typing import Optional
from edges import verify_conditional_edge
from observability.langfuse_setup import langfuse_handler
from utilities.states.report_state import ReportState,WriterState
from utilities.states.research_state import ResearchState
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
import asyncio
from utilities.helpers.logger import log
section_builder = StateGraph(ReportState)
# register nodes
section_builder.add_node("router_node", router_node)
section_builder.add_node("header_writer_node", header_writer_node)
section_builder.add_node("section_writer_node", section_writer_node)
section_builder.add_node("footer_writer_node", footer_writer_node)
section_builder.add_node("verify_report_node", verify_report_node)
# edges
section_builder.add_edge(START, "router_node")
section_builder.add_edge("router_node", "header_writer_node")
section_builder.add_edge("header_writer_node", "section_writer_node")
section_builder.add_edge("section_writer_node", "footer_writer_node")
section_builder.add_edge("footer_writer_node", "verify_report_node")
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

# Writer Agent

writer_builder= StateGraph(WriterState)

writer_builder.add_node("detailed_section_writer_node",detailed_section_writer_node)
writer_builder.add_node("detailed_header_writer_node",detailed_header_writer_node)
writer_builder.add_node("detailed_footer_writer_node",detailed_footer_writer_node)
writer_builder.add_node("report_formatter_node",report_formatter_node)

writer_builder.add_edge(START,"detailed_section_writer_node")
writer_builder.add_edge("detailed_section_writer_node","detailed_header_writer_node")
writer_builder.add_edge("detailed_header_writer_node","detailed_footer_writer_node")
writer_builder.add_edge("detailed_footer_writer_node","report_formatter_node")
writer_builder.add_edge("report_formatter_node",END)


writer_graph= writer_builder.compile(checkpointer=memory)

async def main():
    report_state:Optional[ReportState] = None
    research_state:Optional[ResearchState] = None
    writer_state:Optional[WriterState] = None
    
    async for state in section_graph.astream(
        {
            "query": "What is the current status of the american tariffs?",
            "user_feedback": " ",
        },
        stream_mode=["values"],
        config={
            "callbacks": [langfuse_handler],
            "configurable": {"thread_id": "abc123"},
        },
    ):
        report_state = state 
        
    report_state= ReportState(**report_state[1])
    
    async for state in research_graph.astream(
        {
            "query":report_state.query,
            "type_query":report_state.type_of_query,
            "sections":report_state.sections.sections
        },
        stream_mode=["values"],
        config={
            "callbacks":[langfuse_handler],
            "configurable":{"thread_id":"abc123"}
        }
    ):
        research_state= state
    
    research_state=ResearchState(**research_state[1])
    
    log.debug(f"The research state queries are: {research_state.queries}")
    log.debug(f"\n\n\n\nThe research state outputs are: {research_state.outputs}")

    
    
    async for state in writer_graph.astream(
        {
            "query":report_state.query,
            "type_query":report_state.type_of_query,
            "sections":report_state.sections,
            "output_list": research_state.outputs,
            "header":report_state.header,
            "footer":report_state.footer,
        },
        config={
            "callbacks":[langfuse_handler],
            "configurable":{"thread_id":"abc123"}
        }
    ):
        writer_state= state
        print(writer_state)
    print("Final Writer State:",writer_state)
asyncio.run(main())
