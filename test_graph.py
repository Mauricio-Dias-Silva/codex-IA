from codex_ia.core.context import ContextManager
import os

# Test on the codex-IA repo itself
root = os.getcwd()
print(f"Testing ContextManager in {root}")

cm = ContextManager(root)
print("Building graph...")

# Use the new build_graph method (indirectly via get_context logic if desired, or direct)
# Note: I modified get_context to call build_graph, so let's check that or call build_graph directly if accessible
graph = cm.build_graph()

print("\n--- GRAPH OUTPUT ---")
print(graph[:1000]) # First 1000 chars
print("...\n--------------------")

if "PROJECT ARCHITECTURE GRAPH" in graph:
    print("SUCCESS: Graph header found")
else:
    print("FAILURE: Graph header not found")

if "codex_ia/core/agent.py" in graph:
    print("SUCCESS: Found agent.py in graph")
else:
    print("FAILURE: agent.py not found in graph")
