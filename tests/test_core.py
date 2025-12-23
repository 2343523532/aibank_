import unittest
from datetime import datetime
from selfaware_ai_bank.core.base_agent import BaseAgent
from selfaware_ai_bank.core.introspection_engine import IntrospectionEngine
from selfaware_ai_bank.bank_orchestrator import SelfAwareAIBank

class MockAgent(BaseAgent):
    def __init__(self, name="MockAgent"):
        super().__init__(name=name, category="Test", purpose="Testing")

    def execute(self, context):
        return {"status": "success", "value": 42}

class TestBaseAgent(unittest.TestCase):
    def test_initialization(self):
        agent = MockAgent()
        self.assertEqual(agent.name, "MockAgent")
        self.assertEqual(agent.category, "Test")
        self.assertEqual(agent.purpose, "Testing")
        self.assertTrue(agent.state.active)

    def test_execute(self):
        agent = MockAgent()
        result = agent.execute({})
        self.assertEqual(result, {"status": "success", "value": 42})

    def test_update_state(self):
        agent = MockAgent()
        agent.update_state(notes={"foo": "bar"})
        self.assertEqual(agent.state.notes["foo"], "bar")
        self.assertIsInstance(agent.state.last_update, datetime)

class TestIntrospectionEngine(unittest.TestCase):
    def test_analyze_performance(self):
        bank = SelfAwareAIBank()
        agent = MockAgent()
        bank.register_agent(agent)

        # Run agent to generate history
        bank.run_agent(agent)

        engine = IntrospectionEngine(bank)
        analysis = engine.analyze_performance()

        self.assertEqual(analysis["agents_tracked"], 1)
        self.assertEqual(analysis["categories"]["Test"], 1)

class TestBankOrchestrator(unittest.TestCase):
    def test_register_agent(self):
        bank = SelfAwareAIBank()
        agent = MockAgent()
        bank.register_agent(agent)
        self.assertIn(agent, bank.agents)
        self.assertTrue(bank.has_agent(MockAgent))

    def test_run_all(self):
        bank = SelfAwareAIBank()
        agent1 = MockAgent(name="Agent1")
        agent2 = MockAgent(name="Agent2")
        bank.register_agents([agent1, agent2])

        results = bank.run_all()
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0][0], "Agent1")
        self.assertEqual(results[1][0], "Agent2")

    def test_summary(self):
        bank = SelfAwareAIBank()
        agent = MockAgent()
        bank.register_agent(agent)
        bank.run_agent(agent)

        summary = bank.summary()
        self.assertIn("agents", summary)
        self.assertIn("history", summary)
        self.assertIn("introspection", summary)

if __name__ == '__main__':
    unittest.main()
