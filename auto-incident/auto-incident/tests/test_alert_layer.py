"""Tests for alert layer."""
import pytest
from datetime import datetime

from src.alert_layer import parse_alert, AlertEvent, TriggerType


def test_parse_generic_webhook():
    payload = {
        "trigger_type": "latency_spike",
        "service": "api-gateway",
        "threshold": 1000,
        "value": 2500,
    }
    alert = parse_alert(payload)
    assert alert.trigger_type == "latency_spike"
    assert alert.service == "api-gateway"
    assert alert.threshold == 1000
    assert alert.value == 2500


def test_parse_prometheus_alertmanager():
    payload = {
        "alerts": [
            {
                "labels": {"alertname": "HighErrorRate", "service": "user-service"},
                "annotations": {"threshold": "0.05", "value": "0.12"},
            }
        ]
    }
    alert = parse_alert(payload)
    assert alert.service == "user-service"
    assert alert.threshold == 0.05
    assert alert.value == 0.12


def test_parse_missing_fields_defaults():
    payload = {}
    alert = parse_alert(payload)
    assert alert.trigger_type == "error_rate"
    assert alert.service == "unknown"
    assert alert.threshold == 0
