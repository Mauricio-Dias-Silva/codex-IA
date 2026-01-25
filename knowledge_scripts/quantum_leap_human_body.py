"""
🧘 QUANTUM LEAP - PART 4: HOLISTIC HUMAN BODY MASTERCLASS
Expansão de Conhecimento: Anatomia, Fisiologia e Visão Holística Integrada.

Foco: Absorver TUDO sobre o corpo humano para o projeto 'Corpo Humano Holístico'.

Domínios:
- Anatomia e Fisiologia Avançada (Ocidental)
- Medicina Tradicional Chinesa (MTC) e Meridianos
- Ayurveda e Doshas
- Psicossomática e Conexão Mente-Corpo
- Eixo Intestino-Cérebro e Microbiota
- Bioquímica Nutricional
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codex_ia.core.vector_store import CodexVectorStore
from codex_ia.core.llm_client import GeminiClient
from google.genai import types
import time

class QuantumLeapTrainer:
    """Massive knowledge expansion for Human Body."""
    
    def __init__(self):
        self.store = CodexVectorStore()
        self.llm = GeminiClient()
        # Force Flash for speed/volume
        self.llm.model = "gemini-2.0-flash" 
        self.indexed_count = 0
        
    def generate_and_index(self, domain: str, prompt: str, metadata: dict):
        """Generate knowledge and index with quality check."""
        try:
            response = self.llm.client.models.generate_content(
                model=self.llm.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=5000
                )
            )
            
            if response and response.text and len(response.text) > 500:
                doc_id = self.store.index_text(
                    text=response.text,
                    metadata=metadata
                )
                self.indexed_count += 1
                word_count = len(response.text.split())
                
                doc_preview = str(doc_id[0]) if doc_id and isinstance(doc_id, list) else "indexed"
                
                print(f"   ✅ {doc_preview[:12]}... | ~{word_count} palavras")
                return True
            else:
                print(f"   ⚠️  Resposta muito curta, pulando")
                return False
                
        except Exception as e:
            print(f"   ❌ Erro: {str(e)[:50]}...")
            return False

def run_quantum_leap_body():
    """Execute massive knowledge expansion - HUMAN BODY."""
    
    trainer = QuantumLeapTrainer()
    
    topics = [
        
        # === ANATOMIA & FISIOLOGIA OCIDENTAL (Deep Dive) ===
        {
            "category": "HUMAN_BODY_WESTERN",
            "domain": "NEUROANATOMY_FUNCTIONAL",
            "prompt": """Você é Neurocientista e Anatomista.
            
Ensine: NEUROANATOMIA FUNCIONAL AVANÇADA

Tópicos:
- Estrutura detalhada do Sistema Nervoso Central e Periférico
- Vias Ascendentes (Sensoriais) e Descendentes (Motoras)
- Sistema Límbico e o processamento emocional
- Tronco Encefálico e controle autonômico (Respiração, Batimentos)
- Neuroplasticidade e regeneração nervosa
- Barreiras Hematoencefálica e líquor

Nível Medicina Doutorado. 3500 palavras."""
        },
        {
            "category": "HUMAN_BODY_WESTERN",
            "domain": "CARDIOVASCULAR_PHYSIOLOGY",
            "prompt": """Você é Fisiologista Cardiovascular.
            
Ensine: FISIOLOGIA CARDIOVASCULAR E HEMODINÂMICA

Tópicos:
- Ciclo Cardíaco detalhado (Pressão x Volume)
- Eletrofisiologia Cardíaca (Potenciais de ação)
- Regulação da Pressão Arterial (Sistema Renina-Angiotensina-Aldosterona)
- Microcirculação e trocas capilares (Lei de Starling)
- Sangue: Hematopoiese e coagulação

Técnico avançado. 3200 palavras."""
        },
        {
            "category": "HUMAN_BODY_WESTERN",
            "domain": "IMMUNE_SYSTEM_INTEGRATED",
            "prompt": """Você é Imunologista.
            
Ensine: SISTEMA IMUNE E RESPOSTA INFLAMATÓRIA

Tópicos:
- Imunidade Inata (Barreiras, Fagócitos, Complemento)
- Imunidade Adaptativa (Linfócitos T e B, Anticorpos)
- Complexo Principal de Histocompatibilidade (MHC)
- A cascata da inflamação e resolução
- Psiconeuroimunologia (conexão mente-imunidade)

Técnico. 3200 palavras."""
        },
        
        # === VISÃO HOLÍSTICA & INTEGRATIVA ===
        {
            "category": "HOLISTIC_HEALTH",
            "domain": "GUT_BRAIN_AXIS",
            "prompt": """Você é especialista em Medicina Integrativa.
            
Explique: O EIXO INTESTINO-CÉREBRO (GUT-BRAIN AXIS)

Tópicos:
- O nervo vago como via de comunicação bidirecional
- Microbiota intestinal e produção de neurotransmissores (Serotonina, GABA)
- Disbiose e impacto na saúde mental (Depressão, Ansiedade)
- Permeabilidade intestinal (Leaky Gut) e inflamação sistêmica
- Protocolos de modulação intestinal

