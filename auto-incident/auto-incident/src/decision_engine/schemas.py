"""RCA and action schemas."""
from pydantic import BaseModel, Field


class RCAReport(BaseModel):
    """Root Cause Analysis report with recommended actions."""

    summary: str
    root_cause: str
    evidence_summary: list[dict] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)
