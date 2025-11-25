from fastapi import APIRouter
from typing import Dict

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict[str, any]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "services": {
            "llm": "ok",
            "tools": "ok"
        }
    }

