"""
🌌 QUANTUM LEAP - PART 2: SOCIETY & HUMAN SCIENCES
Expansão de Conhecimento: Medicina, Direito, Negócios e Humanidades.

Domínios:
- Medicina & Saúde (Clínica, Neuro, Emergência)
- Direito Brasileiro (Constitucional, Civil, Digital)
- Negócios & Finanças (Estratégia, Valuation, Marketing)
- Psicologia & Neurociência
- Agricultura & Sustentabilidade
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codex_ia.core.vector_store import CodexVectorStore
from codex_ia.core.llm_client import GeminiClient
from google.genai import types
import time

class QuantumLeapTrainer:
    """Massive knowledge expansion with quality control."""
    
    def __init__(self):
        self.store = CodexVectorStore()
        self.llm = GeminiClient()
        self.indexed_count = 0
        
    def generate_and_index(self, domain: str, prompt: str, metadata: dict):
        """Generate knowledge and index with quality check."""
        try:
            response = self.llm.client.models.generate_content(
                model=self.llm.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=4000
                )
            )
            
            if response and response.text and len(response.text) > 500:
                doc_id = self.store.index_text(
                    text=response.text,
                    metadata=metadata
                )
                self.indexed_count += 1
                word_count = len(response.text.split())
                
                # Logic to handle list return from vector_store (FIXED)
                doc_preview = str(doc_id[0]) if doc_id and isinstance(doc_id, list) else "indexed"
                
                print(f"   ✅ {doc_preview[:12]}... | ~{word_count} palavras")
                return True
            else:
                print(f"   ⚠️  Resposta muito curta, pulando")
                return False
                
        except Exception as e:
            print(f"   ❌ Erro: {str(e)[:50]}...")
            return False

def run_quantum_leap_part2():
    """Execute massive knowledge expansion - PART 2."""
    
    trainer = QuantumLeapTrainer()
    
    # === TOPIC LIST PART 2 (30 topics) ===
    topics = [
        
        # === MEDICINA & SAÚDE (6 topics) ===
        {
            "category": "MEDICINE_CLINICAL",
            "domain": "CARDIOLOGY_ADVANCED",
            "prompt": """Você é cardiologista sênior.
            
Ensine: CARDIOLOGIA CLÍNICA AVANÇADA

Tópicos:
- Fisiopatologia da Insuficiência Cardíaca
- Interpretação avançada de ECG (bloqueios, isquemias)
- Farmacologia cardiovascular (Betabloqueadores, IECA/BRA)
- Síndromes Coronarianas Agudas
- Arritmias complexas e ablação
- Prevenção cardiovascular secundária

Residência médica level. 3200 palavras."""
        },
        {
            "category": "MEDICINE_NEURO",
            "domain": "NEUROLOGY_CLINICAL",
            "prompt": """Você é neurologista.
            
Explique: NEUROLOGIA CLÍNICA

Tópicos:
- AVC: Protocolos de trombólise e manuseio
- Epilepsia: Classificação e tratamento medicamentoso
- Doenças Desmielinizantes (Esclerose Múltipla)
- Cefaleias: Migrânea vs Tensional vs Salvas
- Exame neurológico detalhado (pares cranianos, reflexos)
- Neuroimagem: O que buscar em TC e RM

Técnico profundo. 3000 palavras."""
        },
        {
            "category": "MEDICINE_EMERGENCY",
            "domain": "EMERGENCY_MEDICINE",
            "prompt": """Você é médico emergencista.
            
Ensine: MEDICINA DE EMERGÊNCIA & TRAUMA

Tópicos:
- Protocolo ATLS (ABCDE do trauma)
- PCR e ACLS (Ritmos chocáveis vs não chocáveis)
- Manejo de Via Aérea Difícil (RSI - Sequência Rápida)
- Sepsis Bundle (1h e 3h)
- Intoxicações Exógenas comuns
- Choque (Hipovolêmico, Cardiogênico, Distributivo)

Prático e técnico. 3000 palavras."""
        },
        {
            "category": "MEDICINE_PSYCH",
            "domain": "PSYCHIATRY_CLINICAL",
            "prompt": """Você é psiquiatra.
            
Explique: PSIQUIATRIA CLÍNICA E PSICOFARMACOLOGIA

Tópicos:
- Transtornos de Humor (Depressão Maior, Bipolar)
- Esquizofrenia e Psicoses
- Transtornos de Ansiedade (Pânico, TAG)
- Psicofarmacologia: ISRS, Duais, Antipsicóticos, Estabilizadores
- Neurobiologia dos transtornos mentais
- Emergências psiquiátricas

Acadêmico. 3000 palavras."""
        },
        {
            "category": "MEDICINE_BASIC",
            "domain": "IMMUNOLOGY_ADVANCED",
            "prompt": """Você é imunologista.
            