Científico e Integrativo. 3500 palavras."""
        },
        {
            "category": "HOLISTIC_HEALTH",
            "domain": "PSYCHOSOMATIC_MEDICINE",
            "prompt": """Você é especialista em Psicossomática e Nova Medicina Germânica.
            
Explique: PSICOSSOMÁTICA E A BIOLOGIA DAS EMOÇÕES

Tópicos:
- Mecanismos fisiológicos do estresse crônico (Eixo HPA)
- Como traumas emocionais se manifestam fisicamente (Teoria Polivagal)
- Simbolismo do corpo e órgãos (ex: Fígado/Raiva, Pulmão/Tristeza)
- Epigenética: Como o ambiente/emoção altera a expressão gênica
- Casos de estudo de remissão espontânea

Profundo e revelador. 3200 palavras."""
        },
        {
            "category": "HOLISTIC_HEALTH",
            "domain": "QUANTUM_BIOLOGY",
            "prompt": """Você é Biofísico Quântico.
            
Ensine: BIOLOGIA QUÂNTICA E O CORPO HUMANO

Tópicos:
- Efeitos quânticos em processos biológicos (Fotossíntese, Olfato, Visão)
- Biofótons e comunicação celular por luz
- O campo bioelétrico do corpo (The Body Electric - Robert Becker)
- Consciência e microtúbulos (Teoria Orch-OR Penrose/Hameroff)
- A água estruturada no corpo (EZ Water - Gerald Pollack)

Vanguarda da ciência. 3500 palavras."""
        },

        # === MEDICINA TRADICIONAL & ENERGÉTICA ===
        {
            "category": "ANCIENT_MEDICINE",
            "domain": "TCM_MERIDIANS",
            "prompt": """Você é Grão-Mestre em Medicina Tradicional Chinesa (MTC).
            
Ensine: FUNDAMENTOS DA MTC E MERIDIANOS

Tópicos:
- Teoria do Yin-Yang e os 5 Elementos na fisiologia
- O conceito de Qi (Energia Vital), Jing (Essência) e Shen (Espírito)
- Mapeamento detalhado dos 12 Meridianos Principais
- Zang-Fu (Órgãos e Vísceras na visão energética)
- Diagnóstico por Língua e Pulso
- Acupuntura: Mecanismos científicos e energéticos

Mestre e detalhado. 3500 palavras."""
        },
        {
            "category": "ANCIENT_MEDICINE",
            "domain": "AYURVEDA_DOSHAS",
            "prompt": """Você é Vaidya (Médico Ayurvédico).
            
Ensine: AYURVEDA E A CIÊNCIA DA VIDA

Tópicos:
- Os 5 Grandes Elementos (Pancha Mahabhuta)
- Os 3 Doshas (Vata, Pitta, Kapha): Fisiologia e Psicologia
- Agni (Fogo Digestivo) e Ama (Toxinas)
- Dhatus (Tecidos) e Ojas (Vitalidade)
- Rotina Diária (Dinacharya) para equilíbrio
- Fitoterapia Ayurvédica básica

Profundo e tradicional. 3200 palavras."""
        },
        {
            "category": "ANCIENT_MEDICINE",
            "domain": "CHAKRA_ENDOCRINE_SYSTEM",
            "prompt": """Você é especialista em Medicina Vibracional.
            
Explique: RELAÇÃO SISTEMA ENDÓCRINO E CHAKRAS

Tópicos:
- Correlação anatômica entre Glândulas e Chakras Principais
- Raiz/Suprarrenais (Sobrevivência)
- Sacro/Gônadas (Criação)
- Plexo Solar/Pâncreas (Poder pessoal)
- Cardíaco/Timo (Imunidade e Amor)
- Laríngeo/Tireoide (Expressão)
- Frontal/Pituitária (Comando)
- Coronário/Pineal (Conexão e Ritmos Circadianos)

Integrativo. 3000 palavras."""
        }
        
    ]
    
    print("\n" + "=" * 80)
    print("🧘 QUANTUM LEAP PART 4 - HOLISTIC HUMAN BODY")
    print("=" * 80)
    print(f"\n📊 Total de tópicos: {len(topics)}")
    print(f"📈 Expansão estimada: ~{len(topics) * 3200} palavras")
    print("🎯 Foco: Upgrade para o projeto 'Corpo Humano Holístico'")
    
    print("\n🚀 Iniciando...")
    
    start_time = time.time()
    
    for i, topic in enumerate(topics, 1):
        print(f"\n[{i}/{len(topics)}] {topic['category']}: {topic['domain']}")
        
        metadata = {
            'source': 'QUANTUM_LEAP_BODY',
            'category': topic['category'],
            'domain': topic['domain'],
            'level': 'Masterclass',
            'type': 'HOLISTIC_KNOWLEDGE',
            'project_target': 'corpo_humano_holistico'
        }
        
        trainer.generate_and_index(
            domain=topic['domain'],
            prompt=topic['prompt'],
            metadata=metadata
        )
        
        time.sleep(1)
    
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    
    print("\n" + "=" * 80)
    print("🧘 QUANTUM LEAP BODY COMPLETO!")
    print("=" * 80)
    print("O Codex agora é um especialista em saúde integrativa.")

if __name__ == "__main__":
    run_quantum_leap_body()
