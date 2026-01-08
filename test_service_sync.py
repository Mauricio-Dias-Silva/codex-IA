import sys
import os

# Add painel-pythonjet to path to simulate django app context (partially)
sys.path.append(r"c:\Users\Mauricio\Desktop\painel-pythonjet")

try:
    from dashboard.services.codex_service import CodexService
    print("✅ Imported CodexService successfully.")
    
    # Check if methods exist
    if hasattr(CodexService, 'run_squad_mission') and hasattr(CodexService, 'run_nightly_optimization'):
        print("✅ Methods 'run_squad_mission' and 'run_nightly_optimization' found.")
    else:
        print("❌ Missing methods.")
        
except ImportError as e:
    print(f"❌ Import Error: {e}")
    # Debug info
    print(f"Sys Path: {sys.path}")
except Exception as e:
    print(f"❌ Error: {e}")
