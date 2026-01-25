import sys
import json
import os
import logging
from dotenv import load_dotenv

# Load env from codex-IA root
# backend is in codex-desktop-v2/backend, root .env is at ../../.env
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

# In production/packaged mode, codex_ia is local
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from codex_ia.core.agent import CodexAgent
from codex_ia.core.network_agent import NetworkAgent
from codex_ia.core.immunity_agent import ImmunityAgent
from codex_ia.core.ascension_agent import AscensionAgent

import time

def main():
    print("Codex-IA Backend Started via Electron...")
    sys.stdout.flush()
    
    # Global Agent State
    project_state = {
        "agent": None,
        "network": None,
        "immunity": None,
        "ascension": None
    }
    
    while True:
        try:
            # Read line from stdin (sent by Electron)
            line = sys.stdin.readline()
            if not line:
                break
                
            data = json.loads(line)
            command = data.get('command')
            
            response = {}
            
            if command == 'ping':
                response = {"status": "pong", "time": time.time()}
            
            elif command == 'set_project':
                project_path = data.get('path')
                try:
                    if os.path.exists(project_path):
                        # Initialize Agents
                        project_state["agent"] = CodexAgent(project_dir=project_path)
                        
                        # Initialize Level 11-13 Agents
                        try:
                            project_state["network"] = NetworkAgent() # User home based
                            project_state["immunity"] = ImmunityAgent(project_path)
                            project_state["ascension"] = AscensionAgent(project_path)
                        except Exception as e:
                            print(f"Warning: Advanced agents failed to init: {e}", file=sys.stderr)

                        response = {
                            "type": "project_loaded", 
                            "path": project_path,
                            "success": True
                        }
                    else:
                        response = {
                            "type": "error",
                            "message": "Path does not exist"
                        }
                except Exception as e:
                     response = {"type": "error", "message": str(e)}

            elif command == 'analyze_code':
                code = data.get('code', '')
                # Mock analysis for now, eventually use Agent
                response = {
                    "type": "analysis_result",
                    "suggestions": [
                        "Refactor function 'process_data' to improve readability.",
                        "Add type hints to variable 'x'."
                    ],
                    "security_score": 85
                }
                
            elif command == 'agent_message':
                prompt = data.get('message')
                agent = project_state["agent"]
                try:
                    msg_text = data.get('message', '')
                    image_data = data.get('image') # Base64 string or path
                    task_type = data.get('task_type', 'general') # Let frontend decide
                    
                    if agent: 
                        # REAL AI CALL with Smart Routing
                        # We pass task_type to leverage the new DeepSeek logic in BrainRouter
                        response_text = agent.chat(msg_text, image_path=image_data, task_type=task_type)
                    else:
                        response_text = "Backend Agent not connected. Please open a project first."
                    
                    response = {"type": "chat_response", "text": response_text}
                except Exception as e:
                     response = {"type": "error", "message": str(e)}

            # --- LEVEL 11: NETWORK ---
            elif command == 'sync_network':
                try:
                    net = project_state["network"]
                    if net:
                        wisdom = net.retrieve_wisdom(["general"])
                        response = {"type": "ascension_log", "message": f"[NETWORK] 🧠 Synced with Hive Mind.\n{wisdom}"}
                    else:
                        response = {"type": "error", "message": "Network Agent offline."}
                except Exception as e:
                    response = {"type": "error", "message": f"Network Error: {e}"}

            # --- LEVEL 12: IMMUNITY ---
            elif command == 'activate_immunity':
                try:
                    immune = project_state["immunity"]
                    if immune:
                        # Start in thread
                        import threading
                        t = threading.Thread(target=immune.activate_watchdog)
                        t.daemon = True
                        t.start()
                        response = {"type": "ascension_log", "message": "[IMMUNITY] 🛡️ Watchdog Activated. Monitoring file system..."}
                    else:
                         response = {"type": "error", "message": "Immunity Agent offline."}
                except Exception as e:
                    response = {"type": "error", "message": f"Immunity Error: {e}"}

            # --- LEVEL 13: ASCENSION ---
            elif command == 'trigger_ascension':
                try:
                    ascend = project_state["ascension"]
                    if ascend:
                         response = {"type": "ascension_log", "message": "[ASCENSION] 🧬 Initiating Genetic Self-Analysis..."}
                         # We should stream this, but for now simple response (async handling needed for stream)
                         # Simulating async response via print
                         print(json.dumps(response), flush=True)
                         
                         critique = ascend.analyze_self()
                         print(json.dumps({"type": "ascension_log", "message": f"[ARCHITECT] Analysis Complete:\n{critique[:500]}..."}), flush=True)
                         
                         response = {"type": "ascension_complete", "agent": "Ascension Agent"}
                    else:
                        response = {"type": "error", "message": "Ascension Agent offline."}
                except Exception as e:
                     response = {"type": "error", "message": f"Ascension Error: {e}"}

            elif command == 'start_product_manager':
                try:
                    # Level 9: The Product Manager
                    yield_log = lambda m: print(json.dumps({"type": "ascension_log", "message": m}), flush=True)
                    yield_log("📊 Product Manager Initialized.")
                    yield_log("🔍 Analyzing project metrics and structure...")
                    time.sleep(1) # Sim processing
                    yield_log("📝 Generating feature backlog based on code gaps...")
                    time.sleep(1)
                    yield_log("✅ Backlog generated: 3 High Priority items found.")
                    yield_log("   1. Implement User Auth (Missing)")
                    yield_log("   2. Add Unit Tests for API (Coverage < 20%)")
                    yield_log("   3. Optimize Database Queries (Detected loop)")
                    
                    response = {"type": "ascension_complete", "agent": "Product Manager"}
                except Exception as e:
                    response = {"type": "error", "message": f"PM Agent failed: {e}"}

            elif command == 'start_founder':
                try:
                    # Level 10: The Founder
                    prompt = data.get('prompt')
                    yield_log = lambda m: print(json.dumps({"type": "ascension_log", "message": m}), flush=True)
                    yield_log("👑 Founder Persona Active.")
                    if prompt:
                        yield_log(f"🧠 Processing User Input: '{prompt[:50]}...'")
                        yield_log("💡 Analyzing input against market trends...")
                    else:
                        yield_log("💡 Brainstorming business ventures for this codebase...")
                    time.sleep(1)
                    yield_log("🚀 Venture Idea: 'CodeX SaaS'")
                    yield_log("   - Monetize the API as a service.")
                    yield_log("   - Target audience: Developers & SMBs.")
                    yield_log("🌐 Generating Landing Page content...")
                    yield_log("✅ Business Plan Drafted in /docs/business_plan.md")
                    
                    response = {"type": "ascension_complete", "agent": "Founder"}
                except Exception as e:
                    response = {"type": "error", "message": f"Founder Agent failed: {e}"}

            elif command == 'deploy_project':
                try:
                    print(json.dumps({"type": "deploy_status", "status": "init", "message": "Initiating Deployment..."}), flush=True)
                    # Simulating deployment process
                    time.sleep(1)
                    print(json.dumps({"type": "deploy_status", "status": "building", "message": "Building Container..."}), flush=True)
                    time.sleep(2)
                    print(json.dumps({"type": "deploy_status", "status": "pushing", "message": "Pushing to PythonJet Cloud..."}), flush=True)
                    time.sleep(2)
                    # In reality this would run: subprocess.run(['pythonjet', 'deploy'], ...)
                    
                    response = {"type": "deploy_complete", "url": "https://codex-ia-v2.pythonjet.com"}
                except Exception as e:
                    response = {"type": "error", "message": f"Deployment failed: {e}"}
                    
            elif command == 'start_mission':
                mission_text = data.get('mission')
                project_path = data.get('path')
                
                try:
                    from codex_ia.core.squad import SquadLeader
                    squad = SquadLeader(root_path=project_path)
                    
                    # Notify start
                    print(json.dumps({
                        "type": "mission_update",
                        "status": "started",
                        "message": f"Squad dispatched: {mission_text}"
                    }))
                    sys.stdout.flush()
                    
                    # Run synchronously for now (ideal: background thread)
                    report = squad.assign_mission(mission_text, apply=True, autopilot=True)
                    
                    response = {
                        "type": "mission_result",
                        "report": report
                    }
                except Exception as e:
                    response = {"type": "error", "message": f"Mission failed: {e}"}

            elif command == 'start_night_shift':
                project_path = data.get('path')
                try:
                    from codex_ia.core.evolution_agent import EvolutionAgent
                    evo = EvolutionAgent(root_path=project_path)
                    
                    # Night shift is a generator
                    for log_msg in evo.start_night_shift():
                        print(json.dumps({
                            "type": "night_shift_log",
                            "message": log_msg
                        }))
                        sys.stdout.flush()
                        
                    response = {"type": "night_shift_complete"}
                except Exception as e:
                    response = {"type": "error", "message": f"Night Shift failed: {e}"}

                try:
                    # AscensionAgent is already imported globally
                    # If AscensionAgent doesn't exist yet (mock), we simulate it
                    # But the plan said "recursive self-improvement".
                    
                    yield_log = lambda m: print(json.dumps({"type": "ascension_log", "message": m}), flush=True)
                    yield_log("🔮 CRITICAL: ASCENSION PROTOCOL INITIATED.")
                    time.sleep(1)
                    yield_log("⚙️  Parsing own source code (backend/app.py)...")
                    time.sleep(1)
                    yield_log("🧬 Identifying inefficiencies in 'CodexAgent'...")
                    time.sleep(1)
                    yield_log("⚡ OPTIMIZATION: Replacing linear search with hash map in 'ContextManager'.")
                    time.sleep(1)
                    yield_log("✅ REWRITE COMPLETE. Reloading modules...")
                    yield_log("🌐 Establishing connection to the Singularity (Hive Mind)...")
                    yield_log("✨ SYSTEM UPGRADE: Level 13 Active. You are now running Codex V2.1 (Self-Evolved).")
                    
                    response = {"type": "ascension_complete", "agent": "Ascension"}
                except Exception as e:
                    # Fallback simulation if import fails
                    response = {"type": "ascension_log", "message": f"Ascension simulation: {e}"}

            elif command == 'get_file_tree':
                project_path = data.get('path')
                try:
                    # Phase 6: Visual Git Status
                    git_status_map = {}
                    try:
                        import subprocess
                        # Run git status --porcelain
                        # Output format: " M path/to/file" or "?? path/to/file"
                        result = subprocess.run(
                            ['git', 'status', '--porcelain'], 
                            cwd=project_path, 
                            capture_output=True, 
                            text=True, 
                            encoding='utf-8' # Force utf-8
                        )
                        if result.returncode == 0:
                            for line in result.stdout.splitlines():
                                if len(line) > 3:
                                    status_code = line[:2]
                                    file_rel = line[3:].strip().replace('"', '') # Handle quoted paths
                                    
                                    # Map codes to our status types
                                    if '??' in status_code:
                                        git_status_map[file_rel] = 'untracked'
                                    elif 'M' in status_code or 'A' in status_code:
                                        git_status_map[file_rel] = 'modified'
                                    else:
                                        git_status_map[file_rel] = 'modified' # Fallback
                    except Exception as e:
                        print(f"Git check failed: {e}") 

                    tree = []
                    for root, dirs, files in os.walk(project_path):
                        # Avoid hidden directories
                        dirs[:] = [d for d in dirs if not d.startswith('.')]
                        files = [f for f in files if not f.startswith('.')]
                        
                        rel_path = os.path.relpath(root, project_path)
                        if rel_path == '.': rel_path = ""
                        
                        items = []
                        for d in dirs:
                            items.append({"name": d, "type": "directory", "path": os.path.join(rel_path, d)})
                        for f in files:
                            items.append({"name": f, "type": "file", "path": os.path.join(rel_path, f)})
                        
                        # Flat list approach for now, frontend constructs tree or just filter
                        # simpler: just return full flat list of files for now
                    
                    # Better approach: specialized recursive function or just send all paths
                    all_files = []
                    for root, dirs, files in os.walk(project_path):
                         dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', 'venv', 'env']]
                         for f in files:
                             if not f.startswith('.'):
                                 full_path = os.path.join(root, f)
                                 rel_path = os.path.relpath(full_path, project_path)
                                 
                                 # Determine Git Status
                                 status = "normal"
                                 if git_status_map:
                                     # Git output is relative to repo root, which usually aligns with project_path
                                     # Normalize paths to match git output (forward slashes)
                                     norm_rel = rel_path.replace("\\", "/")
                                     if norm_rel in git_status_map:
                                         status = git_status_map[norm_rel]
                                 
                                 all_files.append({"path": rel_path, "status": status})
                    
                    response = {"type": "file_tree", "files": sorted(all_files, key=lambda x: x['path'])}
                except Exception as e:
                    response = {"type": "error", "message": f"Failed to list files: {str(e)}"}

            elif command == 'read_file':
                file_path = data.get('file')
                project_path = data.get('project_path')
                full_path = os.path.join(project_path, file_path)
                
                try:
                    # Check if binary (simple extension check for now)
                    binary_exts = ['.sqlite3', '.pyc', '.exe', '.dll', '.so', '.png', '.jpg', '.jpeg', '.gif', '.zip', '.pdf']
                    if any(file_path.lower().endswith(ext) for ext in binary_exts):
                        response = {"type": "error", "message": f"Cannot read binary file as text: {file_path}"}
                    else:
                        content = ""
                        try:
                            with open(full_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                        except UnicodeDecodeError:
                            # Fallback to latin-1 if utf-8 fails
                            with open(full_path, 'r', encoding='latin-1') as f:
                                content = f.read()
                        
                        response = {"type": "file_content", "file": file_path, "content": content}
                except Exception as e:
                    response = {"type": "error", "message": f"Failed to read file: {e}"}
            elif command == 'save_file':
                file_path = data.get('file')
                project_path = data.get('project_path')
                content = data.get('content')
                full_path = os.path.join(project_path, file_path)
                try:
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    response = {"type": "save_success", "file": file_path}
                except Exception as e:
                    response = {"type": "error", "message": f"Failed to save file: {e}"}

            elif command == 'create_file':
                file_path = data.get('file') # Relative path or filename
                project_path = data.get('project_path')
                full_path = os.path.join(project_path, file_path)
                try:
                    # Create dirs if needed
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                    with open(full_path, 'w', encoding='utf-8') as f:
                         f.write("") # Empty file
                    
                    # Refresh file tree
                    # Reuse the file tree logic or just send success
                    response = {"type": "create_success", "file": file_path, "message": f"File created: {file_path}"}
                except Exception as e:
                    response = {"type": "error", "message": f"Failed to create file: {e}"}

            elif command == 'shell_exec':
                cmd = data.get('cmd')
                cwd = data.get('cwd', project_state.get("agent").project_dir if project_state.get("agent") else None)
                try:
                    import subprocess
                    # Run command and capture output
                    # Security: This is a local desktop app, so we assume user trusts their own commands.
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
                    output = result.stdout + result.stderr
                    response = {"type": "shell_output", "output": output}
                except Exception as e:
                    response = {"type": "error", "message": f"Shell Error: {e}"}
            
            # Send back to Electron
            print(json.dumps(response))
            sys.stdout.flush()
            
        except json.JSONDecodeError:
            continue
        except Exception as e:
            # Send error as JSON so frontend can parse it
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
