"""
🌌 QUANTUM LEAP - PART 3: PHYSICS & TESLA MASTERCLASS
Expansão de Conhecimento: Física Quântica, Newtoniana e Nikola Tesla (Patentes e Visão).

Domínios:
- Física Quântica (Entanglement, QFT, Computing)
- Física Newtoniana (Mecânica Clássica, Óptica, Termo)
- Nikola Tesla Deep Dive (Patentes, Wardenclyffe, Visão)
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

def run_quantum_leap_part3():
    """Execute massive knowledge expansion - PART 3 (Physics & Tesla)."""
    
    trainer = QuantumLeapTrainer()
    
    topics = [
        
        # === NIKOLA TESLA DEEP DIVE (10 topics) ===
        {
            "category": "TESLA_MASTERCLASS",
            "domain": "TESLA_AC_SYSTEMS",
            "prompt": """Você é Nikola Tesla (engenheiro elétrico).
            
Explique: SISTEMAS DE CORRENTE ALTERNADA (AC) E MOTORES DE INDUÇÃO

Tópicos:
- O Campo Magnético Rotativo (descoberta fundamental)
- Motor de Indução Polifásico (princípio de funcionamento)
- Patentes principais (US 381,968; US 382,280)
- Vantagens sobre DC (transmissão a longa distância)
- A Guerra das Correntes (Westinghouse vs Edison)
- Transformadores e Distribuição de Energia
- Geradores Hidrelétricos (Niagara Falls)

Técnico e histórico detalhado. 3500 palavras."""
        },
        {
            "category": "TESLA_MASTERCLASS",
            "domain": "TESLA_COIL_HIGH_VOLTAGE",
            "prompt": """Você é Nikola Tesla.
            
Ensine: BOBINA DE TESLA E ALTA TENSÃO/ALTA FREQUÊNCIA

Tópicos:
- Circuito Ressonante (L-C circuit physics)
- Transformador de Núcleo de Ar
- Spark Gap e Capacitores
- Skin Effect (Efeito Pelicular)
- Comportamento de eletricidade em alta frequência
- Patentes relacionadas (System of Electric Lighting)
- Experimentos em Colorado Springs (raios artificiais)

Física avançada e engenharia. 3200 palavras."""
        },
        {
            "category": "TESLA_MASTERCLASS",
            "domain": "WIRELESS_ENERGY_TRANSFER",
            "prompt": """Você é Nikola Tesla.
            
Explique: TRANSMISSÃO DE ENERGIA SEM FIO (WIRELESS ENERGY)

Tópicos:
- Torre de Wardenclyffe (design e propósito)
- Ressonância Terrestre (Earth Resonance)
- Ondas Estacionárias Terrestres
- Magnifying Transmitter (Transmissor de Ampliação)
- Patente US 1,119,732 (Apparatus for Transmitting Electrical Energy)
- Visão do "World Wireless System" (energia e dados globais)
- Por que o projeto parou (J.P. Morgan)

Técnico e visionário. 3500 palavras."""
        },
        {
            "category": "TESLA_MASTERCLASS",
            "domain": "TESLA_TURBINE",
            "prompt": """Você é Nikola Tesla (engenheiro mecânico).
            
Ensine: TURBINA DE TESLA (BLADELESS TURBINE)

Tópicos:
- Princípio da Camada Limite (Boundary Layer effect)
- Adesão e Viscosidade de fluidos
- Design de discos paralelos (sem palhetas)
- Eficiência teórica vs prática
- Aplicações (bombas, compressores, geotermia)
- Patente US 1,061,206
- Por que não foi adotada na época (limitação de materiais)

Engenharia mecânica avançada. 3000 palavras."""
        },
        {
            "category": "TESLA_MASTERCLASS",
            "domain": "TELEAUTOMATON_RADIO",
            "prompt": """Você é Nikola Tesla.
            
Explique: TELEAUTOMATON E CONTROLE DE RÁDIO

Tópicos:
- O primeiro barco controlado por rádio (Madison Square Garden, 1898)
- Patente US 613,809 (Method of and Apparatus for Controlling Mechanism of Moving Vessels)
- Lógica de portas E (AND logic) primitiva
- Coherer (detector de ondas de rádio)
- Visão sobre robótica e "telautomatics"
- Disputa de invenção do rádio (Marconi vs Tesla)

