@echo off
title Build CodexIDE
echo ========================================
echo      BUILDING CODEX-IA IDE (.EXE)
echo ========================================

echo [1/4] Installing Build Tools...
pip install --upgrade pip
pip install pyinstaller

echo [2/4] Installing Dependencies (Critical for Flet)...
:: Ensure Flet and project libaries are installed
pip install "flet[all]" google-genai rich python-dotenv fpdf2

echo [3/4] Running Flet Pack...
:: 'flet pack' wraps PyInstaller and automatically handles Flet's hidden imports and asset bundling.
:: This solves the common "charade" of Flet build failures.
flet pack codex_gui.py --name "CodexIA_Triad" --product-name "Codex-IA" --file-description "Advanced AI IDE (God Mode)" --hidden-import "codex_ia" --hidden-import "codex_ia.neural_link" --hidden-import "codex_ia.core" -y

echo [4/4] Build Complete.
echo.
echo Your new IDE is located in: dist\CodexIDE.exe
echo.
pause
