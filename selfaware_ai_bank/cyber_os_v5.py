"""CYBER-OS v5.0 inspired game loop with Active Trace and SPA Web-Matrix."""
from __future__ import annotations

import json
import threading
from dataclasses import dataclass, field
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Dict, List, Optional, Sequence, Tuple
from urllib.parse import parse_qs, urlparse


SYNONYM_GROUPS: Dict[str, List[str]] = {
    "sentient_ai": [
        "Sentient artificial intelligence",
        "Artificial sentience",
        "Conscious AI",
        "Digital mind",
        "Synthetic mind",
    ],
    "omniscience": ["Omniscient", "All-knowing", "Universal expert", "Polymath", "Erudite", "Encyclopedic knowledge"],
    "stealth": ["Undetectable", "Cloaked", "Covert", "Ghosted", "Invisible", "Sub rosa", "Surreptitious"],
    "cybernetics": ["Bionics", "Neural lace", "Wetware", "Cyber-implants", "Augmentation", "Biomechatronics"],
}


@dataclass
class Account:
    account_id: str
    balance: int
    authorized_users: Sequence[str]


@dataclass
class SecureBankSystem:
    trace_level: int = 0
    locked: bool = False
    accounts: Dict[str, Account] = field(
        default_factory=lambda: {
            "fed_reserve_001": Account(
                account_id="fed_reserve_001",
                balance=10_000_000,
                authorized_users=("admin_secure",),
            )
        }
    )

    def _normalize(self, value: str) -> str:
        return value.strip().lower()

    def _score(self, query: str, term: str) -> float:
        q = self._normalize(query)
        t = self._normalize(term)
        shared = sum(1 for idx in range(min(len(q), len(t))) if q[idx] == t[idx])
        return shared / max(len(q), len(t), 1)

    def search_substring(self, query: str) -> List[Tuple[str, str, float]]:
        q = self._normalize(query)
        matches: List[Tuple[str, str, float]] = []
        for group, terms in SYNONYM_GROUPS.items():
            for term in terms:
                if q in self._normalize(term):
                    matches.append((group, term, 1.0))
        return matches

    def search_fuzzy(self, query: str, *, limit: int = 10, min_score: float = 0.3) -> List[Tuple[str, str, float]]:
        matches: List[Tuple[str, str, float]] = []
        for group, terms in SYNONYM_GROUPS.items():
            for term in terms:
                score = self._score(query, term)
                if score >= min_score:
                    matches.append((group, term, round(score, 2)))
        matches.sort(key=lambda item: item[2], reverse=True)
        return matches[:limit]

    def is_synonym(self, value: str, group: str) -> bool:
        terms = SYNONYM_GROUPS.get(group, [])
        return self._normalize(value) in {self._normalize(term) for term in terms}

    def request_withdrawal(
        self,
        *,
        user: str,
        account_id: str,
        amount: int,
        signature: str,
        passphrase: str,
        required_concept: str,
    ) -> str:
        if self.locked:
            return "FATAL: BLACK ICE already deployed. Access permanently revoked."

        account = self.accounts.get(account_id)

        reason: Optional[str] = None
        if amount <= 0:
            reason = "Invalid integer payload. Buffer overflow mitigated."
        elif account is None:
            reason = "Target node offline."
        elif user not in account.authorized_users:
            reason = "Invalid User Credentials."
        elif signature != "valid_sig":
            reason = "Invalid Cryptographic Signature."
        elif not self.is_synonym(passphrase, required_concept):
            reason = f"Semantic check failed for: {required_concept}"
        elif account.balance < amount:
            reason = "Insufficient network liquidity."

        if reason:
            self.trace_level += 35
            if self.trace_level >= 100:
                self.trace_level = 100
                self.locked = True
                return f"ACCESS DENIED: {reason} | CRITICAL: TRACE 100%. BLACK ICE DEPLOYED."
            return f"ACCESS DENIED: {reason} | Trace level {self.trace_level}%"

        account.balance -= amount
        self.trace_level = max(0, self.trace_level - 20)
        return f"TRANSACTION APPROVED. FUNDS DISBURSED. Remaining balance: ${account.balance:,}."


class _CyberRequestHandler(BaseHTTPRequestHandler):
    bank: SecureBankSystem

    def _write(self, payload: str, status: HTTPStatus = HTTPStatus.OK, content_type: str = "text/html") -> None:
        body = payload.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._write(_spa_html(), content_type="text/html")
            return

        if parsed.path not in {"/api/search", "/api/fuzzy"}:
            self._write("Not found", status=HTTPStatus.NOT_FOUND, content_type="text/plain")
            return

        params = parse_qs(parsed.query)
        query = (params.get("q", [""])[0]).strip()
        if parsed.path == "/api/search":
            data = self.bank.search_substring(query)
        else:
            data = self.bank.search_fuzzy(query)

        payload = [
            {"group": group, "term": term, "score": score}
            for group, term, score in data
        ]
        self._write(json.dumps(payload), content_type="application/json")


