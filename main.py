# file: selfaware_ai_bank/core/base_agent.py
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """Base class for all AI Bank agents."""
    
    def __init__(self, name, category, purpose):
        self.name = name
        self.category = category
        self.purpose = purpose
        self.state = {"active": True, "last_update": None}
    
    @abstractmethod
    def execute(self, context):
        """Main operational method each agent implements."""
        pass

    def report_status(self):
        return {
            "agent": self.name,
            "category": self.category,
            "status": "active" if self.state["active"] else "inactive"
        }
