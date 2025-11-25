"""Router node"""
from backend.src.models.state import ReportState
from backend.src.chains.builders import get_router_chain
from backend.src.helpers.logger import log

async def router_node(state: ReportState):
    try:
        log.debug("Starting router_node...")
        query = state.query
        chain = get_router_chain()
        response = await chain.ainvoke({"query": query})
        return {"type_of_query": response.content}
    except Exception as e:
        log.error(f"Error in router_node: {e}")
        return {"type_of_query": "factual_query"}

