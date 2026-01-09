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
        self.page.title = "Codex-IA IDE (Level 13)"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 0
        self.page.bgcolor = "#111214"
        self.page.window_min_width = 800
        self.page.window_min_height = 600

    def init_agent(self, path):
        """Initializes or Re-initializes the Agent for a specific path."""
        def worker():
            try:
                self.add_log(f"🔄 Loading Project: {path}...", "blue")
                load_dotenv(os.path.join(path, ".env")) # Load project specific env
                from codex_ia.core.agent import CodexAgent
                self.agent = CodexAgent(project_dir=path)
                self.current_project_dir = path
                self.refresh_file_list()
                self.add_log("✅ Project Loaded Successfully.", "green")
                self.update_title()
            except Exception as e:
                self.add_log(f"❌ Error loading project: {e}", "red")
        
        threading.Thread(target=worker, daemon=True).start()

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
                ft.NavigationRailDestination(icon="school_outlined", selected_icon="school", label="Training"),
                ft.NavigationRailDestination(icon="radar", selected_icon="radar", label="The Hunter"),
                ft.NavigationRailDestination(icon="hive", selected_icon="hive", label="The Swarm"),
            ],
            on_change=self.nav_change,
            bgcolor="#1e1f22",
        )

        # --- Views ---
        self.editor_view = self.build_editor_view()
        self.chat_view = self.build_chat_view()
        self.mission_view = self.build_mission_view()
        self.night_view = self.build_night_view()
        self.training_view = self.build_training_view()
        
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
        
        # Cloud Tools (External)
        if idx == 5: # Hunter
            self.page.launch_url("https://pythonjet-dashboard.fly.dev/hunter/") # Replace with actual URL
            return
        if idx == 6: # Swarm
            self.page.launch_url("https://pythonjet-dashboard.fly.dev/swarm/")
            return
            
        views = [self.editor_view, self.chat_view, self.mission_view, self.night_view, self.training_view]
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
                 for msg in evo.start_night_shift():
                     self.night_log.controls.append(ft.Text(msg))
                     self.page.update()
             threading.Thread(target=worker, daemon=True).start()

         return ft.Container(content=ft.Column([ft.Text("Night Shift", size=20), ft.ElevatedButton("Start", on_click=run_night), self.night_log]), padding=20, expand=True)

    def build_training_view(self):
        self.training_log = ft.Markdown("")
        self.teach_input = ft.TextField(hint_text="Teach...", expand=True)
        
        def run_teach(_):
            lesson = self.teach_input.value
            if not self.agent: return
            self.agent.network_agent.store_experience("Manual", "Instruction", lesson, True, ["manual"])
            self.training_log.value += f"\n✅ Learned: {lesson}"
            self.teach_input.value = ""
            self.page.update()

        return ft.Container(content=ft.Column([
            ft.Text("Training", size=20), 
            ft.Row([self.teach_input, ft.ElevatedButton("Teach", on_click=run_teach)]),
            ft.Container(content=self.training_log, expand=True, bgcolor="#0d0d0d", padding=10)
        ]), padding=20, expand=True)

def main(page: ft.Page):
    CodexIDE(page)

if __name__ == "__main__":
    ft.app(main)
