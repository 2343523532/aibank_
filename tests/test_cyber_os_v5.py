from __future__ import annotations

import json
from urllib.request import urlopen

from selfaware_ai_bank.cyber_os_v5 import MatrixServer, SecureBankSystem, scan_network


def test_scan_network_lists_expected_nodes() -> None:
    nodes = scan_network()
    assert any("MATRIX_WEB" in node for node in nodes)
    assert any("FED_RESERVE_MAINFRAME" in node for node in nodes)


def test_trace_level_and_lockout_progression() -> None:
    bank = SecureBankSystem()

    denied = bank.request_withdrawal(
        user="intruder",
        account_id="fed_reserve_001",
        amount=100,
        signature="bad_sig",
        passphrase="invalid",
        required_concept="stealth",
    )
    assert "ACCESS DENIED" in denied
    assert bank.trace_level == 35
    assert bank.locked is False

    bank.request_withdrawal(
        user="intruder",
        account_id="fed_reserve_001",
        amount=100,
        signature="bad_sig",
        passphrase="invalid",
        required_concept="stealth",
    )
    denied = bank.request_withdrawal(
        user="intruder",
        account_id="fed_reserve_001",
        amount=100,
        signature="bad_sig",
        passphrase="invalid",
        required_concept="stealth",
    )
    assert "BLACK ICE DEPLOYED" in denied
    assert bank.trace_level == 100
    assert bank.locked is True


def test_successful_withdrawal_reduces_trace() -> None:
    bank = SecureBankSystem(trace_level=40)
    approved = bank.request_withdrawal(
        user="admin_secure",
        account_id="fed_reserve_001",
        amount=500,
        signature="valid_sig",
        passphrase="covert",
        required_concept="stealth",
    )
    assert "TRANSACTION APPROVED" in approved
    assert bank.trace_level == 20


def test_api_endpoints() -> None:
    bank = SecureBankSystem()
    server = MatrixServer(bank, port=8091)
    server.start()
    try:
        with urlopen("http://127.0.0.1:8091/api/search?q=covert", timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
        assert payload
        assert payload[0]["group"] == "stealth"

        with urlopen("http://127.0.0.1:8091/", timeout=5) as response:
            page = response.read().decode("utf-8")
        assert "TERMINAL OUTPUT STREAM" in page
    finally:
        server.stop()
