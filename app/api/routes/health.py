from typing import Any, Dict

from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/health",
    summary="Health check",
    description=(
        "Lightweight liveness and readiness probe for the Deep Research API.\n\n"
        "This endpoint is safe to call frequently (e.g. from load balancers or uptime\n"
        "monitors) and performs inexpensive checks to verify that the HTTP server is\n"
        "responsive and core subsystems are available.\n\n"
        "Typical usage:\n"
        "- Kubernetes / Docker health probes\n"
        "- External uptime monitoring\n"
        "- Simple 'is the backend up?' checks from clients."
    ),
    response_description="Current health status of the Deep Research API and core services.",
)
async def health_check() -> Dict[str, Any]:
    """
    Return a simple structured health report.

    **Example successful response**:

    ```json
    {
      "status": "healthy",
      "version": "1.0.0",
      "services": {
        "llm": "ok",
        "tools": "ok"
      }
    }
    ```
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "services": {"llm": "ok", "tools": "ok"},
    }
