"""LangGraph orchestration for the incident investigation pipeline."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Optional

from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph

from src.alert_layer.schemas import AlertEvent
from src.agents.logs_agent import LogsAgent
from src.agents.metrics_agent import MetricsAgent
from src.agents.deploy_intel_agent import DeployIntelAgent
from src.decision_engine import DecisionEngine
from src.decision_engine.schemas import RCAReport
from src.memory import IncidentMemory


class IncidentState(TypedDict):
    """State passed through the investigation graph."""

    alert: AlertEvent
    memory: IncidentMemory
    rca: Optional[RCAReport]


def commander_plan(state: IncidentState) -> dict[str, Any]:
    """Trigger and plan: initialize memory, prepare for investigation."""
    memory = IncidentMemory()
    return {"memory": memory}


def investigate_telemetry(state: IncidentState) -> dict[str, Any]:
    """Run Logs + Metrics agents in parallel."""
    alert = state["alert"]
    memory = state["memory"]
    logs_agent = LogsAgent()
    metrics_agent = MetricsAgent()

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(logs_agent.investigate, alert, memory),
            executor.submit(metrics_agent.investigate, alert, memory),
        ]
        for f in as_completed(futures):
            f.result()
    return {}


def deploy_intel(state: IncidentState) -> dict[str, Any]:
    """Run Deploy Intel Agent - correlates with CI/CD and config changes."""
    alert = state["alert"]
    memory = state["memory"]
    agent = DeployIntelAgent()
    agent.investigate(alert, memory)
    return {}


def decision_engine(state: IncidentState) -> dict[str, Any]:
    """Generate RCA and rollback recommendation."""
    memory = state["memory"]
    engine = DecisionEngine()
    rca = engine.generate_rca(memory)
    return {"rca": rca}


def build_graph() -> StateGraph:
    """Build and compile the incident investigation graph."""
    builder = StateGraph(IncidentState)

    builder.add_node("commander_plan", commander_plan)
    builder.add_node("investigate_telemetry", investigate_telemetry)
    builder.add_node("deploy_intel", deploy_intel)
    builder.add_node("decision_engine", decision_engine)

    builder.add_edge(START, "commander_plan")
    builder.add_edge("commander_plan", "investigate_telemetry")
    builder.add_edge("investigate_telemetry", "deploy_intel")
    builder.add_edge("deploy_intel", "decision_engine")
    builder.add_edge("decision_engine", END)

    return builder.compile()


def run_graph(alert: AlertEvent) -> dict[str, Any]:
    """Execute the investigation graph and return the result."""
    graph = build_graph()
    initial: IncidentState = {
        "alert": alert,
        "memory": IncidentMemory(),  # placeholder, commander_plan overwrites
        "rca": None,
    }
    result = graph.invoke(initial)
    return {
        "incident_id": result["memory"].incident_id,
        "alert": {
            "trigger_type": result["alert"].trigger_type,
            "service": result["alert"].service,
        },
        "rca": result["rca"].model_dump() if result["rca"] else None,
    }
