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

builder = StateGraph(ReportState)
# register nodes
builder.add_node("router_node", router_node)
builder.add_node("header_writer_node", header_writer_node)
builder.add_node("section_writer_node", section_writer_node)
builder.add_node("footer_writer_node", footer_writer_node)
builder.add_node("reference_writer_node", reference_writer_node)
builder.add_node("verify_report_node", verify_report_node)
# edges
builder.add_edge(START, "router_node")
builder.add_edge("router_node", "header_writer_node")
builder.add_edge("header_writer_node", "section_writer_node")
builder.add_edge("section_writer_node", "footer_writer_node")
builder.add_edge("footer_writer_node", "reference_writer_node")
builder.add_edge("reference_writer_node", "verify_report_node")
builder.add_conditional_edges("verify_report_node", verify_conditional_edge)

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)


async def main():
    async for s in graph.astream(
        {
            "query": "What is the current status of the american tariffs?",
            "user_feedback": " ",
        },
        config={
            "callbacks": [langfuse_handler],
            "configurable": {"thread_id": "abc123"},
        },
    ):
        print(s)


asyncio.run(main())
