from typing import Dict, Optional

from pydantic import BaseModel


class StartResearchRequest(BaseModel):
    query: str
    api_keys: Dict[str, str]
    langfuse_config: Optional[Dict[str, str]] = None
    session_id: Optional[str] = None


class CreateSessionRequest(BaseModel):
    pass


class ValidateConfigRequest(BaseModel):
    api_keys: Dict[str, str]
