import unittest

from main import calculate_total_liquidity, identify_high_risk_exposures, summarize_trigger_signals


class TestMainHelpers(unittest.TestCase):
    def test_calculate_total_liquidity(self):
        context = {"liquidity_levels": {"USD": 1500, "EUR": 2500, "JPY": 300}}
        self.assertEqual(calculate_total_liquidity(context), 4300.0)

    def test_identify_high_risk_exposures(self):
        context = {
            "credit_portfolio": [
                {"name": "A", "prob_default": 0.02},
                {"name": "B", "prob_default": 0.06},
                {"name": "C", "prob_default": 0.1},
            ]
        }
        result = identify_high_risk_exposures(context, threshold=0.05)
        self.assertEqual([item["name"] for item in result], ["B", "C"])

    def test_summarize_trigger_signals(self):
        context = {"triggers": ["Fraud", "Liquidity", "Fraud"]}
        self.assertEqual(summarize_trigger_signals(context), {"Fraud": 2, "Liquidity": 1})


if __name__ == "__main__":
    unittest.main()
