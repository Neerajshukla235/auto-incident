"""Incident triage agent - first step of incident commander."""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional
from utils.config import config


class IncidentTriageOutput(BaseModel):
    """Output schema for incident triage."""
    severity: str = Field(..., description="Incident severity: critical, high, medium, low")
    category: str = Field(..., description="Incident category: outage, performance, security, data")
    description: str = Field(..., description="Parsed incident description")
    immediate_actions: list[str] = Field(..., description="List of immediate actions to take")
    assigned_team: Optional[str] = Field(None, description="Team that should handle this incident")


class IncidentTriageAgent:
    """Triage incoming incidents and assess severity."""
    
    def __init__(self):
        """Initialize the triage agent."""
        config.validate()
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=config.GOOGLE_API_KEY,
            model=config.MODEL_NAME,
            temperature=config.TEMPERATURE,
        )
        self.parser = PydanticOutputParser(pydantic_object=IncidentTriageOutput)
        self._setup_prompt()
    
    def _setup_prompt(self):
        """Setup the triage prompt template."""
        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are an incident triage specialist. Analyze incoming incident reports and assess:
1. Severity level (critical/high/medium/low)
2. Category (outage/performance/security/data)
3. Clear description of the issue
4. Immediate actions to take
5. Recommended team assignment

Respond with valid JSON matching the specified format."""
            ),
            ("user", "Incident Report: {incident_report}")
        ])
    
    def triage(self, incident_report: str) -> IncidentTriageOutput:
        """
        Triage an incident report.
        
        Args:
            incident_report: Description of the incident
            
        Returns:
            IncidentTriageOutput with parsed incident information
        """
        chain = self.prompt | self.llm | self.parser
        result = chain.invoke({"incident_report": incident_report})
        return IncidentTriageOutput(**result)