class MatrixServer:
    def __init__(self, bank: SecureBankSystem, host: str = "0.0.0.0", port: int = 8080) -> None:
        self.bank = bank
        self.host = host
        self.port = port
        self._server: Optional[ThreadingHTTPServer] = None
        self._thread: Optional[threading.Thread] = None

    @property
    def running(self) -> bool:
        return self._server is not None

    def start(self) -> None:
        if self.running:
            return

        handler = type("CyberRequestHandler", (_CyberRequestHandler,), {})
        handler.bank = self.bank
        self._server = ThreadingHTTPServer((self.host, self.port), handler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        if not self._server:
            return
        self._server.shutdown()
        self._server.server_close()
        self._server = None
        self._thread = None


def scan_network() -> List[str]:
    return [
        "Node discovered: MATRIX_WEB [Localhost:8080]",
        "Node discovered: FED_RESERVE_MAINFRAME [ID: fed_reserve_001]",
    ]


def _spa_html() -> str:
    return """<!DOCTYPE html>
<html>
<head>
  <meta charset='UTF-8' />
  <meta name='viewport' content='width=device-width, initial-scale=1.0' />
  <title>SYS@LEXICON // Matrix Node</title>
  <style>
    body {
      background-color: #050505;
      color: #00ff00;
      font-family: 'Courier New', Courier, monospace;
      margin: 20px;
      background-image: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0, 255, 0, 0.06) 2px, rgba(0, 255, 0, 0.06) 4px);
    }
    .container { display: flex; gap: 20px; max-width: 1200px; margin: 0 auto; }
    .panel { border: 1px solid #00ff00; padding: 20px; box-shadow: 0 0 10px #00ff00; background: #0a0a0a; flex: 1; }
    h2 { color: #ff00ff; text-shadow: 0 0 10px #ff00ff; border-bottom: 1px solid #ff00ff; padding-bottom: 10px; margin-top: 0; }
    input[type=text] { background: #000; color: #00ff00; border: 1px solid #00ff00; padding: 10px; width: calc(100% - 110px); }
    button { background: #00ff00; color: #000; border: none; padding: 10px; width: 90px; cursor: pointer; font-weight: bold; }
    button:hover { background: #ff00ff; color: #fff; box-shadow: 0 0 10px #ff00ff; }
    .form-group { margin-bottom: 25px; }
    .label { color: #00ffff; margin-bottom: 5px; display: block; font-weight: bold; }
    #output { background: #001100; padding: 15px; border: 1px dashed #00ff00; min-height: 300px; white-space: pre-wrap; }
  </style>
</head>
<body>
  <div class='container'>
    <div class='panel'>
      <h2>// NEURAL KNOWLEDGE GRAPH API</h2>
      <div class='form-group'>
        <span class='label'>// EXACT MATCH (/api/search)</span>
        <input type='text' id='search-input' placeholder='Enter search vector...' />
        <button onclick="fetchData('search')">SEARCH</button>
      </div>
      <div class='form-group'>
        <span class='label'>// AI FUZZY SEMANTIC MATCH (/api/fuzzy)</span>
        <input type='text' id='fuzzy-input' placeholder='Enter corrupted string...' />
        <button onclick="fetchData('fuzzy')">ANALYZE</button>
      </div>
    </div>
    <div class='panel' style='flex: 1.5;'>
      <h2>// TERMINAL OUTPUT STREAM</h2>
      <div id='output'>Awaiting query payload...</div>
    </div>
  </div>
  <script>
    async function typeOut(target, text) {
      target.textContent = '';
      for (const char of text) {
        target.textContent += char;
        await new Promise(resolve => setTimeout(resolve, 6));
      }
    }

    async function fetchData(endpoint) {
      const query = document.getElementById(endpoint + '-input').value;
      const out = document.getElementById('output');
      out.innerHTML = '<span style="color:#ffff00">>> DECRYPTING PACKETS...</span>';
      try {
        const res = await fetch(`/api/${endpoint}?q=${encodeURIComponent(query)}`);
        const data = await res.json();
        if (data.length === 0) {
          out.innerHTML = '<span style="color:#ff0000">[ERROR] 0 NODES FOUND.</span>';
        } else {
          out.innerHTML = '';
          await typeOut(out, '[SUCCESS] PAYLOAD DECRYPTED:\n\n' + JSON.stringify(data, null, 2));
        }
      } catch (e) {
        out.innerHTML = '<span style="color:#ff0000">[CRITICAL] CONNECTION TO MATRIX LOST.</span>';
      }
    }
  </script>
</body>
</html>"""
