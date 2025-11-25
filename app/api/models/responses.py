from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class TaskResponse(BaseModel):
    task_id: str
    session_id: str
    status: str
    created_at: str


class ProgressInfo(BaseModel):
    current_stage: Optional[str] = None
    stage_progress: float = 0.0


class ResearchStatusResponse(BaseModel):
    task_id: str
    status: str
    progress: ProgressInfo
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class SessionResponse(BaseModel):
    session_id: str
    created_at: str


class MessageResponse(BaseModel):
    role: str
    content: str
    type: Optional[str] = None
    timestamp: str
    error: Optional[str] = None


class ChatResponse(BaseModel):
    chat_id: str
    messages: List[MessageResponse]
