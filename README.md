# LogAgent - Multi-Agent AI Incident Commander

A LangGraph-based multi-agent AI system for intelligent incident response orchestration with a Streamlit frontend.

## Overview

This is **Step 1** of building an intelligent incident commander that:
- ✅ Triages incidents automatically using AI
- 🔄 Routes incidents to appropriate teams based on severity and category
- 📊 Provides real-time incident analysis
- 🚀 Prepares foundation for advanced multi-agent orchestration

## Tech Stack

- **LangGraph**: Multi-agent workflow orchestration
- **LangChain**: LLM interactions and prompting
- **Streamlit**: Interactive web interface
- **Google Gemini Pro**: Intelligence engine
- **Python 3.11+**: Core runtime

## Project Structure

```
LogAgent/
├── src/
│   └── app.py                 # Streamlit application
├── agents/
│   ├── triage_agent.py        # Incident triage logic
│   └── orchestrator.py        # LangGraph workflow
├── utils/
│   └── config.py              # Configuration management
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Add your Google Gemini API key:

```
GOOGLE_API_KEY=your-google-api-key-here
```

### 3. Run the Application

```bash
streamlit run src/app.py
```

The app will open at `http://localhost:8501`

## Usage

1. **Report an Incident**: Describe the incident in the text area
2. **Automatic Analysis**: The triage agent analyzes severity, category, and required actions
3. **View Results**: See immediate actions and team assignments
4. **Track History**: Review all processed incidents

## Features (Step 1)

### Incident Triage Agent
- Analyzes incident descriptions
- Determines severity (critical, high, medium, low)
- Categorizes incidents (outage, performance, security, data)
- Suggests immediate actions
- Recommends team assignment

### LangGraph Orchestrator
- Entry point: Incident triage node
- Routing node: Escalation logic based on severity
- Foundation for future agents (notification, escalation, remediation, etc.)

## Next Steps (Roadmap)

- [ ] **Step 2**: Add notification agent
- [ ] **Step 3**: Implement escalation agent
- [ ] **Step 4**: Build incident remediation agent
- [ ] **Step 5**: Add analytics and reporting
- [ ] **Step 6**: Integration with external systems (PagerDuty, Slack, etc.)

## API Reference

### IncidentTriageAgent

```python
from agents.triage_agent import IncidentTriageAgent

agent = IncidentTriageAgent()
result = agent.triage("Your incident description")
# Returns: IncidentTriageOutput with severity, category, actions, etc.
```

### IncidentOrchestrator

```python
from agents.orchestrator import IncidentOrchestrator

orchestrator = IncidentOrchestrator()
result = orchestrator.process_incident("Your incident description")
# Returns: Final workflow state with all processing results
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Your Google Gemini API key | Yes |
| `LOG_LEVEL` | Logging level (INFO, DEBUG, WARNING) | No |
| `ENVIRONMENT` | Environment type (development, production) | No |

## Troubleshooting

### Google API Key Error
- Ensure `.env` file exists in the project root
- Verify `GOOGLE_API_KEY` is correctly set
- Check API key has required permissions

### Dependencies Issue
```bash
pip install --upgrade -r requirements.txt
```

## Contributing

This is Step 1 of a larger project. Contributions for additional agents and features are welcome!

## License

MIT License - See LICENSE file for details

## Support

For issues or questions, please create an issue in the project repository.
