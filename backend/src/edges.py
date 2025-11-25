"""Edge definitions for graph conditional routing"""
from backend.src.models.state import ReportState
from langgraph.graph import END

def verify_conditional_edge(state: ReportState):
    return END if state.report_framework else "header_writer_node"

