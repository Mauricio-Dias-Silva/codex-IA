# Deploy Codex-IA para Google App Engine

## Pré-requisitos
1. Conta Google Cloud com billing ativado
2. gcloud CLI instalado e configurado
3. IP da VM: **34.148.70.131** (já configurado no ALLOWED_HOSTS)

## Comandos de Deploy

```bash
# 1. Coletar arquivos estáticos
python manage.py collectstatic --noinput

# 2. Criar arquivo .gcloudignore (ignorar venv e outros)
echo "venv/
*.pyc
__pycache__/
db.sqlite3
.git/
.env" > .gcloudignore

# 3. Deploy para App Engine
gcloud app deploy app.yaml --project=CODEX_PROJECT_ID

# 4. Ver logs
gcloud app logs tail -s default
```

## Variáveis de Ambiente (App Engine)

Adicione ao `app.yaml` ou configure via Console:

```yaml
env_variables:
  SECRET_KEY: "sua-secret-key-production"
  DEBUG: "False"
  # Copie todas as chaves de API do .env local
  GEMINI_API_KEY: "..."
  MISTRAL_API_KEY: "..."
  # etc
```

## ⚠️ IMPORTANTE - Segurança

1. **Nunca comite o .env no Git**
2. **Configure SECRET_KEY única em produção**
3. **DEBUG=False em produção**
4. **Proteção anti-vazamento ATIVA** ✅

## Alternativa Rápida: Deploy Manual

Se preferir deploy manual na VM existente (34.148.70.131):

```bash
# SSH na VM
gcloud compute ssh NOME_DA_VM --zone=ZONA

# Na VM:
cd /caminho/para/codex-ia
git pull
pip install -r requirements.txt
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn  # ou reiniciar manualmente
```

## Status
- ✅ App.yaml configurado
- ✅ Settings.py pronto para produção
- ✅ Proteção de código implementada
- ⏳ Aguardando deploy manual ou automático
