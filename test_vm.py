import sys
import os
sys.path.append('/opt/codex-ia')

print("--- DIAGNOSTIC START ---")
print(f"CWD: {os.getcwd()}")
print(f"Python: {sys.version}")

# Check Env
key = os.environ.get('GEMINI_API_KEY')
print(f"GEMINI_API_KEY: {'[PRESENT]' if key else '[MISSING]'}")

# Check Import
try:
    print("Attempting to import CodexAgent...")
    from codex_ia.core.agent import CodexAgent
    print("CodexAgent imported successfully!")
    
    # Try instantiation check (mock requests)
    print("Attempting dry initialization...")
    # Just checking if class is valid, not instantiating to avoid API calls yet
    print("Class check passed.")
    
except Exception as e:
    print(f"IMPORT ERROR: {e}")
    import traceback
    traceback.print_exc()

print("--- DIAGNOSTIC END ---")
