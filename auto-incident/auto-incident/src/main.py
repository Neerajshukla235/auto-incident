"""Main entrypoint - FastAPI webhook and pipeline."""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.alert_layer import parse_alert
from src.agents import CommanderAgent


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.commander = CommanderAgent()
    yield
    app.state.commander = None


app = FastAPI(
    title="Autonomous Incident Commander",
    description="Agentic AI First Responder for cloud incidents",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/webhook/alert")
def handle_alert(payload: dict):
    """
    Receive alert from Prometheus, Datadog, PagerDuty, or generic webhook.
    Triggers full investigation pipeline and returns RCA.
    """
    try:
        alert = parse_alert(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid alert payload: {e}")

    commander: CommanderAgent = app.state.commander
    result = commander.run(alert)
    return result


@app.get("/health")
def health():
    return {"status": "ok"}


# Serve frontend last so API routes take precedence
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")


def run_cli(alert_service: str = "api-gateway", trigger_type: str = "latency_spike"):
    """Run pipeline from CLI with a mock alert."""
    payload = {
        "trigger_type": trigger_type,
        "service": alert_service,
        "threshold": 1000,
        "value": 2500,
    }
    alert = parse_alert(payload)
    commander = CommanderAgent()
    result = commander.run(alert)
    return result


if __name__ == "__main__":
    import json
    result = run_cli()
    print(json.dumps(result, indent=2))
