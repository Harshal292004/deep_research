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

Project Layout
--------------
- `main.py` wires FastAPI, CORS, and routes
- `app/api/routes/` contains HTTP endpoints for research sessions
- `app/services/` and `src/` hold the orchestration logic and LangGraph nodes

Testing
-------
Run `pytest` once tests are added. No automated tests ship with the repo today.


