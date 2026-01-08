import flet as ft
import os
import sys
import threading
import time
from dotenv import load_dotenv

sys.path.append(os.getcwd())

def main(page: ft.Page):
    # --- APP CONFIGURATION ---
    page.title = "Codex-IA Turbo"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.bgcolor = "#111214"
    
    # --- STATE ---
    agent = None
    selected_image_path = None # For Vision

    # --- UI COMPONENTS ---

    # 1. Navigation Rail
    def nav_change(e):
        index = e.control.selected_index
        chat_view.visible = (index == 0)
        files_view.visible = (index == 1)
        mission_view.visible = (index == 2)
        night_view.visible = (index == 3)
        founder_view.visible = (index == 4)
        
        if index == 1:
            refresh_file_list()
            
        page.update()

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon="chat_bubble_outline", 
                selected_icon="chat_bubble", 
                label="Chat"
            ),
            ft.NavigationRailDestination(
                icon="folder_open", 
                selected_icon="folder", 
                label="Files"
            ),
            ft.NavigationRailDestination(
                icon="rocket_launch_outlined", 
                selected_icon="rocket_launch", 
                label="Missions"
            ),
             ft.NavigationRailDestination(
                icon="bedtime_outlined", 
                selected_icon="bedtime", 
                label="Night Shift"
            ),
             ft.NavigationRailDestination(
                icon="monetization_on_outlined", 
                selected_icon="monetization_on", 
                label="Founder"
            ),
        ],
        on_change=nav_change,
        bgcolor="#1e1f22",
    )

    # 2. Chat View
    chat_history = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    
    def add_msg(text, is_user=False):
        try:
             align = ft.CrossAxisAlignment.END if is_user else ft.CrossAxisAlignment.START
             bg = "#2b2d31" if is_user else "#1e1f22"
             chat_history.controls.append(
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Markdown(text, selectable=True),
                            padding=15,
                            border_radius=10,
                            bgcolor=bg,
                            # constraints=ft.BoxConstraints(max_width=800), # Removed for compatibility
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START,
                )
            )
             page.update()
        except Exception as e:
            print(f"Error adding message: {e}")

    chat_input = ft.TextField(
        hint_text="Type a message...",
        expand=True,
        border_color="#383a40",
        filled=True,
        bgcolor="#383a40",
        on_submit=lambda e: send_message_click(None)
    )

    # --- VISION SUPPORT ---
    selected_image_label = ft.Text("", color="cyan", visible=False)

    def on_image_selected(e):
        pass # Disabled for stability
        # nonlocal selected_image_path
        # if e.files and len(e.files) > 0:
        #     selected_image_path = e.files[0].path
        #     selected_image_label.value = f"📷 Image: {e.files[0].name}"
        #     selected_image_label.visible = True
        #     chat_input.hint_text = "Describe what to do with this image..."
        # else:
        #     selected_image_path = None
        #     selected_image_label.visible = False
        # page.update()

    # image_picker = ft.FilePicker()
    # image_picker.on_result = on_image_selected
    # page.overlay.append(image_picker)

    btn_image = ft.IconButton(
        icon="image",
        tooltip="Upload Image (Vision) - DISABLED",
        on_click=lambda _: add_msg("⚠️ Vision disabled due to Flet compatibility issues.") # image_picker.pick_files...
    )

    # --- COUNCIL CONTROLS ---
    def change_brain(e):
        if not agent: return
        brain = dropdown_brain.value
        if agent.llm_client.set_brain(brain):
            add_msg(f"🧠 Brain Switched to: {brain.upper()}", False)
        else:
            add_msg(f"❌ Failed to switch to {brain}", False)

    def run_debate(e):
        message = chat_input.value
        if not message: return
        
        chat_input.value = ""
        add_msg(f"📜 Council Convened: '{message}'", True)
        add_msg("🗳️ Gathering opinions from Gemini, GPT-4, Grok, DeepSeek... please wait.", False)
        page.update()
        
        def worker():
             if not agent: return
             # Call the new method
             verdict = agent.llm_client.council_meeting(message)
             add_msg(verdict)
        
        threading.Thread(target=worker, daemon=True).start()

    dropdown_brain = ft.Dropdown(
        width=150,
        options=[
            ft.dropdown.Option("gemini", "Gemini 2.0"),
            ft.dropdown.Option("openai", "OpenAI (GPT-4)"),
            ft.dropdown.Option("xai", "Grok (xAI)"),
            ft.dropdown.Option("deepseek", "DeepSeek (Coder)"),
            ft.dropdown.Option("groq", "Groq (Llama3)"),
            ft.dropdown.Option("ollama", "Ollama (Local)"),
        ],
        value="gemini",
        bgcolor="#2b2d31",
        border_radius=10,
        text_size=12,
        height=40,
        content_padding=10
    )
    dropdown_brain.on_change = change_brain
    
    btn_debate = ft.IconButton(
        icon="groups",
        tooltip="Council Meeting (Ask ALL AIs)",
        icon_color="purple",
        on_click=run_debate
    )
    # ----------------------

    def send_message_click(e):
        nonlocal selected_image_path
        message = chat_input.value
        if not message and not selected_image_path:
            return
            
        chat_input.value = ""
        chat_input.focus()
        add_msg(message if message else "[Image Upload]", True)
        
        # Capture current image path and reset UI
        current_image = selected_image_path
        selected_image_path = None
        selected_image_label.visible = False
        chat_input.hint_text = "Type a message..."
        page.update()

        def worker():
            if not agent:
                add_msg("⚠️ Agent not ready.")
                return
            
            nonlocal current_image
            
            # Show image in chat if present
            if current_image:
                 add_msg(f"📷 Analyzing image: { os.path.basename(current_image) } ...") # Helper text
            
            # Send to Agents
            response = agent.chat(message, image_path=current_image)
            add_msg(response)

        threading.Thread(target=worker, daemon=True).start()

    chat_view = ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.Text("Chat with Codex", size=20, weight="bold"), ft.Container(expand=True), dropdown_brain]),
                ft.Divider(),
                chat_history,
                ft.Row([selected_image_label]), # Show selected image file
                ft.Row([btn_debate, btn_image, chat_input, ft.IconButton(icon="send", on_click=send_message_click)]),
            ],
            expand=True,
        ),
        padding=20,
        visible=True,
        expand=True
    )

    # 3. Files View
    file_list = ft.Column(scroll=ft.ScrollMode.AUTO)
    
    def refresh_file_list():
        file_list.controls.clear()
        if not agent: return
        
        try:
             # Simple walk
             for root, dirs, files in os.walk(agent.project_dir):
                 if ".git" in root or "__pycache__" in root: continue
                 
                 for f in files:
                     path = os.path.join(root, f)
                     rel_path = os.path.relpath(path, agent.project_dir)
                     
                     file_list.controls.append(
                         ft.ListTile(
                             leading=ft.Icon(ft.icons.INSERT_DRIVE_FILE),
                             title=ft.Text(rel_path),
                             on_click=lambda _, p=path: open_file(p)
                         )
                     )
        except Exception as e:
            file_list.controls.append(ft.Text(f"Error: {e}"))
        page.update()
        
    def open_file(path):
        os.startfile(path) # Windows only

    files_view = ft.Container(
        content=ft.Column(
            [
                ft.Text("Project Files", size=20, weight="bold"),
                ft.Divider(),
                ft.ElevatedButton("Refresh", on_click=lambda _: refresh_file_list()),
                file_list
            ],
             expand=True
        ),
        padding=20,
        visible=False,
        expand=True
    )

    # 4. Mission Control View
    mission_input = ft.TextField(hint_text="Describe the mission...", expand=True, multiline=True)
    mission_log = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    
    # Autopilot Controls
    chk_autopilot = ft.Checkbox(label="Enable Autopilot (Self-Correction)", value=False)
    chk_web_search = ft.Checkbox(label="Allow Web Search 🌐 ", value=False) # New
    txt_verification = ft.TextField(label="Verification Command (optional)", hint_text="e.g., pytest tests/")

    def dispatch_squad(e):
        if not mission_input.value or not agent: return
        
        mission = mission_input.value
        use_auto = chk_autopilot.value
        use_web = chk_web_search.value
        verify_cmd = txt_verification.value
        
        mission_input.value = ""
        
        mission_log.controls.append(ft.Text(f"🚀 Mission Started: {mission}", color="green"))
        if use_auto:
             mission_log.controls.append(ft.Text(f"🤖 Autopilot ENGAGED. Verification: {verify_cmd}", color="cyan"))
        if use_web:
             mission_log.controls.append(ft.Text(f"🌐 Web Search ENABLED.", color="blue"))

        page.update()
        
        def worker():
            try:
                from codex_ia.core.squad import SquadLeader
                squad = SquadLeader(agent.project_dir)
                
                # Updated assign_mission signature support
                result = squad.assign_mission(
                    mission, 
                    apply=True, 
                    autopilot=use_auto, 
                    verification_command=verify_cmd,
                    web_search=use_web
                )
                
                mission_log.controls.append(ft.Markdown(f"### Mission Report\n{result}"))
                page.update()
            except Exception as ex:
                mission_log.controls.append(ft.Text(f"Error: {ex}", color="red"))
                page.update()
                
        threading.Thread(target=worker, daemon=True).start()

    mission_view = ft.Container(
        content=ft.Column(
            [
                ft.Text("Mission Control (Squad)", size=20, weight="bold"),
                ft.Divider(),
                mission_input,
                ft.Row([chk_autopilot, chk_web_search]),
                txt_verification,
                ft.ElevatedButton("Dispatch Squad", icon="rocket_launch", on_click=dispatch_squad),
                ft.Divider(),
                ft.Text("Mission Log:", weight="bold"),
                mission_log
            ],
            expand=True
        ),
        padding=20,
        visible=False,
        expand=True
    )

    # 5. Night Shift View
    night_log = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    
    def start_night_shift(e):
        night_log.controls.append(ft.Text("🌙 Night Shift Started... Good night, sir.", color="purple"))
        page.update()
        
        def worker():
            try:
                from codex_ia.core.evolution_agent import EvolutionAgent
                evo = EvolutionAgent(agent.project_dir)
                for msg in evo.start_night_shift():
                     night_log.controls.append(ft.Text(msg))
                     page.update()
                night_log.controls.append(ft.Text("🌞 Night Shift Complete.", color="yellow"))
            except Exception as ex:
                night_log.controls.append(ft.Text(f"Error: {ex}", color="red"))
            page.update()
            
        threading.Thread(target=worker, daemon=True).start()

    night_view = ft.Container(
         content=ft.Column(
            [
                ft.Text("Night Shift (Autonomous Evolution)", size=20, weight="bold"),
                ft.Text("The AI will optimize code and add tests while you sleep.", size=12, color="grey"),
                ft.Divider(),
                ft.ElevatedButton("Start Night Shift", icon="bedtime", on_click=start_night_shift),
                ft.Divider(),
                night_log
            ],
            expand=True
        ),
        padding=20,
        visible=False,
        expand=True
    )
    
    # 6. Founder View
    founder_input = ft.TextField(hint_text="Target Niche (e.g. 'Pet Shops', 'Lawyers')", expand=True)
    founder_log = ft.Markdown("Ready to brainstorm...")
    btn_brainstorm = ft.ElevatedButton("Brainstorm Ideas", icon="lightbulb", bgcolor="orange", color="white")
    
    # State for selected idea
    selected_idea_input = ft.TextField(hint_text="Paste your favorite idea details here...", multiline=True, min_lines=3)
    btn_build_landing = ft.ElevatedButton("Build Landing Page", icon="build", bgcolor="green", color="white", disabled=True)

    def run_brainstorm(e):
        if not founder_input.value: return
        founder_log.value = "🔍 Researching Market Data... please wait.\n"
        page.update()
        
        def worker():
            try:
                from codex_ia.core.founder_agent import FounderAgent
                if agent:
                    founder = FounderAgent(agent.project_dir)
                    # It runs as a generator now
                    for msg in founder.brainstorm_ideas(founder_input.value):
                         founder_log.value += f"\n{msg}\n"
                         page.update()
                    
                    founder_log.value += "\n✅ Brainstorm Complete. Pick an idea and paste it below to build."
                    btn_build_landing.disabled = False
                else:
                    founder_log.value += "❌ Agent not initialized."
            except Exception as ex:
                founder_log.value += f"Error: {ex}"
            page.update()
            
        threading.Thread(target=worker, daemon=True).start()

    def run_build_landing(e):
        if not selected_idea_input.value: return
        founder_log.value += "\n👷 Dispatching Squad to build Landing Page...\n"
        page.update()
        
        def worker():
            try:
                from codex_ia.core.founder_agent import FounderAgent
                if agent:
                    founder = FounderAgent(agent.project_dir)
                    report = founder.build_landing_page(selected_idea_input.value)
                    
                    founder_log.value += f"\n✅ Build Complete!\nFile: landing_pages/index.html\n"
                    founder_log.value += f"Status: {report.get('apply_status')}\n"
            except Exception as ex:
                founder_log.value += f"Error: {ex}"
            page.update()
            
        threading.Thread(target=worker, daemon=True).start()

    btn_brainstorm.on_click = run_brainstorm
    btn_build_landing.on_click = run_build_landing

    founder_view = ft.Container(
        content=ft.Column([
            ft.Text("👔 The Founder", size=24, weight="bold"),
            ft.Text("Market Research -> Ideation -> MVP Construction", color="grey"),
            ft.Divider(),
            ft.Row([founder_input, btn_brainstorm]),
            ft.Container(content=founder_log, bgcolor="#0d0d0d", padding=10, expand=True, border_radius=5),
            ft.Divider(),
            ft.Text("Build Phase", weight="bold"),
            selected_idea_input,
            btn_build_landing
        ]),
        padding=20,
        visible=False,
        expand=True
    )

    # --- LAYOUT ---
    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                chat_view,
                files_view,
                mission_view,
                night_view,
                founder_view
            ],
            expand=True,
        )
    )

    # --- BACKGROUND INIT ---
    def init_background():
        nonlocal agent
        try:
            load_dotenv(override=True)
            from codex_ia.core.agent import CodexAgent
            agent = CodexAgent(project_dir=".")
            add_msg("✅ System Online.")
        except Exception as e:
            add_msg(f"❌ Error: {e}")

    add_msg("🔄 Initializing...", False)
    threading.Thread(target=init_background, daemon=True).start()

if __name__ == "__main__":
    ft.app(main)
