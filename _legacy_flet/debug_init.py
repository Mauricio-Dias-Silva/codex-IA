import sys
import os
import logging

# Configure logging to print to console
logging.basicConfig(level=logging.DEBUG)

# Add the current directory to sys.path so we can import codex_ia
current_dir = os.getcwd()
sys.path.append(current_dir)

print(f"Current Directory: {current_dir}")
print("Attempting to import CodexAgent...")

try:
    from codex_ia.core.agent import CodexAgent
    print("Import successful.")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error during import: {e}")
    sys.exit(1)

print("Attempting to initialize CodexAgent...")
try:
    agent = CodexAgent(project_dir=current_dir)
    print("CodexAgent initialized successfully!")
    print(f"Active Brain: {agent.llm_client.active_brain}")
    print(f"Available Neurons: {list(agent.llm_client.neurons.keys())}")
except Exception as e:
    print(f"Initialization failed: {e}")
    import traceback
    traceback.print_exc()
