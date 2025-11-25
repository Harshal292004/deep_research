# Backend Separation Refactoring Plan

## Overview

This plan outlines the refactoring to separate the business logic (`src/` folder) into a standalone backend API, while keeping the Streamlit app as a thin frontend client.

## Architecture Goals

1. **Backend API** (FastAPI) - Contains all business logic, graph execution, tool orchestration
2. **Frontend** (Streamlit) - Simple UI that makes HTTP requests to the backend
3. **Clear separation** - No business logic in frontend, no UI logic in backend

---

## Current Architecture Problems

### Issues with Current Setup:
1. **Tight Coupling**: Streamlit app directly imports and executes business logic
2. **State Management**: API keys stored in Streamlit session state, passed to backend
3. **Module Reloading**: Complex dynamic module reloading in `app.py` (lines 104-182)
4. **No API Layer**: Cannot be used by other clients (mobile, web, CLI)
5. **Testing Difficulty**: Hard to test business logic without Streamlit
6. **Deployment Complexity**: Frontend and backend must be deployed together

---

## Proposed Architecture

```
┌─────────────────┐         HTTP/REST         ┌──────────────────┐
│  Streamlit App  │ ────────────────────────> │   Backend API    │
│   (Frontend)    │ <──────────────────────── │   (FastAPI)      │
│                 │      WebSocket/SSE         │                  │
└─────────────────┘                           └──────────────────┘
                                                       │
                                                       │
                                              ┌────────┴────────┐
                                              │                 │
                                         ┌────▼────┐      ┌────▼────┐
                                         │  LLMs   │      │  Tools  │
                                         │  APIs   │      │  APIs   │
                                         └─────────┘      └─────────┘
```

---

## Phase 1: Backend API Structure

### 1.1 Create Backend Directory Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Settings (moved from src/config.py)
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── research.py     # Research pipeline endpoints
│   │   │   ├── sessions.py      # Session/chat management
│   │   │   └── health.py        # Health check endpoint
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── requests.py      # Request models (Pydantic)
│   │   │   └── responses.py     # Response models (Pydantic)
│   │   │
│   │   └── dependencies.py      # FastAPI dependencies (auth, etc.)
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── pipeline.py          # Main research pipeline orchestrator
│   │   ├── session_manager.py   # Session/thread management
│   │   └── graph_factory.py     # Graph creation and initialization
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── research_service.py  # Research pipeline service
│   │   ├── config_service.py    # API key management service
│   │   └── langfuse_service.py  # Langfuse integration
│   │
│   └── models/                  # Business logic models (from src/)
│       ├── __init__.py
│       ├── state.py             # State models
│       ├── tools.py             # Tool models
│       └── report.py             # Report models
│
├── src/                         # Move existing src/ here (or refactor)
│   ├── nodes/
│   ├── tools/
│   ├── chains/
│   ├── prompts/
│   └── ...
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### 1.2 API Endpoints Design

#### Research Pipeline Endpoints

```python
# POST /api/v1/research/start
# Start a new research task
Request:
{
    "query": "string",
    "user_feedback": "string (optional)",
    "api_keys": {
        "EXA_API_KEY": "string",
        "SERPER_API_KEY": "string",
        ...
    },
    "langfuse_config": {
        "public_key": "string (optional)",
        "secret_key": "string (optional)",
        "host": "string (optional)"
    }
}

Response:
{
    "task_id": "uuid",
    "session_id": "uuid",
    "status": "pending",
    "created_at": "iso_datetime"
}

# GET /api/v1/research/{task_id}/status
# Get research task status
Response:
{
    "task_id": "uuid",
    "status": "pending|processing|completed|failed",
    "progress": {
        "current_stage": "section|research|writer",
        "stage_progress": 0.0-1.0
    },
    "result": {
        "markdown": "string (if completed)",
        "error": "string (if failed)"
    }
}

# GET /api/v1/research/{task_id}/stream
# Server-Sent Events stream for real-time updates
# Streams: stage updates, progress, intermediate results

# POST /api/v1/research/{task_id}/cancel
# Cancel a running research task
```

#### Session Management Endpoints

