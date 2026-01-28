import subprocess
import os
import sys

# Ensure assets dir exists
if not os.path.exists("assets"):
    os.makedirs("assets")

print("🚀 Starting Build Process for Codex-IA Turbo via Subprocess...")

cmd = [
    sys.executable, "-m", "PyInstaller",
    "codex_gui.py",
    "--name=CodexIA_Turbo",
    "--onefile",
    "--windowed",
    "--add-data=codex_ia;codex_ia",
    "--distpath=dist",
    "--clean",
    "-y"
]

if os.path.exists("assets/app.ico"):
    cmd.append("--icon=assets/app.ico")

try:
    subprocess.check_call(cmd)
    print("✅ Build Complete! Check the 'dist' folder for CodexIA_Turbo.exe")
except subprocess.CalledProcessError as e:
    print(f"❌ Build Failed: {e}")
