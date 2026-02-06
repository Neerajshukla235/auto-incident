#!/bin/bash
# Test the Autonomous Incident Commander API
# Ensure the server is running: python run.py

BASE_URL="${BASE_URL:-http://localhost:8000}"

echo "=== Health check ==="
curl -s "$BASE_URL/health" | python3 -m json.tool

echo -e "\n=== Test 1: Latency spike alert ==="
curl -s -X POST "$BASE_URL/webhook/alert" \
  -H "Content-Type: application/json" \
  -d '{"trigger_type": "latency_spike", "service": "api-gateway", "threshold": 1000, "value": 2500}' \
  | python3 -m json.tool

echo -e "\n=== Test 2: Error rate alert ==="
curl -s -X POST "$BASE_URL/webhook/alert" \
  -H "Content-Type: application/json" \
  -d '{"trigger_type": "error_rate", "service": "user-service", "threshold": 0.05, "value": 0.12}' \
  | python3 -m json.tool

echo -e "\n=== Test 3: Prometheus-style alert ==="
curl -s -X POST "$BASE_URL/webhook/alert" \
  -H "Content-Type: application/json" \
  -d '{
    "alerts": [{
      "labels": {"alertname": "HighErrorRate", "service": "payment-service"},
      "annotations": {"threshold": "0.05", "value": "0.15"}
    }]
  }' \
  | python3 -m json.tool
