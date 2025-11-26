from datetime import datetime
from typing import Dict, List
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.api.models.requests import CreateSessionRequest
from app.api.models.responses import ChatResponse, MessageResponse, SessionResponse

router = APIRouter()
sessions: Dict[str, Dict] = {}
chats: Dict[str, Dict] = {}


@router.post(
    "",
    response_model=SessionResponse,
    summary="Create a new session",
    description=(
        "Create a new logical session container.\n\n"
        "Sessions are lightweight server-side objects that you can use to group\n"
        "multiple research tasks and chats together for a given user or UI tab."
    ),
    response_description="The newly created session identifier and metadata.",
)
async def create_session() -> SessionResponse:
    """
    Create a new session for grouping research runs and chats.

    **Example successful response**:

    ```json
    {
      \"session_id\": \"9f2d7808-5f1b-4a3a-9e8e-7c6b12345678\",
      \"created_at\": \"2025-11-26T13:01:45.000000\"
    }
    ```
    """
    session_id = str(uuid4())
    sessions[session_id] = {
        "session_id": session_id,
        "created_at": datetime.now().isoformat(),
        "chats": [],
    }
    return SessionResponse(
        session_id=session_id, created_at=sessions[session_id]["created_at"]
    )


@router.get(
    "/{session_id}",
    response_model=Dict,
    summary="Get session details",
    description=(
        "Fetch the raw server-side representation of a session.\n\n"
        "The payload currently includes minimal metadata and a list of associated\n"
        "chat identifiers."
    ),
    response_description="Full JSON representation of the session, including chat IDs.",
)
async def get_session(session_id: str) -> Dict:
    """
    Retrieve metadata and associated chats for a particular session.

    **Example successful response**:

    ```json
    {
      \"session_id\": \"9f2d7808-5f1b-4a3a-9e8e-7c6b12345678\",
      \"created_at\": \"2025-11-26T13:01:45.000000\",
      \"chats\": [
        \"chat_01J4N9C4P3Z9K8YQ8M2Z4X1V6G\"
      ]
    }
    ```
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]


@router.get(
    "/{session_id}/chats/{chat_id}",
    response_model=ChatResponse,
    summary="Get chat history",
    description=(
        "Fetch the message history for a particular chat within a session.\n\n"
        "This is typically used by frontends to restore conversation context\n"
        "when a user revisits a session or chat."
    ),
    response_description="Chat identifier and ordered list of messages.",
)
async def get_chat_history(session_id: str, chat_id: str) -> ChatResponse:
    """
    Retrieve the messages belonging to a particular chat.

    **Example successful response**:

    ```json
    {
      \"chat_id\": \"chat_01J4N9C4P3Z9K8YQ8M2Z4X1V6G\",
      \"messages\": [
        {
          \"role\": \"user\",
          \"content\": \"Summarize the latest research on RAG.\",
          \"type\": \"message\",
          \"timestamp\": \"2025-11-26T13:02:01.123456\",
          \"error\": null
        }
      ]
    }
    ```
    """
    if chat_id not in chats:
        raise HTTPException(status_code=404, detail="Chat not found")
    chat = chats[chat_id]
    return ChatResponse(chat_id=chat_id, messages=chat.get("messages", []))


@router.delete(
    "/{session_id}/chats/{chat_id}",
    summary="Delete a chat",
    description=(
        "Delete a stored chat thread from a session.\n\n"
        "This operation is irreversible and removes all associated messages."
    ),
    response_description="Confirmation that the chat has been deleted.",
)
async def delete_chat(chat_id: str) -> Dict:
    """
    Permanently delete the chat identified by `chat_id`.

    **Example successful response**:

    ```json
    {
      \"status\": \"deleted\"
    }
    ```
    """
    if chat_id not in chats:
        raise HTTPException(status_code=404, detail="Chat not found")
    del chats[chat_id]
    return {"status": "deleted"}
