"""Command line demo for the SelfAware AI Bank framework."""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from pprint import pprint
from typing import Iterable, Optional

from selfaware_ai_bank import SelfAwareAIBank
from selfaware_ai_bank.agents import CreditRiskAnalyzer, LiquidityOptimizer, StressTester
from selfaware_ai_bank.cyber_os_v5 import MatrixServer, SYNONYM_GROUPS, SecureBankSystem, scan_network


def build_demo_context() -> dict:
    # Self-awareness: Maintaining a transparent view of the sandbox data.
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


def parse_args(args: Optional[Iterable[str]] = None) -> argparse.Namespace:
    # Self-awareness: Recognising CLI preferences to adapt runtime behaviour.
    parser = argparse.ArgumentParser(description="Run the SelfAware AI Bank demo scenario.")
    parser.add_argument(
        "--target-buffer",
        type=float,
        default=1_000_000.0,
        help="Desired liquidity buffer for the optimizer (default: 1,000,000).",
    )
    parser.add_argument(
        "--high-risk-threshold",
        type=float,
        default=0.05,
        help="Probability threshold for flagging risky exposures (default: 0.05).",
    )
    parser.add_argument(
        "--summary-path",
        type=Path,
        help="Optional file path for saving the introspection summary as JSON.",
    )
    parser.add_argument(
        "--no-markdown",
        action="store_true",
        help="Disable auto-loading of markdown-defined agents.",
    )
    parser.add_argument(
        "--cyber-os",
        action="store_true",
        help="Run the interactive CYBER-OS v5.0 gameplay loop.",
    )
    return parser.parse_args(args=args)


def run_cyber_os() -> None:
    bank = SecureBankSystem()
    web = MatrixServer(bank)

    print("CYBER-OS v5.0 booted. Type 'help' for commands.")
    while True:
        command = input("root@cyber-os:~# ").strip().lower()
        if command == "help":
            print("Modules: net-up, net-down, scan, bank, status, exit")
        elif command == "net-up":
            web.start()
            print("Public Matrix Interface online on http://localhost:8080")
        elif command == "net-down":
            web.stop()
            print("Public Matrix Interface taken offline.")
        elif command == "scan":
            print("Scanning 192.168.0.x subnet...")
            for result in scan_network():
                print(result)
        elif command == "status":
            print(f"ACTIVE NETWORK TRACE LEVEL: {bank.trace_level}%")
            if bank.locked:
                print("BLACK ICE ACTIVE: terminal is permanently locked.")
        elif command == "bank":
            concept = random.choice(list(SYNONYM_GROUPS.keys()))
            print(f">> ICE ACTIVE: Semantic concept required '{concept}'")
            user = input("User ID: ")
            account = input("Account ID: ")
            amount = int(input("Amount: ") or "0")
            signature = input("Signature: ")
            passphrase = input("Semantic Passphrase: ")
            result = bank.request_withdrawal(
                user=user,
                account_id=account,
                amount=amount,
                signature=signature,
                passphrase=passphrase,
                required_concept=concept,
            )
            print(result)
        elif command == "exit":
            web.stop()
            print("Terminating connection...")
            return
        else:
            print("ERROR: Command not found. Type 'help'.")


def load_markdown_agents(bank: SelfAwareAIBank, enable_markdown: bool) -> None:
    # Self-awareness: Respecting user choice about dynamic agent creation.
    if not enable_markdown:
        return

    docs_path = Path("docs")
    if not docs_path.exists():
        return

    markdown_specs = bank.load_markdown_roles(*docs_path.rglob("*.md"))
    bank.load_agents_from_specs(markdown_specs)


def maybe_write_summary(summary_path: Optional[Path], summary: dict) -> None:
    # Self-awareness: Persisting insights for longer-term learning when requested.
    if not summary_path:
        return

    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2))


def main(argv: Optional[Iterable[str]] = None) -> None:
    args = parse_args(argv)

    if args.cyber_os:
        run_cyber_os()
        return

    bank = SelfAwareAIBank(context=build_demo_context())
    bank.register_agents(
        [
            LiquidityOptimizer(target_buffer=args.target_buffer),
            CreditRiskAnalyzer(high_risk_threshold=args.high_risk_threshold),
            StressTester(),
        ]
    )

    load_markdown_agents(bank, enable_markdown=not args.no_markdown)

    print("Running SelfAware AI Bank demo...\n")
    results = bank.run_all()
    for agent_name, output in results:
        print(f"Agent: {agent_name}")
        pprint(output)
        print()

    summary = bank.summary()
    maybe_write_summary(args.summary_path, summary)

    print("Introspection summary:")
    pprint(summary)


if __name__ == "__main__":
    main()
