"""Commander Agent - orchestrates triage, planning, and task delegation."""
from typing import Any


from src.alert_layer.schemas import AlertEvent
from src.agents.graph import run_graph


class CommanderAgent:
    """
    Commander (Orchestrator) using LangGraph:
    - Incident triager
    - Planning
    - Task delegation via graph (Logs + Metrics parallel, then Deploy Intel)
    - Decision making via Decision Engine
    """

    def run(self, alert: AlertEvent, memory: None = None) -> dict[str, Any]:
        """
        Execute full investigation pipeline via LangGraph.
        Memory is created internally by the graph; the `memory` param is ignored for API compatibility.
        """
        return run_graph(alert)
