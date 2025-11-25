from datetime import datetime
from typing import Any, AsyncGenerator, Dict, Optional

from app.core.pipeline import ResearchPipeline
from app.core.session_manager import SessionManager


class ResearchService:
    def __init__(self):
        self.pipeline = ResearchPipeline()
        self.session_manager = SessionManager()

    async def start_research(
        self,
        query: str,
        api_keys: Dict[str, str],
        langfuse_config: Optional[Dict[str, str]] = None,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Start a research task"""
        # Create or get session
        if not session_id:
            session_id = self.session_manager.create_session()

        # Create pipeline instance with API keys
        task_id = await self.pipeline.start(
            query=query,
            session_id=session_id,
            api_keys=api_keys,
            langfuse_config=langfuse_config,
        )

        return {
            "task_id": task_id,
            "session_id": session_id,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
        }

    async def get_status(self, task_id: str) -> Dict[str, Any]:
        """Get research task status"""
        return await self.pipeline.get_status(task_id)

    async def stream_updates(
        self, task_id: str
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream updates via Server-Sent Events"""
        async for update in self.pipeline.stream_updates(task_id):
            yield update

    async def cancel_task(self, task_id: str):
        """Cancel a running task"""
        await self.pipeline.cancel_task(task_id)
