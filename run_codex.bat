@echo off
title Codex-IA Desktop
color 0A

echo ==================================================
echo      INITIATING CODEX-IA (LEVEL 13)
echo ==================================================
echo.

:: Check for Virtual Environment
if exist "venv\Scripts\activate.bat" (
    echo [BOOT] Activating Virtual Environment...
    call venv\Scripts\activate.bat
) else (
    echo [BOOT] No venv found. using global Python...
)

:: Check dependencies (Quietly)
echo [BOOT] Checking Core Functions...
python -c "import google.genai; import rich; import dotenv" 2>NUL
if %errorlevel% neq 0 (
    echo [WARNING] Dependencies might be missing. Installing...
    pip install google-genai rich python-dotenv
)

:: Run the Agent
echo [BOOT] Connecting to Neural Network...
echo.
python codex_cli.py

:: Keep window open if it crashes
if %errorlevel% neq 0 (
    echo.
    echo [CRITICAL ERROR] The agent crashed. See above for details.
    pause
)
