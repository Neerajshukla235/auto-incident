"""Decision & Action Engine - synthesizes RCA and rollback recommendation."""
import json
import re

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

from src.agents.llm import get_llm
from src.memory import IncidentMemory
from .schemas import RCAReport


SYSTEM_PROMPT = """You are a Decision & Action Engine. Synthesize all findings, hypotheses, and evidence into:
1. A concise incident summary
2. The most likely root cause
3. A brief evidence summary (list of key points)
4. Recommended actions (e.g., "Rollback to version v2.3.0", "Increase database pool size")

Output MUST be valid JSON in this exact format:
{
  "summary": "...",
  "root_cause": "...",
  "evidence_summary": ["...", "..."],
  "recommended_actions": ["...", "..."]
}"""


class DecisionEngine:
    """Generates RCA and rollback recommendations from Shared Incident Memory."""

    def __init__(self):
        self.llm = get_llm()
        self.parser = StrOutputParser()

    def generate_rca(self, memory: IncidentMemory) -> RCAReport:
        """Produce RCA report from incident memory."""

        # 1. Collect shared incident context
        context = memory.get_context()

        prompt = f"""
    Incident ID: {memory.incident_id}

    All findings, hypotheses, and evidence:
    {context}

    Generate the RCA report as JSON.
    """

        # 2. Invoke LLM
        chain = self.llm | self.parser
        raw = chain.invoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=prompt),
            ]
        )

        # 3. Extract JSON from LLM output (handles ```json blocks)
        json_str = raw
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", raw)
        if match:
            json_str = match.group(1).strip()

        # 4. Parse JSON safely
        data = json.loads(json_str)

        # 5. Normalize evidence_summary → List[Dict]
        normalized_evidence = []
        for item in data.get("evidence_summary", []):
            normalized_evidence.append(
                {
                    "description": item,
                    "source": "decision_engine",
                    "confidence": 0.8,
                }
            )

        # 6. Build and return validated RCAReport
        return RCAReport(
            summary=data.get("summary", ""),
            root_cause=data.get("root_cause", ""),
            evidence_summary=normalized_evidence,
            recommended_actions=data.get("recommended_actions", []),
        )