Ensine: IMUNOLOGIA MÉDICA

Tópicos:
- Imunidade Inata vs Adquirida
- Células T e B (maturação e ativação)
- Citocinas e cascatas inflamatórias
- Hipersensibilidades (Tipos I, II, III, IV)
- Imunodeficiências primárias
- Mecanismos de doenças autoimunes

PhD level. 3000 palavras."""
        },
        {
            "category": "MEDICINE_BASIC",
            "domain": "PATHOLOGY_GENERAL",
            "prompt": """Você é patologista.
            
Explique: PATOLOGIA GERAL

Tópicos:
- Adaptação celular (hipertrofia, metaplasia)
- Lesão e morte celular (necrose vs apoptose)
- Inflamação aguda e crônica
- Reparo tecidual e cicatrização
- Carcinogênese e Neoplasias (benigno vs maligno)
- Distúrbios hemodinâmicos (trombose, embolia)

Técnico. 2800 palavras."""
        },


        # === DIREITO & LEGISLAÇÃO (6 topics) ===
        {
            "category": "LAW_BRAZIL",
            "domain": "CONSTITUTIONAL_LAW_BR",
            "prompt": """Você é jurista constitucionalista brasileiro.
            
Ensine: DIREITO CONSTITUCIONAL (CF/88)

Tópicos:
- Controle de Constitucionalidade (Concentrado vs Difuso)
- Direitos e Garantias Fundamentais (Art. 5º detalhado)
- Organização dos Poderes e Freios e Contrapesos
- Processo Legislativo Constitucional
- Remédios Constitucionais (HC, MS, MI)
- Ações do Controle Concentrado (ADI, ADC, ADPF)

Nível OAB/Concurso Juiz. 3500 palavras."""
        },
        {
            "category": "LAW_BRAZIL",
            "domain": "CIVIL_LAW_CONTRACTS",
            "prompt": """Você é professor de Direito Civil.
            
Explique: TEORIA GERAL DOS CONTRATOS E OBRIGAÇÕES

Tópicos:
- Princípios contratuais (Boa-fé objetiva, Função social)
- Vícios do negócio jurídico
- Inadimplemento e Mora
- Contratos em espécie: Compra e Venda, Locação
- Responsabilidade Civil (Subjetiva vs Objetiva)
- Prescrição e Decadência

Jurídico técnico. 3000 palavras."""
        },
        {
            "category": "LAW_BRAZIL",
            "domain": "PENAL_LAW_BR",
            "prompt": """Você é criminalista.
            
Ensine: DIREITO PENAL - PARTE GERAL

Tópicos:
- Teoria do Delito (Fato Típico, Ilícito, Culpável)
- Dolo e Culpa (Teorias)
- Erro de Tipo e Erro de Proibição
- Concurso de Pessoas e de Crimes
- Teoria da Pena e Dosimetria
- Excludentes de Ilicitude

Nível Concurso MP/Magistratura. 3000 palavras."""
        },
        {
            "category": "LAW_TECH",
            "domain": "DIGITAL_LAW_LGPD",
            "prompt": """Você é especialista em Direito Digital.
            
Explique: DIREITO DIGITAL E LGPD

Tópicos:
- Lei Geral de Proteção de Dados (Fundamentos e bases legais)
- Direitos dos Titulares de Dados
- Responsabilidade Civil na Internet (Marco Civil)
- Smart Contracts e validade jurídica
- Crimes Cibernéticos (Lei Carolina Dieckmann e atualizações)
- Compliance Digital e Governança de Dados

Técnico jurídico. 3000 palavras."""
        },
        {
            "category": "LAW_ADMINISTRATIVE",
            "domain": "ADMIN_LAW_PUBLIC",
            "prompt": """Você é administrativista.
            
Ensine: DIREITO ADMINISTRATIVO E LICITAÇÕES

Tópicos:
- Princípios da Administração Pública (LIMPE)
- Atos Administrativos (Atributos e Elementos)
- Nova Lei de Licitações (Lei 14.133/21) detalhada
- Contratos Administrativos
- Improbidade Administrativa (atualizações)
- Processo Administrativo Federal

Nível avançado. 3200 palavras."""
        },
        {
            "category": "LAW_TAX",
            "domain": "TAX_LAW_BR",
            "prompt": """Você é tributarista.
            
Explique: SISTEMA TRIBUTÁRIO NACIONAL

Tópicos:
- Princípios constitucionais tributários
- Limitações ao poder de tributar
- Espécies tributárias (Impostos, Taxas, Contribuições)
- Obrigação e Crédito Tributário
- Prescrição e Decadência tributária
- Reforma Tributária (visão geral técnica)

