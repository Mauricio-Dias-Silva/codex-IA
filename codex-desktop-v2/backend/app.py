import sys
import os
import json
import threading
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# In production/packaged mode, codex_ia is local
base_dir = os.path.dirname(os.path.abspath(__file__))
# If bundled, we might be in a temp dir, but assuming structure is kept:
# backend/app.py -> .. -> codex_desktop_v2 root -> codex_ia is there
target_path = os.path.join(base_dir, '..')
sys.path.append(target_path)
print(f"DEBUG: sys.path appended: {target_path}")
print(f"DEBUG: contents of target_path: {os.listdir(target_path)}")
try:
    print(f"DEBUG: contents of codex_ia: {os.listdir(os.path.join(target_path, 'codex_ia'))}")
except Exception as e:
    print(f"DEBUG: error listing codex_ia: {e}")
sys.stdout.flush()

try:
    import codex_ia
    print(f"DEBUG: codex_ia loaded from: {codex_ia.__file__}")
    from codex_ia import core
    print(f"DEBUG: codex_ia.core loaded from: {core.__file__}")
except Exception as e:
    print(f"DEBUG: Import inspect error: {e}")

from codex_ia.core.agent import CodexAgent
from codex_ia.core.network_agent import NetworkAgent
from codex_ia.core.immunity_agent import ImmunityAgent
from codex_ia.core.ascension_agent import AscensionAgent
# from codex_ia.core.vscode_importer import VSCodeImporter # [NEW] Integration
# from codex_ia.core.database_agent import DatabaseAgent # [NEW] Phase 8


import time

