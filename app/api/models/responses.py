from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TaskResponse(BaseModel):
    """Metadata returned after a research task has been enqueued."""

    task_id: str = Field(
        ...,
        description=(
            "Opaque identifier of the research task.\n\n"
            "Use this ID with `/api/v1/research/{task_id}/status` or\n"
            "`/api/v1/research/{task_id}/stream` to track progress and fetch results."
        ),
        examples=["task_01J4N9C4P3Z9K8YQ8M2Z4X1V6G"],
    )
    session_id: str = Field(
        ...,
        description=(
            "ID of the session associated with this research run.\n\n"
            "If you provided a `session_id` in the request it will be echoed here,\n"
            "otherwise it will be a newly created session ID."
        ),
        examples=["9f2d7808-5f1b-4a3a-9e8e-7c6b12345678"],
    )
    status: str = Field(
        ...,
        description="Initial task status immediately after enqueueing (typically `pending`).",
        examples=["pending"],
    )
    created_at: str = Field(
        ...,
        description="ISO-8601 timestamp indicating when the task was created.",
        examples=["2025-11-26T14:32:10.123456"],
    )


class ProgressInfo(BaseModel):
    """Fine-grained progress information for a running research task."""

    current_stage: Optional[str] = Field(
        default=None,
        description=(
            "Human-readable name of the current pipeline stage.\n\n"
            "Common values include `search`, `analysis`, `synthesis`, `writing`, etc."
        ),
        examples=["analysis"],
    )
    stage_progress: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description=(
            "Fractional progress (0.0–1.0) of the current stage.\n\n"
            "This is scoped to the current stage, not the entire pipeline."
        ),
        examples=[0.35],
    )


class ResearchStatusResponse(BaseModel):
    """Current status snapshot for a research task."""

    task_id: str = Field(
        ...,
        description="Identifier of the research task being inspected.",
        examples=["task_01J4N9C4P3Z9K8YQ8M2Z4X1V6G"],
    )
    status: str = Field(
        ...,
        description=(
            "High-level state of the task.\n\n"
            "Typical values include `pending`, `running`, `completed`, `failed`, or `cancelled`."
        ),
        examples=["running"],
    )
    progress: ProgressInfo = Field(
        ...,
        description="Fine-grained progress information about the current stage of the pipeline.",
    )
    result: Optional[Dict[str, Any]] = Field(
        default=None,
        description=(
            "Structured research output produced by the pipeline, if available.\n\n"
            "The exact schema depends on the orchestration logic, but commonly includes:\n"
            "- a synthesized written report,\n"
            "- key findings and citations, and\n"
            "- any supporting structured data."
        ),
        examples=[
            {
                "summary": "High-level summary of the research findings...",
                "sections": [
                    {
                        "title": "Background",
                        "content": "Detailed background discussion...",
                    }
                ],
            }
        ],
    )
    error: Optional[str] = Field(
        default=None,
        description="Populated when the task has failed or hit an unrecoverable error.",
        examples=["Upstream search API returned 500"],
    )


class SessionResponse(BaseModel):
    """Minimal representation of a created session."""

    session_id: str = Field(
        ...,
        description="Unique identifier for the session.",
        examples=["9f2d7808-5f1b-4a3a-9e8e-7c6b12345678"],
    )
    created_at: str = Field(
        ...,
        description="ISO-8601 timestamp indicating when the session was created.",
        examples=["2025-11-26T13:01:45.000000"],
    )


class MessageResponse(BaseModel):
    """
    Representation of a single message in a chat transcript associated with a session.
    """

    role: str = Field(
        ...,
        description="Logical actor that produced the message (e.g. `user`, `assistant`, `system`).",
        examples=["assistant"],
    )
    content: str = Field(
        ...,
        description="Raw text content of the message.",
        examples=["Here is a structured report summarizing the current state of RAG..."],
    )
    type: Optional[str] = Field(
        default=None,
        description=(
            "Optional message type or channel classification.\n\n"
            "This can be used to distinguish between regular messages, tool calls,\n"
            "streamed deltas, system notices, etc."
        ),
        examples=["message"],
    )
    timestamp: str = Field(
        ...,
        description="ISO-8601 timestamp when the message was emitted.",
        examples=["2025-11-26T13:02:01.123456"],
    )
    error: Optional[str] = Field(
        default=None,
        description="If present, describes an error related to this message (e.g. tool failure).",
        examples=["Search provider rate limited this request"],
    )


class ChatResponse(BaseModel):
    """Container for a single chat and its associated messages."""

    chat_id: str = Field(
        ...,
        description="Identifier of the chat thread within a session.",
        examples=["chat_01J4N9C4P3Z9K8YQ8M2Z4X1V6G"],
    )
    messages: List[MessageResponse] = Field(
        ...,
        description="Chronologically ordered list of messages in this chat.",
    )