```python
# POST /api/v1/sessions
# Create a new session
Response:
{
    "session_id": "uuid",
    "created_at": "iso_datetime"
}

# GET /api/v1/sessions/{session_id}
# Get session details
Response:
{
    "session_id": "uuid",
    "chats": [
        {
            "chat_id": "uuid",
            "title": "string",
            "created_at": "iso_datetime",
            "last_message_at": "iso_datetime"
        }
    ]
}

# GET /api/v1/sessions/{session_id}/chats/{chat_id}
# Get chat history
Response:
{
    "chat_id": "uuid",
    "messages": [
        {
            "role": "user|assistant",
            "content": "string",
            "type": "text|markdown",
            "timestamp": "iso_datetime",
            "error": "string (optional)"
        }
    ]
}

# DELETE /api/v1/sessions/{session_id}/chats/{chat_id}
# Delete a chat
```

#### Health & Config Endpoints

```python
# GET /api/v1/health
# Health check
Response:
{
    "status": "healthy|degraded|unhealthy",
    "version": "string",
    "services": {
        "llm": "ok|error",
        "tools": "ok|error"
    }
}

# POST /api/v1/config/validate
# Validate API keys (without storing)
Request:
{
    "api_keys": {
        "EXA_API_KEY": "string",
        ...
    }
}
Response:
{
    "valid": true|false,
    "missing_keys": ["string"],
    "invalid_keys": ["string"]
}
```

---

## Phase 2: Backend Implementation

### 2.1 FastAPI Application Setup

**File: `backend/app/main.py`**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import research, sessions, health
from app.core.config import settings

