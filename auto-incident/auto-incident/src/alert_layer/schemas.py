"""Alert layer schemas."""
from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


TriggerType = Literal["latency_spike", "error_rate"]


class AlertEvent(BaseModel):
    """Normalized alert event from external systems."""

    trigger_type: TriggerType
    service: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    threshold: float
    value: Optional[float] = None
    raw_payload: dict[str, Any] = Field(default_factory=dict)
