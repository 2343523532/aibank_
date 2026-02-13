"""High level orchestration for coordinating bank agents."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, Type

from .core.base_agent import BaseAgent
from .core.introspection_engine import IntrospectionEngine
from .utils.markdown_loader import MarkdownAgentSpec, parse_role_markdown


@dataclass
class RunRecord:
    """Keeps a log of every agent execution."""

    agent: str
    timestamp: datetime
    output: Dict[str, Any]

    @property
    def confidence(self) -> Optional[float]:
        confidence = self.output.get("confidence")
        return float(confidence) if confidence is not None else None


class SelfAwareAIBank:
    """Coordinates a collection of autonomous banking agents."""

    def __init__(self, *, context: Optional[Dict[str, Any]] = None) -> None:
        self.agents: List[BaseAgent] = []
        self.context: Dict[str, Any] = context or {}
        self.history: List[Dict[str, Any]] = []
        self.introspection = IntrospectionEngine(self)

    # ------------------------------------------------------------------
    # Registration helpers
    # ------------------------------------------------------------------
    def register_agent(self, agent: BaseAgent) -> None:
        self.agents.append(agent)

    def register_agents(self, agents: Iterable[BaseAgent]) -> None:
        for agent in agents:
            self.register_agent(agent)

    def load_agents_from_specs(self, specs: Sequence[MarkdownAgentSpec]) -> None:
        for spec in specs:
            self.register_agent(spec.to_agent())

    def load_markdown_roles(self, *paths: Path) -> List[MarkdownAgentSpec]:
        specs = []
        for path in paths:
            spec = parse_role_markdown(path.read_text())
            specs.append(spec)
        return specs

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------
    def run_agent(self, agent: BaseAgent) -> Dict[str, Any]:
        output = agent.execute(self.context)
        agent.update_state(notes={"last_output": output})
        record = RunRecord(agent=agent.name, timestamp=datetime.now(timezone.utc), output=output)
        log_entry = {
            "agent": record.agent,
            "timestamp": record.timestamp.isoformat(),
            "output": record.output,
        }
        if record.confidence is not None:
            log_entry["confidence"] = record.confidence
        self.history.append(log_entry)
        return output

    def run_all(self) -> List[Tuple[str, Dict[str, Any]]]:
        results: List[Tuple[str, Dict[str, Any]]] = []
        for agent in self.agents:
            output = self.run_agent(agent)
            results.append((agent.name, output))
        return results

    # ------------------------------------------------------------------
    # Reporting utilities
    # ------------------------------------------------------------------
    def agent_statuses(self) -> List[Dict[str, Any]]:
        return [agent.report_status() for agent in self.agents]

    def summary(self) -> Dict[str, Any]:
        summary = {
            "agents": self.agent_statuses(),
            "history": list(self.history),
            "introspection": self.introspection.analyze_performance(),
        }
        summary["interventions"] = self.introspection.evolve()
        return summary

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------
    def update_context(self, **kwargs: Any) -> None:
        self.context.update(kwargs)

    def has_agent(self, agent_type: Type[BaseAgent]) -> bool:
        return any(isinstance(agent, agent_type) for agent in self.agents)
