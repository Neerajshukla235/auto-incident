# Test Samples for Autonomous Incident Commander

## Quick test (CLI, no server)

```bash
cd auto-incident
python -c "
from src.main import run_cli
import json
result = run_cli(alert_service='api-gateway', trigger_type='latency_spike')
print(json.dumps(result, indent=2))
"
```

## Start server and test

```bash
# Terminal 1: start server
python run.py

# Terminal 2: run tests
chmod +x test_samples/test_app.sh
./test_samples/test_app.sh
```

## Manual curl examples

**Latency spike:**
```bash
curl -X POST http://localhost:8000/webhook/alert \
  -H "Content-Type: application/json" \
  -d '{"trigger_type": "latency_spike", "service": "api-gateway", "threshold": 1000, "value": 2500}'
```

**Error rate:**
```bash
curl -X POST http://localhost:8000/webhook/alert \
  -H "Content-Type: application/json" \
  -d '{"trigger_type": "error_rate", "service": "user-service", "threshold": 0.05, "value": 0.12}'
```

## Sample data

- `alerts.json` – alert payloads for different scenarios
- `sample_logs.json` – sample logs used by mock integration (for reference)
