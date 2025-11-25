# Backend Separation - Quick Reference

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                       │
│  - UI Components (chat, config, sidebar)                    │
│  - API Client (HTTP requests)                               │
│  - Session State Management                                 │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST API
                       │ WebSocket/SSE (for streaming)
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   API Routes │  │   Services   │  │    Core      │    │
│  │              │  │              │  │              │    │
│  │ - research   │→ │ - research    │→ │ - pipeline   │    │
│  │ - sessions   │  │ - config     │  │ - graphs     │    │
│  │ - health     │  │ - langfuse   │  │ - sessions   │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              Business Logic (src/)                   │  │
│  │  - nodes/    - tools/    - chains/    - prompts/     │  │
│  └─────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │   External APIs      │
            │  - LLM APIs          │
            │  - Search APIs       │
            │  - GitHub API        │
            └──────────────────────┘
```

---

## Key API Endpoints

### 1. Start Research

```bash
POST /api/v1/research/start
Content-Type: application/json

{
  "query": "What is the current status of quantum computing?",
  "user_feedback": " ",
  "api_keys": {
    "EXA_API_KEY": "your_key",
    "SERPER_API_KEY": "your_key",
    "GITHUB_ACCESS_TOKEN": "your_token",
    "TOGETHER_API_KEY": "your_key",
    "TAVLIY_API_KEY": "your_key",
    "GROQ_API_KEY": "your_key"
  },
  "langfuse_config": {
    "public_key": "pk-lf-...",
    "secret_key": "sk-lf-...",
    "host": "https://cloud.langfuse.com"
  }
}

Response: 200 OK
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "session_id": "660e8400-e29b-41d4-a716-446655440001",
  "status": "pending",
  "created_at": "2025-01-20T10:00:00Z"
}
```

### 2. Get Research Status

```bash
GET /api/v1/research/{task_id}/status

Response: 200 OK
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress": {
    "current_stage": "research",
    "stage_progress": 0.65
  },
  "result": null
}

# When completed:
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": {
    "current_stage": "writer",
    "stage_progress": 1.0
  },
  "result": {
    "markdown": "# Report Title\n\n## Section 1\n..."
  }
}
```

### 3. Stream Research Updates (SSE)

```bash
GET /api/v1/research/{task_id}/stream
Accept: text/event-stream

# Server sends:
data: {"stage": "section", "progress": 0.25, "message": "Generating report structure..."}
data: {"stage": "research", "progress": 0.50, "message": "Researching section 1..."}
data: {"stage": "writer", "progress": 0.75, "message": "Writing final report..."}
data: {"stage": "completed", "progress": 1.0, "result": {"markdown": "..."}}
```

### 4. Create Session

```bash
POST /api/v1/sessions

Response: 200 OK
{
  "session_id": "660e8400-e29b-41d4-a716-446655440001",
  "created_at": "2025-01-20T10:00:00Z"
}
```

### 5. Get Chat History

```bash
GET /api/v1/sessions/{session_id}/chats/{chat_id}

Response: 200 OK
{
  "chat_id": "770e8400-e29b-41d4-a716-446655440002",
  "messages": [
    {
      "role": "user",
      "content": "What is quantum computing?",
      "type": "text",
      "timestamp": "2025-01-20T10:00:00Z"
    },
    {
      "role": "assistant",
      "content": "# Quantum Computing Report\n\n...",
      "type": "markdown",
      "timestamp": "2025-01-20T10:05:00Z"
    }
  ]
}
```

### 6. Health Check

```bash
GET /api/v1/health

Response: 200 OK
{
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "llm": "ok",
    "tools": "ok"
  }
}
```

---

## Frontend API Client Usage

### Python Example

```python
from services.api_client import ResearchAPIClient

# Initialize client
client = ResearchAPIClient(base_url="http://localhost:8000")

# Start research
result = await client.start_research(
    query="What is quantum computing?",
    api_keys={
        "EXA_API_KEY": "...",
        "SERPER_API_KEY": "...",
        # ... other keys
    },
    session_id="your-session-id"
)

task_id = result["task_id"]

