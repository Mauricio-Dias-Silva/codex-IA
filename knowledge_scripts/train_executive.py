"""
🎯 EXECUTIVE INTELLIGENCE TRAINER
Alimenta o Codex com conhecimento estratégico de CEOs, VCs e líderes globais.
"""

import os
import sys

# Adiciona o path do projeto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codex_ia.core.vector_store import CodexVectorStore
from codex_ia.core.llm_client import GeminiClient

def train_executive_intelligence():
    """Gera e indexa conhecimento executivo/estratégico de alto nível."""
    
    store = CodexVectorStore()
    llm = GeminiClient()
    
    # Tópicos de Inteligência Executiva
    executive_topics = [
        {
            "domain": "EXECUTIVE_STRATEGY",
            "prompt": """Você é um consultor de estratégia McKinsey/BCG.
            
            Crie um documento executivo sobre: COMO OS CEOS DE GRANDES EMPRESAS TOMAM DECISÕES
            
            Inclua:
            - Framework OODA Loop (Observe, Orient, Decide, Act)
            - Matriz de Eisenhower (Urgente vs Importante)
            - First Principles Thinking (Elon Musk)
            - Jeff Bezos: "Decisões Tipo 1 vs Tipo 2"
            - Steve Jobs: Foco e simplicidade
            - Netflix Culture Deck: Context over Control
            
            Gere 3000 palavras de estratégia pura."""
        },
        {
            "domain": "VENTURE_CAPITAL",
            "prompt": """Você é um partner da Sequoia Capital/Y Combinator.
            
            Explique: O QUE VENTURE CAPITALISTS PROCURAM EM STARTUPS
            
            Tópicos:
            - Product-Market Fit (Marc Andreessen)
            - Traction Metrics (DAU, MRR, LTV/CAC)
            - Team-First Investing
            - TAM (Total Addressable Market) Analysis
            - Unit Economics
            - Competitive Moats (Peter Thiel: "Monopoly")
            - Pitch Deck Breakdown (Guy Kawasaki 10-20-30)
            
            Gere um guia de 2500 palavras."""
        },
        {
            "domain": "PRODUCT_STRATEGY",
            "prompt": """Você é o Head of Product do Google/Meta.
            
            Ensine: COMO GRANDES TECH COMPANIES DECIDEM O QUE CONSTRUIR
            
            Frameworks:
            - Jobs to Be Done (Clayton Christensen)
            - RICE Score (Reach, Impact, Confidence, Effort)
            - OKRs (Objectives and Key Results - Google)
            - North Star Metric
            - A/B Testing Philosophy (Facebook)
            - Minimum Lovable Product vs MVP
            - Kano Model (Features Must-Have vs Delighters)
            
            Gere 2800 palavras práticas."""
        },
        {
            "domain": "GROWTH_HACKING",
            "prompt": """Você é o Growth Lead do Dropbox/Airbnb.
            
            Revele: TÁTICAS DE CRESCIMENTO QUE FUNCIONARAM PARA UNICÓRNIOS
            
            Cases:
            - Dropbox: Referral Loop (Give 500MB, Get 500MB)
            - Airbnb: Craigslist Integration Hack
            - Hotmail: "PS: I love you. Get your free email at Hotmail"
            - PayPal: $20 por cadastro
            - Uber: Promo codes virais
            - TikTok: Algoritmo de viralização
            - Clubhouse: Invite-Only FOMO
            
            Gere um playbook de 2000 palavras."""
        },
        {
            "domain": "PRICING_PSYCHOLOGY",
            "prompt": """Você é o Chief Revenue Officer da Stripe/Salesforce.
            
            Explique: CIÊNCIA POR TRÁS DO PRICING DE SAAS E E-COMMERCE
            
            Estratégias:
            - Anchoring Effect (Preço "riscado")
            - Freemium to Premium Conversion
            - Value-Based Pricing vs Cost-Plus
            - Tiered Pricing Psychology (Good, Better, Best)
            - Dynamic Pricing (Amazon, Uber)
            - Loss Aversion (Trials que viram assinatura)
            - Psychological Price Points ($99 vs $100)
            
            Gere 2200 palavras com exemplos reais."""
        },
        {
            "domain": "MARKET_TIMING",
            "prompt": """Você é um analista de tendências da CB Insights/Gartner.
            
            Ensine: COMO IDENTIFICAR ONDAS TECNOLÓGICAS ANTES DA MASSA
            
            Metodologia:
            - Gartner Hype Cycle
            - Crossing the Chasm (Geoffrey Moore)
            - Technology Adoption Curve
            - Lindy Effect (Nassim Taleb)
            - Sinais de Zeitgeist (Google Trends, Reddit, HN)
            - Pattern Recognition em IPOs e Aquisições
            - Investimento contrário (Warren Buffett)
            
            Gere um framework de 2500 palavras."""
        },
        {
            "domain": "OPERATIONAL_EXCELLENCE",
            "prompt": """Você é o COO da Toyota/Amazon.
            
            Revele: SISTEMAS OPERACIONAIS DE EMPRESAS CLASSE MUNDIAL
            
            Princípios:
            - Kaizen (Melhoria Contínua)
            - Six Sigma e Lean Manufacturing
            - Amazon's "Working Backwards" (começar pelo press release)
            - Toyota's Andon Cord (parar a linha se houver defeito)
            - Shopify's "Trust Battery"
            - Spotify's Squad/Tribe Model
            - Automatização Radical (Tesla Gigafactories)
            
            Gere um manual de 3000 palavras."""
        },
        {
            "domain": "CUSTOMER_OBSESSION",
            "prompt": """Você é o VP of Customer Experience da Zappos/Ritz-Carlton.
            
            Ensine: COMO CRIAR CUSTOMER EXPERIENCE QUE VIRA MARKETING
            
            Táticas:
            - Zappos: 365-day return policy
            - Ritz-Carlton: $2000 de autonomia por funcionário
            - Disney: "Magic Moments"
            - Net Promoter Score (NPS) obsession
            - Customer Success antes do Customer Support
            - Turning Complainers into Advocates
            - Surprise and Delight Moments
            
            Gere um guia de 2300 palavras com cases."""
        }
    ]
    
    print("🧠 INICIANDO EXECUTIVE INTELLIGENCE TRAINING...")
    print("=" * 60)
    
    for i, topic in enumerate(executive_topics, 1):
        print(f"\n[{i}/{len(executive_topics)}] 🎯 Domínio: {topic['domain']}")
        
        try:
            # Gera conhecimento via Gemini 2.5 Pro
            from google import genai
            from google.genai import types
            
            response = llm.client.models.generate_content(
                model=llm.model,
                contents=topic['prompt'],
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=4000
                )
            )
            
            if response and response.text:
                # Indexa no Vector Store
                doc_id = store.index_text(
                    text=response,
                    metadata={
                        'source': 'EXECUTIVE_INTELLIGENCE_TRAINING',
                        'domain': topic['domain'],
                        'level': 'C-LEVEL',
                        'type': 'STRATEGIC_FRAMEWORK'
                    }
                )
                
                preview = response[:200].replace('\n', ' ')
                print(f"   ✅ Indexado: {doc_id}")
                print(f"   📝 Preview: {preview}...")
                print(f"   📊 Tokens: ~{len(response.split())}")
            else:
                print(f"   ❌ Falha ao gerar conteúdo")
                
        except Exception as e:
            print(f"   ⚠️  Erro: {str(e)}")
            continue
    
    print("\n" + "=" * 60)
    print("🎓 EXECUTIVE TRAINING COMPLETO!")
    print("💡 Codex agora pensa como um Board of Directors.")

if __name__ == "__main__":
    train_executive_intelligence()
