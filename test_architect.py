import os
from dotenv import load_dotenv
load_dotenv(override=True)
from codex_ia.core.architect_agent import ArchitectAgent

# Setup
root = os.getcwd()
print(f"Testing ArchitectAgent in {root}")

agent = ArchitectAgent(root)
print("Asking the Architect to design a 'User Notification System'...")

requirements = """
We need a system to send notifications to users via Email and SMS.
- Users can configure their preferences (Email, SMS, Both, None).
- We need a history of sent notifications.
- High volume support (queueing).
"""

try:
    design = agent.generate_design_doc(requirements)
    print("\n--- DESIGN DOCUMENT RECEIVED ---\n")
    print(design[:1000] + "\n...(Truncated)")
    
    # Save it to a file for review
    with open("ARCHITECT_DESIGN_TEST.md", "w", encoding='utf-8') as f:
        f.write(design)
    print("\nSaved design to ARCHITECT_DESIGN_TEST.md")

except Exception as e:
    print(f"\nCRITICAL FAILURE: {e}")
