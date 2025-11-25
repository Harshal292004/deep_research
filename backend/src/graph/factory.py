"""Graph factory for creating research pipeline graphs"""
from typing import Optional, Tuple
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from backend.src.models.state import ReportState, ResearchState, WriterState
from backend.src.nodes import router, structure, verification, research, writer
from backend.src.edges import verify_conditional_edge

def create_section_graph(langfuse_callback=None) -> StateGraph:
    """Create section graph"""
    section_builder = StateGraph(ReportState)
    # Register nodes
    section_builder.add_node("router_node", router.router_node)
    section_builder.add_node("header_writer_node", structure.header_writer_node)
    section_builder.add_node("section_writer_node", structure.section_writer_node)
    section_builder.add_node("footer_writer_node", structure.footer_writer_node)
    section_builder.add_node("verify_report_node", verification.verify_report_node)
    # Edges
    section_builder.add_edge(START, "router_node")
    section_builder.add_edge("router_node", "header_writer_node")
    section_builder.add_edge("header_writer_node", "section_writer_node")
    section_builder.add_edge("section_writer_node", "footer_writer_node")
    section_builder.add_edge("footer_writer_node", "verify_report_node")
    section_builder.add_conditional_edges("verify_report_node", verify_conditional_edge)
    
    memory = MemorySaver()
    return section_builder.compile(checkpointer=memory)

def create_research_graph(langfuse_callback=None) -> StateGraph:
    """Create research graph"""
    research_builder = StateGraph(ResearchState)
    research_builder.add_node("query_generation_node", research.query_generation_node)
    research_builder.add_node("tool_output_node", research.tool_output_node)
    research_builder.add_edge(START, "query_generation_node")
    research_builder.add_edge("query_generation_node", "tool_output_node")
    research_builder.add_edge("tool_output_node", END)
    
    memory = MemorySaver()
    return research_builder.compile(checkpointer=memory)

def create_writer_graph(langfuse_callback=None) -> StateGraph:
    """Create writer graph"""
    writer_builder = StateGraph(WriterState)
    writer_builder.add_node("detailed_section_writer_node", writer.detailed_section_writer_node)
    writer_builder.add_node("detailed_header_writer_node", writer.detailed_header_writer_node)
    writer_builder.add_node("detailed_footer_writer_node", writer.detailed_footer_writer_node)
    writer_builder.add_node("report_formatter_node", writer.report_formatter_node)
    writer_builder.add_edge(START, "detailed_section_writer_node")
    writer_builder.add_edge("detailed_section_writer_node", "detailed_header_writer_node")
    writer_builder.add_edge("detailed_header_writer_node", "detailed_footer_writer_node")
    writer_builder.add_edge("detailed_footer_writer_node", "report_formatter_node")
    writer_builder.add_edge("report_formatter_node", END)
    
    memory = MemorySaver()
    return writer_builder.compile(checkpointer=memory)

