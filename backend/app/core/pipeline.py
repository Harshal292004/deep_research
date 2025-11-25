import asyncio
from typing import Dict, Any, Optional, AsyncGenerator
from uuid import uuid4
from datetime import datetime
from app.core.graph_factory import GraphFactory

class ResearchPipeline:
    def __init__(self):
        self.graph_factory = GraphFactory()
        self.active_tasks: Dict[str, Dict[str, Any]] = {}
    
    async def start(
        self,
        query: str,
        user_feedback: str,
        session_id: str,
        api_keys: Dict[str, str],
        langfuse_config: Optional[Dict[str, str]] = None
    ) -> str:
        """Start a research task"""
        task_id = str(uuid4())
        
        # Store task info
        self.active_tasks[task_id] = {
            "status": "pending",
            "query": query,
            "session_id": session_id,
            "api_keys": api_keys,
            "langfuse_config": langfuse_config,
            "user_feedback": user_feedback,
            "current_stage": None,
            "stage_progress": 0.0,
            "result": None,
            "error": None
        }
        
        # Start background task
        asyncio.create_task(self._execute_pipeline(task_id))
        
        return task_id
    
    async def _execute_pipeline(self, task_id: str):
        """Execute the research pipeline"""
        try:
            task = self.active_tasks[task_id]
            task["status"] = "processing"
            task["current_stage"] = "section"
            task["stage_progress"] = 0.0
            
            # Create graphs with API keys
            section_graph, research_graph, writer_graph = self.graph_factory.create_graphs(
                api_keys=task["api_keys"],
                langfuse_config=task.get("langfuse_config")
            )
            
            # Execute section graph
            config_dict = {
                "configurable": {"thread_id": task["session_id"]},
            }
            if task.get("langfuse_config"):
                from langfuse.langchain import CallbackHandler
                langfuse_callback = CallbackHandler(
                    public_key=task["langfuse_config"].get("public_key"),
                    secret_key=task["langfuse_config"].get("secret_key"),
                    host=task["langfuse_config"].get("host", "https://cloud.langfuse.com")
                )
                config_dict["callbacks"] = [langfuse_callback]
            
            report_state = None
            async for state in section_graph.astream(
                {
                    "query": task["query"],
                    "user_feedback": task["user_feedback"],
                },
                stream_mode=["values"],
                config=config_dict,
            ):
                report_state = state
                task["stage_progress"] = 0.33
            
            if not report_state:
                raise Exception("Failed to generate report structure")
            
            # Import here to avoid circular imports
            from backend.src.models.state import ReportState, ResearchState
            report_state = ReportState(**report_state[1])
            
            task["current_stage"] = "research"
            task["stage_progress"] = 0.33
            
            # Execute research graph
            research_state = None
            async for state in research_graph.astream(
                {
                    "query": report_state.query,
                    "type_of_query": report_state.type_of_query,
                    "sections": report_state.sections.sections if report_state.sections else [],
                },
                stream_mode=["values"],
                config=config_dict,
            ):
                research_state = state
                task["stage_progress"] = 0.66
            
            if not research_state:
                raise Exception("Failed to complete research phase")
            
            research_state = ResearchState(**research_state[1])
            
            task["current_stage"] = "writer"
            task["stage_progress"] = 0.66
            
            # Execute writer graph
            writer_state = None
            async for state in writer_graph.astream(
                {
                    "query": report_state.query,
                    "type_of_query": report_state.type_of_query,
                    "sections": report_state.sections,
                    "outputs": research_state.outputs,
                    "header": report_state.header,
                    "footer": report_state.footer,
                },
                config=config_dict,
            ):
                writer_state = state
                task["stage_progress"] = 0.99
            
            if not writer_state:
                raise Exception("Failed to generate final report")
            
            # Extract markdown from writer state
            markdown = getattr(writer_state, 'markdown', None)
            if markdown:
                task["status"] = "completed"
                task["result"] = {"markdown": markdown}
                task["stage_progress"] = 1.0
            else:
                raise Exception("Report generated but markdown not found")
            
        except Exception as e:
            self.active_tasks[task_id]["status"] = "failed"
            self.active_tasks[task_id]["error"] = str(e)
    
    async def get_status(self, task_id: str) -> Dict[str, Any]:
        """Get task status"""
        task = self.active_tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        return {
            "task_id": task_id,
            "status": task["status"],
            "progress": {
                "current_stage": task.get("current_stage"),
                "stage_progress": task.get("stage_progress", 0.0)
            },
            "result": task.get("result"),
            "error": task.get("error")
        }
    
    async def stream_updates(self, task_id: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream task updates"""
        task = self.active_tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        # Poll for updates
        last_status = None
        while task["status"] in ["pending", "processing"]:
            current_status = task["status"]
            if current_status != last_status:
                yield {
                    "stage": task.get("current_stage", "pending"),
                    "progress": task.get("stage_progress", 0.0),
                    "status": current_status,
                    "message": f"Processing {task.get('current_stage', 'pending')} stage..."
                }
                last_status = current_status
            await asyncio.sleep(1)
        
        # Final update
        if task["status"] == "completed":
            yield {
                "stage": "completed",
                "progress": 1.0,
                "status": "completed",
                "result": task.get("result")
            }
        elif task["status"] == "failed":
            yield {
                "stage": "failed",
                "progress": task.get("stage_progress", 0.0),
                "status": "failed",
                "error": task.get("error")
            }
    
    async def cancel_task(self, task_id: str):
        """Cancel a running task"""
        task = self.active_tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        if task["status"] == "processing":
            task["status"] = "cancelled"
        else:
            raise ValueError(f"Task {task_id} cannot be cancelled (status: {task['status']})")

