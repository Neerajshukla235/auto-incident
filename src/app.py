"""Streamlit UI for LogAgent incident commander."""
import streamlit as st
from agents.orchestrator import IncidentOrchestrator
import json

# Page configuration
st.set_page_config(
    page_title="LogAgent - Incident Commander",
    page_icon="🚨",
    layout="wide",
)

st.title("🚨 LogAgent - Multi-Agent Incident Commander")
st.markdown("*First step: Intelligent incident triage and orchestration*")

# Initialize session state
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = IncidentOrchestrator()

if "incidents" not in st.session_state:
    st.session_state.incidents = []

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    st.info("Ensure OPENAI_API_KEY is set in .env file")
    
    if st.button("Reset Application"):
        st.session_state.clear()
        st.rerun()

# Main interface
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Report Incident")
    incident_report = st.text_area(
        "Describe the incident:",
        placeholder="E.g., Database connection pool exhausted, causing 500 errors across the API...",
        height=150,
    )
    
    submit_button = st.button("Analyze Incident", type="primary", use_container_width=True)

with col2:
    st.header("Quick Info")
    st.metric("Total Incidents", len(st.session_state.incidents))

# Process incident
if submit_button and incident_report:
    with st.spinner("🔄 Analyzing incident..."):
        try:
            result = st.session_state.orchestrator.process_incident(incident_report)
            st.session_state.incidents.append(result)
            
            st.success("✅ Incident analyzed!")
            
            # Display triage results
            if result.get("triage_result"):
                triage = result["triage_result"]
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    severity_colors = {
                        "critical": "🔴",
                        "high": "🟠",
                        "medium": "🟡",
                        "low": "🟢"
                    }
                    st.metric("Severity", f"{severity_colors.get(triage.severity, '❓')} {triage.severity.upper()}")
                
                with col2:
                    st.metric("Category", triage.category.upper())
                
                with col3:
                    st.metric("Assigned To", triage.assigned_team or "Unassigned")
                
                with col4:
                    st.metric("Stage", result.get("workflow_stage", "Unknown"))
                
                st.divider()
                
                # Detailed analysis
                st.subheader("📋 Incident Analysis")
                st.write(f"**Description:** {triage.description}")
                
                st.subheader("⚡ Immediate Actions")
                for i, action in enumerate(triage.immediate_actions, 1):
                    st.write(f"{i}. {action}")
        
        except Exception as e:
            st.error(f"❌ Error processing incident: {str(e)}")

# Incident history
if st.session_state.incidents:
    st.divider()
    st.header("📊 Incident History")
    
    for i, incident in enumerate(reversed(st.session_state.incidents), 1):
        with st.expander(f"Incident #{len(st.session_state.incidents) - i + 1}"):
            st.write(f"**Report:** {incident['incident_report']}")
            if incident.get("triage_result"):
                triage = incident["triage_result"]
                st.json({
                    "severity": triage.severity,
                    "category": triage.category,
                    "assigned_team": triage.assigned_team,
                    "immediate_actions": triage.immediate_actions
                })
