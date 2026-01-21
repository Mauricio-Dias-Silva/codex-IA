"""
📡 NEXUS REAL-TIME CONNECTOR
Módulo de Inteligência Viva para o Codex-IA.

Funcionalidades:
1. BACEN Connector: Puxa Selic, Inflação e Dólar do Banco Central (API SGS).
2. Social & Legal Spy: Monitora RSS feeds de Tecnologia, Direito (STF) e Mercado.
3. Indexação Automática: Salva tudo no ChromaDB com timestamp para análise preditiva.
"""

import os
import sys
import time
import requests
import feedparser
import json
from datetime import datetime

# Adiciona diretório raiz ao path para importar módulos do Codex
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codex_ia.core.vector_store import CodexVectorStore
from codex_ia.core.llm_client import GeminiClient

class NexusCodex:
    def __init__(self):
        self.store = CodexVectorStore()
        # Não precisamos do Gemini para PUXAR dados, só para analisar depois se quisermos.
        # Mas vamos focar na COLETA e INDEXAÇÃO pura agora.
        self.sources = {
            'BACEN': {
                'SELIC': 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json',
                'IPCA': 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json',
                'DOLAR': 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados/ultimos/1?formato=json',
                'IGPM': 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.189/dados/ultimos/1?formato=json'
            },
            'NEWS_FEEDS': [
                {'name': 'STF_JURISPRUDENCIA', 'url': 'https://www.stf.jus.br/arquivo/rss/noticia.xml', 'category': 'LEGAL'},
                {'name': 'SENADO_NOTICIAS', 'url': 'https://www12.senado.leg.br/noticias/feed/conteudo/noticias', 'category': 'POLITICS'},
                {'name': 'MIT_TECH_REVIEW', 'url': 'https://www.technologyreview.com/feed/', 'category': 'TECH'},
                {'name': 'GOOGLE_AI_BLOG', 'url': 'http://googleaiblog.blogspot.com/atom.xml', 'category': 'AI_SCIENCE'}
            ]
        }

    def fetch_financial_data(self):
        """Puxa indicadores econômicos do Banco Central."""
        print("\n💰 [NEXUS] Coletando Dados Financeiros (BACEN)...")
        results = []
        
        headers = {'User-Agent': 'CodexIA/1.0 (Research Bot)'}
        
        for name, url in self.sources['BACEN'].items():
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    # A API retorna lista: [{'data': '01/01/2024', 'valor': '10.5'}]
                    if data and len(data) > 0:
                        item = data[0]
                        valor = item.get('valor')
                        data_ref = item.get('data')
                        
                        text_content = f"INDICADOR ECONÔMICO: {name}\nValor Atual: {valor}\nData Referência: {data_ref}\nFonte: Banco Central do Brasil (SGS)"
                        
                        # Indexar
                        self.store.index_text(
                            text=text_content,
                            metadata={
                                'source': 'BACEN_API',
                                'type': 'FINANCIAL_INDICATOR',
                                'indicator': name,
                                'date': datetime.now().isoformat(),
                                'value': valor
                            }
                        )
                        print(f"   ✅ {name}: {valor} ({data_ref})")
                        results.append(f"{name}: {valor}")
                else:
                    print(f"   ❌ Erro {name}: Status {response.status_code}")
            except Exception as e:
                print(f"   ❌ Erro {name}: {e}")
        
        return results

    def fetch_rss_feeds(self):
        """Monitora Feeds RSS de Alta Autoridade."""
        print("\n📡 [NEXUS] Monitorando Feeds de Inteligência...")
        
        count_new = 0
        
        for feed in self.sources['NEWS_FEEDS']:
            print(f"   🔎 Lendo: {feed['name']}...")
            try:
                parsed = feedparser.parse(feed['url'])
                
                # Pegar as 5 notícias mais recentes
                for entry in parsed.entries[:5]:
                    title = entry.title
                    link = entry.link
                    summary = getattr(entry, 'summary', '') or getattr(entry, 'description', '')
                    published = getattr(entry, 'published', '') or getattr(entry, 'updated', str(datetime.now()))
                    
                    # Limpeza básica de HTML no summary se necessário (mas o Chroma aguenta)
                    
                    content = f"""
                    TÍTULO: {title}
                    RESUMO: {summary}
                    FONTE: {feed['name']} ({feed['category']})
                    DATA: {published}
                    LINK: {link}
                    """
                    
                    # Criar um ID único baseado no link para evitar duplicatas (chave primária lógica)
                    # O Chroma não tem "upsert com ID" fácil na nossa classe wrapper atual, 
                    # então vamos confiar que a busca semântica lidará com redundância 
                    # ou o usuário pode limpar a base periodicamente. 
                    # (Melhoria futura: Check if exists)
                    
                    self.store.index_text(
                        text=content,
                        metadata={
                            'source': 'NEXUS_RSS',
                            'type': 'NEWS_INTELLIGENCE',
                            'category': feed['category'],
                            'feed_name': feed['name'],
                            'date': datetime.now().isoformat()
                        }
                    )
                    count_new += 1
                    # print(f"      + {title[:50]}...")
                    
            except Exception as e:
                print(f"   ❌ Erro ao ler feed {feed['name']}: {e}")
        
        print(f"   ✅ Total de novos items indexados: {count_new}")

    def run_cycle(self):
        """Executa um ciclo completo de atualização."""
        print("="*60)
        print(f"👁️ NEXUS CONNECTED - {datetime.now()}")
        print("="*60)
        
        self.fetch_financial_data()
        self.fetch_rss_feeds()
        
        print("\n💤 Ciclo concluído. O Codex está atualizado.")

if __name__ == "__main__":
    nexus = NexusCodex()
    # Loop infinito ou execução única?
    # Para teste agora, execução única.
    # No servidor, pode rodar via cron ou loop com sleep.
    nexus.run_cycle()
