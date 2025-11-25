from uuid import uuid4
from datetime import datetime
from typing import Dict

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}
    
    def create_session(self) -> str:
        """Create a new session"""
        session_id = str(uuid4())
        self.sessions[session_id] = {
            "session_id": session_id,
            "created_at": datetime.now().isoformat(),
            "chats": []
        }
        return session_id
    
    def get_session(self, session_id: str) -> Dict:
        """Get session by ID"""
        return self.sessions[session_id]
    def add_chat(self, session_id: str, chat_id: str):
        """Add a chat to a session"""
        if session_id in self.sessions:
            if chat_id not in self.sessions[session_id]["chats"]:
                self.sessions[session_id]["chats"].append(chat_id)

