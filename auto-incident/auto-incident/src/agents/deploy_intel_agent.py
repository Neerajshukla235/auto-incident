"""Deploy Intel Agent - historian for CI/CD and config changes."""
from datetime import datetime, timedelta

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

from src.agents.llm import get_llm
from src.integrations.deploy_client import fetch_deploy_history
from src.memory import IncidentMemory
from src.alert_layer.schemas import AlertEvent


SYSTEM_PROMPT = """You are a Deploy Intel Agent (Historian). Correlate incidents with:
- Recent CI/CD deployments
- Configuration changes (pool size, timeouts, etc.)
- Latent configuration bugs

Use findings from Logs and Metrics agents if available. Be concise. Output a finding and a hypothesis about root cause."""


class DeployIntelAgent:
    """Tracks CI/CD history and config diffs, correlates with incidents."""

    def __init__(self):
        self.llm = get_llm()
        self.parser = StrOutputParser()

    def investigate(
        self,
        alert: AlertEvent,
        memory: IncidentMemory,
    ) -> None:
        """Fetch deploy history, analyze with LLM, write findings and hypotheses."""
        since = datetime.utcnow() - timedelta(hours=24)
        deploys = fetch_deploy_history(alert.service, since=since)

        memory.add_evidence("deploy_history", {"deployments": deploys})

        context = memory.get_context()

        prompt = f"""Alert: {alert.trigger_type} on service {alert.service}

Existing findings from other agents:
{context}

Deployment history:
{deploys}

Correlate the incident with recent deployments and config changes. What hypothesis do you have for the root cause?"""

        chain = self.llm | self.parser
        response = chain.invoke(
            [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=prompt)]
        )

        memory.add_finding(agent="deploy_intel", content=response, confidence=0.9)
        memory.add_hypothesis(description=response)
