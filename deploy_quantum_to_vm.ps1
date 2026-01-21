# Deploy Quantum Leap Scripts para VM
# Execute na máquina Windows LOCAL

Write-Host "🌌 Preparando Quantum Leap Scripts para VM..." -ForegroundColor Cyan

# 1. Compactar scripts
Write-Host "📦 Compactando scripts..." -ForegroundColor Yellow
cd C:\Users\Mauricio\Desktop\codex-IA

# Criar arquivo tar.gz com os scripts
tar -czf quantum_scripts.tar.gz knowledge_scripts/quantum_leap_trainer.py knowledge_scripts/train_medicine.py knowledge_scripts/train_law.py knowledge_scripts/train_engineering.py knowledge_scripts/train_quant_finance.py knowledge_scripts/train_advanced_professional.py knowledge_scripts/train_entrepreneurship.py knowledge_scripts/train_strategic_mgmt.py knowledge_scripts/train_urban_governance.py knowledge_scripts/train_sustainability.py knowledge_scripts/train_all_academic.py

if (Test-Path quantum_scripts.tar.gz) {
    Write-Host "✅ Arquivo compactado criado!" -ForegroundColor Green
    
    Write-Host "`n🚀 Agora execute MANUALMENTE na VM:" -ForegroundColor Cyan
    Write-Host "   1. Abra WinSCP ou outro cliente SCP" -ForegroundColor White
    Write-Host "   2. Conecte em: 34.148.70.131" -ForegroundColor White
    Write-Host "   3. Usuário: engmauriciodias33" -ForegroundColor White
    Write-Host "   4. Envie o arquivo: quantum_scripts.tar.gz" -ForegroundColor White
    Write-Host "   5. Para: /tmp/" -ForegroundColor White
    Write-Host "`n   OU use este comando (se SSH funcionar):" -ForegroundColor Yellow
    Write-Host "   scp quantum_scripts.tar.gz engmauriciodias33@34.148.70.131:/tmp/" -ForegroundColor Gray
    
    Write-Host "`n📝 Depois, na VM execute:" -ForegroundColor Cyan
    Write-Host "   cd /opt/codex-ia" -ForegroundColor White
    Write-Host "   tar -xzf /tmp/quantum_scripts.tar.gz" -ForegroundColor White
    Write-Host "   python3 knowledge_scripts/quantum_leap_trainer.py" -ForegroundColor White
    
} else {
    Write-Host "❌ Erro ao criar arquivo!" -ForegroundColor Red
}
