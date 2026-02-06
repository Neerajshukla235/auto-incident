"""Metrics Agent - telemetry analyst for CPU, p99, error rates."""
from datetime import datetime, timedelta

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

from src.agents.llm import get_llm
from src.integrations.metrics_client import fetch_metrics
from src.memory import IncidentMemory
from src.alert_layer.schemas import AlertEvent


SYSTEM_PROMPT = """You are a Metrics Agent (Telemetry Analyst). Analyze system metrics to identify:
- Anomalies in CPU, memory, latency (p99)
- Error rate trends
- Downstream dependency issues inferred from metrics

Be concise. Output a structured finding: what you observed, what it suggests, and your confidence (0-1)."""


class MetricsAgent:
    """Analyzes metrics, detects anomalies in CPU/p99/error rate."""

    def __init__(self):
        self.llm = get_llm()
        self.parser = StrOutputParser()

    def investigate(self, alert: AlertEvent, memory: IncidentMemory) -> None:
        """Fetch metrics, analyze with LLM, write findings to memory."""
        end = datetime.utcnow()
        start = end - timedelta(minutes=15)
        metrics = fetch_metrics(alert.service, start_time=start, end_time=end)

        memory.add_evidence("metrics", metrics)

        prompt = f"""Alert: {alert.trigger_type} on service {alert.service}
Time range: last 15 minutes

Metrics data:
{metrics}

Analyze these metrics. Identify anomalies in CPU, p99 latency, error rate. What does this suggest about the root cause?"""

        chain = self.llm | self.parser
        response = chain.invoke(
            [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=prompt)]
        )

        memory.add_finding(
            agent="metrics",
            content=response,
            confidence=0.8,
        )
