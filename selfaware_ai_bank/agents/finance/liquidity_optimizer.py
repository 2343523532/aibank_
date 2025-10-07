"""Implements a small liquidity balancing agent."""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ...core.base_agent import BaseAgent


class LiquidityOptimizer(BaseAgent):
    """Suggests transfers to move towards a target liquidity buffer."""

    def __init__(self, *, target_buffer: float = 1_000_000.0) -> None:
        super().__init__(
            name="LiquidityOptimizer",
            category="Finance",
            purpose="Monitor account liquidity and recommend redistributions.",
        )
        self.target_buffer = target_buffer

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        liquidity_levels: Dict[str, float] = context.get("liquidity_levels", {})
        transfers: List[Tuple[str, str, float]] = []
        shortages = {acc: bal for acc, bal in liquidity_levels.items() if bal < self.target_buffer}
        surpluses = {acc: bal for acc, bal in liquidity_levels.items() if bal > self.target_buffer}

        for deficit_account, balance in sorted(shortages.items(), key=lambda item: item[1]):
            deficit = self.target_buffer - balance
            for surplus_account, surplus_balance in sorted(surpluses.items(), key=lambda item: item[1], reverse=True):
                available = max(0.0, surplus_balance - self.target_buffer)
                if available <= 0:
                    continue
                transfer_amount = min(deficit, available)
                if transfer_amount <= 0:
                    continue
                transfers.append((surplus_account, deficit_account, round(transfer_amount, 2)))
                surplus_balance -= transfer_amount
                deficit -= transfer_amount
                surpluses[surplus_account] = surplus_balance
                if deficit <= 0:
                    break

        confidence = 0.5 if not transfers else 0.9
        self.update_state(notes={"transfers": transfers})
        return {
            "action": "rebalance_liquidity",
            "transfers": transfers,
            "confidence": confidence,
        }
