import os
import shutil
from codex_ia.core.squad import EngineerAgent, SquadLeader

def test_engineer():
    print("Testing Engineer Agent...")
    eng = EngineerAgent()
    root = "."
    file_path = "test_output/hello.py"
    code = "print('Hello World from Engineer')"
    
    # 1. Test Engineer Direct Write
    res = eng.apply_changes(root, file_path, code)
    print(res)
    
    if os.path.exists("./test_output/hello.py"):
        with open("./test_output/hello.py", "r") as f:
            content = f.read()
            if code in content:
                print("✅ Direct write verification passed.")
            else:
                print("❌ Content mismatch.")
    else:
        print("❌ File not created.")

    # Clean up
    if os.path.exists("./test_output"):
        shutil.rmtree("./test_output")

def test_squad_plan():
    print("\nTesting Squad Planning (Dry Run)...")
    try:
        squad = SquadLeader(".")
        report = squad.assign_mission("Create a python script that prints hello world", apply=False)
        print("✅ Plan:", report['plan'][:50], "...")
        print("✅ Code:", report['code'][:50], "...")
        print("✅ Status:", report['apply_status'])
    except Exception as e:
        print(f"❌ Squad error: {e}")

if __name__ == "__main__":
    test_engineer()
    test_squad_plan()
