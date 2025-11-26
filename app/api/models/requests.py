from typing import Dict, Optional

from pydantic import BaseModel, Field


class StartResearchRequest(BaseModel):
    """
    Input payload for starting a new research task.

    The research pipeline runs asynchronously: this request only enqueues the
    task and returns a `task_id` that you can use with the status or streaming
    endpoints to retrieve progress and results.
    """

    query: str = Field(
        ...,
        description=(
            "Natural language research question or topic to investigate.\n\n"
            "The pipeline will:\n"
            "- search the web and other tools using this query,\n"
            "- analyze and cluster retrieved information, and\n"
            "- synthesize a structured research report."
        ),
        examples=[
            "State of the art techniques for retrieval-augmented generation (RAG) in 2025",
            "Compare the security trade-offs between OAuth 2.1 and OAuth 2.0 for web APIs",
        ],
    )
    api_keys: Dict[str, str] = Field(
        ...,
        description=(
            "Per-request API keys for external tools and providers.\n\n"
            "Keys are typically forwarded to internal tools (e.g. search, GitHub, LLM providers).\n"
            "You can pass only the keys you actually need for a given run."
        ),
        examples=[
            {
                "EXA_API_KEY": "exa-xxxxx",
                "SERPER_API_KEY": "serper-xxxxx",
                "GROQ_API_KEY": "gsk_XXXX",
            }
        ],
    )
    langfuse_config: Optional[Dict[str, str]] = Field(
        default=None,
        description=(
            "Optional Langfuse tracing configuration used to instrument the run.\n\n"
            "If provided, the pipeline may create traces, spans, and logs associated\n"
            "with this research task for observability and debugging."
        ),
        examples=[
            {
                "LANGFUSE_PUBLIC_KEY": "pk-xxxx",
                "LANGFUSE_SECRET_KEY": "sk-xxxx",
                "LANGFUSE_HOST": "https://cloud.langfuse.com",
            }
        ],
    )
    session_id: Optional[str] = Field(
        default=None,
        description=(
            "Optional ID of a previously-created session to associate with this task.\n\n"
            "If omitted, the backend will create a new internal session. This is\n"
            "useful when you want to group multiple research runs under the same\n"
            "UI or conversational session."
        ),
        examples=["9f2d7808-5f1b-4a3a-9e8e-7c6b12345678"],
    )


class CreateSessionRequest(BaseModel):
    """
    Placeholder request body for creating a session.

    The current implementation does not require any fields, but this model
    exists so that the API can evolve in a backwards-compatible way (for
    example, adding optional metadata about the client or user later on).
    """

    pass


class ValidateConfigRequest(BaseModel):
    """
    Request payload for validating a set of API keys or configuration values.

    This can be used by future endpoints or internal tools that need to check
    whether provided credentials are syntactically valid or can authenticate
    against third-party services.
    """

    api_keys: Dict[str, str] = Field(
        ...,
        description="Map of configuration key to raw value (typically API keys or tokens).",
        examples=[
            {
                "EXA_API_KEY": "exa-xxxxx",
                "SERPER_API_KEY": "serper-xxxxx",
                "GITHUB_ACCESS_TOKEN": "ghp_xxxxx",
            }
        ],
    )