app = FastAPI(
    title="Deep Research API",
    version="1.0.0",
    description="Backend API for automated research pipeline"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(research.router, prefix="/api/v1/research", tags=["research"])
app.include_router(sessions.router, prefix="/api/v1/sessions", tags=["sessions"])
app.include_router(health.router, prefix="/api/v1", tags=["health"])
```

### 2.2 Research Pipeline Service

**File: `backend/app/services/research_service.py`**

```python
from typing import Optional, Dict, Any
from app.core.pipeline import ResearchPipeline
from app.core.session_manager import SessionManager
from app.models.state import ResearchPipelineState

class ResearchService:
    def __init__(self):
        self.pipeline = ResearchPipeline()
        self.session_manager = SessionManager()
    
    async def start_research(
        self,
        query: str,
        api_keys: Dict[str, str],
        langfuse_config: Optional[Dict[str, str]] = None,
        session_id: Optional[str] = None,
        user_feedback: str = " "
    ) -> Dict[str, Any]:
        """Start a research task"""
        # Create or get session
        if not session_id:
            session_id = self.session_manager.create_session()
        
        # Initialize pipeline with API keys
        pipeline_instance = self.pipeline.create_instance(
            api_keys=api_keys,
            langfuse_config=langfuse_config
        )
        
        # Start async task
        task_id = await pipeline_instance.start(
            query=query,
            user_feedback=user_feedback,
            session_id=session_id
        )
        
        return {
            "task_id": task_id,
            "session_id": session_id,
            "status": "pending"
        }
    
    async def get_status(self, task_id: str) -> Dict[str, Any]:
        """Get research task status"""
        return await self.pipeline.get_status(task_id)
    
    async def stream_updates(self, task_id: str):
        """Stream updates via Server-Sent Events"""
        async for update in self.pipeline.stream_updates(task_id):
            yield update
```

### 2.3 Pipeline Orchestrator

**File: `backend/app/core/pipeline.py`**

```python
import asyncio
from typing import Dict, Any, Optional, AsyncGenerator
from uuid import uuid4
from app.core.graph_factory import GraphFactory
from app.models.state import ResearchPipelineState

class ResearchPipeline:
    def __init__(self):
        self.graph_factory = GraphFactory()
        self.active_tasks: Dict[str, Dict[str, Any]] = {}
    
    def create_instance(
        self,
        api_keys: Dict[str, str],
        langfuse_config: Optional[Dict[str, str]] = None
    ) -> 'PipelineInstance':
        """Create a pipeline instance with specific API keys"""
        graphs = self.graph_factory.create_graphs(
            api_keys=api_keys,
            langfuse_config=langfuse_config
        )
        return PipelineInstance(graphs, self)
    
    async def start(
        self,
        query: str,
        user_feedback: str,
        session_id: str
    ) -> str:
        """Start a research task"""
        task_id = str(uuid4())
        
        # Store task info
        self.active_tasks[task_id] = {
            "status": "pending",
            "query": query,
            "session_id": session_id
        }
        
        # Start background task
        asyncio.create_task(self._execute_pipeline(task_id, query, user_feedback, session_id))
        
        return task_id
    
    async def _execute_pipeline(
        self,
        task_id: str,
        query: str,
        user_feedback: str,
        session_id: str
    ):
        """Execute the research pipeline"""
        try:
            self.active_tasks[task_id]["status"] = "processing"
            self.active_tasks[task_id]["current_stage"] = "section"
            
            # Get pipeline instance (should be stored per task)
            instance = self.active_tasks[task_id].get("instance")
            
            # Execute section graph
            report_state = await instance.execute_section_graph(query, user_feedback)
            self.active_tasks[task_id]["current_stage"] = "research"
            
            # Execute research graph
            research_state = await instance.execute_research_graph(report_state)
            self.active_tasks[task_id]["current_stage"] = "writer"
            
            # Execute writer graph
            writer_state = await instance.execute_writer_graph(report_state, research_state)
            
            # Store result
            self.active_tasks[task_id]["status"] = "completed"
            self.active_tasks[task_id]["result"] = {
                "markdown": writer_state.markdown
            }
            
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
            "current_stage": task.get("current_stage"),
            "result": task.get("result"),
            "error": task.get("error")
        }
    
    async def stream_updates(self, task_id: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream task updates"""
        # Implementation for SSE streaming
        pass
```

### 2.4 Graph Factory

**File: `backend/app/core/graph_factory.py`**

```python
from typing import Dict, Optional, Tuple
from langgraph.graph import StateGraph
from app.core.config import set_api_keys
from src.graph import create_section_graph, create_research_graph, create_writer_graph

class GraphFactory:
    """Factory for creating graph instances with specific API keys"""
    
    def create_graphs(
        self,
        api_keys: Dict[str, str],
        langfuse_config: Optional[Dict[str, str]] = None
    ) -> Tuple[StateGraph, StateGraph, StateGraph]:
        """Create graph instances with API keys"""
        # Set environment variables
        set_api_keys(api_keys)
        
        # Create langfuse callback if config provided
        langfuse_callback = None
        if langfuse_config:
            from langfuse.langchain import CallbackHandler
            langfuse_callback = CallbackHandler(
                public_key=langfuse_config.get("public_key"),
                secret_key=langfuse_config.get("secret_key"),
                host=langfuse_config.get("host", "https://cloud.langfuse.com")
            )
        
        # Create graphs (these should be stateless or use dependency injection)
        section_graph = create_section_graph(langfuse_callback)
        research_graph = create_research_graph(langfuse_callback)
        writer_graph = create_writer_graph(langfuse_callback)
        
        return section_graph, research_graph, writer_graph
```

---

## Phase 3: Refactor Existing Code

### 3.1 Move Business Logic

**Actions:**
1. Move `src/` folder to `backend/src/` (or refactor as per previous plan)
2. Update imports to use new structure
3. Remove Streamlit-specific code from business logic

### 3.2 Extract Graph Creation

**Current**: Graphs are created at module level in `src/graph.py`

**New**: Create factory functions that accept configuration

```python
# backend/src/graph/factory.py
def create_section_graph(langfuse_callback=None):
    """Create section graph with optional langfuse callback"""
    # Graph creation logic
    pass

def create_research_graph(langfuse_callback=None):
    """Create research graph with optional langfuse callback"""
    pass

def create_writer_graph(langfuse_callback=None):
    """Create writer graph with optional langfuse callback"""
    pass
```

### 3.3 Remove Streamlit Dependencies

**Changes needed:**
- Remove `verify_report_node` patching (lines 148-157 in app.py)
- Make verification configurable or remove user input requirement
- Remove dynamic module reloading (lines 104-182 in app.py)
- Use dependency injection for API keys instead of environment variables

---

## Phase 4: Frontend Refactoring

### 4.1 Streamlit App Structure

```
frontend/
├── app.py                    # Main Streamlit app (simplified)
├── services/
│   ├── __init__.py
│   └── api_client.py         # HTTP client for backend API
├── components/
│   ├── __init__.py
│   ├── chat_ui.py            # Chat UI components
│   ├── config_ui.py          # API key configuration UI
│   └── sidebar.py            # Sidebar components
└── utils/
    ├── __init__.py
    └── session.py            # Session state management
```

### 4.2 API Client

**File: `frontend/services/api_client.py`**

```python
import httpx
from typing import Dict, Optional, AsyncGenerator
import os

class ResearchAPIClient:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("BACKEND_URL", "http://localhost:8000")
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=300.0)
    
    async def start_research(
        self,
        query: str,
        api_keys: Dict[str, str],
        langfuse_config: Optional[Dict[str, str]] = None,
        session_id: Optional[str] = None,
        user_feedback: str = " "
    ) -> Dict:
        """Start a research task"""
        response = await self.client.post(
            "/api/v1/research/start",
            json={
                "query": query,
                "api_keys": api_keys,
                "langfuse_config": langfuse_config or {},
                "session_id": session_id,
                "user_feedback": user_feedback
            }
        )
        response.raise_for_status()
        return response.json()
    
    async def get_research_status(self, task_id: str) -> Dict:
        """Get research task status"""
        response = await self.client.get(f"/api/v1/research/{task_id}/status")
        response.raise_for_status()
        return response.json()
    
    async def stream_research_updates(self, task_id: str) -> AsyncGenerator[Dict, None]:
        """Stream research updates via SSE"""
        async with self.client.stream("GET", f"/api/v1/research/{task_id}/stream") as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    import json
                    yield json.loads(line[6:])
    
    async def create_session(self) -> Dict:
        """Create a new session"""
        response = await self.client.post("/api/v1/sessions")
        response.raise_for_status()
        return response.json()
    
    async def get_chat_history(self, session_id: str, chat_id: str) -> Dict:
        """Get chat history"""
        response = await self.client.get(
            f"/api/v1/sessions/{session_id}/chats/{chat_id}"
        )
        response.raise_for_status()
        return response.json()
```

### 4.3 Simplified Streamlit App

**File: `frontend/app.py`** (simplified version)

```python
import streamlit as st
from services.api_client import ResearchAPIClient
from components.chat_ui import render_chat
from components.config_ui import render_config_panel
from components.sidebar import render_sidebar
import asyncio

# Initialize API client
@st.cache_resource
def get_api_client():
    return ResearchAPIClient()

api_client = get_api_client()

# Page config
st.set_page_config(
    page_title="Open Deep Research",
    page_icon="🔭",
    layout="wide"
)

# Initialize session state
if 'session_id' not in st.session_state:
    response = asyncio.run(api_client.create_session())
    st.session_state.session_id = response['session_id']

if 'api_keys' not in st.session_state:
    st.session_state.api_keys = {
        'EXA_API_KEY': '',
        'SERPER_API_KEY': '',
        # ... other keys
    }

# Render UI
with st.sidebar:
    render_sidebar(api_client)

col_main, col_right = st.columns([2, 1])

with col_right:
    render_config_panel()

with col_main:
    render_chat(api_client)

# Footer
st.divider()
st.caption("Open Deep Research - Automated Research Pipeline")
```

---

## Phase 5: Configuration & Environment

### 5.1 Backend Configuration

**File: `backend/app/core/config.py`**

```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: List[str] = ["http://localhost:8501", "http://localhost:3000"]
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # Task Management
    MAX_CONCURRENT_TASKS: int = 10
    TASK_TIMEOUT: int = 3600  # 1 hour
    
    # Default API Keys (optional, can be overridden per request)
    EXA_API_KEY: str = ""
    SERPER_API_KEY: str = ""
    # ... other defaults
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### 5.2 Environment Variables

**Backend `.env`:**
```env
# Server
HOST=0.0.0.0
PORT=8000
DEBUG=false

# CORS
CORS_ORIGINS=http://localhost:8501,http://localhost:3000

# Optional: Default API keys (can be overridden per request)
EXA_API_KEY=
SERPER_API_KEY=
# ...
```

**Frontend `.env`:**
```env
BACKEND_URL=http://localhost:8000
```

---

## Phase 6: Deployment & Infrastructure

### 6.1 Docker Setup

**Backend Dockerfile:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DEBUG=false
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    ports:
      - "8501:8501"
    environment:
      - BACKEND_URL=http://backend:8000
    depends_on:
      - backend
```

### 6.2 Task Queue (Optional - for production)

For production, consider using a task queue:

```python
# Use Celery or similar for long-running tasks
from celery import Celery

celery_app = Celery('research_tasks')

@celery_app.task
def execute_research_pipeline(task_id: str, query: str, ...):
    # Execute pipeline
    pass
```

---

## Phase 7: Testing Strategy

### 7.1 Backend Tests

```
backend/
├── tests/
│   ├── __init__.py
│   ├── test_api/
│   │   ├── test_research.py
│   │   └── test_sessions.py
│   ├── test_services/
│   │   └── test_research_service.py
│   └── test_core/
│       └── test_pipeline.py
```

### 7.2 Integration Tests

- Test full pipeline execution
- Test API endpoints
- Test error handling
- Test concurrent requests

---

## Implementation Order

1. **Phase 1**: Create backend structure and API endpoints (skeleton)
2. **Phase 2**: Implement core pipeline service
3. **Phase 3**: Refactor existing code to work with backend
4. **Phase 4**: Create simplified Streamlit frontend
5. **Phase 5**: Add configuration and environment setup
6. **Phase 6**: Docker and deployment setup
7. **Phase 7**: Testing

---

## Migration Checklist

### Backend
- [ ] Create FastAPI application structure
- [ ] Implement research pipeline endpoints
- [ ] Implement session management endpoints
- [ ] Create pipeline orchestrator service
- [ ] Create graph factory
- [ ] Move business logic from `src/` to `backend/`
- [ ] Remove Streamlit dependencies from business logic
- [ ] Add error handling and logging
- [ ] Add API documentation (OpenAPI/Swagger)
- [ ] Add health check endpoint
- [ ] Add CORS configuration
- [ ] Add request validation
- [ ] Add rate limiting (optional)

### Frontend
- [ ] Create API client service
- [ ] Refactor Streamlit app to use API client
- [ ] Remove business logic from frontend
- [ ] Update UI components
- [ ] Add error handling for API calls
- [ ] Add loading states
- [ ] Add streaming support (SSE)

### Infrastructure
- [ ] Create Dockerfiles
- [ ] Create docker-compose.yml
- [ ] Add environment configuration
- [ ] Set up development environment
- [ ] Document deployment process

### Testing
- [ ] Write backend unit tests
- [ ] Write API integration tests
- [ ] Write frontend integration tests
- [ ] Test end-to-end pipeline

---

## Benefits of This Architecture

1. **Separation of Concerns**: Clear boundary between frontend and backend
2. **Scalability**: Backend can be scaled independently
3. **Reusability**: Backend API can be used by other clients
4. **Testability**: Business logic can be tested without UI
5. **Deployment Flexibility**: Frontend and backend can be deployed separately
6. **Technology Independence**: Frontend can be replaced (React, Vue, etc.)
7. **Better Error Handling**: Centralized error handling in backend
8. **API Documentation**: Auto-generated OpenAPI docs
9. **Security**: API keys stored server-side, not in frontend
10. **Monitoring**: Better observability with structured logging

---

## Estimated Effort

- **Phase 1** (Structure): 4-6 hours
- **Phase 2** (Implementation): 8-12 hours
- **Phase 3** (Refactoring): 6-8 hours
- **Phase 4** (Frontend): 4-6 hours
- **Phase 5** (Configuration): 2-3 hours
- **Phase 6** (Deployment): 3-4 hours
- **Phase 7** (Testing): 4-6 hours

**Total**: ~31-45 hours

---

## Notes

- Consider using WebSockets or Server-Sent Events for real-time updates
- For production, implement proper authentication/authorization
- Consider adding request rate limiting
- Add comprehensive logging and monitoring
- Consider using a message queue (Redis, RabbitMQ) for task management
- Add API versioning strategy
- Consider adding caching for frequently accessed data

