@echo off
echo ===========================================
echo      SETTING UP DISTRIBUTION FOLDER
echo ===========================================

if not exist "dist" (
    echo [ERROR] 'dist' folder not found. Build probably failed or hasn't finished.
    pause
    exit /b
)

echo [1/2] Copying Environment Variables...
if exist ".env" (
    copy ".env" "dist\.env"
    echo [OK] .env copied.
) else (
    echo [WARNING] .env file not found in root.
)

echo [2/2] Copying Assets and Libraries (Safety Check)...
:: Copy codex_ia folder if exists, to ensure local imports work if not fully frozen
if exist "codex_ia" (
    xcopy /E /I /Y "codex_ia" "dist\codex_ia"
    echo [OK] codex_ia library mirrored.
)

echo.
echo ===========================================
echo      SETUP COMPLETE!
echo ===========================================
echo You can now run: dist\CodexIDE.exe
echo.
pause
