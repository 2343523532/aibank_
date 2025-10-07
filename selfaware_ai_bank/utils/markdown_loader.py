"""Utilities that transform markdown role descriptions into runnable agents."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List

from ..core.base_agent import BaseAgent


@dataclass
class MarkdownAgentSpec:
    name: str
    purpose: str
    capabilities: List[str]

    def to_agent(self) -> BaseAgent:
        spec = self

        class MarkdownAgent(BaseAgent):
            def __init__(self) -> None:
                super().__init__(
                    name=spec.name,
                    category="Markdown",  # default grouping
                    purpose=spec.purpose,
                )

            def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
                matched = [cap for cap in spec.capabilities if cap in context.get("triggers", [])]
                confidence = 0.2 + 0.8 * (len(matched) / max(len(spec.capabilities), 1))
                self.update_state(notes={"matched_capabilities": matched})
                return {
                    "message": f"Processed markdown-defined role '{spec.name}'.",
                    "matched_capabilities": matched,
                    "confidence": round(confidence, 2),
                }

        return MarkdownAgent()


def parse_role_markdown(content: str) -> MarkdownAgentSpec:
    lines = content.splitlines()
    name_match = re.search(r"^#\s*(.+)", lines[0]) if lines else None
    name = name_match.group(1) if name_match else "Unnamed Role"

    purpose_line = next((line for line in lines if line.lower().startswith("purpose:")), "Purpose: Undefined")
    purpose = purpose_line.split(":", 1)[1].strip() if ":" in purpose_line else purpose_line

    capabilities = [line[2:].strip() for line in lines if line.strip().startswith("- ")]

    return MarkdownAgentSpec(name=name, purpose=purpose, capabilities=capabilities)
