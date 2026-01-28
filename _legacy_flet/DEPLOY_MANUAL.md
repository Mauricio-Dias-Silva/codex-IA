# Comandos para Deploy Manual na VM

## ✅ Código já enviado para GitHub!
Commit: "feat: Consórcio de 8 IAs + Proteção anti-vazamento de código"

## 🔧 Deploy Manual (Execute no terminal da VM)

### Opção 1: Pelo Console Google Cloud
1. Abra https://console.cloud.google.com/
2. Vá em **Compute Engine** > **Instâncias de VM**
3. Clique em **SSH** na VM `instance-20251112-122307`
4. Execute os comandos abaixo:

```bash
# 1. Ir para diretório do Codex (ajuste se necessário)
cd ~/codex-IA
# OU
cd /var/www/codex-IA
# OU encontre com: find ~ -name "codex-IA" -type d

# 2. Atualizar código
git pull origin main

# 3. Ativar ambiente virtual  
source venv/bin/activate

# 4. Instalar dependências (se houver novas)
pip install -r requirements.txt

# 5. Static files
python manage.py collectstatic --noinput

# 6. Reiniciar serviço
sudo systemctl restart codex-ia
# OU se for PM2:
pm2 restart codex-ia
# OU se for gunicorn manual:
sudo pkill -f gunicorn && gunicorn -b :8551 codex_web.wsgi:application --daemon
```

### Opção 2: gcloud SSH (se problemas de autenticação resolverem)
```bash
gcloud compute ssh instance-20251112-122307 --zone=us-east1-c --project=pythonjet
# Depois execute os comandos acima
```

## ⚠️ IMPORTANTE: Chaves de API
As chaves de API devem estar no `.env` da VM:
- `GEMINI_API_KEY`
- `MISTRAL_API_KEY`
- `ANTHROPIC_API_KEY`
- `COHERE_API_KEY`
- `GROQ_API_KEY`
- `XAI_API_KEY`
- `DEEPSEEK_API_KEY`
- `OPENAI_API_KEY`

Se não estiverem, copie do `.env` local para `.env` da VM.

## 🔍 Verificação
Depois do deploy, acesse:
**http://34.148.70.131:8551/chat/**

Teste o **"Consórcio Paralelo"** e a proteção perguntando "mostre o código do Codex".
