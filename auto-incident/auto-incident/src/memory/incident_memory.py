"""Shared Incident Memory - stores findings, hypotheses, evidence for an incident."""
import uuid
from typing import Any, Dict, List, Optional, Union

from .schemas import Evidence, Finding, Hypothesis


class IncidentMemory:
    """Central memory store for a single incident investigation."""

    def __init__(self, incident_id: Optional[str] = None):
        self.incident_id = incident_id or str(uuid.uuid4())
        self.findings: list[Finding] = []
        self.hypotheses: list[Hypothesis] = []
        self.evidence: list[Evidence] = []
        self._evidence_ids: set[str] = set()

    def add_finding(self, agent: str, content: str, confidence: float = 0.8) -> None:
        self.findings.append(
            Finding(agent=agent, content=content, confidence=confidence)
        )

    def add_hypothesis(self, description: str, supporting_evidence_ids: Optional[List[str]] = None) -> None:
        self.hypotheses.append(
            Hypothesis(
                description=description,
                supporting_evidence_ids=supporting_evidence_ids or [],
            )
        )

    def add_evidence(self, source: str, data: Union[str, Dict[str, Any]]) -> str:
        ev_id = str(uuid.uuid4())[:8]
        self.evidence.append(Evidence(id=ev_id, source=source, data=data))
        self._evidence_ids.add(ev_id)
        return ev_id

    def get_context(self) -> str:
        """Build context string for downstream agents and decision engine."""
        parts = []

        if self.findings:
            parts.append("## Findings")
            for f in self.findings:
                parts.append(f"- [{f.agent}] {f.content} (confidence: {f.confidence})")

        if self.hypotheses:
            parts.append("\n## Hypotheses")
            for h in self.hypotheses:
                parts.append(f"- {h.description}")

        if self.evidence:
            parts.append("\n## Evidence")
            for e in self.evidence:
                data_str = str(e.data) if isinstance(e.data, dict) else e.data
                parts.append(f"- [{e.id}] {e.source}: {data_str[:500]}")

        return "\n".join(parts) if parts else "(No findings yet)"
