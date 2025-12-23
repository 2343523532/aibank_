# SelfAware AI Bank

SelfAware AI Bank is a lightweight playground for orchestrating cooperative AI agents in a banking domain. The project showcases how multiple specialised agents can share context, execute their domain logic, and feed analytics into an introspection engine that keeps the overall system healthy.

## Features

- **Agent Framework** – Implement custom agents by inheriting from `BaseAgent` and reporting structured results.
- **Finance Agents** – Includes ready-made agents for liquidity optimisation, credit risk analysis, and scenario stress testing.
- **Introspection Engine** – Aggregates execution history and can trigger simple interventions when agents go offline.
- **Markdown Roles** – Convert simple markdown briefs into runnable agents for quick prototyping of new roles.
- **Demo Script** – Run `python main.py` to execute a simulated banking scenario and view agent outputs.

## Project Layout

```
selfaware_ai_bank/
├── agents/
│   └── finance/
│       ├── credit_risk_analyzer.py
│       ├── liquidity_optimizer.py
│       └── stress_tester.py
├── core/
│   ├── base_agent.py
│   └── introspection_engine.py
├── bank_orchestrator.py
└── utils/
    └── markdown_loader.py
docs/
├── finance/
├── engineering/
├── product/
├── marketing/
├── design/
├── governance/
├── operations/
├── testing/
└── consciousness/
```

## Getting Started

1. **Install dependencies** (Python 3.9+ recommended). The project only relies on the Python standard library, so no extra packages are required.
2. **Run the demo:**

   ```bash
   python main.py [--target-buffer 1500000] [--high-risk-threshold 0.08] [--summary-path reports/summary.json]
   ```

   The script registers the bundled agents (including the new stress tester), runs them against a sample context, and prints a system summary. Command-line options let you tailor the demo without editing code.

3. **Add your own agents:**
   - Create a new module that subclasses `BaseAgent`.
   - Implement the `execute` method using the shared context dictionary.
   - Register your agent with `SelfAwareAIBank.register_agent`.

4. **Prototype from Markdown:**
   - Store markdown briefs in the `docs/` directory, e.g.

     ```markdown
     # Fraud Sentinel
     Purpose: Detect anomalies in transaction flows
     - Fraud Detection
     - Transaction Monitoring
     ```

   - Running `main.py` will automatically load these definitions and turn them into runnable agents.

## Next Steps

Ideas for expanding the playground:

- Persist execution history to disk or a database for auditing.
- Integrate external data sources to enrich the shared context.
- Build a web dashboard that visualises agent outputs and performance metrics in real time.

## License

This project is released under the [MIT License](LICENSE).
