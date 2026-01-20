"""
🚀 ENTREPRENEURSHIP MASTERY TRAINER
Conhecimento acadêmico de empreendedorismo (Nível PhD)
Fontes: Harvard, Stanford, Babson College, Kauffman Foundation
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codex_ia.core.vector_store import CodexVectorStore
from codex_ia.core.llm_client import GeminiClient
from google.genai import types

def train_entrepreneurship():
    """Indexa conhecimento acadêmico profundo sobre empreendedorismo."""
    
    store = CodexVectorStore()
    llm = GeminiClient()
    
    topics = [
        {
            "domain": "LEAN_STARTUP_METHODOLOGY",
            "prompt": """Você é um professor de Empreendedorismo da Stanford University.
            
            Ensine em profundidade: LEAN STARTUP METHODOLOGY (Eric Ries)
            
            Cubra academicamente:
            - Build-Measure-Learn Loop (ciclo científico validado)
            - Minimum Viable Product (MVP) vs Concierge MVP
            - Pivot vs Persevere Decision Framework
            - Innovation Accounting metrics
            - Validated Learning através de experimentos
            - Split Testing e Cohort Analysis
            - Runway Extension Strategies
            
            Nível: Doutorado. 3000 palavras. Inclua estudos de caso reais (Dropbox, Zappos)."""
        },
        {
            "domain": "EFFECTUATION_THEORY",
            "prompt": """Você é pesquisador da Darden School of Business (UVA).
            
            Explique: EFFECTUATION THEORY (Saras Sarasvathy)
            
            Contraste com Causation:
            - Bird-in-Hand Principle (recursos disponíveis)
            - Affordable Loss vs Expected Returns
            - Crazy Quilt (parcerias antes de competição)
            - Lemonade Principle (transformar surpresas em oportunidades)
            - Pilot-in-the-Plane (controle sobre predição)
            
            Inclua: Pesquisa empírica com expert entrepreneurs (27 fundadores estudados).
            2500 palavras acadêmicas."""
        },
        {
            "domain": "BUSINESS_MODEL_INNOVATION",
            "prompt": """Você é autor do Business Model Generation (Osterwalder & Pigneur).
            
            Ensine: BUSINESS MODEL CANVAS e teorias de inovação em modelos de negócio
            
            Componentes:
            - 9 Building Blocks detalhados
            - Padrões de Modelos Recorrentes (Freemium, Long Tail, Multi-sided Platforms)
            - Blue Ocean Strategy (Kim & Mauborgne)
            - Disruptive Innovation Theory (Christensen)
            - Platform Economics (Eisenmann, Parker, Van Alstyne)
            
            Acadêmico. 3200 palavras. Casos: Uber, Netflix, Amazon."""
        },
        {
            "domain": "VENTURE_FINANCING",
            "prompt": """Você é professor de Venture Capital na Wharton School.
            
            Explique cientificamente: VENTURE CAPITAL ECOSYSTEM & FINANCING STAGES
            
            Tópicos rigorosos:
            - Pre-seed, Seed, Series A/B/C mechanics
            - Valuation Methods (VC Method, Scorecard, Berkus)
            - Term Sheet Anatomy (liquidation preference, anti-dilution, vesting)
            - Cap Table Management matemático
            - Signaling Theory em fundraising
            - Information Asymmetry (Adverse Selection, Moral Hazard)
            - Exit Strategies (IPO vs M&A dynamics)
            
            PhD-level. 2800 palavras."""
        },
        {
            "domain": "FAMILY_BUSINESS_GOVERNANCE",
            "prompt": """Você é pesquisador do Family Business Center (Harvard).
            
            Ensine: GOVERNANÇA CORPORATIVA EM EMPRESAS FAMILIARES
            
            Research-based:
            - Three-Circle Model (Família, Propriedade, Negócio)
            - Sucessão Planejada (Harvard Family Firm Institute)
            - Family Constitution Design
            - Conflict Resolution Mechanisms
            - Profissionalização sem perda de valores
            - Board of Directors vs Family Council
            - Estate Planning e Holding Structures
            
            Acadêmico rigoroso. 2600 palavras. Cite estudos longitudinais."""
        }
    ]
    
    print("🎓 ENTREPRENEURSHIP MASTERY TRAINING (PhD-Level)...")
    print("=" * 70)
    
    for i, topic in enumerate(topics, 1):
        print(f"\n[{i}/{len(topics)}] 📚 {topic['domain']}")
        
        try:
            response = llm.client.models.generate_content(
                model=llm.model,
                contents=topic['prompt'],
                config=types.GenerateContentConfig(
                    temperature=0.3,  # Baixa para rigor acadêmico
                    max_output_tokens=4000
                )
            )
            
            if response and response.text:
                doc_id = store.index_text(
                    text=response.text,
                    metadata={
                        'source': 'ACADEMIC_ENTREPRENEURSHIP',
                        'domain': topic['domain'],
                        'level': 'PhD',
                        'type': 'SCHOLARLY_CONTENT'
                    }
                )
                print(f"   ✅ Indexado: {doc_id[:16]}...")
                print(f"   📊 ~{len(response.text.split())} palavras")
            else:
                print(f"   ❌ Sem resposta")
                
        except Exception as e:
            print(f"   ⚠️  Erro: {str(e)}")
    
    print("\n" + "=" * 70)
    print("🎓 Empreendedorismo Nível Doutorado: COMPLETO")

if __name__ == "__main__":
    train_entrepreneurship()
