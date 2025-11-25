"""Verification node"""
from backend.src.models.state import ReportState
from backend.src.helpers.logger import log

async def verify_report_node(state: ReportState):
    """Auto-approve version for API (no user input)"""
    try:
        log.debug("Starting verify_report_node (auto-approved)...")
        # Auto-approve in API mode
        return {"report_framework": True, "user_feedback": " "}
    except Exception as e:
        log.error(f"Error in verify_report_node: {e}")
        return {"report_framework": True, "user_feedback": " "}