Técnico. 3000 palavras."""
        },


        # === NEGÓCIOS & ECONOMIA (6 topics) ===
        {
            "category": "BUSINESS_STRATEGY",
            "domain": "STRATEGIC_MANAGEMENT",
            "prompt": """Você é consultor de estratégia (MBB level).
            
Ensine: GESTÃO ESTRATÉGICA AVANÇADA

Tópicos:
- Análise Competitiva (5 Forças, PESTEL, VRIO)
- Estratégias Genéricas de Porter (Custo vs Diferenciação)
- Blue Ocean Strategy e Inovação de Valor
- Balanced Scorecard (BSC) e OKRs
- Estratégia Corporativa vs Unidade de Negócio
- Gestão de Mudança (Kotter, ADKAR)

MBA Level. 3500 palavras."""
        },
        {
            "category": "BUSINESS_FINANCE",
            "domain": "CORPORATE_VALUATION",
            "prompt": """Você é especialista em Valuation.
            
Explique: VALUATION E FINANÇAS CORPORATIVAS

Tópicos:
- Fluxo de Caixa Descontado (DCF) detalhado
- Cálculo do WACC (Ke, Kd, Beta)
- Múltiplos de Mercado (P/E, EV/EBITDA)
- Análise de Demonstrações Financeiras (Vertical/Horizontal)
- VPL, TIR e Payback
- Gestão de Capital de Giro

Técnico financeiro. 3200 palavras."""
        },
        {
            "category": "BUSINESS_MARKETING",
            "domain": "MODERN_MARKETING",
            "prompt": """Você é CMO de tech company.
            
Ensine: MARKETING ESTRATÉGICO E DIGITAL

Tópicos:
- Segmentação, Targeting e Posicionamento (STP)
- Branding e Brand Equity (Keller/Aaker)
- Funil de Vendas e Jornada do Cliente
- Growth Hacking e Métricas (CAC, LTV, Churn)
- Marketing de Conteúdo e Inbound
- Psicologia do Consumidor (Vieses cognitivos em vendas)

Profissional. 3000 palavras."""
        },
        {
            "category": "BUSINESS_STARTUP",
            "domain": "STARTUP_ECOSYSTEM",
            "prompt": """Você é fundador de unicórnio.
            
Explique: METODOLOGIA LEAN STARTUP E VEN TURE CAPITAL

Tópicos:
- Lean Startup (Build-Measure-Learn, MVP)
- Product-Market Fit
- Business Model Canvas e Lean Canvas
- Fundraising: Series A, B, C, Seed, Angel
- Term Sheets e Cap Table basics
- Pitch Deck perfeito
- Escalar operações (Blitzscaling)

Prático e técnico. 3000 palavras."""
        },
        {
            "category": "ECONOMICS",
            "domain": "MACROECONOMICS",
            "prompt": """Você é economista macro.
            
Ensine: MACROECONOMIA E POLÍTICA MONETÁRIA

Tópicos:
- PIB, Inflação e Desemprego (Curva de Phillips)
- Política Fiscal vs Monetária
- Bancos Centrais e Taxas de Juros (Selic, Fed Funds)
- Câmbio e Balança de Pagamentos
- Teorias de Crescimento Econômico (Solow)
- Ciclos Econômicos

Acadêmico. 3000 palavras."""
        },
        {
            "category": "AGRIBUSINESS",
            "domain": "PRECISION_AGRICULTURE",
            "prompt": """Você é engenheiro agrônomo tech.
            
Explique: AGRICULTURA DE PRECISÃO E AGRO 4.0

Tópicos:
- Sensoriamento remoto e Drones no agro
- Sistemas de Informação Geográfica (SIG/GIS)
- Taxa Variável de Aplicação (VRT)
- Monitoramento de colheita e produtividade
- Biotecnologia e melhoramento genético moderno
- Sustentabilidade e créditos de carbono no agro

Técnico avançado. 3000 palavras."""
        },


        # === PSICOLOGIA & HUMANIDADES (6 topics) ===
        {
            "category": "PSYCHOLOGY",
            "domain": "CBT_THERAPY",
            "prompt": """Você é terapeuta TCC.
            
Ensine: TERAPIA COGNITIVO-COMPORTAMENTAL (TCC)

Tópicos:
- Modelo Cognitivo (Situação, Pensamento, Emoção, Comportamento)
- Distorções Cognitivas comuns
- Crenças Centrais e Intermediárias
- Reestruturação Cognitiva
- Experimentos Comportamentais
- Tratamento de Ansiedade e Depressão via TCC

Acadêmico prático. 3000 palavras."""
        },
        {
            "category": "PSYCHOLOGY",
            "domain": "NEUROSCIENCE_BEHAVIOR",
            "prompt": """Você é neurocientista comportamental.
            
