from typing import Dict, Optional, Tuple
from langgraph.graph import StateGraph
from app.core.config import set_api_keys

class GraphFactory:
    """Factory for creating graph instances with specific API keys"""
    
    def create_graphs(
        self,
        api_keys: Dict[str, str],
        langfuse_config: Optional[Dict[str, str]] = None
    ) -> Tuple[StateGraph, StateGraph, StateGraph]:
        """Create graph instances with API keys"""
        # Set environment variables
        set_api_keys(api_keys)
        
        # Import here to avoid circular imports and ensure fresh imports
        import sys
        import importlib
        
        # Force reload of config module to pick up new env vars
        if 'src.config' in sys.modules:
            del sys.modules['src.config']
        if 'config' in sys.modules:
            del sys.modules['config']
        
        # Import graph creation functions
        from backend.src.graph.factory import create_section_graph, create_research_graph, create_writer_graph
        
        # Create langfuse callback if config provided
        langfuse_callback = None
        if langfuse_config:
            from langfuse.langchain import CallbackHandler
            langfuse_callback = CallbackHandler(
                public_key=langfuse_config.get("public_key"),
                secret_key=langfuse_config.get("secret_key"),
                host=langfuse_config.get("host", "https://cloud.langfuse.com")
            )
        
        # Create graphs
        section_graph = create_section_graph(langfuse_callback)
        research_graph = create_research_graph(langfuse_callback)
        writer_graph = create_writer_graph(langfuse_callback)
        
        return section_graph, research_graph, writer_graph