# Poll for status
import asyncio
while True:
    status = await client.get_research_status(task_id)
    if status["status"] == "completed":
        markdown = status["result"]["markdown"]
        break
    elif status["status"] == "failed":
        error = status["error"]
        break
    await asyncio.sleep(2)

# Or stream updates
async for update in client.stream_research_updates(task_id):
    print(f"Stage: {update['stage']}, Progress: {update['progress']}")
    if update.get("result"):
        markdown = update["result"]["markdown"]
```

### JavaScript/TypeScript Example

```typescript
// api-client.ts
class ResearchAPIClient {
  constructor(private baseUrl: string = 'http://localhost:8000') {}

  async startResearch(query: string, apiKeys: Record<string, string>) {
    const response = await fetch(`${this.baseUrl}/api/v1/research/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, api_keys: apiKeys })
    });
    return response.json();
  }

  async getStatus(taskId: string) {
    const response = await fetch(
      `${this.baseUrl}/api/v1/research/${taskId}/status`
    );
    return response.json();
  }

  streamUpdates(taskId: string): EventSource {
    return new EventSource(
      `${this.baseUrl}/api/v1/research/${taskId}/stream`
    );
  }
}

// Usage
const client = new ResearchAPIClient();
const { task_id } = await client.startResearch("Query", apiKeys);

const eventSource = client.streamUpdates(task_id);
eventSource.onmessage = (event) => {
  const update = JSON.parse(event.data);
  console.log(update);
};
```

---

## Directory Structure Comparison

### Before (Monolithic)
```
deep_research/
├── app.py              # 511 lines - UI + business logic
├── src/                # Business logic
│   ├── graph.py
│   ├── nodes.py        # 630 lines
│   └── ...
└── requirements.txt
```

### After (Separated)
```
deep_research/
├── backend/            # FastAPI application
│   ├── app/
│   │   ├── main.py     # FastAPI app (~50 lines)
│   │   ├── api/        # API routes
│   │   ├── services/   # Business services
│   │   └── core/       # Core logic
│   ├── src/            # Business logic (refactored)
│   └── requirements.txt
│
├── frontend/           # Streamlit application
│   ├── app.py          # ~100 lines (UI only)
│   ├── services/       # API client
│   └── components/     # UI components
│
└── docker-compose.yml
```

---

## Key Changes Summary

### Backend Responsibilities
- ✅ Execute research pipeline
- ✅ Manage API keys (per request)
- ✅ Handle long-running tasks
- ✅ Stream updates (SSE/WebSocket)
- ✅ Session/chat management
- ✅ Error handling and logging

### Frontend Responsibilities
- ✅ Render UI components
- ✅ Collect user input
- ✅ Make API requests
- ✅ Display results
- ✅ Manage local session state (UI only)

### What Moves Where

| Component | Before | After |
|-----------|--------|-------|
| Research Pipeline | `app.py` | `backend/app/core/pipeline.py` |
| Graph Creation | `app.py` (dynamic) | `backend/app/core/graph_factory.py` |
| API Key Management | Streamlit session | Backend (per request) |
| Module Reloading | `app.py` | Removed (dependency injection) |
| Chat History | Streamlit session | Backend API |
| Business Logic | `src/` | `backend/src/` |

---

## Migration Steps

1. **Create backend structure** → Set up FastAPI app
2. **Move business logic** → Move `src/` to `backend/src/`
3. **Create API endpoints** → Implement research, sessions, health
4. **Create API client** → HTTP client for frontend
5. **Refactor frontend** → Remove business logic, use API client
6. **Test integration** → Verify end-to-end flow
7. **Deploy** → Docker setup, environment config

---

## Benefits

✅ **Separation**: Clear frontend/backend boundary  
✅ **Scalability**: Scale backend independently  
✅ **Reusability**: API usable by any client  
✅ **Testability**: Test business logic without UI  
✅ **Flexibility**: Replace frontend technology  
✅ **Security**: API keys server-side only  
✅ **Monitoring**: Better observability  

---

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py --server.port 8501
```

### Docker
```bash
docker-compose up
```

Backend: http://localhost:8000  
Frontend: http://localhost:8501  
API Docs: http://localhost:8000/docs