Histórico técnico. 3000 palavras."""
        },
        {
            "category": "TESLA_MASTERCLASS",
            "domain": "DEATH_RAY_TELEFORCE",
            "prompt": """Você é Nikola Tesla (anos finais).
            
Analise: TELEFORCE / DEATH RAY (Raio da Morte)

Tópicos:
- Conceito de feixe de partículas carregadas (Charged Particle Beam)
- Canhão de vácuo (Vacuum chamber design)
- Repulsão eletrostática
- Uso proposto para defesa antiaérea ("Peace Ray")
- Papers perdidos e investigações do FBI pós-morte
- Viabilidade física moderna (armas de energia dirigida)

Investigativo científico. 3000 palavras."""
        },
        {
            "category": "TESLA_MASTERCLASS",
            "domain": "TESLA_OSCILLATOR_EARTHQUAKE",
            "prompt": """Você é Nikola Tesla.
            
Explique: OSCILADOR ELETROMECÂNICO (MÁQUINA DE TERREMOTO)

Tópicos:
- Oscilador a vapor de pistão
- Ressonância mecânica (Mechanical Resonance)
- O experimento do "terremoto" em NY
- Analogia da ponte e soldados marchando
- Potencial para geodinâmica e transmissão de energia mecânica
- Patentes de geradores alternativos

Física mecânica. 2800 palavras."""
        },
        {
            "category": "TESLA_MASTERCLASS",
            "domain": "TESLA_VISION_FUTURE",
            "prompt": """Você é Nikola Tesla (visionário).
            
Discorra: A VISÃO DE FUTURO DE TESLA

Tópicos:
- Smartphone (previsão do dispositivo de bolso em 1926)
- Internet e Wi-Fi (World Wireless System)
- Energia Livre e Renovável (Geotérmica, Solar)
- Modificação Climática (controle do tempo elétrico)
- Fotografia de Pensamento (Thought Photography)
- Eugênia e visões sociais (contexto da época)
- A mulher do futuro (previsões sociais)

Filosófico e futurista. 3000 palavras."""
        },

        # === FÍSICA QUÂNTICA (8 topics) ===
        {
            "category": "PHYSICS_QUANTUM",
            "domain": "QUANTUM_MECHANICS_FOUNDATIONS",
            "prompt": """Você é físico teórico (Copenhagen Institute).
            
Ensine: FUNDAMENTOS DA MECÂNICA QUÂNTICA

Tópicos:
- Função de Onda (Wave Function - Psi)
- Equação de Schrödinger (dependente e independente do tempo)
- Dualidade Onda-Partícula
- Princípio da Incerteza de Heisenberg
- Superposição e Colapso da Função de Onda
- Interpretação de Copenhagen vs Many-Worlds
- Efeito Túnel (Tunneling)

PhD Physics level. 3500 palavras."""
        },
        {
            "category": "PHYSICS_QUANTUM",
            "domain": "QUANTUM_ENTANGLEMENT",
            "prompt": """Você é físico quântico.
            
Explique: ENTRELAÇAMENTO QUÂNTICO (QUANTUM ENTANGLEMENT)

Tópicos:
- O paradoxo EPR (Einstein-Podolsky-Rosen)
- "Spooky action at a distance"
- Teorema de Bell e Violação das Desigualdades de Bell
- Experimentos de Aspect (1982) e Nobel 2022
- Não-localidade
- Teletransporte Quântico (Quantum Teleportation of states)
- Aplicações em Criptografia Quântica (QKD)

Física avançada. 3200 palavras."""
        },
        {
            "category": "PHYSICS_QUANTUM",
            "domain": "QUANTUM_FIELD_THEORY",
            "prompt": """Você é físico de partículas (CERN).
            
Ensine: TEORIA QUÂNTICA DE CAMPOS (QFT) E MODELO PADRÃO

Tópicos:
- Quantização de Campos (Second Quantization)
- QED (Eletrodinâmica Quântica) - Feynman Diagrams
- QCD (Cromodinâmica Quântica) - Quarks e Glúons
- Bósons de Calibre (W, Z, Fóton, Glúon)
- Bóson de Higgs e mecanismo de massa
- Vácuo Quântico e Partículas Virtuais
- Unificação das Forças

PhD level. 3500 palavras."""
        },
        {
            "category": "PHYSICS_QUANTUM",
            "domain": "QUANTUM_COMPUTING_PHYSICS",
            "prompt": """Você é físico computacional.
            
