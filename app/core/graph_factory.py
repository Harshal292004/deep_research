from typing import Dict, Tuple

from langgraph.graph.state import CompiledStateGraph

from app.core.config import set_api_keys


class GraphFactory:
    """Factory for creating graph instances with specific API keys"""

    def create_graphs(
        self, api_keys: Dict[str, str]
    ) -> Tuple[CompiledStateGraph, CompiledStateGraph, CompiledStateGraph]:
        """Create graph instances with API keys"""
        # Set environment variables
        set_api_keys(api_keys)

        # Import here to avoid circular imports and ensure fresh imports
        import sys

        # Force reload of config module to pick up new env vars
        if "src.config" in sys.modules:
            del sys.modules["src.config"]
        if "config" in sys.modules:
            del sys.modules["config"]

        # Import graph creation functions
        from src.graph.factory import (
            create_research_graph,
            create_section_graph,
            create_writer_graph,
        )

        # Create graphs
        section_graph = create_section_graph()
        research_graph = create_research_graph()
        writer_graph = create_writer_graph()

        return section_graph, research_graph, writer_graph
