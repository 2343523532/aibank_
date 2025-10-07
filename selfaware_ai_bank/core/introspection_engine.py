"""Facilities for reviewing and evolving the AI bank."""
from __future__ import annotations

from collections import Counter
from statistics import mean
from typing import Any, Dict, Iterable, List


class IntrospectionEngine:
    """Aggregates signals from agents to surface trends and insights."""

    def __init__(self, bank: "SelfAwareAIBank") -> None:  # noqa: F821 (forward ref)
        self.bank = bank

    def analyze_performance(self) -> Dict[str, Any]:
        """Summarise agent outputs and highlight inactive components."""
        statuses = [agent.report_status() for agent in self.bank.agents]
        category_counts = Counter(status["category"] for status in statuses)
        inactive = [status for status in statuses if not status["active"]]

        run_metrics: Iterable[float] = [entry["confidence"] for entry in self.bank.history if "confidence" in entry]
        avg_confidence = mean(run_metrics) if run_metrics else None

        return {
            "agents_tracked": len(statuses),
            "categories": dict(category_counts),
            "inactive_agents": inactive,
            "average_confidence": avg_confidence,
        }

    def evolve(self) -> List[Dict[str, Any]]:
        """Placeholder evolution routine that toggles dormant agents back online."""
        interventions = []
        for agent in self.bank.agents:
            status = agent.report_status()
            if not status["active"]:
                agent.update_state(active=True, notes={"restarted_by": "introspection"})
                interventions.append({"agent": agent.name, "action": "restarted"})
        return interventions
