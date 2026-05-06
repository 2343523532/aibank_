from __future__ import annotations

from selfaware_ai_bank.agents import TransactionAnomalyDetector


def test_transaction_anomaly_detector_flags_value_velocity_and_region() -> None:
    detector = TransactionAnomalyDetector(high_value_threshold=100_000, velocity_threshold=3)
    context = {
        "transactions": [
            {"id": "TX-1", "account_id": "A", "amount": 25_000, "region": "US"},
            {"id": "TX-2", "account_id": "A", "amount": 125_000, "region": "US"},
            {"id": "TX-3", "account_id": "A", "amount": 50_000, "region": "US"},
            {"id": "TX-4", "account_id": "B", "amount": 500, "region": "Sanctioned-Zone"},
        ]
    }

    result = detector.execute(context)

    assert result["action"] == "detect_transaction_anomalies"
    assert result["risk_score"] == 1.0
    assert result["reason_counts"] == {"high_velocity": 3, "high_value": 1, "blocked_region": 1}
    assert detector.state.notes["flagged_transaction_count"] == 4


def test_transaction_anomaly_detector_handles_empty_context() -> None:
    detector = TransactionAnomalyDetector()

    result = detector.execute({})

    assert result["flagged_transactions"] == []
    assert result["risk_score"] == 0.0
    assert result["confidence"] == 0.35
