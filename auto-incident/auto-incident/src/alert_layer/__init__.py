"""Alert / Trigger layer - parses and normalizes incoming alerts."""
from .trigger import parse_alert
from .schemas import AlertEvent, TriggerType

__all__ = ["parse_alert", "AlertEvent", "TriggerType"]
