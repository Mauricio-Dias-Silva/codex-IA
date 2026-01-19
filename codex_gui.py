import traceback

# Global Exception Logging for Debugging
def log_startup_error(msg):
    with open("startup_error.txt", "a") as f:
        f.write(msg + "\n")

try:
    import flet as ft
    import os
    import sys
    import threading
    import time
    from dotenv import load_dotenv
    
    # Ensure we can import codex_ia
    sys.path.append(os.getcwd())
    
    # Try importing critical libs immediately to catch missing deps
    try:
        import google.generativeai
        import rich
    except ImportError as e:
        log_startup_error(f"CRITICAL: Missing dependency: {e}")

except Exception as e:
    log_startup_error(f"Error during imports: {traceback.format_exc()}")

class CodexIDE:
    def __init__(self, page: ft.Page):
        try:
            self.page = page
            self.setup_page()
            
            # State
            self.agent = None
            self.current_project_dir = os.getcwd() 
            self.selected_file_path = None
            
            # UI Components
            self.build_ui()
            
            # Init Agent
            self.init_agent(self.current_project_dir)
        except Exception as e:
            self.page.add(ft.Text(f"Startup Error: {e}", color="red"))
            log_startup_error(f"Error in CodexIDE.__init__: {traceback.format_exc()}")

    def setup_page(self):
        self.page.title = "Codex-IA IDE (Phase 6: Omnipresence)"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 0
        self.page.bgcolor = "#111214"
        self.page.window_min_width = 800
        self.page.window_min_height = 600
        self.page.window_frameless = False
        self.page.window_title_bar_hidden = False
        # self.page.window_center() # Deprecated in newer Flet versions

    def init_agent(self, path):
        """Initializes or Re-initializes the Agent for a specific path."""
        def worker():
            try:
                self.add_log(f"🔄 Loading Project: {path}...", "blue")
                load_dotenv(os.path.join(path, ".env")) # Load project specific env
                from codex_ia.core.agent import CodexAgent
                self.agent = CodexAgent(project_dir=path)
                
                # [PHASE 5] Initialize Vector Memory 🧠
                try:
                    from codex_ia.core.vector_store import CodexVectorStore
                    self.add_log("🧠 Initializing Neural Memory...", "purple")
                    self.vector_store = CodexVectorStore(persistence_path=os.path.join(path, ".codex_memory"))
                    
                    # Auto-Index in background (Optimized)
                    self.index_project(path)
                except Exception as ve:
                    self.add_log(f"Memory Init Failed: {ve}", "orange")
                    self.vector_store = None

                self.current_project_dir = path
                self.refresh_file_list()
                self.add_log("✅ Project Loaded Successfully.", "green")
                self.update_title()
            except Exception as e:
                self.add_log(f"❌ Error loading project: {e}", "red")
        
        threading.Thread(target=worker, daemon=True).start()
        
        # [PHASE 6] The Sentinel 👁️
        self.init_sentinel(path)

    def init_sentinel(self, path):
        """Starts the real-time watchdog."""
        def on_file_change(file_path):
            filename = os.path.basename(file_path)
            self.add_log(f"👁️ Sentinel saw change: {filename}", "cyan")
            
            # Auto-Reindex Single File in Background
            def reindex():
                if self.vector_store:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Use relative path as key if possible, or filename
                            # ideally we want consistent keys. For now using filename to match index_project
                            self.vector_store.index_file(filename, content)
                            self.add_log(f"🧠 Updated Memory: {filename}", "purple")
                    except Exception as e:
                        print(f"Re-index failed: {e}")
            
            threading.Thread(target=reindex, daemon=True).start()

        try:
            from codex_ia.core.sentinel import Sentinel
            # Stop previous if exists
            if hasattr(self, 'sentinel') and self.sentinel:
                self.sentinel.stop()
            
            self.sentinel = Sentinel(path, on_file_change)
            self.sentinel.start()
            self.add_log("👁️ Sentinel Active (Watchdog)", "cyan")
        except Exception as e:
            self.add_log(f"Sentinel Error: {e}", "red")

    def index_project(self, path):
        """Background indexing of files."""
        def index_worker():
            if not self.vector_store: return
            count = 0
            for root, dirs, files in os.walk(path):
                if ".git" in root or "__pycache__" in root or "venv" in root: continue
                for f in files:
                    if f.endswith(('.py', '.md', '.html', '.css', '.js')):
                        full_path = os.path.join(root, f)
                        try:
                            with open(full_path, 'r', encoding='utf-8') as file:
                                content = file.read()
                                if len(content) < 50000: # Skip huge files
                                    self.vector_store.index_file(f, content) # Use filename as key for now or rel_path
                                    count += 1
                        except: pass
            self.add_log(f"🧠 Indexed {count} files into Neural Memory.", "purple")
            
        threading.Thread(target=index_worker, daemon=True).start()

    def update_title(self):
        self.page.title = f"Codex-IA IDE - {os.path.basename(self.current_project_dir)}"
        self.page.update()

    def build_ui(self):
        # --- Sidebar ---
        self.rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(icon="code", selected_icon="code", label="Editor"),
                ft.NavigationRailDestination(icon="chat_bubble_outline", selected_icon="chat_bubble", label="Chat"),
                ft.NavigationRailDestination(icon="rocket_launch_outlined", selected_icon="rocket_launch", label="Missions"),
                ft.NavigationRailDestination(icon="bedtime_outlined", selected_icon="bedtime", label="Night Shift"),
                # Humanity / Education
                ft.NavigationRailDestination(icon="memory", selected_icon="memory", label="IoT Lab"),
                ft.NavigationRailDestination(icon="school_outlined", selected_icon="school", label="Tutor"),
                # Business Intel
                ft.NavigationRailDestination(icon="radar", selected_icon="radar", label="The Hunter"),
                ft.NavigationRailDestination(icon="hive", selected_icon="hive", label="The Swarm"),
                ft.NavigationRailDestination(icon="groups", selected_icon="groups", label="The Council"),
                ft.NavigationRailDestination(icon="monetization_on", selected_icon="monetization_on", label="Shark Tank"),
                ft.NavigationRailDestination(icon="apps", selected_icon="apps_outage", label="Neural OS"), # [PHASE 5]
            ],
            on_change=self.nav_change,
            bgcolor="#1e1f22",
        )

        # --- Views ---
        self.editor_view = self.build_editor_view()
        self.chat_view = self.build_chat_view()
        self.mission_view = self.build_mission_view()
        self.night_view = self.build_night_view()
        # self.training_view = self.build_training_view() # Replaced by Tutor
        self.iot_view = self.build_iot_view()
        self.tutor_view = self.build_tutor_view()
        self.hunter_view = self.build_hunter_view()
        self.swarm_view = self.build_swarm_view()
        self.council_view = self.build_council_view()
        self.shark_view = self.build_shark_view()
        self.neural_view = self.build_neural_view() # [PHASE 5]
        
        # --- Footer/Log ---
        self.status_bar = ft.Text("Ready", size=12, color="grey")

        # --- Layout ---
        self.body_container = ft.Container(content=self.editor_view, expand=True)
        
        # --- Manual Path Dialog ---
        self.path_input = ft.TextField(label="Project Path", value=self.current_project_dir, width=400)
        self.path_dialog = ft.AlertDialog(
            title=ft.Text("Open Project"),
            content=self.path_input,
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: self.page.close_dialog()),
                ft.TextButton("Open", on_click=self.confirm_path)
            ],
        )

        self.page.add(
            ft.Row(
                [
                    self.rail,
                    ft.VerticalDivider(width=1, color="#2b2d31"),
                    ft.Column([
                        # Workspace Header
                        ft.Container(
                            content=ft.Row([
                                ft.Icon("folder_open", color="cyan"),
                                ft.TextButton("Open Project", on_click=lambda _: self.page.open_dialog(self.path_dialog)),
                                ft.Container(expand=True),
                                self.status_bar
                            ]),
                            padding=10,
                            bgcolor="#191a1d"
                        ),
                        ft.Divider(height=1, color="#2b2d31"),
                        self.body_container
                    ], expand=True)
                ],
                expand=True
            )
        )

    # --- Event Handlers ---

    def confirm_path(self, e):
        path = self.path_input.value
        if os.path.exists(path):
            self.init_agent(path)
            self.page.close_dialog()
        else:
            self.path_input.error_text = "Path does not exist"
            self.page.update()

    def on_folder_picked(self, e):
        # Deprecated due to build issues
        pass

    def nav_change(self, e):
        idx = e.control.selected_index
        
            
        views = [
            self.editor_view, 
            self.chat_view, 
            self.mission_view, 
            self.night_view,
            self.iot_view,
            self.tutor_view,
            self.hunter_view,
            self.swarm_view,
            self.council_view,
            self.shark_view,
            self.neural_view # Index 10
        ]
        if idx < len(views):
            self.body_container.content = views[idx]
        
        if idx == 0: self.refresh_file_list()
        self.page.update()

    def add_log(self, msg, color="white"):
        self.status_bar.value = msg
        self.status_bar.color = color
        self.page.update()

    # --- Builder Methods ---

    def build_editor_view(self):
        self.file_tree = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.code_editor = ft.TextField(
            multiline=True,
            min_lines=30,
            text_size=14,
            text_style=ft.TextStyle(font_family="Consolas"),
            border_color="transparent",
            bgcolor="#111214",
            expand=True,
            read_only=False
        )
        self.current_file_label = ft.Text("No file selected", weight="bold")
        
        def save_file(e):
            if self.selected_file_path:
                try:
                    with open(self.selected_file_path, 'w', encoding='utf-8') as f:
                        f.write(self.code_editor.value)
                    self.add_log(f"Saved {os.path.basename(self.selected_file_path)}", "green")
                except Exception as ex:
                    self.add_log(f"Error saving: {ex}", "red")

        return ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Text("Explorer", weight="bold"), 
                    ft.Divider(), 
                    ft.ElevatedButton("Refresh", on_click=lambda _: self.refresh_file_list()),
                    self.file_tree
                ], expand=True),
                width=250,
                bgcolor="#191a1d",
                padding=10
            ),
            ft.VerticalDivider(width=1),
            ft.Container(
                content=ft.Column([
                    ft.Row([self.current_file_label, ft.IconButton("save", on_click=save_file)]),
                    self.code_editor
                ], expand=True),
                expand=True,
                padding=10
            )
        ], expand=True)

    def refresh_file_list(self):
        self.file_tree.controls.clear()
        try:
            for root, dirs, files in os.walk(self.current_project_dir):
                if ".git" in root or "__pycache__" in root or "venv" in root: continue
                # Very simple flat list for PoC
                for f in files:
                    path = os.path.join(root, f)
                    rel_path = os.path.relpath(path, self.current_project_dir)
                    icons = {".py": "code", ".md": "description", ".json": "data_object"}
                    ext = os.path.splitext(f)[1]
                    
                    self.file_tree.controls.append(
                        ft.ListTile(
                            leading=ft.Icon(icons.get(ext, "insert_drive_file"), size=16),
                            title=ft.Text(rel_path, size=12),
                            dense=True,
                            on_click=lambda _, p=path: self.open_file_in_editor(p)
                        )
                    )
        except: pass
        self.page.update()

    def open_file_in_editor(self, path):
        self.selected_file_path = path
        self.current_file_label.value = os.path.basename(path)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.code_editor.value = f.read()
        except:
            self.code_editor.value = "(Binary file or error reading)"
        self.page.update()

    def build_chat_view(self):
        self.chat_history = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.chat_input = ft.TextField(hint_text="Ask Codex...", expand=True, on_submit=lambda e: self.send_chat())
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Codex Assistant", size=20, weight="bold"),
                ft.Divider(),
                self.chat_history,
                ft.Row([self.chat_input, ft.IconButton("send", on_click=lambda _: self.send_chat())])
            ]),
            padding=20, expand=True
        )

    def send_chat(self):
        msg = self.chat_input.value
        if not msg or not self.agent: return
        self.chat_input.value = ""
        
        self.chat_history.controls.append(ft.Row([ft.Container(content=ft.Text(msg), bgcolor="#2b2d31", padding=10, border_radius=10)], alignment=ft.MainAxisAlignment.END))
        self.page.update()
        
        def worker():
            resp = self.agent.chat(msg)
            self.chat_history.controls.append(ft.Row([ft.Container(content=ft.Markdown(resp), bgcolor="#1e1f22", padding=10, border_radius=10)], alignment=ft.MainAxisAlignment.START))
            self.page.update()
        threading.Thread(target=worker, daemon=True).start()

    def build_mission_view(self):
        # Simplified Mission View
        self.mission_log = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.mission_input = ft.TextField(hint_text="Mission...", expand=True)
        
        def run_mission(_):
            m = self.mission_input.value
            self.mission_input.value = ""
            self.mission_log.controls.append(ft.Text(f"🚀 {m}", color="green"))
            self.page.update()
            def worker():
                from codex_ia.core.squad import SquadLeader
                squad = SquadLeader(self.current_project_dir)
                res = squad.assign_mission(m, apply=True, autopilot=True)
                self.mission_log.controls.append(ft.Markdown(f"### Result\n{res}"))
                self.page.update()
            threading.Thread(target=worker, daemon=True).start()

        return ft.Container(
            content=ft.Column([
                ft.Text("Squad Missions", size=20, weight="bold"),
                ft.Row([self.mission_input, ft.ElevatedButton("Dispatch", on_click=run_mission)]),
                ft.Divider(),
                self.mission_log
            ]),
            padding=20, expand=True
        )

    def build_night_view(self):
         self.night_log = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
         def run_night(_):
             self.night_log.controls.append(ft.Text("🌙 Looking for improvements...", color="purple"))
             self.page.update()
             def worker():
                 from codex_ia.core.evolution_agent import EvolutionAgent
                 evo = EvolutionAgent(self.current_project_dir)
                 for msg in evo.introspect().splitlines(): # Introspect returns string
                     self.night_log.controls.append(ft.Text(msg))
                     self.page.update()
             threading.Thread(target=worker, daemon=True).start()

         return ft.Container(content=ft.Column([ft.Text("Night Shift", size=20), ft.ElevatedButton("Start", on_click=run_night), self.night_log]), padding=20, expand=True)

    def build_iot_view(self):
        self.iot_log = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.iot_desc = ft.TextField(hint_text="Description (e.g., 'Relay on GPIO 5')", expand=True)
        self.iot_plat = ft.Dropdown(options=[ft.dropdown.Option("esp32"), ft.dropdown.Option("arduino")], value="esp32")
        
        def run_iot(_):
            d = self.iot_desc.value
            p = self.iot_plat.value
            self.iot_log.controls.append(ft.Text(f"🔌 Generating firmware for {p}...", color="cyan"))
            self.page.update()
            
            def worker():
                try:
                    from codex_ia.core.iot_agent import IoTAgent
                    iot = IoTAgent(self.current_project_dir)
                    res = iot.generate_firmware(d, p)
                    self.iot_log.controls.append(ft.Markdown(f"```cpp\n{res.get('code')}\n```"))
                    self.page.update()
                except Exception as e:
                    self.iot_log.controls.append(ft.Text(f"Error: {e}", color="red"))
                    self.page.update()
                    
            threading.Thread(target=worker, daemon=True).start()
            
        return ft.Container(content=ft.Column([
            ft.Text("IoT Architect", size=20, weight="bold"),
            ft.Row([self.iot_desc, self.iot_plat, ft.ElevatedButton("Generate", on_click=run_iot)]),
            ft.Divider(),
            self.iot_log
        ]), padding=20, expand=True)

    def build_tutor_view(self):
        self.tutor_log = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.tutor_input = ft.TextField(hint_text="What do you want to learn?", expand=True)
        
        def run_tutor(_):
            topic = self.tutor_input.value
            self.tutor_log.controls.append(ft.Text(f"📚 Preparing lesson on: {topic}...", color="pink"))
            self.page.update()
            
            def worker():
                try:
                    from codex_ia.core.tutor_agent import TutorAgent
                    tutor = TutorAgent(self.current_project_dir)
                    res = tutor.explain_concept(topic)
                    self.tutor_log.controls.append(ft.Markdown(res))
                    self.page.update()
                except Exception as e:
                    self.tutor_log.controls.append(ft.Text(f"Error: {e}", color="red"))
                    self.page.update()
            
            threading.Thread(target=worker, daemon=True).start()
            
        return ft.Container(content=ft.Column([
            ft.Text("Universal Tutor", size=20, weight="bold"),
            ft.Row([self.tutor_input, ft.ElevatedButton("Teach Me", on_click=run_tutor)]),
            ft.Divider(),
            self.tutor_log
        ]), padding=20, expand=True)

    def build_hunter_view(self):
        self.hunter_content = ft.Column(scroll=ft.ScrollMode.AUTO)
        def run_hunt(_):
            self.hunter_content.controls.clear()
            self.hunter_content.controls.append(ft.ProgressBar())
            self.page.update()
            
            def worker():
                # Import dynamically to avoid startup circular deps
                try:
                    from codex_ia.core.trend_hunter import TrendHunterAgent
                    hunter = TrendHunterAgent()
                    opps = hunter.scan_for_opportunities()
                    
                    self.hunter_content.controls.clear()
                    for opp in opps:
                        c = ft.Container(
                            content=ft.Column([
                                ft.Text(opp['title'], size=18, weight="bold", color="green"),
                                ft.Text(opp['description']),
                                ft.Row([
                                    ft.Text(f"💰 {opp['revenue']}", color="cyan"),
                                    ft.Text(f"🔥 {opp['confidence']}%", color="orange")
                                ])
                            ]),
                            bgcolor="#2b2d31", padding=15, border_radius=10, margin=5
                        )
                        self.hunter_content.controls.append(c)
                    self.page.update()
                except Exception as e:
                     self.hunter_content.controls.append(ft.Text(f"Error: {e}", color="red"))
                     self.page.update()

            threading.Thread(target=worker, daemon=True).start()

        return ft.Container(content=ft.Column([
            ft.Text("The Hunter", size=20, weight="bold"),
            ft.ElevatedButton("Scan Opportunities", on_click=run_hunt, icon="radar"),
            ft.Divider(),
            self.hunter_content
        ]), padding=20, expand=True)

    def build_swarm_view(self):
        return ft.Container(content=ft.Text("The Swarm Node - Active", size=20), padding=20, alignment=ft.Alignment(0, 0))

    def build_council_view(self):
        self.council_log = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.council_input = ft.TextField(hint_text="Topic for debate...", expand=True)

        def convene_council(_):
            topic = self.council_input.value
            if not topic: return
            self.council_input.value = ""
            self.council_log.controls.append(ft.Text(f"🗣️ Convening Council on: {topic}", color="cyan"))
            self.council_log.controls.append(ft.ProgressBar())
            self.page.update()
            
            def worker():
                try:
                    # [NEURAL LINK] Use the PythonJet Server (God Mode)
                    from codex_ia.neural_link import NeuralLink
                    
                    # Connect to Brain
                    link = NeuralLink(base_url="http://localhost:8000") # TODO: Make configurable
                    
                    if link.check_connection():
                        res = link.consult_council(topic)
                    else:
                        # Fallback to local if server down (Legacy Mode)
                        self.council_log.controls.append(ft.Text("⚠️ Server unreachable. Using local brain (Low IQ Mode)...", color="orange"))
                        if self.agent:
                            res = self.agent.llm_client.council_meeting(topic)
                        else:
                            res = "Error: No Brain available."

                    # Remove progress bar (last item)
                    if self.council_log.controls: self.council_log.controls.pop()
                    
                    self.council_log.controls.append(ft.Markdown(res))
                    self.page.update()

                except Exception as e:
                    self.council_log.controls.append(ft.Text(f"Error: {e}", color="red"))
                    self.page.update()

            threading.Thread(target=worker, daemon=True).start()

        return ft.Container(content=ft.Column([
            ft.Text("The Council of AIs", size=20, weight="bold"),
             ft.Row([self.council_input, ft.ElevatedButton("Convene", on_click=convene_council, icon="gavel")]),
            ft.Divider(),
            self.council_log
        ]), padding=20, expand=True)

    def build_shark_view(self):
         self.shark_res = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
         
         def call_shark(_):
             self.shark_res.controls.clear()
             self.shark_res.controls.append(ft.ProgressBar())
             self.page.update()
             
             def worker():
                 try:
                     from codex_ia.core.marketing_agent import MarketingAgent
                     agent = MarketingAgent(self.current_project_dir)
                     name = os.path.basename(self.current_project_dir)
                     res = agent.generate_pitch_package(name, "Auto-detected project")
                     
                     # Remove progress bar
                     if self.shark_res.controls: self.shark_res.controls.clear()
                     
                     self.shark_res.controls.append(ft.Markdown(f"# Strategy for {name}\n\n" + res.get('pitch_deck', 'No pitch generated')))
                     self.page.update()
                 except Exception as e:
                     self.shark_res.controls.append(ft.Text(f"Shark Tank Error: {e}", color="red"))
                     self.page.update()

             threading.Thread(target=worker, daemon=True).start()

         return ft.Container(content=ft.Column([
            ft.Text("Shark Tank (Business Intelligence)", size=20, weight="bold"),
            ft.ElevatedButton("Generate Business Plan for Current Project", on_click=call_shark, icon="monetization_on"),
            ft.Divider(),
            self.shark_res
        ]), padding=20, expand=True)

    def build_neural_view(self):
        """
        [PHASE 5] CODEX NEURAL EXPLORER (The Shell)
        Visual file manager with HUD aesthetic.
        """
        self.neural_grid = ft.GridView(
            expand=True,
            runs_count=5,
            max_extent=150,
            child_aspect_ratio=1.0,
            spacing=10,
            run_spacing=10,
        )
        
        self.neural_search = ft.TextField(
            hint_text="Neural Search (e.g. 'Login Logic', 'Database Models')...", 
            expand=True,
            prefix_icon="search",
            border_radius=20,
            bgcolor="#2b2d31",
            on_change=self.filter_neural_grid
        )
        
        # Voice Controls
        self.mic_button = ft.IconButton(
            icon="mic", 
            icon_color="cyan", 
            icon_size=30,
            tooltip="Activate Voice Command (Jarvis)",
            on_click=self.toggle_voice_input
        )
        
        # Initial Load
        self.load_neural_grid()

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon("apps", size=30, color="cyan"),
                    ft.Text("SYSTEM OVERRIDE: NEURAL EXPLORER", size=20, weight="bold", font_family="Consolas"),
                    ft.Container(expand=True),
                    self.mic_button
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=20),
                self.neural_search,
                ft.Divider(color="cyan"),
                self.neural_grid
            ]),
            padding=30,
            expand=True,
            bgcolor="#0a0a0c", # Darker "Void" background
            # image_src="", # Could add a cool HUD background image here later
            border=ft.border.all(1, "cyan"),
            border_radius=10
        )

    def toggle_voice_input(self, e):
        """Activates the Voice Agent."""
        if not hasattr(self, 'voice_agent'):
            try:
                from codex_ia.core.voice_agent import VoiceAgent
                self.voice_agent = VoiceAgent()
                self.add_log("🎙️ Voice System Initialized", "cyan")
            except Exception as ex:
                self.add_log(f"❌ Voice Init Failed: {ex}", "red")
                return

        def listen_loop():
            self.mic_button.icon_color = "red"
            self.mic_button.tooltip = "Listening..."
            self.page.update()
            
            self.voice_agent.speak("Aguardando comando.")
            cmd = self.voice_agent.listen()
            
            self.mic_button.icon_color = "cyan"
            self.mic_button.tooltip = "Activate Voice Command"
            self.page.update()
            
            if cmd:
                self.add_log(f"🗣️ Heard: {cmd}", "green")
                self.process_voice_command(cmd)
            else:
                 self.voice_agent.speak("Não ouvi nada.")

        threading.Thread(target=listen_loop, daemon=True).start()

    def process_voice_command(self, cmd):
        """Interprets voice commands."""
        cmd = cmd.lower()
        if "procurar" in cmd or "buscar" in cmd or "search" in cmd:
            term = cmd.replace("procurar", "").replace("buscar", "").replace("search", "").strip()
            self.neural_search.value = term
            self.filter_neural_grid(None) # Trigger filter
            self.voice_agent.speak(f"Filtrando por {term}")
            self.page.update()
        elif "status" in cmd:
            self.voice_agent.speak("Todos os sistemas operacionais. Nível de inteligência estável.")
        else:
            self.voice_agent.speak("Comando não reconhecido.")

    def filter_neural_grid(self, e):
        self.load_neural_grid(self.neural_search.value)

    def load_neural_grid(self, query=""):
        self.neural_grid.controls.clear()
        try:
            # Gather all files
            all_files = []
            for root, dirs, files in os.walk(self.current_project_dir):
                if ".git" in root or "__pycache__" in root or "venv" in root or "node_modules" in root: continue
                for f in files:
                    full_path = os.path.join(root, f)
                    rel_path = os.path.relpath(full_path, self.current_project_dir)
                    all_files.append((f, rel_path, full_path))
            
            # Filter (Simple fuzzy for now)
            filtered = []
            if query:
                q = query.lower()
                filtered = [item for item in all_files if q in item[0].lower() or q in item[1].lower()]
            else:
                filtered = all_files

            # Create Cards
            for fname, rel_path, full_path in filtered:
                ext = os.path.splitext(fname)[1].lower()
                
                # Icon Logic
                icon = "insert_drive_file"
                color = "white"
                if ext == ".py": icon, color = "code", "blue"
                elif ext == ".md": icon, color = "description", "yellow"
                elif ext == ".json": icon, color = "data_object", "orange"
                elif ext in [".html", ".css", ".js"]: icon, color = "public", "pink"
                
                card = ft.Container(
                    content=ft.Column([
                        ft.Icon(icon, color=color, size=40),
                        ft.Text(fname, weight="bold", size=12, no_wrap=True, text_align="center"),
                        ft.Text(rel_path, size=10, color="grey", no_wrap=True, text_align="center")
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                    bgcolor="#1e1f22",
                    padding=10,
                    border_radius=10,
                    on_click=lambda _, p=full_path: self.open_file_in_editor(p),
                    tooltip=rel_path
                )
                self.neural_grid.controls.append(card)
                
        except Exception as e:
            self.neural_grid.controls.append(ft.Text(f"Error loading grid: {e}", color="red"))
        
        self.page.update()

        if not query:
            # Already loaded everything above (lines 682-726) if query was empty
            # But wait, lines 694-699 filtered by query. If query is empty, filtered is all_files.
            # So the grid is already populated with all files. We don't need to do anything here.
            pass

        # Semantic Search 🧠
        elif self.vector_store and len(query) > 3:
            hits = self.vector_store.semantic_search(query)
            if hits:
                self.neural_grid.controls.clear()
                for hit in hits:
                    fname = os.path.basename(hit['path'])
                    full_path = os.path.join(self.current_project_dir, hit['path'])
                    
                    icon = "bolt"
                    color = "yellow"
                    
                    card = ft.Container(
                        content=ft.Column([
                            ft.Icon(icon, color=color, size=40),
                            ft.Text(fname, weight="bold", size=12, no_wrap=True, text_align="center"),
                            ft.Text(f"Match: {round(hit['score'], 2)}", size=10, color="green", no_wrap=True)
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                        bgcolor="#2b2d31",
                        padding=10,
                        border_radius=10,
                        on_click=lambda _, p=full_path: self.open_file_in_editor(p),
                        border=ft.border.all(1, "yellow")
                    )
                    self.neural_grid.controls.append(card)
                self.page.update()
        
        # If query exists but we didn't use semantic search (len <= 3 or no hits), 
        # the code at the top (lines 694-699) already handled the fuzzy filtering.
        # So we don't need to call self.load_neural_grid(query) again recursively.

def main(page: ft.Page):
    CodexIDE(page)

if __name__ == "__main__":
    ft.app(main)
