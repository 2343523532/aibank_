"""Implements a simple expected loss calculator for credit portfolios."""
from __future__ import annotations

from statistics import mean
from typing import Any, Dict, List

from ...core.base_agent import BaseAgent


class CreditRiskAnalyzer(BaseAgent):
    """Calculates expected loss and flags high risk exposures."""

    def __init__(self, *, high_risk_threshold: float = 0.05) -> None:
        super().__init__(
            name="CreditRiskAnalyzer",
            category="Finance",
            purpose="Estimate expected credit loss and highlight high risk assets.",
        )
        self.high_risk_threshold = high_risk_threshold

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        portfolio: List[Dict[str, Any]] = context.get("credit_portfolio", [])
        expected_losses = []
        risk_flags = []

        for exposure in portfolio:
            probability = float(exposure.get("prob_default", 0.0))
            lgd = float(exposure.get("loss_given_default", 0.0))
            value = float(exposure.get("exposure", 0.0))
            expected_loss = probability * lgd * value
            expected_losses.append(expected_loss)
            if probability >= self.high_risk_threshold:
                risk_flags.append({
                    "name": exposure.get("name", "Unknown"),
                    "prob_default": probability,
                    "exposure": value,
                })

        total_expected_loss = round(sum(expected_losses), 2)
        average_probability = round(mean([e.get("prob_default", 0.0) for e in portfolio]), 4) if portfolio else 0.0

        self.update_state(notes={
            "high_risk_count": len(risk_flags),
            "last_total_expected_loss": total_expected_loss,
        })

        return {
            "expected_loss": total_expected_loss,
            "high_risk_exposures": risk_flags,
            "confidence": 0.85 if portfolio else 0.3,
            "average_probability": average_probability,
        }
