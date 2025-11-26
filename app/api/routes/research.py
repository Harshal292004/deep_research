import json
from datetime import datetime
from typing import Dict

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse

from app.api.models.requests import StartResearchRequest
from app.api.models.responses import ResearchStatusResponse, TaskResponse
from app.services.research_service import ResearchService

router = APIRouter()
research_service = ResearchService()


@router.post(
    "/start",
    response_model=TaskResponse,
    summary="Start a new research task",
    description=(
        "Kick off an asynchronous deep research run.\n\n"
        "The research pipeline executes multiple stages—typically search, analysis,\n"
        "synthesis, and report generation—using the supplied query and tool API keys.\n"
        "This endpoint **does not** block until the research is finished; instead it\n"
        "returns a `task_id` that you can poll or stream.\n\n"
        "Recommended usage pattern:\n"
        "1. Call this endpoint with your research query and required tool API keys.\n"
        "2. Store the returned `task_id` and `session_id` on the client side.\n"
        "3. Poll `/api/v1/research/{task_id}/status` or open\n"
        "   `/api/v1/research/{task_id}/stream` to monitor progress and retrieve\n"
        "   the final result.\n"
    ),
    response_description="Metadata about the newly created research task, including task and session identifiers.",
)
async def start_research(request: StartResearchRequest) -> TaskResponse:
    """
    Enqueue a new research task backed by the internal research pipeline.

    **Example request body**:

    ```json
    {
      "query": "State of the art techniques for retrieval-augmented generation (RAG) in 2025",
      "api_keys": {
        "EXA_API_KEY": "exa-xxxxx",
        "SERPER_API_KEY": "serper-xxxxx",
        "GROQ_API_KEY": "gsk_XXXX"
      },
      "langfuse_config": {
        "LANGFUSE_PUBLIC_KEY": "pk-xxxx",
        "LANGFUSE_SECRET_KEY": "sk-xxxx",
        "LANGFUSE_HOST": "https://cloud.langfuse.com"
      }
    }
    ```

    **Example successful response**:

    ```json
    {
      "task_id": "task_01J4N9C4P3Z9K8YQ8M2Z4X1V6G",
      "session_id": "9f2d7808-5f1b-4a3a-9e8e-7c6b12345678",
      "status": "pending",
      "created_at": "2025-11-26T14:32:10.123456"
    }
    ```
    """
    try:
        result = await research_service.start_research(
            query=request.query,
            api_keys=request.api_keys,
            langfuse_config=request.langfuse_config,
            session_id=request.session_id,
        )
        return TaskResponse(
            task_id=result["task_id"],
            session_id=result["session_id"],
            status=result["status"],
            created_at=result.get("created_at", datetime.now().isoformat()),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{task_id}/status",
    response_model=ResearchStatusResponse,
    summary="Get research task status",
    description=(
        "Fetch the latest status snapshot for a research task.\n\n"
        "This is the easiest way to periodically poll for completion from a\n"
        "frontend or backend client. For real-time streaming updates, consider\n"
        "using the `/stream` endpoint instead.\n"
    ),
    response_description="Current status, progress information, and (when available) the research result.",
)
async def get_research_status(task_id: str) -> ResearchStatusResponse:
    """
    Retrieve a structured status object for the given `task_id`.

    **Example successful response (task running)**:

    ```json
    {
      "task_id": "task_01J4N9C4P3Z9K8YQ8M2Z4X1V6G",
      "status": "running",
      "progress": {
        "current_stage": "analysis",
        "stage_progress": 0.35
      },
      "result": null,
      "error": null
    }
    ```

    **Example successful response (task completed)**:

    ```json
    {
      "task_id": "task_01J4N9C4P3Z9K8YQ8M2Z4X1V6G",
      "status": "completed",
      "progress": {
        "current_stage": "writing",
        "stage_progress": 1.0
      },
      "result": {
        "summary": "High-level summary of the research findings...",
        "sections": [
          {
            "title": "Background",
            "content": "Detailed background discussion..."
          }
        ]
      },
      "error": null
    }
    ```
    """
    try:
        status = await research_service.get_status(task_id)
        return ResearchStatusResponse(**status)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{task_id}/stream",
    summary="Stream research updates (Server-Sent Events)",
    description=(
        "Open a Server-Sent Events (SSE) stream that emits incremental updates\n"
        "about the specified research task.\n\n"
        "Each event is sent as a JSON-encoded `data:` line. The stream stays\n"
        "open until the task completes, fails, or is cancelled.\n\n"
        "This is ideal for UIs that want low-latency status updates without\n"
        "manually polling the `/status` endpoint."
    ),
    response_class=StreamingResponse,
    response_description="An SSE stream of JSON-encoded progress updates and (eventually) final result data.",
)
async def stream_research_updates(task_id: str):
    """
    Stream live updates for a research task using Server-Sent Events (SSE).

    **Example CURL usage**:

    ```bash
    curl -N http://localhost:8000/api/v1/research/TASK_ID/stream
    ```

    **Example event payload** (sent as `data: <json>\\n\\n`):

    ```json
    {
      "task_id": "task_01J4N9C4P3Z9K8YQ8M2Z4X1V6G",
      "status": "running",
      "progress": {
        "current_stage": "search",
        "stage_progress": 0.5
      }
    }
    ```
    """

    async def generate():
        try:
            async for update in research_service.stream_updates(task_id):
                yield f"data: {json.dumps(update)}\n\n"
        except ValueError as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.post(
    "/{task_id}/cancel",
    summary="Cancel a running research task",
    description=(
        "Attempt to cancel a running research task.\n\n"
        "Cancellation is best-effort: the underlying pipeline will stop future\n"
        "work as soon as safely possible, but some in-flight tool calls or\n"
        "requests may still complete."
    ),
    response_description="Confirmation that the cancellation request was accepted.",
)
async def cancel_research(task_id: str) -> Dict:
    """
    Cancel a running task identified by `task_id`.

    **Example successful response**:

    ```json
    {
      "status": "cancelled",
      "task_id": "task_01J4N9C4P3Z9K8YQ8M2Z4X1V6G"
    }
    ```
    """
    try:
        await research_service.cancel_task(task_id)
        return {"status": "cancelled", "task_id": task_id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
