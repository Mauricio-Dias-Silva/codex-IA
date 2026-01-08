import os
import time
from codex_ia.core.squad import SquadLeader

def test_autopilot_self_correction():
    print("Testing Autopilot Self-Correction...")
    
    # 1. Setup a failing test case scenario
    # We want the agent to write a file that MUST fail the test initially, 
    # but since we can't force it to write bad code, we'll give it a hard task 
    # that requires iteration? 
    # Easier: We rely on the fact that we can't completely control the first output,
    # but we can verify the MECHANISM.
    
    # Let's try a simple math function but the 'verify' command checks for a specific specific string output.
    
    squad = SquadLeader(".")
    
    # We'll ask it to print "HELLO WORLD"
    # Verification command: python test_output/check.py (which checks for HELLO WORLD)
    
    # Create the check script manually
    os.makedirs("test_output", exist_ok=True)
    with open("test_output/check.py", "w") as f:
        f.write('import sys\nwith open("test_output/target.py") as f: c=f.read()\nif "HELLO WORLD" not in c: sys.exit(1)\nprint("Found it!")')
    
    mission = "Create a python script at test_output/target.py that prints exactly 'HELLO WORLD' in uppercase."
    cmd = "python test_output/check.py"
    
    print(f"Mission: {mission}")
    print(f"Verify Cmd: {cmd}")
    
    report = squad.assign_mission(mission, apply=True, autopilot=True, verification_cmd=cmd)
    
    print("\n--- REPORT ---")
    print(f"Autopilot Status: {report.get('autopilot_status')}")
    print(f"Verification Out: {report.get('verification_out')}")
    
    if "✅ Verification Passed" in report.get('autopilot_status', ''):
        print("✅ TEST PASSED: Autopilot successfully verified the code.")
    else:
        print("❌ TEST FAILED: Autopilot did not converge.")

if __name__ == "__main__":
    test_autopilot_self_correction()
