from datetime import datetime
from typing import Dict, List
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.api.models.requests import CreateSessionRequest
from app.api.models.responses import ChatResponse, MessageResponse, SessionResponse

router = APIRouter()
sessions: Dict[str, Dict] = {}
chats: Dict[str, Dict] = {}


@router.post("", response_model=SessionResponse)
async def create_session() -> SessionResponse:
    """Create a new session"""
    session_id = str(uuid4())
    sessions[session_id] = {
        "session_id": session_id,
        "created_at": datetime.now().isoformat(),
        "chats": [],
    }
    return SessionResponse(
        session_id=session_id, created_at=sessions[session_id]["created_at"]
    )


@router.get("/{session_id}", response_model=Dict)
async def get_session(session_id: str) -> Dict:
    """Get session details"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]


@router.get("/{session_id}/chats/{chat_id}", response_model=ChatResponse)
async def get_chat_history(session_id: str, chat_id: str) -> ChatResponse:
    """Get chat history"""
    if chat_id not in chats:
        raise HTTPException(status_code=404, detail="Chat not found")
    chat = chats[chat_id]
    return ChatResponse(chat_id=chat_id, messages=chat.get("messages", []))


@router.delete("/{session_id}/chats/{chat_id}")
async def delete_chat(chat_id: str) -> Dict:
    """Delete a chat"""
    if chat_id not in chats:
        raise HTTPException(status_code=404, detail="Chat not found")
    del chats[chat_id]
    return {"status": "deleted"}
