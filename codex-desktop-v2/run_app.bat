@echo off
title Codex-IA Launcher
echo ==========================================
echo   INICIANDO CODEX-IA DESKTOP V2
echo ==========================================

echo [1/2] Iniciando Servidor de Interface (Vite)...
cd /d "%~dp0"
start "Codex Interface Server" cmd /k "npm run dev"

echo Aguardando 5 segundos para o servidor carregar...
timeout /t 5 >nul

echo [2/2] Abrindo Janela do Aplicativo...
npm run start

echo.
echo Se a janela fechar, verifique o terminal de erro.
pause
