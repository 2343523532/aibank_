"""Facilities for reviewing and evolving the AI bank."""
from __future__ import annotations

from collections import Counter
from statistics import mean
from typing import Any, Dict, Iterable, List, Optional


class IntrospectionEngine:
    """Aggregates signals from agents to surface trends and insights."""

    def __init__(self, bank: "SelfAwareAIBank") -> None:  # noqa: F821 (forward ref)
        self.bank = bank

    def analyze_performance(self) -> Dict[str, Any]:
        """Summarise agent outputs and highlight inactive components."""
        statuses = [agent.report_status() for agent in self.bank.agents]
        category_counts = Counter(status["category"] for status in statuses)
        inactive = [status for status in statuses if not status["active"]]

        confidence_by_agent: Dict[str, List[float]] = {}
        for entry in self.bank.history:
            if "confidence" not in entry:
                continue
            confidence_by_agent.setdefault(entry["agent"], []).append(float(entry["confidence"]))

        run_metrics: Iterable[float] = [value for values in confidence_by_agent.values() for value in values]
        avg_confidence = mean(run_metrics) if run_metrics else None
        low_confidence_agents = sorted(
            agent for agent, values in confidence_by_agent.items() if values and values[-1] < 0.5
        )
        health_score = self._health_score(
            agent_count=len(statuses),
            inactive_count=len(inactive),
            average_confidence=avg_confidence,
            low_confidence_count=len(low_confidence_agents),
        )

        return {
            "agents_tracked": len(statuses),
            "categories": dict(category_counts),
            "inactive_agents": inactive,
            "average_confidence": avg_confidence,
            "low_confidence_agents": low_confidence_agents,
            "health_score": health_score,
            "recommendations": self._recommendations(inactive, low_confidence_agents, avg_confidence),
        }

    def _health_score(
        self,
        *,
        agent_count: int,
        inactive_count: int,
        average_confidence: Optional[float],
        low_confidence_count: int,
    ) -> float:
        """Score operational health from 0.0 to 1.0 using explainable penalties."""
        if agent_count == 0:
            return 0.0

        score = 1.0
        score -= inactive_count / agent_count * 0.4
        score -= low_confidence_count / agent_count * 0.2
        if average_confidence is not None:
            score *= average_confidence
        return round(max(0.0, min(1.0, score)), 4)

    def _recommendations(
        self,
        inactive: List[Dict[str, Any]],
        low_confidence_agents: List[str],
        average_confidence: Optional[float],
    ) -> List[str]:
        """Produce concrete next actions for operators reviewing the demo bank."""
        recommendations: List[str] = []
        if inactive:
            recommendations.append("Restart inactive agents and inspect their last state notes.")
        if low_confidence_agents:
            agents = ", ".join(low_confidence_agents)
            recommendations.append(f"Review low-confidence agent outputs: {agents}.")
        if average_confidence is None:
            recommendations.append("Run at least one agent cycle to establish confidence baselines.")
        elif average_confidence < 0.7:
            recommendations.append("Refresh scenario data before acting on low-confidence insights.")
        if not recommendations:
            recommendations.append("System telemetry is stable; continue monitoring drift and anomalies.")
        return recommendations

    def evolve(self) -> List[Dict[str, Any]]:
        """Placeholder evolution routine that toggles dormant agents back online."""
        interventions = []
        for agent in self.bank.agents:
            status = agent.report_status()
            if not status["active"]:
                agent.update_state(active=True, notes={"restarted_by": "introspection"})
                interventions.append({"agent": agent.name, "action": "restarted"})
        return interventions
