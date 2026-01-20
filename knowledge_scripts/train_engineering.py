"""
🏗️ ENGINEERING KNOWLEDGE TRAINER
Engenharia (Múltiplas Disciplinas - Nível Acadêmico)
Fontes: MIT, Stanford, CREA, NBRs
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codex_ia.core.vector_store import CodexVectorStore
from codex_ia.core.llm_client import GeminiClient
from google.genai import types

def train_engineering_knowledge():
    """Indexa conhecimento de engenharia multidisciplinar."""
    
    store = CodexVectorStore()
    llm = GeminiClient()
    
    topics = [
        {
            "domain": "STRUCTURAL_ENGINEERING",
            "prompt": """Você é engenheiro civil estrutural (MIT).
            
            Ensine: ENGENHARIA ESTRUTURAL & ANÁLISE DE ESTRUTURAS
            
            Fundamentos técnicos:
            - Estática e Resistência dos Materiais
            - Tipos de Carregamento (permanente, acidental, vento, sismo)
            - Elementos Estruturais (vigas, pilares, lajes)
            - Concreto Armado (NBR 6118)
            - Estruturas Metálicas (NBR 8800)
            - Análise Matricial (MEF - Método dos Elementos Finitos)
            - Dimensionamento e Verificação
            - Patologias Estruturais
            
            Rigor acadêmico + prático. 3000 palavras."""
        },
        {
            "domain": "ELECTRICAL_POWER_SYSTEMS",
            "prompt": """Você é engenheiro eletricista (Stanford).
            
            Explique: SISTEMAS ELÉTRICOS DE POTÊNCIA
            
            Fundamentos:
            - Geração de Energia (hidro, térmica, solar, eólica)
            - Transmissão e Distribuição (linhas AT, MT, BT)
            - Transformadores e Subestações
            - Proteção de Sistemas (relés, disjuntores)
            - Qualidade de Energia (harmônicos, fator potência)
            - Smart Grids e Microgrids
            - Normas NBR 5410 e NR-10
            
            PhD-level. 2800 palavras."""
        },
        {
            "domain": "INDUSTRIAL_AUTOMATION",
            "prompt": """Você é especialista em automação (SENAI/ISA).
            
            Ensine: AUTOMAÇÃO INDUSTRIAL & CONTROLE DE PROCESSOS
            
            Tecnologias:
            - CLPs (Controladores Lógicos Programáveis)
            - SCADA Systems (Supervisory Control)
            - Instrumentação Industrial (sensores, atuadores)
            - Redes Industriais (Profibus, Modbus, Ethernet/IP)
            - Controle PID (Proporcional-Integral-Derivativo)
            - Industry 4.0 (IoT, Digital Twin)
            - Segurança Funcional (IEC 61508, SIL)
            
            Rigoroso. 3200 palavras."""
        },
        {
            "domain": "MECHANICAL_DESIGN",
            "prompt": """Você é engenheiro mecânico (MIT Mechanical Engineering).
            
            Explique: PROJETO MECÂNICO & ANÁLISE DE RESISTÊNCIA
            
            Conceitos fundamentais:
            - Mecânica dos Sólidos (tensão, deformação, fadiga)
            - Elementos de Máquinas (engrenagens, rolamentos, eixos)
            - Seleção de Materiais (aços, ligas, compósitos)
            - CAD/CAE/CAM (SolidWorks, ANSYS)
            - Análise de Falhas (Goodman, S-N curves)
            - Manufatura (usinagem, fundição, soldagem)
            - Tolerâncias e Ajustes (ISO)
            
            Acadêmico. 2700 palavras."""
        },
        {
            "domain": "CONSTRUCTION_MANAGEMENT",
            "prompt": """Você é especialista em Gestão de Obras (PMI Construction).
            
            Ensine: GERENCIAMENTO DE PROJETOS DE CONSTRUÇÃO
            
            Framework:
            - Planejamento de Obras (WBS, Cronograma)
            - Orçamentação (BDI, composições unitárias)
            - Controle de Custos (Curva S, Earned Value)
            - Logística de Canteiro
            - Gestão de Riscos (FMEA, análise qualitativa)
            - Qualidade em Obras (PBQP-H, ISO 9001)
            - BIM (Building Information Modeling)
            - Lean Construction
            
            Rigor técnico. 2600 palavras."""
        },
        {
            "domain": "WATER_RESOURCES_ENGINEERING",
            "prompt": """Você é engenheiro de recursos hídricos.
            
            Explique: ENGENHARIA DE RECURSOS HÍDRICOS
            
            Fundamentos:
            - Hidrologia (ciclo hidrológico, bacias)
            - Hidráulica (escoamento, redes)
            - Sistemas de Abastecimento de Água
            - Tratamento de Água (ETA processes)
            - Esgotamento Sanitário e ETEs
            - Drenagem Urbana
            - Barragens e Reservatórios
            - Gestão Integrada de Recursos Hídricos
            
            Acadêmico. 2500 palavras."""
        }
    ]
    
    print("🏗️ ENGINEERING KNOWLEDGE (Academic Level)...")
    print("=" * 70)
    
    for i, topic in enumerate(topics, 1):
        print(f"\n[{i}/{len(topics)}] ⚙️ {topic['domain']}")
        
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
                        'source': 'ACADEMIC_ENGINEERING',
                        'domain': topic['domain'],
                        'level': 'Engineering_School',
                        'type': 'TECHNICAL_KNOWLEDGE'
                    }
                )
                print(f"   ✅ {doc_id[:16]}... | ~{len(response.text.split())} palavras")
                
        except Exception as e:
            print(f"   ⚠️  {str(e)}")
    
    print("\n" + "=" * 70)
    print("✅ Engenharia: Base Técnica Multidisciplinar")

if __name__ == "__main__":
    train_engineering_knowledge()
