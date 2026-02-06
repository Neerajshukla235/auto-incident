"""Deploy / CI-CD integration - Jenkins, ArgoCD, GitHub Actions. Mock for Phase 1."""
from datetime import datetime, timedelta
from typing import Any, Optional


def fetch_deploy_history(
    service: str,
    limit: int = 10,
    since: Optional[datetime] = None,
) -> list[dict[str, Any]]:
    """
    Fetch recent deployment history for a service.
    Returns mock data in Phase 1.
    """
    since = since or datetime.utcnow() - timedelta(hours=24)
    return [
        {
            "deploy_id": "dpl-001",
            "version": "v2.3.1",
            "timestamp": (datetime.utcnow() - timedelta(minutes=30)).isoformat(),
            "commit": "a1b2c3d",
            "branch": "main",
            "status": "success",
            "config_diff": {
                "pool_size": {"old": 10, "new": 50},
                "timeout_seconds": {"old": 30, "new": 5},
            },
        },
        {
            "deploy_id": "dpl-002",
            "version": "v2.3.0",
            "timestamp": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
            "commit": "e4f5g6h",
            "branch": "main",
            "status": "success",
            "config_diff": {},
        },
    ]
