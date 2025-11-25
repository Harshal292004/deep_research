"""API client for backend communication"""
import httpx
import os
from typing import Dict, Optional, AsyncGenerator
import json

class ResearchAPIClient:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("BACKEND_URL", "http://localhost:8000")
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=300.0)
    
    async def start_research(
        self,
        query: str,
        api_keys: Dict[str, str],
        langfuse_config: Optional[Dict[str, str]] = None,
        session_id: Optional[str] = None,
        user_feedback: str = " "
    ) -> Dict:
        """Start a research task"""
        response = await self.client.post(
            "/api/v1/research/start",
            json={
                "query": query,
                "api_keys": api_keys,
                "langfuse_config": langfuse_config or {},
                "session_id": session_id,
                "user_feedback": user_feedback
            }
        )
        response.raise_for_status()
        return response.json()
    
    async def get_research_status(self, task_id: str) -> Dict:
        """Get research task status"""
        response = await self.client.get(f"/api/v1/research/{task_id}/status")
        response.raise_for_status()
        return response.json()
    
    async def stream_research_updates(self, task_id: str) -> AsyncGenerator[Dict, None]:
        """Stream research updates via SSE"""
        async with self.client.stream("GET", f"/api/v1/research/{task_id}/stream") as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    yield json.loads(line[6:])
    
    async def create_session(self) -> Dict:
        """Create a new session"""
        response = await self.client.post("/api/v1/sessions")
        response.raise_for_status()
        return response.json()
    
    async def get_chat_history(self, session_id: str, chat_id: str) -> Dict:
        """Get chat history"""
        response = await self.client.get(
            f"/api/v1/sessions/{session_id}/chats/{chat_id}"
        )
        response.raise_for_status()
        return response.json()
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

