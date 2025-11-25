"""Graph factory for creating research pipeline graphs"""

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.models.state import ReportState, ResearchState, WriterState
from src.nodes import research, router, structure, writer


def create_section_graph() -> CompiledStateGraph:
    """Create section graph"""
    section_builder = StateGraph(ReportState)
    # Nodes
    section_builder.add_node("router_node", router.router_node)
    section_builder.add_node("header_writer_node", structure.header_writer_node)
    section_builder.add_node("section_writer_node", structure.section_writer_node)
    section_builder.add_node("footer_writer_node", structure.footer_writer_node)
    # Edges
    section_builder.add_edge(START, "router_node")
    section_builder.add_edge("router_node", "header_writer_node")
    section_builder.add_edge("header_writer_node", "section_writer_node")
    section_builder.add_edge("section_writer_node", "footer_writer_node")
    return section_builder.compile()


def create_research_graph() -> CompiledStateGraph:
    """Create research graph"""
    research_builder = StateGraph(ResearchState)
    # Nodes
    research_builder.add_node("query_generation_node", research.query_generation_node)
    research_builder.add_node("tool_output_node", research.tool_output_node)
    # Edges
    research_builder.add_edge(START, "query_generation_node")
    research_builder.add_edge("query_generation_node", "tool_output_node")
    research_builder.add_edge("tool_output_node", END)
    return research_builder.compile()


def create_writer_graph() -> CompiledStateGraph:
    """Create writer graph"""
    writer_builder = StateGraph(WriterState)
    # Nodes
    writer_builder.add_node(
        "detailed_section_writer_node", writer.detailed_section_writer_node
    )
    writer_builder.add_node(
        "detailed_header_writer_node", writer.detailed_header_writer_node
    )
    writer_builder.add_node(
        "detailed_footer_writer_node", writer.detailed_footer_writer_node
    )
    writer_builder.add_node("report_formatter_node", writer.report_formatter_node)
    # Edges
    writer_builder.add_edge(START, "detailed_section_writer_node")
    writer_builder.add_edge(
        "detailed_section_writer_node", "detailed_header_writer_node"
    )
    writer_builder.add_edge(
        "detailed_header_writer_node", "detailed_footer_writer_node"
    )
    writer_builder.add_edge("detailed_footer_writer_node", "report_formatter_node")
    writer_builder.add_edge("report_formatter_node", END)
    return writer_builder.compile()
