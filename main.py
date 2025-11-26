from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health, research, sessions
from app.core.config import settings

app = FastAPI(
    title="Deep Research API",
    version="1.0.0",
    description=(
        "Backend API for orchestrating automated deep research tasks.\n\n"
        "This service exposes endpoints to:\n"
        "- create lightweight research **sessions** used to group runs and chats,\n"
        "- start asynchronous **research tasks** that execute a multi-step pipeline\n"
        "  (search, analysis, synthesis, and report generation),\n"
        "- poll or stream **task status and progress**, and\n"
        "- perform basic health checks.\n\n"
        "Use the `/api/v1/research` endpoints when you want to run the research\n"
        "pipeline, and `/api/v1/sessions` to manage conversational or UI-level\n"
        "sessions that you associate with those runs."
    ),
    summary="Automated research orchestration API",
    contact={
        "name": "Deep Research API",
        "url": "https://localhost:8000/docs",
    },
    license_info={
        "name": "MIT",
    },
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


@app.get("/")
async def root():
    return {"message": "Deep Research API", "version": "1.0.0"}
