# Codex-IA Web Server Launcher
Write-Host "[CODEX-IA] Iniciando Servidor Web na porta 8550..." -ForegroundColor Cyan

$scriptPath = $PSScriptRoot
Set-Location $scriptPath

# Check venv
if (Test-Path "venv") {
    Write-Host "[ENV] Ativando venv..." -ForegroundColor Green
    & ".\venv\Scripts\Activate.ps1"
} else {
    Write-Host "[ENV] AVISO: venv nao encontrado." -ForegroundColor Yellow
}

Write-Host "[RUN] Iniciando Flet Web App..." -ForegroundColor Cyan
Write-Host "Acesse: http://localhost:8550" -ForegroundColor White

flet run codex_gui.py --web --port 8550 --hidden
