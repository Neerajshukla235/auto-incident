"""Tests for Shared Incident Memory."""
import pytest

from src.memory import IncidentMemory, Finding, Hypothesis, Evidence


def test_add_finding():
    m = IncidentMemory()
    m.add_finding("logs", "Connection timeout detected", 0.9)
    assert len(m.findings) == 1
    assert m.findings[0].agent == "logs"
    assert m.findings[0].content == "Connection timeout detected"
    assert m.findings[0].confidence == 0.9


def test_add_hypothesis():
    m = IncidentMemory()
    m.add_hypothesis("Database pool exhaustion", ["ev1", "ev2"])
    assert len(m.hypotheses) == 1
    assert "pool exhaustion" in m.hypotheses[0].description
    assert m.hypotheses[0].supporting_evidence_ids == ["ev1", "ev2"]


def test_add_evidence_returns_id():
    m = IncidentMemory()
    ev_id = m.add_evidence("logs", {"error": "timeout"})
    assert ev_id
    assert len(m.evidence) == 1
    assert m.evidence[0].id == ev_id


def test_get_context():
    m = IncidentMemory()
    m.add_finding("logs", "Stack trace found")
    m.add_hypothesis("Config change caused issue")
    ctx = m.get_context()
    assert "Findings" in ctx
    assert "Stack trace found" in ctx
    assert "Hypotheses" in ctx
    assert "Config change" in ctx
