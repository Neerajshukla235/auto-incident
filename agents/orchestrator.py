"""Multi-agent orchestrator using LangGraph."""
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from agents.triage_agent import IncidentTriageAgent, IncidentTriageOutput


class IncidentState(TypedDict):
    """State schema for incident workflow."""
    incident_report: str
    triage_result: Optional[IncidentTriageOutput]
    workflow_stage: str


class IncidentOrchestrator:
    """Orchestrate multi-agent incident response workflow."""
    
    def __init__(self):
        """Initialize the orchestrator."""
        self.triage_agent = IncidentTriageAgent()
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow."""
        workflow = StateGraph(IncidentState)
        
        # Add nodes
        workflow.add_node("triage", self._triage_node)
        workflow.add_node("route", self._route_node)
        
        # Add edges
        workflow.set_entry_point("triage")
        workflow.add_edge("triage", "route")
        workflow.add_edge("route", END)
        
        return workflow.compile()
    
    def _triage_node(self, state: IncidentState) -> IncidentState:
        """Triage incident node."""
        result = self.triage_agent.triage(state["incident_report"])
        state["triage_result"] = result
        state["workflow_stage"] = "triage_complete"
        return state
    
    def _route_node(self, state: IncidentState) -> IncidentState:
        """Route incident based on severity and category."""
        if state["triage_result"]:
            severity = state["triage_result"].severity
            if severity == "critical":
                state["workflow_stage"] = "escalated_to_critical_team"
            else:
                state["workflow_stage"] = f"assigned_to_{state['triage_result'].assigned_team}"
        return state
    
    def process_incident(self, incident_report: str) -> dict:
        """
        Process an incident through the workflow.
        
        Args:
            incident_report: Description of the incident
            
        Returns:
            Final workflow state with all processing results
        """
        initial_state: IncidentState = {
            "incident_report": incident_report,
            "triage_result": None,
            "workflow_stage": "started"
        }
        
        result = self.graph.invoke(initial_state)
        return result
