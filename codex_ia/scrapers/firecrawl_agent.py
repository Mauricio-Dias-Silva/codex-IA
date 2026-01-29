import os
import requests
import logging

logger = logging.getLogger(__name__)

class FirecrawlAgent:
    """
    Agente especialista em ler a Web Profunda (Deep Scraping).
    Usa a API do Firecrawl para converter qualquer site em Markdown limpo.
    """
    
    API_URL = "https://api.firecrawl.dev/v0/scrape"

    def __init__(self, api_key=None):
        # Tenta pegar do argumento ou do ENV
        self.api_key = api_key or os.environ.get("FIRECRAWL_API_KEY")
        if not self.api_key:
            logger.warning("⚠️ Firecrawl API Key não configurada. Agente rodará em modo simulação.")

    def scrape_url(self, url: str) -> str:
        if not self.api_key:
            return f"[SIMULAÇÃO] Conteúdo simulado de {url}. Configure FIRECRAWL_API_KEY."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "url": url,
            "pageOptions": {
                "onlyMainContent": True,
                "includeTags": ["h1", "h2", "h3", "p", "a", "code", "pre"],
            }
        }
        
        try:
            logger.info(f"🔥 Firecrawl lendo: {url}")
            response = requests.post(self.API_URL, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return data['data'].get('markdown', '')
                else:
                    logger.error(f"❌ Erro Firecrawl: {data.get('error')}")
                    return None
            else:
                logger.error(f"❌ Erro HTTP {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Falha na conexão com Firecrawl: {e}")
            return None
