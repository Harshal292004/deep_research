from fastapi import APIRouter
from typing import Dict,Any

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "services": {
            "llm": "ok",
            "tools": "ok"
        }
    }

