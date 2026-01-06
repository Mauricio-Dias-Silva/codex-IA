from codex_ia.core.immunity_agent import ImmunityAgent
import time
import os
import threading

print("--- Testing Level 12: The Immunity (Auto-Revert) ---")

# Setup dummy file
test_file = "test_stability.py"
with open(test_file, "w") as f:
    f.write("def foo():\n    return True\n")

print(f"[1] Created safe file: {test_file}")

# Init Agent
agent = ImmunityAgent(".")
# Mocking the _revert_file because we might not be in a git repo or don't want to mess git HEAD in verification
# But we want to verify the LOGIC.
original_revert = agent._revert_file
def mock_revert(path):
    print(f"[MOCK REVERT] Reverting {path}...")
    with open(path, "w") as f:
        f.write("def foo():\n    return True\n")

agent._revert_file = mock_revert

# Manually trigger stability check on BAD code
print("\n[2] Injecting BAD code (Syntax Error)...")
with open(test_file, "w") as f:
    f.write("def foo():\n    return Tru  # Missing 'e' \n")

agent.verify_stability(os.path.abspath(test_file))

# Check if reverted
with open(test_file, "r") as f:
    content = f.read()
    
if "return True" in content:
    print("\n[3] [OK] File was auto-reverted successfully!")
else:
    print(f"\n[3] [FAIL] File remaining broken: {content}")
    exit(1)

# Cleanup
if os.path.exists(test_file):
    os.remove(test_file)

print("\n--- [SUCCESS] Level 12 Verified ---")
