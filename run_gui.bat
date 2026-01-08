@echo off
title Codex-IA Antigravity (Visual)
color 0B

echo ==================================================
echo      INITIATING ANTIGRAVITY UI (LEVEL 13)
echo ==================================================
echo.

:: Check for Virtual Environment
if exist "venv\Scripts\activate.bat" (
    echo [BOOT] Activating Virtual Environment...
    call venv\Scripts\activate.bat
) else (
    echo [BOOT] No venv found. using global Python...
)

:: Check dependencies
echo [BOOT] Checking Visual Core (Flet)...
python -c "import flet; import google.genai" 2>NUL
if %errorlevel% neq 0 (
    echo [WARNING] Visual dependencies missing. Installing Flet...
    pip install "flet[all]" google-genai rich python-dotenv
)

:: Run the GUI
echo [BOOT] Launching Visual Interface...
python codex_gui.py

:: Keep window open if crash
if %errorlevel% neq 0 (
    echo.
    echo [CRITICAL ERROR] The visual interface crashed.
    pause
)
