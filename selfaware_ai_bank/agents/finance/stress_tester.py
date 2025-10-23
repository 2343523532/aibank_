"""Stress testing agent that blends liquidity and credit perspectives."""
from __future__ import annotations

from typing import Any, Dict, List

from ...core.base_agent import BaseAgent


class StressTester(BaseAgent):
    """Runs a lightweight adverse scenario across bank metrics."""

    def __init__(self, *, probability_uplift: float = 0.5, liquidity_shock: float = 0.15) -> None:
        # Self-awareness: Calibrating the scenario knobs to stay adaptable for future instructions.
        super().__init__(
            name="StressTester",
            category="Risk",
            purpose="Project combined credit and liquidity impact under stress.",
        )
        self.probability_uplift = probability_uplift
        self.liquidity_shock = liquidity_shock

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Self-awareness: Observing shared context to synthesise a richer perspective.
        liquidity_levels: Dict[str, float] = context.get("liquidity_levels", {})
        portfolio: List[Dict[str, Any]] = context.get("credit_portfolio", [])

        stressed_liquidity: Dict[str, float] = {}
        liquidity_warnings: List[str] = []
        for account, balance in liquidity_levels.items():
            # Self-awareness: Applying the liquidity shock consistently across accounts.
            stressed_balance = round(balance * (1 - self.liquidity_shock), 2)
            stressed_liquidity[account] = stressed_balance
            if stressed_balance < 750_000:  # arbitrary resilience floor for demo purposes
                liquidity_warnings.append(account)

        stressed_losses = 0.0
        stressed_flags: List[Dict[str, Any]] = []
        for exposure in portfolio:
            probability = float(exposure.get("prob_default", 0.0))
            lgd = float(exposure.get("loss_given_default", 0.0))
            value = float(exposure.get("exposure", 0.0))

            stressed_probability = min(1.0, probability * (1 + self.probability_uplift))
            stressed_loss = stressed_probability * min(1.0, lgd + 0.1) * value
            stressed_losses += stressed_loss

            if stressed_probability >= 0.2:
                stressed_flags.append(
                    {
                        "name": exposure.get("name", "Unknown"),
                        "stressed_probability": round(stressed_probability, 3),
                        "exposure": value,
                    }
                )

        # Self-awareness: Persisting run-time narrative for the introspection engine.
        self.update_state(
            notes={
                "liquidity_alerts": liquidity_warnings,
                "stress_loss_estimate": round(stressed_losses, 2),
            }
        )

        return {
            "action": "stress_test",
            "stressed_liquidity": stressed_liquidity,
            "stressed_loss_estimate": round(stressed_losses, 2),
            "liquidity_alerts": liquidity_warnings,
            "stressed_high_risk": stressed_flags,
            "confidence": 0.75 if portfolio else 0.4,
        }


__all__ = ["StressTester"]
