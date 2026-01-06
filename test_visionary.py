from codex_ia.core.visionary_agent import VisionaryAgent
import os
import json

# Setup
root = os.getcwd()
print(f"Testing VisionaryAgent in {root}")

# Ensure we have goals
if not os.path.exists("business_goals.json"):
    print("Creating dummy business goals...")
    with open("business_goals.json", "w") as f:
        json.dump([{"goal": "Test Goal", "metric": "Test Metric"}], f)

agent = VisionaryAgent(root)
print("Asking the Visionary to align code with business goals...")

try:
    proposal = agent.align_code_with_goals()
    print("\nPROPOSAL RECEIVED:")
    print(proposal[:500] + "...")
    
    if "VISIONARY PROPOSAL" in proposal:
        print("\nSUCCESS: Visionary Agent generated a proposal.")
    else:
        print("\nFAILURE: Output did not contain expected header.")

except Exception as e:
    print(f"\nCRITICAL FAILURE: {e}")
