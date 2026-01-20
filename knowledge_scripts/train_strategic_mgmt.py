"""
🏛️ STRATEGIC MANAGEMENT TRAINER
Gestão Estratégica de Negócios (Nível Acadêmico)
Fontes: Porter, Mintzberg, Barney, Hamel, Prahalad
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codex_ia.core.vector_store import CodexVectorStore
from codex_ia.core.llm_client import GeminiClient
from google.genai import types

def train_strategic_management():
    """Indexa teorias clássicas e contemporâneas de estratégia empresarial."""
    
    store = CodexVectorStore()
    llm = GeminiClient()
    
    topics = [
        {
            "domain": "COMPETITIVE_STRATEGY_PORTER",
            "prompt": """Você é Michael Porter (Harvard Business School).
            
            Ensine suas teorias fundamentais de ESTRATÉGIA COMPETITIVA:
            
            1. Five Forces Framework (análise estrutural da indústria)
            2. Generic Strategies (Cost Leadership, Differentiation, Focus)
            3. Value Chain Analysis
            4. Competitive Advantage of Nations (Diamond Model)
            5. Shared Value Creation
            
            Rigor acadêmico: defina cada conceito, explique aplicações práticas,
            cite limitações teóricas debatidas por Mintzberg e outros.
            
            3500 palavras. Nível: Mestrado/Doutorado."""
        },
        {
            "domain": "RESOURCE_BASED_VIEW",
            "prompt": """Você é Jay Barney (University of Utah).
            
            Explique: RESOURCE-BASED VIEW (RBV) OF THE FIRM
            
            Teoria profunda:
            - VRIN Framework (Valuable, Rare, Inimitable, Non-substitutable)
            - Dynamic Capabilities (Teece, Pisano, Shuen)
            - Knowledge-Based View (Grant)
            - Core Competencies (Prahalad & Hamel)
            - Absorptive Capacity (Cohen & Levinthal)
            
            Contraste com Industrial Organization (IO) perspective.
            Acadêmico rigoroso. 3000 palavras."""
        },
        {
            "domain": "BLUE_OCEAN_STRATEGY",
            "prompt": """Você é W. Chan Kim (INSEAD).
            
            Ensine: BLUE OCEAN STRATEGY vs RED OCEAN COMPETITION
            
            Framework completo:
            - Value Innovation (qualidade + preço)
            - Strategy Canvas Tool
            - Four Actions Framework (Eliminate-Reduce-Raise-Create)
            - Six Paths Framework
            - Casos canônicos: Cirque du Soleil, Nintendo Wii, Southwest Airlines
            
            Crítica acadêmica: responda às objeções de Porter sobre sustentabilidade.
            2800 palavras de análise."""
        },
        {
            "domain": "STRATEGIC_PLANNING_SYSTEMS",
            "prompt": """Você é Henry Mintzberg (McGill University).
            
            Ensine: ESCOLAS DE PENSAMENTO ESTRATÉGICO (Safari da Estratégia)
            
            10 Escolas:
            1. Design (SWOT)
            2. Planning (Ansoff)
            3. Positioning (Porter)
            4. Entrepreneurial (vision-driven)
            5. Cognitive (mental frames)
            6. Learning (emergent strategy)
            7. Power (negotiation)
            8. Cultural (social process)
            9. Environmental (reactive)
            10. Configuration (transformation)
            
            Critique: "Ascensão e Queda do Planejamento Estratégico".
            PhD-level. 3200 palavras."""
        },
        {
            "domain": "BALANCED_SCORECARD",
            "prompt": """Você é Robert Kaplan (Harvard).
            
            Explique: BALANCED SCORECARD & STRATEGY MAPS
            
            Estrutura científica:
            - 4 Perspectivas (Financial, Customer, Internal Process, Learning & Growth)
            - Causa-Efeito entre indicadores
            - Leading vs Lagging Indicators
            - Strategy-Focused Organization
            - Integração com Activity-Based Costing (ABC)
            
            Casos: Mobil, Cigna, Unibanco.
            Rigor acadêmico. 2700 palavras."""
        }
    ]
    
    print("🏛️ STRATEGIC MANAGEMENT (Academic Level)...")
    print("=" * 70)
    
    for i, topic in enumerate(topics, 1):
        print(f"\n[{i}/{len(topics)}] 📖 {topic['domain']}")
        
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
                        'source': 'ACADEMIC_STRATEGY',
                        'domain': topic['domain'],
                        'level': 'Graduate',
                        'type': 'MANAGEMENT_THEORY'
                    }
                )
                print(f"   ✅ {doc_id[:16]}... | ~{len(response.text.split())} palavras")
                
        except Exception as e:
            print(f"   ⚠️  {str(e)}")
    
    print("\n" + "=" * 70)
    print("✅ Gestão Estratégica: Biblioteca Completa")

if __name__ == "__main__":
    train_strategic_management()
