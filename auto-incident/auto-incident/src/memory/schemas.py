"""Shared memory schemas."""
from typing import Any, Dict, Union

from pydantic import BaseModel, Field


class Finding(BaseModel):
    """A finding from an investigator agent."""

    agent: str
    content: str
    confidence: float = Field(ge=0, le=1)


class Hypothesis(BaseModel):
    """A causal hypothesis about the incident."""

    description: str
    supporting_evidence_ids: list[str] = Field(default_factory=list)


class Evidence(BaseModel):
    """Raw evidence from logs, metrics, or deploy history."""

    id: str
    source: str
    data: Union[str, Dict[str, Any]]
