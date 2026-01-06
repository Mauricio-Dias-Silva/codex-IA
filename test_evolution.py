from codex_ia.core.evolution_agent import EvolutionAgent
import os

root = os.getcwd()
print(f"Testing EvolutionAgent in {root}")

agent = EvolutionAgent(root)
opps = agent.scan_for_improvements()

print(f"Found {len(opps)} opportunities.")
for op in opps:
    print(f"- {op['file']}: {op['type']}")

found_debt = any(op['file'] == 'test_debt.py' and op['type'] == 'TECH_DEBT' for op in opps)

if found_debt:
    print("SUCCESS: Detected tech debt in test_debt.py")
else:
    print("FAILURE: Did not detect tech debt")
