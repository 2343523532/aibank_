# file: main.py
from selfaware_ai_bank.bank_orchestrator import SelfAwareAIBank
from selfaware_ai_bank.agents.finance.liquidity_optimizer import LiquidityOptimizer
from selfaware_ai_bank.agents.finance.credit_risk_analyzer import CreditRiskAnalyzer

if __name__ == "__main__":
    ai_bank = SelfAwareAIBank()
    ai_bank.register_agent(LiquidityOptimizer())
    ai_bank.register_agent(CreditRiskAnalyzer())
    
    ai_bank.context = {
        "liquidity_levels": {"USD": 800000, "EUR": 2500000, "JPY": 900000}
    }
    
    ai_bank.run_all()
