"""Parse and normalize alert payloads from various sources."""
from datetime import datetime

from .schemas import AlertEvent, TriggerType


def parse_alert(payload: dict) -> AlertEvent:
    """
    Parse alert payload into normalized AlertEvent.
    Supports Prometheus Alertmanager and generic JSON webhook formats.
    """
    # Prometheus Alertmanager format
    if "alerts" in payload and payload["alerts"]:
        alert = payload["alerts"][0]
        labels = alert.get("labels", {})
        annotations = alert.get("annotations", {})

        trigger_type: TriggerType = "error_rate"
        if "latency" in str(labels.get("alertname", "")).lower():
            trigger_type = "latency_spike"
        elif "error" in str(labels.get("alertname", "")).lower():
            trigger_type = "error_rate"

        service = labels.get("service", labels.get("job", "unknown"))
        value = None
        if "value" in annotations:
            try:
                value = float(annotations["value"])
            except (ValueError, TypeError):
                pass

        return AlertEvent(
            trigger_type=trigger_type,
            service=service,
            timestamp=datetime.utcnow(),
            threshold=float(annotations.get("threshold", 0)),
            value=value,
            raw_payload=payload,
        )

    # Generic webhook format
    trigger_type = payload.get("trigger_type", "error_rate")
    if trigger_type not in ("latency_spike", "error_rate"):
        trigger_type = "error_rate"

    return AlertEvent(
        trigger_type=trigger_type,
        service=payload.get("service", "unknown"),
        timestamp=datetime.utcnow(),
        threshold=float(payload.get("threshold", 0)),
        value=payload.get("value"),
        raw_payload=payload,
    )
