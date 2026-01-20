"""
⚖️ LEGAL & TAX KNOWLEDGE TRAINER
Direito e Tributário (Nível Acadêmico)
Fontes: Harvard Law, Yale Law, Receita Federal, Código Civil/Tributário
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codex_ia.core.vector_store import CodexVectorStore
from codex_ia.core.llm_client import GeminiClient
from google.genai import types

def train_legal_knowledge():
    """Indexa conhecimento jurídico e tributário brasileiro."""
    
    store = CodexVectorStore()
    llm = GeminiClient()
    
    topics = [
        {
            "domain": "CONTRACT_LAW_BRAZIL",
            "prompt": """Você é professor de Direito Civil (USP/FGV).
            
            Ensine: DIREITO CONTRATUAL BRASILEIRO
            
            Framework jurídico (Código Civil 2002):
            - Princípios Fundamentais (Autonomia da Vontade, Boa-Fé, Função Social)
            - Formação do Contrato (proposta, aceitação, vício de consentimento)
            - Validade (agente capaz, objeto lícito, forma prescrita)
            - Inadimplemento e Responsabilidade Civil
            - Contratos Típicos (compra/venda, locação, prestação serviços)
            - Rescisão, Resolução, Resilição
            - Arbitragem e Mediação (Lei 9.307/96)
            
            Acadêmico rigoroso. 3000 palavras. Cite artigos do CC."""
        },
        {
            "domain": "CORPORATE_LAW",
            "prompt": """Você é advogado empresarial (Pinheiro Neto, Machado Meyer).
            
            Explique: DIREITO SOCIETÁRIO & GOVERNANÇA CORPORATIVA
            
            Estrutura legal:
            - Tipos Societários (S.A., Ltda, Eireli, SLU)
            - Sociedade Anônima (Lei 6.404/76 - LSA)
            - Órgãos Sociais (AGO, Conselho, Diretoria)
            - Responsabilidade dos Administradores
            - Operações Societárias (M&A, cisão, fusão, incorporação)
            - Acordos de Acionistas
            - CVM e Mercado de Capitais
            
            PhD-level. 2800 palavras."""
        },
        {
            "domain": "TAX_LAW_BRAZIL",
            "prompt": """Você é tributarista (Receita Federal + Academia).
            
            Ensine: SISTEMA TRIBUTÁRIO NACIONAL
            
            Fundamentos constitucionais:
            - Princípios Tributários (Legalidade, Anterioridade, Capacidade Contributiva)
            - Competências Tributárias (União, Estados, Municípios)
            - Tributos Federais (IRPF, IRPJ, IPI, PIS, COFINS, CSLL)
            - ICMS (Estadual) e ISS (Municipal)
            - Simples Nacional (LC 123/2006)
            - Planejamento Tributário vs Evasão Fiscal
            - Processo Administrativo Fiscal (CARF)
            
            Rigoroso. 3200 palavras. Cite CTN."""
        },
        {
            "domain": "LABOR_LAW_BRAZIL",
            "prompt": """Você é especialista em Direito do Trabalho (CLT).
            
            Explique: DIREITO TRABALHISTA E REFORMA (Lei 13.467/2017)
            
            Framework CLT:
            - Relação de Emprego (requisitos: pessoalidade, subordinação, onerosidade)
            - Contrato de Trabalho (prazo determinado vs indeterminado)
            - Jornada de Trabalho (44h semanais, horas extras)
            - Férias, 13º Salário, FGTS
            - Rescisão Contratual (justa causa, sem justa causa, pedido demissão)
            - Reforma Trabalhista 2017 (terceirização, trabalho intermitente)
            - Justiça do Trabalho (CLT + TST)
            
            Acadêmico. 2700 palavras."""
        },
        {
            "domain": "DIGITAL_LAW_LGPD",
            "prompt": """Você é especialista em Direito Digital.
            
            Ensine: LGPD E PROTEÇÃO DE DADOS NO BRASIL
            
            Lei 13.709/2018:
            - Princípios da LGPD (finalidade, adequação, necessidade)
            - Bases Legais para Tratamento de Dados
            - Direitos dos Titulares (acesso, correção, portabilidade, exclusão)
            - DPO (Data Protection Officer) - Encarregado
            - Transferência Internacional de Dados
            - ANPD (Autoridade Nacional)
            - Sanções e Compliance
            - Comparação com GDPR (Europa)
            
            Rigor técnico-legal. 2600 palavras."""
        },
        {
            "domain": "INTELLECTUAL_PROPERTY",
            "prompt": """Você é advogado de PI (Propriedade Intelectual).
            
            Explique: PROPRIEDADE INTELECTUAL NO BRASIL
            
            Framework legal:
            - Direito Autoral (Lei 9.610/98)
            - Propriedade Industrial (Lei 9.279/96 - LPI)
            - Patentes (invenção vs modelo utilidade)
            - Marcas (registro INPI)
            - Software (proteção híbrida)
            - Segredo Industrial (Trade Secrets)
            - Licenciamento e Franchising
            - Violação e Enforcement
            
            Acadêmico. 2500 palavras."""
        }
    ]
    
    print("⚖️ LEGAL & TAX KNOWLEDGE (Academic Level)...")
    print("=" * 70)
    
    for i, topic in enumerate(topics, 1):
        print(f"\n[{i}/{len(topics)}] 📜 {topic['domain']}")
        
        try:
            response = llm.client.models.generate_content(
                model=llm.model,
                contents=topic['prompt'],
                config=types.GenerateContentConfig(
                    temperature=0.1,  # Muito baixa para precisão legal
                    max_output_tokens=4000
                )
            )
            
            if response and response.text:
                doc_id = store.index_text(
                    text=response.text,
                    metadata={
                        'source': 'ACADEMIC_LAW',
                        'domain': topic['domain'],
                        'level': 'Law_School',
                        'jurisdiction': 'Brazil',
                        'type': 'LEGAL_KNOWLEDGE'
                    }
                )
                print(f"   ✅ {doc_id[:16]}... | ~{len(response.text.split())} palavras")
                
        except Exception as e:
            print(f"   ⚠️  {str(e)}")
    
    print("\n" + "=" * 70)
    print("✅ Direito: Base Jurídica Completa")
    print("⚠️  DISCLAIMER: Apenas educacional, não é consultoria jurídica")

if __name__ == "__main__":
    train_legal_knowledge()