Explique: NEUROCIÊNCIA DO COMPORTAMENTO

Tópicos:
- Neurotransmissores (Dopamina, Serotonina, GABA)
- Sistema Límbico e Emoções
- Córtex Pré-frontal e Funções Executivas
- Neuroplasticidade e Aprendizagem
- Mecanismos do Vício e Recompensa
- Sono e Memória

Científico rigoroso. 3200 palavras."""
        },
        {
            "category": "HISTORY",
            "domain": "GEOPOLITICS_MODERN",
            "prompt": """Você é analista geopolítico.
            
Ensine: GEOPOLÍTICA MUNDIAL MODERNA

Tópicos:
- Teorias Geopolíticas (Heartland, Rimland)
- Ordem Mundial Pós-Guerra Fria e Multipolaridade
- Conflitos no Oriente Médio (histórico e atual)
- Ascensão da China e Belt and Road Initiative
- Geopolítica da Energia (Petróleo, Gás, Renováveis)
- Soft Power vs Hard Power

Analítico profundo. 3200 palavras."""
        },
        {
            "category": "HISTORY",
            "domain": "BRAZIL_HISTORY_DEEP",
            "prompt": """Você é historiador brasileiro.
            
Explique: FORMAÇÃO SÓCIO-POLÍTICA DO BRASIL

Tópicos:
- Colonização e Ciclos Econômicos (Açúcar, Ouro, Café)
- Escravidão e suas consequências estruturais
- Independência e Período Imperial
- Era Vargas e Industrialização
- Ditadura Militar (economia e política)
- Redemocratização e Constituição de 88

Acadêmico crítico. 3000 palavras."""
        },
        {
            "category": "PHILOSOPHY",
            "domain": "MODERN_PHILOSOPHY",
            "prompt": """Você é filósofo.
            
Ensine: FILOSOFIA MODERNA E CONTEMPORÂNEA

Tópicos:
- Racionalismo (Descartes) vs Empirismo (Hume)
- Kant e a Revolução Copernicana na filosofia
- Existencialismo (Sartre, Camus)
- Fenomenologia
- Ética Utilitarista vs Deontológica
- Pós-modernismo (Foucault, Derrida) - conceitos chave

Acadêmico. 3000 palavras."""
        },
        {
            "category": "SOCIOLOGY",
            "domain": "SOCIOLOGY_CLASSIC",
            "prompt": """Você é sociólogo.
            
Explique: TEORIA SOCIOLÓGICA CLÁSSICA E CONTEMPORÂNEA

Tópicos:
- Durkheim (Fato Social, Suicídio)
- Marx (Materialismo Histórico, Luta de Classes)
- Weber (Ação Social, Ética Protestante)
- Escola de Frankfurt e Teoria Crítica
- Sociedade Líquida (Bauman)
- Desigualdade Social e Estrutura

Acadêmico. 3000 palavras."""
        }
        
    ]
    
    print("\n" + "=" * 80)
    print("🌌 QUANTUM LEAP PART 2 - HUMAN SCIENCES EXPANSION")
    print("=" * 80)
    print(f"\n📊 Total de tópicos: {len(topics)}")
    print(f"📈 Expansão estimada: ~{len(topics) * 3000} palavras")
    print(f"⏱️  Tempo estimado: {len(topics) * 10 // 60} minutos")
    
    print("\n🚀 Iniciando automaticamente (modo no-input)...")
    
    start_time = time.time()
    
    for i, topic in enumerate(topics, 1):
        print(f"\n[{i}/{len(topics)}] {topic['category']}: {topic['domain']}")
        
        metadata = {
            'source': 'QUANTUM_LEAP_PART2',
            'category': topic['category'],
            'domain': topic['domain'],
            'level': 'Professional/Academic',
            'type': 'DEEP_KNOWLEDGE',
            'interconnected': True
        }
        
        trainer.generate_and_index(
            domain=topic['domain'],
            prompt=topic['prompt'],
            metadata=metadata
        )
        
        # Small delay to avoid API rate limits
        if i % 10 == 0:
            print(f"\n   ⏸️  Pausa breve (evitar rate limit)...")
            time.sleep(3)
        else:
            time.sleep(1)
    
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    
    print("\n" + "=" * 80)
    print("🌌 QUANTUM LEAP PART 2 COMPLETO!")
    print("=" * 80)
    print(f"✅ Indexados: {trainer.indexed_count}/{len(topics)} tópicos")
    print(f"⏱️  Tempo total: {minutes}m {seconds}s")
    print(f"🧠 Base de conhecimento expandida com Medicina, Direito, Negócios e Humanidades!")
    print("\n🔗 Reinicie o servidor após finalizar todas as partes.")

if __name__ == "__main__":
    run_quantum_leap_part2()
