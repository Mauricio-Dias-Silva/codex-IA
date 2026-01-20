#!/bin/bash
# Script de deploy para VM

echo "🚀 Atualizando Codex-IA na VM..."

cd /home/mauriciodsilva205/codex-IA
git pull origin main

source venv/bin/activate
pip install -r requirements.tx --quiet

# Copiar .env local para VM (se necessário)
# Nota: As chaves de API devem estar no .env da VM

python manage.py collectstatic --noinput

sudo systemctl restart codex-ia

echo "✅ Deploy concluído!"
echo "Acesse: http://34.148.70.131:8551/chat/"
