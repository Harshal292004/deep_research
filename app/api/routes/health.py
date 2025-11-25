from typing import Any, Dict

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "services": {"llm": "ok", "tools": "ok"},
    }
