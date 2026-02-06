# 🤖 Autonomous Incident Commander

An **Agentic AI First Responder** that autonomously detects, investigates, and resolves complex cloud incidents by reasoning across telemetry, logs, and deployment intelligence.


---

## Problem Statement

In high-velocity cloud environments, human reaction time is often the bottleneck during incidents. Traditional alerting systems can detect failures, but they lack the ability to **investigate, reason, and decide autonomously**.

This project addresses that gap by building an **Autonomous Incident Commander** capable of:
- Independent investigation
- Multi-agent reasoning
- Cross-domain correlation
- Actionable resolution recommendations

---

## Solution Overview

The system is designed as a **Commander-led multi-agent architecture** where specialized agents collaborate to diagnose incidents in real time.

Instead of reacting to alerts, the system **reasons about failures** using a structured decision loop:

> **Detect → Plan → Investigate → Correlate → Decide → Act → Report**

---

## Agent Architecture

### Commander Agent (Orchestrator)
- Receives alerts and classifies incidents
- Creates investigation plans
- Orchestrates sub-agents
- Correlates findings
- Determines root cause and recommended action

### Logs Agent (Forensic Analyst)
- Parses distributed application logs
- Identifies error patterns and stack traces
- Extracts temporal correlations

### Metrics Agent (Telemetry Analyst)
- Analyzes system performance metrics
- Detects anomalies in latency, CPU, and memory
- Infers downstream dependency issues

### Deploy Intelligence Agent (Historian)
- Tracks CI/CD deployments and configuration changes
- Correlates incidents with recent system changes
- Identifies latent configuration bugs

**Outcome:**  
The system generates a full Root Cause Analysis (RCA) and recommends an **immediate configuration rollback**.

---

## Automated RCA Output

The system automatically generates a structured RCA report including:
- Incident summary
- Evidence from each agent
- Root cause explanation
- Recommended remediation steps

---

## Quick Start

### Setup

```bash
cd auto-incident
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
```

**LLM options:**

- **Ollama (default, local):** Install [Ollama](https://ollama.ai) and run `ollama pull llama3.2`. No API key needed.
- **OpenAI:** Set `LLM_PROVIDER=openai` and `OPENAI_API_KEY` in `.env`
- **Anthropic:** Set `LLM_PROVIDER=anthropic` and `ANTHROPIC_API_KEY` in `.env`

### Run the server

```bash
python run.py
```

Or:

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Then open **http://localhost:8000** in your browser for the RCA report UI. Use the form to trigger an investigation and view the report.

### Trigger an investigation

**Webhook (Prometheus-compatible or generic):**

```bash
curl -X POST http://localhost:8000/webhook/alert \
  -H "Content-Type: application/json" \
  -d '{"trigger_type": "latency_spike", "service": "api-gateway", "threshold": 1000, "value": 2500}'

```

**CLI (mock alert):**

```bash
python -c "from src.main import run_cli; import json; print(json.dumps(run_cli(), indent=2))"
```

### API

- `POST /webhook/alert` - Ingest alert, run full pipeline, return RCA
- `GET /health` - Health check
