import os
import flet as ft
from codex_gui import main

if __name__ == "__main__":
    # Cloud Run injects the PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting Codex-IA Web Server on port {port}...")
    
    # Enable Web View
    ft.app(
        target=main, 
        view=ft.AppView.WEB_BROWSER, 
        port=port,
        host="0.0.0.0" # Required for Cloud Run external access
    )
