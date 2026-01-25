import traceback

# Global Exception Logging for Debugging
def log_startup_error(msg):
    with open("startup_error.txt", "a") as f:
        f.write(msg + "\n")

import flet as ft
import os
import sys
import threading
import time
from dotenv import load_dotenv
from fpdf import FPDF
import datetime

# Ensure we can import codex_ia
sys.path.append(os.getcwd())

# Try importing critical libs immediately to catch missing deps
try:
    import google.generativeai
    import rich
except ImportError as e:
    log_startup_error(f"CRITICAL: Missing dependency: {e}")

class CodexIDE:
    def __init__(self, page: ft.Page):
        try:
            self.page = page
            self.setup_page()
            
            # State
            self.agent = None
            self.current_project_dir = os.getcwd() 
            self.selected_file_path = None
            self.vector_store = None
            
            # [PHASE 2] Voice Command State 🎙️
            self.is_listening = False
            self.mic_button = ft.IconButton(
                icon="mic_off", 
                icon_color="grey", 
                tooltip="Toggle Voice Command (Protocol Jarvis)",
                on_click=self.toggle_voice_mode
            )
            
            # Health Indicators
            self.health_icons = {
                "gemini": ft.Icon("cloud", color="grey", size=16, tooltip="Gemini (Cloud) Status"),
                "ollama": ft.Icon("computer", color="grey", size=16, tooltip="Ollama (Local) Status"),
                "groq": ft.Icon("bolt", color="grey", size=16, tooltip="Groq Status")
            }
            
            # [PHASE 3] Sentinel Alerts
            self.sentinel_alerts = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

            # UI Components
            self.build_ui()
            self.page.update()
            
            # Init Agent
            self.init_agent(self.current_project_dir)
            self.start_health_monitor()
            self.page.update()
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
            time.sleep(2) # Give UI time to render first
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
                        
                        # 1. Update Memory
                        self.vector_store.index_file(filename, content)
                        self.add_log(f"🧠 Updated Memory: {filename}", "purple")
                        
                        # 2. [PHASE 3] Proactive Bug Check (Local LLM)
                        if self.agent:
                            analysis = self.agent.analyze_file_change(file_path, content)
                            if analysis:
                                self.sentinel_alerts.controls.insert(0, ft.Container(
                                    content=ft.Column([
                                        ft.Text(f"👁️ {filename}", weight="bold", color="cyan"),
                                        ft.Markdown(analysis)
                                    ]),
                                    bgcolor="#2b2d31", padding=10, border_radius=5, margin=5
                                ))
                                self.page.update()
                    except Exception as e:
                        print(f"Sentinel processing failed: {e}")
            
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
                if any(x in root.lower() for x in [".git", "__pycache__", "venv", "node_modules", "static", "staticfiles", "dist", "build", "assets"]): continue
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
        # --- Core Controls ---
        # self.file_picker = ft.FilePicker()
        # self.page.overlay.append(self.file_picker)

        # --- Sidebar ---
        self.rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(icon="code", label="Editor"),
                ft.NavigationRailDestination(icon="chat", label="Chat"),
                ft.NavigationRailDestination(icon="rocket", label="Missions"),
                ft.NavigationRailDestination(icon="memory", label="IoT"),
                ft.NavigationRailDestination(icon="apps", label="Neural"),
                ft.NavigationRailDestination(icon="healing", label="Debug"),
            ],
            on_change=self.nav_change,
            bgcolor="#1e1f22",
        )

        # --- Views ---
        self.editor_view = self.build_editor_view()
        self.chat_view = self.build_chat_view()
        self.mission_view = self.build_mission_view()
        self.night_view = self.build_night_view()
        self.iot_view = self.build_iot_view()
        self.tutor_view = self.build_tutor_view()
        self.hunter_view = self.build_hunter_view()
        self.swarm_view = self.build_swarm_view()
        self.council_view = self.build_council_view()
        self.shark_view = self.build_shark_view()
        self.neural_view = self.build_neural_view()
        self.debug_view = self.build_debug_view() # [PHASE 3]
        
        # --- Footer/Log ---
        self.status_bar = ft.Text("Ready", size=12, color="grey")

        # --- Main Layout Container ---
        # This container holds the active view (Editor, Chat, etc.)
        self.body_container = ft.Container(
            content=self.editor_view, 
            expand=True, 
            bgcolor="#111214",
            padding=5
        )
        
        # --- Manual Path Dialog ---
        self.path_input = ft.TextField(label="Project Path", value=self.current_project_dir, width=400)
        self.path_dialog = ft.AlertDialog(
            title=ft.Text("Open Project"),
            content=self.path_input,
            actions=[
                ft.TextButton(content=ft.Text("Cancel"), on_click=lambda _: self.page.close_dialog()),
                ft.TextButton(content=ft.Text("Open"), on_click=self.confirm_path)
            ],
        )

        # --- FINAL LAYOUT CONSTRUCTION ---
        # Using a simple Row to divide Sidebar from Main Content
        self.page.add(
            ft.Row(
                [
                    # Col 1: Sidebar
                    ft.Container(content=self.rail, width=100, bgcolor="#1e1f22"),
                    
                    # Col 2: Main Application Area
                    ft.Container(
                        content=ft.Column([
                            # Header
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon("folder", color="cyan"),
                                    ft.TextButton(content=ft.Text("Open Project", color="cyan"), on_click=lambda _: self.page.open_dialog(self.path_dialog)),
                                    ft.Container(expand=True),
                                    self.status_bar
                                ]),
                                padding=5,
                                height=40,
                                bgcolor="#191a1d"
                            ),
                            # Active View
                            self.body_container
                        ], spacing=0, expand=True),
                        expand=True 
                    )
                ],
                expand=True,
                spacing=0
            )
        )
        
        # Force initial view update
        self.nav_change(None)
        self.page.update()

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
        # Initial call (e=None) or interaction change
        idx = self.rail.selected_index if e is None else e.control.selected_index
        
        # Simplified mapping (Step 368)
        views = {
            0: self.editor_view,
            1: self.chat_view,
            2: self.mission_view,
            3: self.iot_view,
            4: self.neural_view,
            5: self.debug_view
        }
        
        if idx in views:
            self.body_container.content = views[idx]
        
        if idx == 0: self.refresh_file_list()
        
        try:
            self.page.update()
        except:
            pass

    def add_log(self, msg, color="white"):
        self.status_bar.value = msg
        self.status_bar.color = color
        self.page.update()

    def start_health_monitor(self):
        """Starts a background thread to check AI provider health."""
        def monitor():
            while True:
                if self.agent and hasattr(self.agent.llm_client, "check_all_health"):
                    try:
                        status = self.agent.llm_client.check_all_health()
                        for name, is_healthy in status.items():
                            if name in self.health_icons:
                                self.health_icons[name].color = "green" if is_healthy else "red"
                        self.page.update()
                    except Exception as e:
                        print(f"Health monitor error: {e}")
                time.sleep(15) # Check every 15 seconds
        
        threading.Thread(target=monitor, daemon=True).start()

    # --- Builder Methods ---

    def build_editor_view(self):
        # 1. File Explorer
        self.file_tree = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        
        # 2. Code Editor
        self.code_editor = ft.TextField(
            multiline=True,
            min_lines=30,
            text_size=14, 
            text_style=ft.TextStyle(font_family="Consolas"),
            color="white",
            border_color="transparent",
            bgcolor="#111214",
            expand=True,
            read_only=False,
            value="Welcome to Codex-IA.\nSelect a file from the explorer to begin."
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

        # 3. Assemble Editor View (Row: Explorer | Editor)
        return ft.Row(
            [
                # Col 1: Explorer
                ft.Container(
                    content=ft.Column([
                        ft.Text("Explorer", weight="bold"), 
                        ft.Divider(height=1, color="#333"), 
                    ft.ElevatedButton(content=ft.Text("Refresh"), on_click=lambda _: self.refresh_file_list(), height=30),
                        self.file_tree
                    ], spacing=5, expand=True),
                    width=250,
                    bgcolor="#191a1d",
                    padding=10
                ),
                # Col 2: Editor
                ft.Container(
                    content=ft.Column([
                        ft.Row([self.current_file_label, ft.Container(content=ft.Icon("save"), on_click=save_file, padding=5, tooltip="Save")]),
                        self.code_editor
                    ], spacing=5, expand=True),
                    expand=True,
                    padding=10,
                    bgcolor="#111214"
                )
            ],
            expand=True,
            spacing=2 
        )

    def refresh_file_list(self):
        self.file_tree.controls.clear()
        try:
            items_found = 0
            for root, dirs, files in os.walk(self.current_project_dir):
                if any(x in root.lower() for x in [".git", "__pycache__", "venv", "node_modules", "static", "staticfiles", "dist", "build", "assets"]): continue
                for f in files:
                    items_found += 1
                    path = os.path.join(root, f)
                    rel_path = os.path.relpath(path, self.current_project_dir)
                    icons = {".py": "code", ".md": "description", ".json": "data_object"}
                    ext = os.path.splitext(f)[1]
                    
                    self.file_tree.controls.append(
                        ft.TextButton(
                            content=ft.Text(f"📄 {rel_path}", color="white"),
                            on_click=lambda _, p=path: self.open_file_in_editor(p)
                        )
                    )
            if items_found == 0:
                 self.file_tree.controls.append(ft.Text("No files found in: " + self.current_project_dir, color="red"))
        except Exception as e:
             self.file_tree.controls.append(ft.Text(f"Error listing files: {e}", color="red"))
             print(f"File List Error: {e}")
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
        
        # [OPTIMIZATION] Vision Lab 👁️
        self.selected_image_path = None
        self.image_preview = ft.Container(visible=False)
        
        def clear_image(e):
            self.selected_image_path = None
            self.image_preview.visible = False
            self.page.update()

        def on_image_picked(e):
            if e.files and len(e.files) > 0:
                self.selected_image_path = e.files[0].path
                self.image_preview.content = ft.Row([
                    ft.Icon("image", color="cyan"), 
                    ft.Text(f"Attached: {e.files[0].name}", color="cyan", size=12),
                    ft.IconButton(icon="close", icon_size=14, on_click=clear_image)
                ], alignment=ft.MainAxisAlignment.START)
                self.image_preview.visible = True
                self.add_log(f"👁️ Vision Ready: {e.files[0].name}", "cyan")
                self.page.update()

        # self.file_picker.on_result = on_image_picked


        # [OPTIMIZATION] Brain Selector 🧠
        self.brain_selector = ft.Dropdown(
            options=[
                ft.dropdown.Option("auto", "Brain Router (Auto)"),
                ft.dropdown.Option("gemini", "Gemini 1.5 (Cloud)"),
                ft.dropdown.Option("ollama", "Ollama (Local - 0 Custo)"),
                ft.dropdown.Option("groq", "Groq (High Speed)"),
            ],
            value="auto",
            width=200,
            height=40,
            text_size=12
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Codex Assistant", size=20, weight="bold"),
                    ft.Container(expand=True),
                    ft.Row([
                        self.health_icons["gemini"],
                        self.health_icons["ollama"],
                        self.health_icons["groq"]
                    ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.VerticalDivider(width=20),
                    # [FEATURE] Vision Button
                    # ft.IconButton(icon="add_a_photo", tooltip="Attach Image (Codex Vision)", on_click=lambda _: self.file_picker.pick_files(allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE)),
                    
                    # [FEATURE] Voice Command (Jarvis) 🎙️
                    self.mic_button,

                    self.brain_selector,
                    ft.IconButton(icon="picture_as_pdf", icon_color="red", tooltip="Export Chat to PDF", on_click=self.export_chat_to_pdf)
                ]),
                ft.Divider(),
                ft.Row([
                    # Col 1: Chat Main
                    ft.Column([
                        self.chat_history,
                        self.image_preview, # Show attached image indicator above input
                        ft.Row([self.chat_input, ft.Container(content=ft.Icon("send"), on_click=lambda _: self.send_chat(), padding=5, tooltip="Send")])
                    ], expand=3),
                    
                    # Col 2: Sentinel Alerts (Phase 3)
                    ft.VerticalDivider(width=1),
                    ft.Column([
                        ft.Text("Sentinel Alerts 👁️", weight="bold", size=14, color="cyan"),
                        self.sentinel_alerts,
                        ft.ElevatedButton(content=ft.Text("Clear Alerts"), on_click=lambda _: (self.sentinel_alerts.controls.clear(), self.page.update()))
                    ], expand=1)
                ], expand=True)
            ]),
            padding=20, expand=True
        )

    def toggle_voice_mode(self, e):
        """Activates/Deactivates Jarvis Mode."""
        if self.is_listening:
            self.is_listening = False
            self.mic_button.icon = "mic_off"
            self.mic_button.icon_color = "grey"
            self.add_log("🔇 Voice Mode Deactivated", "grey")
        else:
            self.is_listening = True
            self.mic_button.icon = "mic"
            self.mic_button.icon_color = "red"
            self.add_log("🎙️ Jarvis is listening...", "red")
            threading.Thread(target=self.listen_loop, daemon=True).start()
        self.page.update()

    def listen_loop(self):
        """Background listener for Voice Commands."""
        try:
            import speech_recognition as sr
            r = sr.Recognizer()
            
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                
                while self.is_listening:
                    try:
                        # Listen for a moment
                        audio = r.listen(source, timeout=5, phrase_time_limit=10)
                        
                        # Transcribe
                        text = r.recognize_google(audio, language="pt-BR")
                        
                        if text:
                            text = text.lower()
                            self.add_log(f"🗣️ Heard: {text}", "cyan")
                            
                            # Auto-send to chat
                            self.chat_input.value = text
                            self.send_chat()
                            
                    except sr.WaitTimeoutError:
                        pass # Just silence
                    except sr.UnknownValueError:
                        pass # Noise
                    except Exception as e:
                        print(f"Voice Error: {e}")
                        if not self.is_listening: break
        except ImportError:
            self.add_log("❌ Install 'SpeechRecognition' and 'pyaudio'", "red")
            self.is_listening = False
            self.mic_button.icon = "mic_off"
            self.page.update()
        except Exception as ex:
             self.add_log(f"Microphone Error: {ex}", "red")
             self.is_listening = False
             self.mic_button.icon = "mic_off"
             self.page.update()
    
    def export_chat_to_pdf(self, e):
        if not self.chat_history.controls:
            self.add_log("⚠️ Nothing to export.", "orange")
            return

        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            # Use core font that supports some accents (Arial/Helvetica is standard)
            pdf.set_font("Helvetica", size=12)
            
            pdf.set_font("Helvetica", "B", 16)
            pdf.cell(0, 10, txt="Codex-IA Chat Export", new_x="LMARGIN", new_y="NEXT", align='C')
            pdf.set_font("Helvetica", "I", 10)
            pdf.cell(0, 10, txt=f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", new_x="LMARGIN", new_y="NEXT", align='C')
            pdf.ln(5)
            
            for row in self.chat_history.controls:
                if not isinstance(row, ft.Row): continue
                
                sender = "Unknown"
                text = ""
                
                try:
                    container = row.controls[0]
                    content_control = container.content
                    
                    if row.alignment == ft.MainAxisAlignment.END:
                        sender = "USER"
                        if isinstance(content_control, ft.Text):
                            text = content_control.value
                    else:
                        sender = "CODEX-IA"
                        if isinstance(content_control, ft.Markdown):
                            text = content_control.value
                    
                    if text:
                        # Normalize text to Latin-1 range to avoid crashes with standard fonts
                        # Replace unsupported chars with ?
                        text = text.encode('latin-1', 'replace').decode('latin-1')
                        
                        if sender == "USER":
                            pdf.set_text_color(0, 0, 255) # Blue
                            pdf.set_font("Helvetica", "B", 11)
                            pdf.multi_cell(0, 7, f"You: {text}", new_x="LMARGIN", new_y="NEXT", align='R')
                        else:
                            pdf.set_text_color(0, 0, 0) # Black
                            pdf.set_font("Helvetica", "", 11)
                            pdf.multi_cell(0, 7, f"Codex: {text}", new_x="LMARGIN", new_y="NEXT", align='L')
                        
                        pdf.ln(2)
                except Exception as ex:
                   print(f"Row parse error: {ex}")

            filename = f"chat_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf.output(filename)
            self.add_log(f"✅ Chat exported to {filename}", "green")
            os.startfile(filename) 
            
        except Exception as ex:
            self.add_log(f"❌ Export failed: {ex}", "red")
            print(traceback.format_exc())

    def send_chat(self):
        msg = self.chat_input.value
        # Allow sending if there is an image, even if msg is empty (captioning)
        if (not msg and not self.selected_image_path) or not self.agent: return
        
        self.chat_input.value = ""
        
        # Get selected brain
        selected_brain = self.brain_selector.value
        use_fallback = (selected_brain == "auto")
        
        # Capture current image if any
        current_image = self.selected_image_path
        
        # UI Feedback for Image
        user_content = [ft.Text(msg)]
        if current_image:
             user_content.insert(0, ft.Container(
                 content=ft.Row([ft.Icon("image", color="cyan"), ft.Text("Image Attached", italic=True, size=12)]),
                 margin=ft.margin.only(bottom=5)
             ))

        # If not auto, set the active brain in the router
        if not use_fallback:
            self.agent.llm_client.active_brain = selected_brain

        self.chat_history.controls.append(ft.Row([ft.Container(content=ft.Column(user_content), bgcolor="#2b2d31", padding=10, border_radius=10)], alignment=ft.MainAxisAlignment.END))
        self.page.update()
        
        # Clear image selection from UI immediately
        if self.selected_image_path:
             self.selected_image_path = None
             self.image_preview.visible = False
             self.page.update()
        
        # [MEMORY HOOK] User Message
        if hasattr(self, 'vector_store') and self.vector_store:
            threading.Thread(target=self.vector_store.index_chat, args=("USER", msg), daemon=True).start()
        
        def worker():
            try:
                # Pass image_path to the agent
                resp = self.agent.chat(msg, use_fallback=use_fallback, image_path=current_image)
                self.chat_history.controls.append(ft.Row([ft.Container(content=ft.Markdown(resp), bgcolor="#1e1f22", padding=10, border_radius=10)], alignment=ft.MainAxisAlignment.START))
                self.page.update()
                
                # [MEMORY HOOK] AI Response
                if hasattr(self, 'vector_store') and self.vector_store:
                    self.vector_store.index_chat("CODEX", resp)
            except Exception as e:
                self.add_log(f"Chat Error: {e}", "red")
                
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

         return ft.Container(content=ft.Column([ft.Text("Night Shift", size=20), ft.ElevatedButton(content=ft.Text("Start"), on_click=run_night), self.night_log]), padding=20, expand=True)

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

    def download_model(self, model_name):
        """Triggers ollama pull command."""
        self.iot_log.controls.append(ft.Text(f"📥 Baixando modelo: {model_name}...", color="yellow"))
        self.page.update()
        
        def pull():
            try:
                import subprocess
                process = subprocess.Popen(f"ollama pull {model_name}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                for line in process.stdout:
                    if "success" in line.lower():
                        self.iot_log.controls.append(ft.Text(f"✅ {model_name} baixado com sucesso!", color="green"))
                    elif "pulling" in line.lower():
                        # Simple progress indicator could go here
                        pass
                self.page.update()
            except Exception as e:
                self.iot_log.controls.append(ft.Text(f"Erro ao baixar: {e}", color="red"))
                self.page.update()
        
        threading.Thread(target=pull, daemon=True).start()

    def handle_clear_memory(self, e):
        """Clears the local vector database."""
        if self.vector_store:
            success = self.vector_store.clear_memory()
            if success:
                self.add_log("🧠 Neural Memory wiped successfully.", "green")
                self.iot_log.controls.append(ft.Text("🧹 Memória Neural limpa.", color="green"))
            else:
                self.add_log("❌ Failed to clear memory.", "red")
            self.page.update()

    def handle_reindex(self, e):
        """Manually triggers project reindexing."""
        if self.vector_store:
            self.add_log("🔄 Manually reindexing project...", "blue")
            self.index_project(self.current_project_dir)
            self.iot_log.controls.append(ft.Text("🔄 Reindexação iniciada...", color="blue"))
            self.page.update()
            
        return ft.Container(content=ft.Column([
            ft.Text("IoT Architect", size=20, weight="bold"),
            ft.Row([self.iot_desc, self.iot_plat, ft.ElevatedButton(content=ft.Text("Generate"), on_click=run_iot)]),
            ft.Divider(),
            ft.Text("Local Model Manager (Ollama)", size=18, weight="bold", color="yellow"),
            ft.Row([
                ft.ElevatedButton(content=ft.Text("Pull Llama 3.2 (3B)"), on_click=lambda _: self.download_model("llama3.2:3b"), icon="download"),
                ft.ElevatedButton(content=ft.Text("Pull Llama 3.2 (1B)"), on_click=lambda _: self.download_model("llama3.2:1b"), icon="download"),
                ft.ElevatedButton(content=ft.Text("Pull Qwen2.5-Coder (1.5B)"), on_click=lambda _: self.download_model("qwen2.5-coder:1.5b"), icon="download"),
            ]),
            ft.Divider(),
            ft.Text("Neural Memory Tools", size=18, weight="bold", color="purple"),
            ft.Row([
                ft.ElevatedButton(content=ft.Text("🧹 Clear Memory"), on_click=self.handle_clear_memory, color="red"),
                ft.ElevatedButton(content=ft.Text("🔄 Force Reindex"), on_click=self.handle_reindex, color="purple"),
            ]),
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
            ft.Row([self.tutor_input, ft.ElevatedButton(content=ft.Text("Teach Me"), on_click=run_tutor)]),
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
            ft.ElevatedButton(content=ft.Text("Scan Opportunities"), on_click=run_hunt, icon="radar"),
            ft.Divider(),
            self.hunter_content
        ]), padding=20, expand=True)

    def build_swarm_view(self):
        """
        [PHASE 4] The Hive Mind (Swarm Intelligence)
        """
        self.mission_input = ft.TextField(
            label="Swarm Mission Objective", 
            hint_text="Describe the complex software system you want the Swarm to build...", 
            multiline=True, 
            min_lines=3,
            text_size=14,
            border_color="cyan"
        )
        self.swarm_log = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=5)

        def deploy_swarm(e):
            if not self.swarm:
                self.swarm_log.controls.append(ft.Text("❌ Swarm not initialized (Check startup logs)", color="red"))
                self.page.update()
                return
            
            mission = self.mission_input.value
            if not mission:
                self.mission_input.error_text = "Mission cannot be empty"
                self.page.update()
                return
            
            self.mission_input.error_text = None
            self.swarm_log.controls.append(ft.Text(f"🚀 Deploying Swarm for mission: {mission}...", color="cyan", weight="bold"))
            self.page.update()
            
            def worker():
                try:
                    for sender, content in self.swarm.start_mission_iterative(mission):
                        color = "cyan" if sender == "SYSTEM" else "green" if sender == "Developer" else "red" if sender == "QA" else "orange"
                        
                        # Format message for better readability
                        if sender == "SYSTEM":
                            self.swarm_log.controls.append(ft.Text(f"{content}", color=color, italic=True))
                        else:
                            self.swarm_log.controls.append(ft.Container(
                                content=ft.Column([
                                    ft.Text(f"👤 {sender}", weight="bold", color=color),
                                    ft.Markdown(content)
                                ]),
                                bgcolor="#1e1f22",
                                padding=10,
                                border_radius=5,
                                margin=ft.margin.only(bottom=5)
                            ))
                        self.page.update()
                        
                except Exception as ex:
                    self.swarm_log.controls.append(ft.Text(f"❌ Critical Swarm Error: {ex}", color="red", weight="bold"))
                    self.page.update()

            threading.Thread(target=worker, daemon=True).start()

        return ft.Container(content=ft.Column([
            ft.Row([ft.Icon("hub", color="cyan", size=30), ft.Text("The Hive Mind (Swarm Intelligence)", size=22, weight="bold", color="cyan")]),
            ft.Text("Multi-Agent Collaboration: Architect, Developer, and QA working in unison.", size=12, color="grey"),
            ft.Divider(color="grey"),
            self.mission_input,
            ft.ElevatedButton(content=ft.Text("Deploy Swarm Agents"), on_click=deploy_swarm, icon="rocket_launch", bgcolor="pink", color="white", height=45),
            ft.Divider(),
            ft.Container(
                content=self.swarm_log, 
                bgcolor="#111111", 
                padding=15, 
                border_radius=8, 
                border=ft.border.all(1, "#333333"),
                expand=True
            )
        ]), padding=20, expand=True)

    def build_debug_view(self):
        """
        [PHASE 3] Autonomous Self-Healing UI.
        Integrates with core.auto_debugger.AutoDebugger.
        """
        self.debug_log = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.test_cmd_input = ft.TextField(label="Test Command", value="pytest", width=300)
        
        def run_self_healing(_):
            self.debug_log.controls.clear()
            self.debug_log.controls.append(ft.Text("🚑 Starting Autonomous Self-Healing Sequence...", color="orange", weight="bold"))
            self.debug_log.controls.append(ft.ProgressBar())
            self.page.update()
            
            def worker():
                try:
                    from codex_ia.core.auto_debugger import AutoDebugger
                    from pathlib import Path
                    
                    debugger = AutoDebugger(Path(self.current_project_dir))
                    
                    # Redirect print to log
                    def log_callback(msg):
                        # Clean up color codes if any
                        clean_msg = msg.replace('\033[92m', '').replace('\033[0m', '')
                        color = "green" if "✅" in msg else "red" if "❌" in msg or "⚠️" in msg else "white"
                        self.debug_log.controls.append(ft.Text(clean_msg, color=color))
                        self.page.update()
                        
                    # Inject logger (Monkey patch print for demo simplicity or use custom observer)
                    # For now we just run it and capture result
                    
                    self.debug_log.controls.append(ft.Text(f"Running tests: {self.test_cmd_input.value}...", color="cyan"))
                    self.page.update()
                    
                    result = debugger.auto_fix_loop(max_iterations=3)
                    
                    # Remove progress bar
                    if isinstance(self.debug_log.controls[-1], ft.ProgressBar):
                        self.debug_log.controls.pop()
                        
                    if result['success']:
                        self.debug_log.controls.append(ft.Text(f"✅ HEALING SUCCESSFUL! Fixed in {result['iterations']} iterations.", size=20, color="green", weight="bold"))
                    else:
                        self.debug_log.controls.append(ft.Text(f"❌ HEALING FAILED. Final status: {result['final_status']}", size=20, color="red", weight="bold"))
                        
                    # Show details
                    for fix in result['fixes_applied']:
                         with self.debug_log.controls.append(ft.ExpansionTile(
                             title=ft.Text(f"Fix for {fix['error']['type']}"),
                             controls=[
                                 ft.Markdown(f"**Diagnosis:** {fix['analysis'].get('diagnosis')}\n\n**Patch:**\n```python\n{fix['analysis'].get('code_patch')}\n```")
                             ]
                         )): pass
                    
                    self.page.update()
                    
                except Exception as e:
                    import traceback
                    self.debug_log.controls.append(ft.Text(f"Critical Error: {e}\n{traceback.format_exc()}", color="red"))
                    self.page.update()

            threading.Thread(target=worker, daemon=True).start()

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon("healing", color="red", size=30),
                    ft.Text("Autonomous Self-Healing", size=25, weight="bold")
                ]),
                ft.Text("This agent runs your tests, detects errors, and re-writes the code automatically until it passes.", italic=True, color="grey"),
                ft.Divider(),
                ft.Row([
                    self.test_cmd_input,
                    ft.ElevatedButton(content=ft.Text("START HEALING LOOP"), icon="medical_services", on_click=run_self_healing, bgcolor="red", color="white")
                ]),
                ft.Divider(),
                ft.Container(
                    content=self.debug_log,
                    bgcolor="#1a1a1a",
                    border=ft.border.all(1, "#333"),
                    border_radius=10,
                    padding=15,
                    expand=True
                )
            ]),
            padding=20,
            expand=True
        )
        def run_mission(_):
            goal = self.mission_input.value
            if not goal or not self.swarm: return
            
            self.mission_input.value = ""
            self.swarm_log.controls.append(ft.Text(f"🚀 MISSION STARTED: {goal}", weight="bold", size=16, color="yellow"))
            self.page.update()
            
            def worker():
                try:
                    # Clear previous bus state if needed or just append
                    # self.swarm.message_bus = [] 
                    
                    # Start mission in a separate thread so we can poll logs
                    mission_thread = threading.Thread(target=self.swarm.start_mission, args=(goal,), daemon=True)
                    mission_thread.start()
                    
                    last_idx = 0
                    while mission_thread.is_alive() or last_idx < len(self.swarm.message_bus):
                        current_bus = self.swarm.message_bus
                        if last_idx < len(current_bus):
                            new_msgs = current_bus[last_idx:]
                            for msg in new_msgs:
                                color = "white"
                                if "Architect" in msg: color = "cyan"
                                elif "Developer" in msg: color = "green"
                                elif "QA" in msg: color = "red"
                                
                                self.swarm_log.controls.append(ft.Text(msg, color=color, font_family="Consolas"))
                                self.page.update()
                            last_idx = len(current_bus)
                        time.sleep(0.5) # Poll rate
                    
                    self.swarm_log.controls.append(ft.Divider())
                    self.swarm_log.controls.append(ft.Text("✅ Swarm Mission Complete", color="yellow", weight="bold"))
                    self.page.update()
                except Exception as e:
                    self.swarm_log.controls.append(ft.Text(f"Swarm Error: {e}", color="red"))
                    self.page.update()

            threading.Thread(target=worker, daemon=True).start()

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon("hive", color="yellow", size=30),
                    ft.Text("The Swarm (Multi-Agent System)", size=20, weight="bold"),
                    ft.Container(expand=True),
                    ft.Chip(label="Architect: DaVinci", bgcolor="cyan"),
                    ft.Chip(label="Dev: Alan", bgcolor="green"),
                    ft.Chip(label="QA: Grace", bgcolor="red"),
                ]),
                ft.Row([self.mission_input, ft.ElevatedButton(content=ft.Text("Deploy Swarm"), on_click=run_mission, icon="rocket_launch")]),
                ft.Divider(),
                ft.Container(
                    content=self.swarm_log,
                    bgcolor="#111214",
                    padding=10,
                    border_radius=10,
                    expand=True,
                    border=ft.border.all(1, "yellow")
                )
            ]),
            padding=20, expand=True
        )

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
                    # [NEURAL LINK] Attempt Server Connection
                    # from codex_ia.neural_link import NeuralLink
                    # link = NeuralLink(base_url="http://localhost:8000")
                    server_online = False # Force local for now to guarantee "Unlock" experience
                    
                    if server_online:
                        pass # res = link.consult_council(topic)
                    else:
                        # [LOCAL MODE] The Council Simulator
                        self.council_log.controls.append(ft.Text("⚠️ Neural Link Offline. Running Council locally...", color="orange"))
                        self.page.update()
                        
                        prompt = f"""
                        ACT AS: The Council of Three AI Personas.
                        TOPIC: {topic}
                        
                        PERSONAS:
                        1. 🔵 THE INNOVATOR (Steve Jobs style): Radical, abstract, visionary ideas.
                        2. 🟡 THE PRAGMATIST (Engineer): Feasibility, cost, complexity, "how to build".
                        3. 🔴 THE GUARDIAN (Security/Legacy): Safety, risks, bugs, "what can go wrong".
                        
                        FORMAT:
                        Generate a dialogue script where they debate the topic.
                        Use emojis for each speaker.
                        End with a "VERDICT".
                        """
                        
                        if self.agent:
                            res = self.agent.llm_client.send_message(prompt)
                        else:
                            # Fallback if agent not init
                            from codex_ia.core.llm_client import GeminiClient
                            client = GeminiClient()
                            res = client.send_message(prompt)

                    # Remove progress bar (last item)
                    if isinstance(self.council_log.controls[-1], ft.ProgressBar):
                         self.council_log.controls.pop()
                    
                    self.council_log.controls.append(ft.Markdown(res))
                    self.page.update()
                    
                except Exception as e:
                    if isinstance(self.council_log.controls[-1], ft.ProgressBar):
                         self.council_log.controls.pop()
                    self.council_log.controls.append(ft.Text(f"Council Error: {e}", color="red"))
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
            ft.ElevatedButton(content=ft.Text("Generate Business Plan for Current Project"), on_click=call_shark, icon="monetization_on"),
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
    import os
    port = int(os.environ.get("PORT", 8551))
    host = os.environ.get("HOST", "0.0.0.0")
    
    # Run as desktop app
    ft.app(
        target=main,
        port=port,
        host=host
    )
