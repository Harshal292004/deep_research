from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import Dict
from uuid import uuid4
from datetime import datetime
import json
import asyncio

from app.api.models.requests import StartResearchRequest
from app.api.models.responses import TaskResponse, ResearchStatusResponse
from app.services.research_service import ResearchService

router = APIRouter()
research_service = ResearchService()

@router.post("/start", response_model=TaskResponse)
async def start_research(request: StartResearchRequest) -> TaskResponse:
    """Start a new research task"""
    try:
        result = await research_service.start_research(
            query=request.query,
            api_keys=request.api_keys,
            langfuse_config=request.langfuse_config,
            session_id=request.session_id,
            user_feedback=request.user_feedback
        )
        return TaskResponse(
            task_id=result["task_id"],
            session_id=result["session_id"],
            status=result["status"],
            created_at=result.get("created_at", datetime.now().isoformat())
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{task_id}/status", response_model=ResearchStatusResponse)
async def get_research_status(task_id: str) -> ResearchStatusResponse:
    """Get research task status"""
    try:
        status = await research_service.get_status(task_id)
        return ResearchStatusResponse(**status)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{task_id}/stream")
async def stream_research_updates(task_id: str):
    """Stream research updates via Server-Sent Events"""
    async def generate():
        try:
            async for update in research_service.stream_updates(task_id):
                yield f"data: {json.dumps(update)}\n\n"
        except ValueError as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@router.post("/{task_id}/cancel")
async def cancel_research(task_id: str) -> Dict:
    """Cancel a running research task"""
    try:
        await research_service.cancel_task(task_id)
        return {"status": "cancelled", "task_id": task_id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

