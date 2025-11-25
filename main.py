from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health, research, sessions
from app.core.config import settings

app = FastAPI(
    title="Deep Research API",
    version="1.0.0",
    description="Backend API for automated research pipeline",
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