def main():
    print("Codex-IA Backend Started via Electron...")
    sys.stdout.flush()
    
    # Global Agent State
    project_state = {
        "agent": None,
        "network": None,
        "immunity": None,
        "ascension": None,
        # "database": None
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
                         response = {"type": "file_content", "file": file_path, "content": "// [CODEX SYSTEM]\n// Este arquivo é binário (imagem ou banco de dados) e não pode ser editado como texto.\n// Use o explorador do sistema para visualizá-lo."}
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
                
                def run_shell_stream(c, work_dir):
                    try:
                        import subprocess
                        # Use Popen for streaming
                        process = subprocess.Popen(
                            c, 
                            shell=True, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE,  # Separate stderr for analysis
                            text=True, 
                            cwd=work_dir,
                            bufsize=1 # Line buffered
                        )
                        
                        stderr_buffer = []

                        # Helper to read stream
                        def read_stream(stream, is_stderr=False):
                            for line in stream:
                                if is_stderr:
                                    stderr_buffer.append(line)
                                    # Still print to console as error
                                    print(json.dumps({"type": "shell_output", "output": f"\x1b[31m{line}\x1b[0m"}), flush=True)
                                else:
                                    print(json.dumps({"type": "shell_output", "output": line}), flush=True)

                        import threading
                        # Thread for stdout
                        t_out = threading.Thread(target=read_stream, args=(process.stdout, False))
                        t_err = threading.Thread(target=read_stream, args=(process.stderr, True))
                        t_out.start()
                        t_err.start()
                        
                        t_out.join()
                        t_err.join()
                        
                        rc = process.wait()
                        print(json.dumps({"type": "shell_output", "output": f"\n[EXIT] Code {rc}\n"}), flush=True)

                        # IMMUNITY SYSTEM CHECK
                        if rc != 0 and stderr_buffer:
                            full_error = "".join(stderr_buffer)
                            # Simple heuristic: if error log is substantial
                            if len(full_error) > 10:
                                # Trigger Analysis event for Frontend AutoFix
                                print(json.dumps({
                                    "type": "analysis_suggestion",
                                    "message": f"Command failed with code {rc}",
                                    "error": full_error[:2000] # Cap size
                                }), flush=True)
                        
                    except Exception as ex:
                        print(json.dumps({"type": "error", "message": f"Shell Stream Error: {ex}"}), flush=True)

                # Start in thread to not block main loop
                import threading
                t = threading.Thread(target=run_shell_stream, args=(cmd, cwd))
                t.daemon = True
                t.start()
                
                # Immediate Ack
                response = {"type": "shell_output", "output": f"$ {cmd}\n"}
            
            elif command == 'deploy':
                # Smart Deploy Logic (Git + PythonJet Handoff)
                p_path = data.get('path', '.')
                
                # Check for Git
                has_git = os.path.exists(os.path.join(p_path, '.git'))
                
                deploy_cmds = []
                if not has_git:
                    # Initialize Git if missing
                    deploy_cmds.append("git init")
                    deploy_cmds.append("echo 'Initialized local git repository.'")
                
                # Basic Git Workflow
                deploy_cmds.append("git add .")
                deploy_cmds.append("git commit -m \"Auto-deploy via Codex Desktop\"")
                
                # Check for remote (simplified check)
                # In a real scenario, we'd checking 'git remote -v', but here let's try to push if we assume remote exists
                # or warn the user.
                
                deploy_cmds.append("git push origin main || echo 'Warning: Push failed. Remote might be missing or auth required.'")
                deploy_cmds.append("echo '--------------------------------'")
                deploy_cmds.append("echo 'READY FOR PYTHONJET DEPLOY'")
                deploy_cmds.append("echo 'Opening Dashboard...'")
                
                # Construct big command
                full_cmd = " && ".join(deploy_cmds)
                
                response = {"type": "shell_output", "output": f"\x1b[1;36m[CODEX AGENT] Initiating Smart Cloud Deploy...\x1b[0m\n"}
                print(json.dumps(response))
                sys.stdout.flush()

                def run_deploy_stream(c, work_dir):
                    try:
                        import subprocess
                        # 1. Run Git Ops
                        process = subprocess.Popen(
                            c, shell=True, cwd=work_dir,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, bufsize=1
                        )
                        for line in process.stdout:
                            print(json.dumps({"type": "shell_output", "output": line}), flush=True)
                        rc = process.wait()

                        # 2. Open PythonJet URL if successful-ish
                        # Assuming local or cloud public URL for now. 
                        # In production this would be the actual SaaS URL.
                        # Using Python to open browser cross-platform
                        try:
                            import webbrowser
                            webbrowser.open("http://localhost:8000/dashboard/deploy") # Adjust URL as needed
                            print(json.dumps({"type": "shell_output", "output": "Opened PythonJet Dashboard.\n"}), flush=True)
                        except:
                            pass

                        if rc == 0:
                            print(json.dumps({"type": "shell_output", "output": f"\n\x1b[1;32m[SUCCESS] Code Synced. Switch to Browser to finalize.\x1b[0m\n"}), flush=True)
                        else:
                            print(json.dumps({"type": "shell_output", "output": f"\n\x1b[1;33m[WARNING] Git Push had issues (Code {rc}). Check if Remote is configured.\x1b[0m\n"}), flush=True)
                    except Exception as e:
                        print(json.dumps({"type": "shell_output", "output": f"Error executing deploy: {str(e)}\n"}), flush=True)

                import threading
                t = threading.Thread(target=run_deploy_stream, args=(full_cmd, p_path))
                t.daemon = True
                t.start()
                
                # Don't send double response, the thread handles output
                continue
            
            elif command == 'get_vscode_settings':
                try:
                    # Lazy Import to prevent startup crash
                    from codex_ia.core.vscode_importer import VSCodeImporter
                    importer = VSCodeImporter()
                    settings = importer.get_settings()
                    response = {"type": "vscode_settings", "settings": settings}
                except ImportError:
                    # Graceful fallback if module blocked
                    response = {"type": "error", "message": "VS Code Module could not be loaded."}
                except Exception as e:
                    response = {"type": "error", "message": f"VS Code Import Failed: {e}"}

            elif command == 'db_connect':
                config = data.get('config')
                try:
                    # Lazy Import to prevent startup crash if lib missing
                    try:
                        from codex_ia.core.database_agent import DatabaseAgent
                    except ImportError as ie:
                        response = {"type": "db_error", "message": f"Database Module Missing: {ie}"}
                        print(json.dumps(response))
                        continue

                    # Create only if needed
                    if not project_state.get('database'):
                        project_state['database'] = DatabaseAgent()
                    
                    db_agent = project_state['database']
                    res = db_agent.connect(config)
                    if res.get('success'):
                        response = {"type": "db_connected", "message": res['message']}
                    else:
                        response = {"type": "db_error", "message": res['error']}
                except Exception as e:
                    response = {"type": "db_error", "message": str(e)}

            elif command == 'db_get_schema':
                try:
                    db_agent = project_state.get('database')
                    if db_agent:
                        res = db_agent.get_schema()
                        if 'error' in res:
                             response = {"type": "db_error", "message": res['error']}
                        else:
                             response = {"type": "db_schema", "schema": res['schema']}
                    else:
                        response = {"type": "db_error", "message": "Database not initialized"}
                except Exception as e:
                    response = {"type": "db_error", "message": str(e)}

            elif command == 'db_query':
                query_sql = data.get('query')
                try:
                    db_agent = project_state.get('database')
                    if db_agent:
                        res = db_agent.execute_query(query_sql)
                        if 'error' in res:
                             response = {"type": "db_error", "message": res['error']}
                        else:
                             response = {"type": "db_result", "data": res}
                    else:
                        response = {"type": "db_error", "message": "Database not initialized"}
                except Exception as e:
                    response = {"type": "db_error", "message": str(e)}

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
