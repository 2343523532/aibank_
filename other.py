# file: selfaware_ai_bank/bank_orchestrator.py
import importlib
import pkgutil

class SelfAwareAIBank:
    def __init__(self):
        self.agents = []
        self.context = {}
    
    def register_agent(self, agent_instance):
        print(f"[System] Registering agent: {agent_instance.name}")
        self.agents.append(agent_instance)
    
    def run_all(self):
        for agent in self.agents:
            print(f"\n[System] Executing {agent.name}...")
            result = agent.execute(self.context)
            print(f"[{agent.name}] -> {result}")
    
    def load_all_agents(self, package="selfaware_ai_bank.agents"):
        for _, name, is_pkg in pkgutil.walk_packages([package.replace('.', '/')]):
            if not is_pkg:
                try:
                    module = importlib.import_module(f"{package}.{name}")
                    for attr in dir(module):
                        obj = getattr(module, attr)
                        if isinstance(obj, type) and hasattr(obj, "execute"):
                            self.register_agent(obj())
                except Exception as e:
                    print(f"Error loading {name}: {e}")
