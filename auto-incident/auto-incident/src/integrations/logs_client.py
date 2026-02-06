"""Logs integration - Loki, CloudWatch, etc. Mock implementation for Phase 1."""
from datetime import datetime, timedelta
from typing import Any, Optional


def fetch_logs(
    service: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """
    Fetch application logs for a service within a time range.
    Returns mock data in Phase 1.
    """
    end = end_time or datetime.utcnow()
    start = start_time or end - timedelta(minutes=15)

    # Mock stack traces and errors
    return [
        {
            "timestamp": start.isoformat(),
            "level": "ERROR",
            "message": "Connection timeout to database pool",
            "service": service,
            "trace_id": "abc123",
            "stack_trace": (
                "java.sql.SQLException: Connection timeout\n"
                "  at com.app.DatabasePool.getConnection(DatabasePool.java:42)\n"
                "  at com.app.UserService.findById(UserService.java:89)"
            ),
        },
        {
            "timestamp": (start + timedelta(minutes=2)).isoformat(),
            "level": "ERROR",
            "message": "Too many connections",
            "service": service,
            "trace_id": "def456",
            "stack_trace": (
                "org.postgresql.util.PSQLException: Too many connections\n"
                "  at org.postgresql.core.v3.QueryExecutorImpl.receiveErrorResponse"
            ),
        },
        {
            "timestamp": (start + timedelta(minutes=5)).isoformat(),
            "level": "WARN",
            "message": "High latency detected in /api/users",
            "service": service,
            "latency_ms": 4500,
        },
    ]
