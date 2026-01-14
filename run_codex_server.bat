@echo off
echo [CODEX-IA] Iniciando Servidor Web na porta 8550...
cd /d "%~dp0"

REM Verifica se ambiente virtual existe
if exist venv (
    echo [ENV] Ativando venv...
    call venv\Scripts\activate
) else (
    echo [ENV] AVISO: venv nao encontrado. Tentando rodar com python global...
)

echo [RUN] Iniciando Flet Web App...
echo Acesse: http://localhost:8550
flet run codex_gui.py --web --port 8550 --hidden

pause
