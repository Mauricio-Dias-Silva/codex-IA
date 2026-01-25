"""
Script de Análise Completa do PythonJet via Codex-IA
Analisa arquitetura, segurança, performance e escalabilidade
"""

from codex_ia.core.agent import CodexAgent
from codex_ia.core.vector_store import CodexVectorStore
import os
from pathlib import Path

def analyze_pythonjet():
    # Inicializar Codex
    print('🧠 Inicializando Codex-IA...')
    vector_store = CodexVectorStore()
    agent = CodexAgent(vector_store)
    
    # Caminho do projeto
    pythonjet_path = Path(r'C:\Users\Mauricio\Desktop\painel-pythonjet')
    
    # Arquivos principais para análise
    files_to_analyze = [
        'config/settings.py',
        'config/urls.py',
        'dashboard/views.py',
        'dashboard/models.py',
        'dashboard/apps/fintech/services.py',
        'dashboard/apps/fintech/models.py',
        'dashboard/apps/fintech/views.py',
        'dashboard/middleware/self_healing.py',
        'dashboard/middleware/query_monitor.py',
    ]
    
    # Construir contexto com os arquivos
    context = '=== ANÁLISE DO PROJETO PYTHONJET ===\n\n'
    context += 'ESTRUTURA DO PROJETO:\n'
    
    total_lines = 0
    files_read = 0
    
    for file in files_to_analyze:
        filepath = pythonjet_path / file
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = len(content.split('\n'))
                    total_lines += lines
                    files_read += 1
                    
                    # Pega primeiras 3000 chars de cada arquivo
                    preview = content[:3000]
                    if len(content) > 3000:
                        preview += '\n... (truncado)\n'
                    
                    context += f'\n--- {file} ({lines} linhas) ---\n{preview}\n'
            except Exception as e:
                context += f'\n❌ Erro ao ler {file}: {e}\n'
    
    context += f'\n\n📊 ESTATÍSTICAS:\n'
    context += f'- Arquivos analisados: {files_read}\n'
    context += f'- Total de linhas: {total_lines}\n'
    
    # Query de análise técnica
    query = f'''
{context}

VOCÊ É UM SENIOR SOFTWARE ARCHITECT COM 15 ANOS DE EXPERIÊNCIA.

Analise o PYTHONJET - um SaaS que permite criar e deployar aplicações Django/Flask/Node automaticamente no Google Cloud Run.

CONTEXTO TÉCNICO:
- Framework: Django 4.x
- Stack: Python, PostgreSQL, Redis, Celery
- Deploy: Google Cloud Run + Cloud SQL
- Features: AI code generation, marketplace, fintech (banking), auto-scaling

MUDANÇAS RECENTES (Auditoria Fase 1 e 2):
✅ Resolvido: 6 security warnings (HTTPS, HSTS, SECRET_KEY, cookies)
✅ Resolvido: N+1 queries no dashboard (select_related)
✅ Resolvido: Error handling em imports dinâmicos
✅ Arquitetura: Fintech app migrado para dashboard/apps/

---

ANÁLISE REQUERIDA:

1. **ARQUITETURA** (0-10)
   - Separação de responsabilidades
   - Padrões de design
   - Organização de módulos

2. **SEGURANÇA** (0-10)
   - Vulnerabilidades conhecidas
   - Best practices
   - Surface attack

3. **PERFORMANCE** (0-10)
   - Database queries
   - Caching strategy
   - Async processing

4. **ESCALABILIDADE** (0-10)
   - Horizontal scaling readiness
   - Database design
   - Stateless architecture

5. **MANUTENIBILIDADE** (0-10)
   - Code quality
   - Documentação
   - Test coverage

---

FORMATO DE RESPOSTA:

## 📊 SCORE GERAL: X/10

## ✅ PONTOS FORTES
1. [Principal vantagem técnica]
2. [Segunda vantagem]
3. [Terceira vantagem]

## ⚠️ PONTOS FRACOS
1. [Principal problema]
2. [Segundo problema]
3. [Terceiro problema]

## 🎯 RECOMENDAÇÕES PRIORITÁRIAS
1. [Ação urgente #1]
2. [Ação urgente #2]
3. [Ação urgente #3]

## 🔮 VEREDITO FINAL
[Análise crítica de 2-3 parágrafos sobre a viabilidade do projeto em produção]

Seja TÉCNICO, OBJETIVO e CRÍTICO. Use dados dos arquivos analisados.
'''

    print('🔍 Analisando código...\n')
    print('=' * 80)
    
    # Executar análise
    response = agent.chat(query)
    
    print(response)
    print('\n' + '=' * 80)
    print(f'\n✅ Análise completa! ({files_read} arquivos, {total_lines} linhas)')
    
    # Salvar resultado
    output_file = pythonjet_path / 'CODEX_ANALYSIS.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f'# Análise Técnica do PythonJet - Codex-IA\n\n')
        f.write(f'**Data:** {__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n')
        f.write(response)
    
    print(f'📄 Relatório salvo em: {output_file}')

if __name__ == '__main__':
    try:
        analyze_pythonjet()
    except Exception as e:
        print(f'❌ Erro: {e}')
        import traceback
        traceback.print_exc()
