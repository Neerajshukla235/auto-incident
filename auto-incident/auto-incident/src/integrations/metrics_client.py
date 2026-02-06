"""Metrics integration - Prometheus, Datadog, etc. Mock implementation for Phase 1."""
from datetime import datetime, timedelta
from typing import Any, List, Optional


def fetch_metrics(
    service: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    metrics: Optional[List[str]] = None,
) -> dict[str, Any]:
    """
    Fetch system metrics for a service within a time range.
    Returns mock data in Phase 1.
    """
    end = end_time or datetime.utcnow()
    start = start_time or end - timedelta(minutes=15)

    return {
        "service": service,
        "time_range": {"start": start.isoformat(), "end": end.isoformat()},
        "cpu_percent": 92.5,
        "memory_percent": 78.2,
        "p99_latency_ms": 4200,
        "error_rate": 0.15,
        "request_rate": 1200,
        "time_series": {
            "p99": [1200, 1500, 2800, 4200, 3800],
            "cpu": [45, 62, 78, 92, 91],
            "error_rate": [0.01, 0.02, 0.08, 0.15, 0.14],
        },
    }
