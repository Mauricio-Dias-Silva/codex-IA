import os
from dotenv import load_dotenv
load_dotenv(override=True)
from codex_ia.core.squad import SquadLeader

# Setup
root = os.getcwd()
print(f"Testing Squad (Level 8) in {root}...\n")

squad = SquadLeader(root)

mission = "Create a thread-safe Singleton class in Python using a metaclass."
print(f"MISSION: {mission}\n")
print("Squad assembling... 🤖🤖🤖")

try:
    result = squad.assign_mission(mission)
    
    print("\n--- 1. PLAN ---")
    print(result['plan'][:300] + "...")
    
    print("\n--- 2. CODE ---")
    print(result['code'])
    
    print("\n--- 3. TESTS ---")
    print(result['tests'])
    
    print("\n✅ Squad Mission Complete!")

except Exception as e:
    print(f"\n❌ Squad Failed: {e}")
