Deep Research API
=================

A FastAPI backend that orchestrates the automated research pipeline found under `app/` and `src/`.

Requirements
------------
- Python 3.10+
- `uv` or `pip` for installing the dependencies declared in `pyproject.toml`

Setup
-----
1. Create a virtual environment: `python -m venv .venv && source .venv/bin/activate`
2. Install dependencies: `pip install -e .`
3. Duplicate `.env.example` (if present) to `.env`, then fill in any API keys defined in `app/core/config.py`

Run the API
-----------
- Start the server: `uvicorn main:app --reload`
- Visit `http://localhost:8000/docs` for the interactive Swagger UI
- A simple health check lives at `http://localhost:8000/api/v1/health`

API Overview
------------

The API is organized around two main concepts:

- **Research tasks** (`/api/v1/research`): asynchronous, multi-step research runs
  that search, analyze, and synthesize information into structured reports.
- **Sessions and chats** (`/api/v1/sessions`): lightweight containers used to
  group multiple research runs and conversational exchanges for a given user or
  UI tab.

Key endpoints
~~~~~~~~~~~~~

- **Health**
  - `GET /api/v1/health` — liveness/readiness probe with basic service status.

- **Research**
  - `POST /api/v1/research/start` — enqueue a new research task.
  - `GET /api/v1/research/{task_id}/status` — poll for task status and result.
  - `GET /api/v1/research/{task_id}/stream` — stream real-time updates via SSE.
  - `POST /api/v1/research/{task_id}/cancel` — attempt to cancel a running task.

- **Sessions & chats**
  - `POST /api/v1/sessions` — create a new session.
  - `GET /api/v1/sessions/{session_id}` — fetch session metadata and chats.
  - `GET /api/v1/sessions/{session_id}/chats/{chat_id}` — get chat history.
  - `DELETE /api/v1/sessions/{session_id}/chats/{chat_id}` — delete a chat.

Typical usage pattern
~~~~~~~~~~~~~~~~~~~~~

1. **Create a session (optional but recommended)**:

   ```bash
   curl -X POST http://localhost:8000/api/v1/sessions
   ```

2. **Start a research task**:

   ```bash
   curl -X POST http://localhost:8000/api/v1/research/start \
     -H "Content-Type: application/json" \
     -d '{
       "query": "State of the art techniques for retrieval-augmented generation (RAG) in 2025",
       "api_keys": {
         "EXA_API_KEY": "exa-xxxxx",
         "SERPER_API_KEY": "serper-xxxxx",
         "GROQ_API_KEY": "gsk_XXXX"
       },
       "session_id": "<optional-session-id>"
     }'
   ```

3. **Track progress via polling**:

   ```bash
   curl http://localhost:8000/api/v1/research/<task_id>/status
   ```

4. **Or stream updates via SSE**:

   ```bash
   curl -N http://localhost:8000/api/v1/research/<task_id>/stream
   ```

The same patterns apply when calling the API from a frontend—use the `task_id`
and `session_id` returned by `/research/start` to wire progress indicators and
result views.

Project Layout
--------------
- `main.py` wires FastAPI, CORS, and routes
- `app/api/routes/` contains HTTP endpoints for research sessions
- `app/services/` and `src/` hold the orchestration logic and LangGraph nodes

Testing
-------
Run `pytest` once tests are added. No automated tests ship with the repo today.


