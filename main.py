"""Command line demo for the SelfAware AI Bank framework."""
from __future__ import annotations

from pathlib import Path
from pprint import pprint

from selfaware_ai_bank import SelfAwareAIBank
from selfaware_ai_bank.agents import CreditRiskAnalyzer, LiquidityOptimizer


def build_demo_context() -> dict:
    return {
        "liquidity_levels": {
            "USD": 800_000,
            "EUR": 2_500_000,
            "JPY": 900_000,
            "GBP": 1_500_000,
        },
        "credit_portfolio": [
            {"name": "Retail Mortgages", "exposure": 5_000_000, "prob_default": 0.01, "loss_given_default": 0.35},
            {"name": "Corporate Loans", "exposure": 3_200_000, "prob_default": 0.06, "loss_given_default": 0.45},
            {"name": "SME Lending", "exposure": 1_100_000, "prob_default": 0.08, "loss_given_default": 0.5},
        ],
        "triggers": ["Fraud Detection", "Liquidity Monitoring"],
    }


def main() -> None:
    bank = SelfAwareAIBank(context=build_demo_context())
    bank.register_agents([LiquidityOptimizer(), CreditRiskAnalyzer()])

    docs_path = Path("docs")
    markdown_specs = []
    if docs_path.exists():
        markdown_specs = bank.load_markdown_roles(*docs_path.glob("*.md"))
        bank.load_agents_from_specs(markdown_specs)

    print("Running SelfAware AI Bank demo...\n")
    results = bank.run_all()
    for agent_name, output in results:
        print(f"Agent: {agent_name}")
        pprint(output)
        print()

    print("Introspection summary:")
    pprint(bank.summary())


if __name__ == "__main__":
    main()
