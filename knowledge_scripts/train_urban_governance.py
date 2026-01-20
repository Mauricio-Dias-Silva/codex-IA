"""
🏙️ URBAN GOVERNANCE & SMART CITIES TRAINER
Gestão de Cidades (Nível Acadêmico - Urban Planning)
Fontes: MIT, LSE Cities, UN-Habitat, Brookings Institution
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codex_ia.core.vector_store import CodexVectorStore
from codex_ia.core.llm_client import GeminiClient
from google.genai import types

def train_urban_governance():
    """Conhecimento de governança municipal e planejamento urbano."""
    
    store = CodexVectorStore()
    llm = GeminiClient()
    
    topics = [
        {
            "domain": "SMART_CITIES_FRAMEWORK",
            "prompt": """Você é pesquisador do MIT Media Lab (Carlo Ratti).
            
            Ensine: SMART CITIES - URBAN INFORMATICS & IOT GOVERNANCE
            
            Estrutura acadêmica:
            - Definição ISO 37120 (Sustainable Cities Indicators)
            - Sensor Networks deployment (Barcelona, Singapore)
            - Citizen Engagement Platforms (participatory budgeting)
            - Data Privacy em vigilância urbana
            - Mobility-as-a-Service (MaaS) integration
            - Energy Grid Optimization (smart meters)
            - Waste Management inteligente
            
            PhD-level. 3000 palavras. Ético e baseado em evidências."""
        },
        {
            "domain": "PARTICIPATORY_BUDGETING",
            "prompt": """Você é especialista em Orçamento Participativo (Porto Alegre Model).
            
            Explique: PARTICIPATORY BUDGETING THEORY & PRACTICE
            
            Rigor acadêmico:
            - Origens (RS, Brasil - 1989)
            - Deliberative Democracy theory (Habermas)
            - Assemblies Structure (regional/thematic)
            - PB Digital (Paris, Lisboa, NYC)
            - Impact on inequality reduction (World Bank studies)
            - Critiques: elite capture, low turnout
            - Escalabilidade para metrópoles
            
            Cite estudos empíricos. 2600 palavras."""
        },
        {
            "domain": "SUSTAINABLE_URBAN_PLANNING",
            "prompt": """Você é professor de Urban Planning (LSE Cities - Ricky Burdett).
            
            Ensine: SUSTAINABLE URBAN DEVELOPMENT (SDG 11)
            
            Frameworks:
            - Compact City Model (densidade vs sprawl)
            - Transit-Oriented Development (TOD)
            - Green Infrastructure (parks, permeable surfaces)
            - Affordable Housing strategies (Vienna Social Housing)
            - Mixed-Use Zoning vs Euclidean Zoning
            - Climate Adaptation Plans
            - Circular Economy in cities
            
            Acadêmico. 3200 palavras. Casos: Copenhagen, Curitiba, Medellín."""
        },
        {
            "domain": "PUBLIC_GOVERNANCE_NEW_MODELS",
            "prompt": """Você é pesquisador de Public Administration (Harvard Kennedy School).
            
            Explique: NEW PUBLIC GOVERNANCE PARADIGMS
            
            Teorias:
            - New Public Management (NPM) vs Traditional Public Administration
            - Network Governance (collaborative governance)
            - Co-production of Public Services
            - Accountability Mechanisms (horizontal vs vertical)
            - E-Government Maturity Models
            - Transparency Laws (FOIA, LAI)
            - Anti-Corruption Systems (Integrity Pacts)
            
            Rigor acadêmico. 2800 palavras."""
        },
        {
            "domain": "RESILIENT_CITIES",
            "prompt": """Você é diretor da Resilient Cities Network (Rockefeller Foundation).
            
            Ensine: URBAN RESILIENCE FRAMEWORK
            
            Científico:
            - Resilience vs Robustness vs Adaptability
            - Shocks vs Stresses (disasters vs chronic issues)
            - City Resilience Index (Arup/Rockefeller)
            - Nature-Based Solutions (green/blue infrastructure)
            - Community-Based Disaster Risk Reduction
            - Post-Disaster Recovery Planning
            - Casos: New Orleans (Katrina), Christchurch (earthquake)
            
            PhD-level. 2700 palavras."""
        }
    ]
    
    print("🏙️ URBAN GOVERNANCE & SMART CITIES (Academic)...")
    print("=" * 70)
    
    for i, topic in enumerate(topics, 1):
        print(f"\n[{i}/{len(topics)}] 🏛️ {topic['domain']}")
        
        try:
            response = llm.client.models.generate_content(
                model=llm.model,
                contents=topic['prompt'],
                config=types.GenerateContentConfig(
                    temperature=0.25,
                    max_output_tokens=4000
                )
            )
            
            if response and response.text:
                doc_id = store.index_text(
                    text=response.text,
                    metadata={
                        'source': 'ACADEMIC_URBAN_PLANNING',
                        'domain': topic['domain'],
                        'level': 'Graduate',
                        'type': 'URBAN_GOVERNANCE'
                    }
                )
                print(f"   ✅ {doc_id[:16]}... | ~{len(response.text.split())} palavras")
                
        except Exception as e:
            print(f"   ⚠️  {str(e)}")
    
    print("\n" + "=" * 70)
    print("✅ Urban Governance: Knowledge Base Ready")

if __name__ == "__main__":
    train_urban_governance()
