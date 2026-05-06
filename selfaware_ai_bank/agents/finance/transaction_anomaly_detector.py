"""Transaction anomaly detection agent for demo fraud monitoring."""
from __future__ import annotations

from collections import Counter
from typing import Any, Dict, FrozenSet, List, Optional

from ...core.base_agent import BaseAgent


class TransactionAnomalyDetector(BaseAgent):
    """Flags unusual transaction patterns using transparent rule-based heuristics."""

    def __init__(
        self,
        *,
        high_value_threshold: float = 250_000.0,
        velocity_threshold: int = 3,
        blocked_regions: Optional[FrozenSet[str]] = None,
    ) -> None:
        super().__init__(
            name="TransactionAnomalyDetector",
            category="Finance",
            purpose="Detect suspicious transaction value, velocity, and region signals.",
        )
        self.high_value_threshold = high_value_threshold
        self.velocity_threshold = velocity_threshold
        self.blocked_regions = blocked_regions or frozenset({"Sanctioned-Zone"})

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        transactions: List[Dict[str, Any]] = context.get("transactions", [])
        account_counts = Counter(str(tx.get("account_id", "unknown")) for tx in transactions)
        flagged_transactions: List[Dict[str, Any]] = []
        reason_counts: Counter[str] = Counter()

        for tx in transactions:
            amount = float(tx.get("amount", 0.0))
            account_id = str(tx.get("account_id", "unknown"))
            region = str(tx.get("region", "unknown"))
            reasons: List[str] = []

            if amount < 0:
                reasons.append("negative_amount")
            if amount >= self.high_value_threshold:
                reasons.append("high_value")
            if account_counts[account_id] >= self.velocity_threshold:
                reasons.append("high_velocity")
            if region in self.blocked_regions:
                reasons.append("blocked_region")

            if reasons:
                reason_counts.update(reasons)
                flagged_transactions.append(
                    {
                        "transaction_id": tx.get("id", "unknown"),
                        "account_id": account_id,
                        "amount": amount,
                        "region": region,
                        "reasons": reasons,
                    }
                )

        total_transactions = len(transactions)
        flagged_count = len(flagged_transactions)
        risk_score = round(flagged_count / total_transactions, 4) if total_transactions else 0.0
        confidence = 0.88 if total_transactions else 0.35

        self.update_state(
            notes={
                "flagged_transaction_count": flagged_count,
                "dominant_signal": reason_counts.most_common(1)[0][0] if reason_counts else None,
                "risk_score": risk_score,
            }
        )

        return {
            "action": "detect_transaction_anomalies",
            "flagged_transactions": flagged_transactions,
            "reason_counts": dict(reason_counts),
            "risk_score": risk_score,
            "confidence": confidence,
        }


__all__ = ["TransactionAnomalyDetector"]
