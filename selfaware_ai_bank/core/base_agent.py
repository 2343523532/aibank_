"""Core primitives for the Self Aware AI Bank agents."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class AgentState:
    """Lightweight state container shared by every agent."""

    active: bool = True
    last_update: Optional[datetime] = None
    notes: Dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """Base class that all specialised agents inherit from."""

    def __init__(self, name: str, category: str, purpose: str) -> None:
        self.name = name
        self.category = category
        self.purpose = purpose
        self.state = AgentState()

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run the agent against the shared bank context."""

    def update_state(self, *, active: Optional[bool] = None, notes: Optional[Dict[str, Any]] = None) -> None:
        """Persist runtime information for introspection."""
        if active is not None:
            self.state.active = active
        if notes:
            self.state.notes.update(notes)
        self.state.last_update = datetime.utcnow()

    def report_status(self) -> Dict[str, Any]:
        """Return a structured view that the introspection engine can consume."""
        return {
            "agent": self.name,
            "category": self.category,
            "purpose": self.purpose,
            "active": self.state.active,
            "last_update": self.state.last_update.isoformat() if self.state.last_update else None,
            "notes": dict(self.state.notes),
        }
