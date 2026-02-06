"""Logs Agent - forensic analyst for stack traces and error patterns."""
from datetime import datetime, timedelta

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

from src.agents.llm import get_llm
from src.integrations.logs_client import fetch_logs
from src.memory import IncidentMemory
from src.alert_layer.schemas import AlertEvent


SYSTEM_PROMPT = """You are a Logs Agent (Forensic Analyst). Analyze application logs to identify:
- Error patterns and stack traces
- Temporal correlations (when did errors spike?)
- Root cause clues from exception messages

Be concise. Output a structured finding: what you observed, what it suggests, and your confidence (0-1)."""


class LogsAgent:
    """Parses logs, identifies errors and stack traces, extracts temporal correlations."""

    def __init__(self):
        self.llm = get_llm()
        self.parser = StrOutputParser()

    def investigate(self, alert: AlertEvent, memory: IncidentMemory) -> None:
        """Fetch logs, analyze with LLM, write findings to memory."""
        end = datetime.utcnow()
        start = end - timedelta(minutes=15)
        logs = fetch_logs(alert.service, start_time=start, end_time=end)

        memory.add_evidence("logs", {"logs": logs})

        prompt = f"""Alert: {alert.trigger_type} on service {alert.service}
Time range: last 15 minutes

Logs data:
{logs}

Analyze these logs. Identify error patterns, stack traces, and temporal correlations. What does this suggest about the root cause?"""

        chain = self.llm | self.parser
        response = chain.invoke(
            [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=prompt)]
        )

        memory.add_finding(
            agent="logs",
            content=response,
            confidence=0.85,
        )
