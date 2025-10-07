# Inside main.py
from selfaware_ai_bank.core.introspection_engine import IntrospectionEngine

introspector = IntrospectionEngine(ai_bank)
status_report = introspector.analyze_performance()
print(status_report)
introspector.evolve()
