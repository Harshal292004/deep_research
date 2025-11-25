from pydantic import BaseModel
from typing import Dict, Optional

class StartResearchRequest(BaseModel):
    query: str
    user_feedback: str = " "
    api_keys: Dict[str, str]
    langfuse_config: Optional[Dict[str, str]] = None
    session_id: Optional[str] = None

class CreateSessionRequest(BaseModel):
    pass  # No fields needed, session is auto-created

class ValidateConfigRequest(BaseModel):
    api_keys: Dict[str, str]

