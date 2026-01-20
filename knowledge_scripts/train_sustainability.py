"""
🌍 SUSTAINABLE DEVELOPMENT TRAINER
Crescimento Sustentável (Nível Acadêmico - ESG/UN SDGs)
Fontes: UN, IPCC, Ellen MacArthur Foundation, B Lab
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codex_ia.core.vector_store import CodexVectorStore
from codex_ia.core.llm_client import GeminiClient
from google.genai import types

def train_sustainability():
    """Conhecimento profundo sobre desenvolvimento sustentável e ESG."""
    
    store = CodexVectorStore()
    llm = GeminiClient()
    
    topics = [
        {
            "domain": "CIRCULAR_ECONOMY",
            "prompt": """Você é pesquisador da Ellen MacArthur Foundation.
            
            Ensine: CIRCULAR ECONOMY PRINCIPLES & BUSINESS MODELS
            
            Framework acadêmico:
            - Butterfly Diagram (biological vs technical cycles)
            - ReSOLVE Framework (Regenerate, Share, Optimize, Loop, Virtualize, Exchange)
            - Product-as-a-Service models
            - Design for Disassembly
            - Industrial Symbiosis (Kalundborg example)
            - Extended Producer Responsibility (EPR)
            - Life Cycle Assessment (LCA) methodology
            
            PhD-level. 3000 palavras. Casos: Philips, Patagonia, Interface."""
        },
        {
            "domain": "ESG_INTEGRATION",
            "prompt": """Você é analista do Sustainability Accounting Standards Board (SASB).
            
            Explique: ESG FRAMEWORKS & MATERIALITY ASSESSMENT
            
            Rigoroso:
            - GRI Standards (Global Reporting Initiative)
            - SASB Materiality Map (77 indústrias)
            - TCFD Climate Risk Disclosure
            - CDP (Carbon Disclosure Project)
            - B Corp Certification (Impact Assessment)
            - EU Taxonomy for Sustainable Activities
            - Greenwashing detection
            
            Acadêmico. 2800 palavras. Evidências empíricas sobre ROI de ESG."""
        },
        {
            "domain": "CLIMATE_SCIENCE_BUSINESS",
            "prompt": """Você é cientista climático do IPCC (Painel Intergovernamental).
            
            Ensine: CLIMATE CHANGE MITIGATION FOR BUSINESS
            
            Científico:
            - Carbon Pricing mechanisms (cap-and-trade, carbon tax)
            - Science-Based Targets (SBTi) methodology
            - Scope 1, 2, 3 Emissions accounting
            - Renewable Energy Transition economics
            - Carbon Offset vs Carbon Removal
            - Net-Zero vs Carbon Neutral
            - Stranded Assets risk
            
            PhD-level. 3200 palavras. Rigor climático + viabilidade econômica."""
        },
        {
            "domain": "SOCIAL_ENTREPRENEURSHIP",
            "prompt": """Você é Muhammad Yunus (Nobel da Paz, Grameen Bank).
            
            Explique: SOCIAL BUSINESS THEORY & IMPACT INVESTING
            
            Acadêmico:
            - Social Business vs Charity vs Traditional Business
            - Impact Measurement (IRIS+, GIIRS)
            - Theory of Change (ToC) design
            - Blended Value Proposition
            - Patient Capital vs Venture Philanthropy
            - Bottom of the Pyramid (BoP) strategies
            - Casos: Grameen, TOMS, Aravind Eye Care
            
            Rigor acadêmico. 2700 palavras."""
        },
        {
            "domain": "SUSTAINABLE_DEVELOPMENT_GOALS",
            "prompt": """Você é coordenador de SDGs da ONU (Jeffrey Sachs).
            
            Ensine: 17 SUSTAINABLE DEVELOPMENT GOALS - IMPLEMENTATION
            
            Framework científico:
            - SDG Interlinkages (system dynamics)
            - Indicator Framework (232 indicators)
            - National Voluntary Reviews (VNRs)
            - Multi-Stakeholder Partnerships
            - Financing mechanisms (blended finance)
            - Leave No One Behind principle
            - SDG Localization (municipal level)
            
            Acadêmico profundo. 3000 palavras. Casos: Nordics, Rwanda, Costa Rica."""
        },
        {
            "domain": "REGENERATIVE_AGRICULTURE",
            "prompt": """Você é cientista agrário (Rodale Institute).
            
            Explique: REGENERATIVE AGRICULTURE & FOOD SYSTEMS
            
            Científico:
            - Soil Health fundamentals (carbon sequestration)
            - Agroecology vs Conventional Farming
            - Permaculture design principles
            - Holistic Planned Grazing
            - Supply Chain transparency (blockchain)
            - Food Waste reduction strategies
            - True Cost Accounting
            
            PhD-level. 2600 palavras. Evidências de yield, carbono, biodiversity."""
        }
    ]
    
    print("🌍 SUSTAINABLE DEVELOPMENT KNOWLEDGE (Academic)...")
    print("=" * 70)
    
    for i, topic in enumerate(topics, 1):
        print(f"\n[{i}/{len(topics)}] 🌱 {topic['domain']}")
        
        try:
            response = llm.client.models.generate_content(
                model=llm.model,
                contents=topic['prompt'],
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=4000
                )
            )
            
            if response and response.text:
                doc_id = store.index_text(
                    text=response.text,
                    metadata={
                        'source': 'ACADEMIC_SUSTAINABILITY',
                        'domain': topic['domain'],
                        'level': 'PhD',
                        'type': 'ESG_KNOWLEDGE',
                        'ethical': True
                    }
                )
                print(f"   ✅ {doc_id[:16]}... | ~{len(response.text.split())} palavras")
                
        except Exception as e:
            print(f"   ⚠️  {str(e)}")
    
    print("\n" + "=" * 70)
    print("✅ Sustainability Knowledge: Complete & Ethical")

if __name__ == "__main__":
    train_sustainability()