Explique: FÍSICA DA COMPUTAÇÃO QUÂNTICA

Tópicos:
- Qubit (Esfera de Bloch)
- Portas Lógicas Quânticas (Hadamard, CNOT, Pauli)
- Algoritmo de Shor (fatoração) e Grover (busca)
- Decoherência Quântica e Correção de Erro
- Implementações Físicas (Supercondutores, Íons Aprisionados, Fotônicos)
- Supremacia Quântica

Técnico. 3000 palavras."""
        },

        # === FÍSICA NEWTONIANA/CLÁSSICA (6 topics) ===
        {
            "category": "PHYSICS_CLASSICAL",
            "domain": "NEWTONIAN_MECHANICS",
            "prompt": """Você é físico clássico.
            
Ensine: MECÂNICA NEWTONIANA AVANÇADA

Tópicos:
- As 3 Leis de Newton (análise vetorial profunda)
- Gravitação Universal
- Mecânica Lagrangiana e Hamiltoniana (reformulando Newton)
- Conservação de Momento Linear e Angular
- Dinâmica de Corpos Rígidos (Tensor de Inércia)
- Osciladores Harmônicos e Amortecidos
- Referenciais Inerciais e Não-Inerciais (Força de Coriolis)

Universitário avançado. 3200 palavras."""
        },
        {
            "category": "PHYSICS_CLASSICAL",
            "domain": "THERMODYNAMICS_CLASSICAL",
            "prompt": """Você é físico termodinâmico.
            
Ensine: TERMODINÂMICA CLÁSSICA

Tópicos:
- As 4 Leis da Termodinâmica (0, 1, 2, 3)
- Entropia e a Seta do Tempo
- Ciclos Termodinâmicos (Carnot, Otto, Diesel)
- Potenciais Termodinâmicos (Gibbs, Helmholtz)
- Equações de Estado (Gás Ideal, Van der Waals)
- Transmissão de Calor (Condução, Convecção, Radiação)
- Maxwell Relations

Física rigorosa. 3000 palavras."""
        },
        {
            "category": "PHYSICS_CLASSICAL",
            "domain": "OPTICS_ELECTROMAGNETISM",
            "prompt": """Você é físico especialista em Eletromagnetismo (Maxwell).
            
Explique: ELETROMAGNETISMO E ÓPTICA FÍSICA

Tópicos:
- Equações de Maxwell (forma diferencial e integral)
- Ondas Eletromagnéticas (propagação, polarização)
- Óptica Ondulatória (Interferência, Difração, Experimento fenda dupla)
- Vetor de Poynting e Energia
- Guias de Onda e Fibra Óptica (reflexão interna total)
- Espectro Eletromagnético completo

PhD level. 3200 palavras."""
        }
        
    ]
    
    print("\n" + "=" * 80)
    print("🌌 QUANTUM LEAP PART 3 - PHYSICS & TESLA MASTERCLASS")
    print("=" * 80)
    print(f"\n📊 Total de tópicos: {len(topics)}")
    print(f"📈 Expansão estimada: ~{len(topics) * 3200} palavras")
    print(f"⏱️  Tempo estimado: {len(topics) * 10 // 60} minutos")
    
    print("\n🚀 Iniciando automaticamente...")
    
    start_time = time.time()
    
    for i, topic in enumerate(topics, 1):
        print(f"\n[{i}/{len(topics)}] {topic['category']}: {topic['domain']}")
        
        metadata = {
            'source': 'QUANTUM_LEAP_PART3',
            'category': topic['category'],
            'domain': topic['domain'],
            'level': 'Masterclass',
            'type': 'DEEP_KNOWLEDGE',
            'interconnected': True
        }
        
        trainer.generate_and_index(
            domain=topic['domain'],
            prompt=topic['prompt'],
            metadata=metadata
        )
        
        if i % 10 == 0:
            print(f"\n   ⏸️  Pausa breve...")
            time.sleep(3)
        else:
            time.sleep(1)
    
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    
    print("\n" + "=" * 80)
    print("🌌 QUANTUM LEAP PART 3 COMPLETO!")
    print("=" * 80)
    print(f"✅ Indexados: {trainer.indexed_count}/{len(topics)} tópicos")
    print(f"⏱️  Tempo total: {minutes}m {seconds}s")
    print(f"⚡ Tesla e Física Quântica integrados ao cérebro!")

if __name__ == "__main__":
    run_quantum_leap_part3()
