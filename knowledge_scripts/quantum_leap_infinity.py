"""
♾️ QUANTUM LEAP INFINITY - AUTONOMOUS KNOWLEDGE EXPANSION ENGINE
Target: 2,000,000+ Words

Este script não possui tópicos hardcoded. Ele funciona como um AGENTE AUTÔNOMO:
1. Escolhe uma Macro-Área (ex: Nanotecnologia, História Antiga, Astrofísica)
2. Pede ao Gemini: "Gere 5 tópicos PhD ultra-específicos e inéditos nesta área"
3. Gera o conteúdo para cada tópico
4. Indexa na memória
5. Repete indefinidamente até atingir a meta.

Isso garante diversidade infinita sem repetição.
"""

import os
import sys
import json
import random
import time
from datetime import datetime

# Setup paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codex_ia.core.vector_store import CodexVectorStore
from codex_ia.core.llm_client import GeminiClient
from google.genai import types

# === CONFIGURATION ===
TARGET_WORDS = 2_000_000
WORDS_PER_TOPIC = 3500
DB_FILE = "infinity_state.json"

MACRO_DOMAINS = [
    "Engenharia Aeroespacial Avançada", "Medicina Genômica", "Direito Internacional Público",
    "Arqueologia Proibida e Mistérios", "Física de Partículas", "Filosofia da Mente",
    "Economia Comportamental", "Inteligência Artificial AGI", "Nanotecnologia Molecular",
    "História da Guerra Fria", "Botânica e Farmacognosia", "Culinária Molecular",
    "Engenharia de Materiais", "Criptografia Quântica", "Psicologia Junguiana",
    "Oceanografia Abissal", "Teologia Comparada", "Arquitetura Sustentável",
    "Geopolítica do Ártico", "Mitologia Suméria e Babilônica", "Biohacking e Longevidade",
    "Programação de Sistemas Operacionais", "Matemática Topológica", "Virologia",
    "Astronomia de Ondas Gravitacionais"
]

class InfinityEngine:
    def __init__(self):
        self.store = CodexVectorStore()
        self.llm = GeminiClient()
        # FORCE GEMINI FLASH FOR HIGH SPEED & VOLUME
        self.llm.model = "gemini-2.0-flash-exp" 
        self.state = self._load_state()
        
    def _load_state(self):
        if os.path.exists(DB_FILE):
            try:
                with open(DB_FILE, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"total_words": 0, "topics_covered": []}

    def _save_state(self):
        with open(DB_FILE, 'w') as f:
            json.dump(self.state, f, indent=2)

    def generate_new_topics(self, macro_domain):
        """Asks Gemini to invent new specific topics."""
        prompt = f"""
        Atue como um Curador de Enciclopédia de Nível PhD.
        Estamos construindo uma base de conhecimento sobre: {macro_domain}.
        
        Tópicos JÁ COBERTOS (Evite estes): {json.dumps(self.state['topics_covered'][-20:])}
        
        Gere 3 sub-tópicos EXTREMAMENTE ESPECÍFICOS, TÉCNICOS e AVANÇADOS dentro de '{macro_domain}'.
        Não quero introduções. Quero "Deep Dives".
        ex: em vez de "História de Roma", prefira "A Logística de Abastecimento das Legiões na Gália".
        
        Retorne APENAS uma lista Python de strings. Exemplo:
        ["Tópico A", "Tópico B", "Tópico C"]
        """
        
        try:
            response = self.llm.client.models.generate_content(
                model=self.llm.model,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.7) # Higher temp for creativity
            )
            text = response.text.strip()
            # Cleanup Markdown stuff if present
            text = text.replace("```python", "").replace("```", "").strip()
            return eval(text) # Dangerous but effective for simple list parsing
        except Exception as e:
            print(f"⚠️ Erro gerando tópicos: {e}")
            return []

    def generate_content(self, topic):
        """Generates the masterclass content."""
        prompt = f"""
        Você é a maior autoridade mundial em: {topic}.
        
        Escreva um Artigo Técnico/Científico Completo (Masterclass) sobre isso.
        
        Estrutura Obrigatória:
        1. Fundamentos Teóricos Profundos
        2. Complexidades Técnicas e Nuances
        3. Casos de Estudo ou Aplicações Práticas
        4. Controvérsias ou Desafios Atuais
        5. Conclusão Prospectiva
        
        Estilo: Acadêmico, Denso, Rico em Vocabulário Técnico.
        Mínimo: 3000 palavras.
        """
        
        try:
            response = self.llm.client.models.generate_content(
                model=self.llm.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3, # Lower temp for accuracy
                    max_output_tokens=6000 # Max possible
                )
            )
            return response.text
        except Exception as e:
            print(f"⚠️ Erro gerando conteúdo: {e}")
            return None

    def run(self):
        print("\n" + "♾️" * 40)
        print(f"   INFINITY ENGINE STARTED | TARGET: {TARGET_WORDS:,} WORDS")
        print("♾️" * 40 + "\n")
        
        while self.state['total_words'] < TARGET_WORDS:
            # 1. Pick a random domain
            domain = random.choice(MACRO_DOMAINS)
            print(f"🔍 Explorando Domínio: {domain}")
            
            # 2. Invent sub-topics
            topics = self.generate_new_topics(domain)
            if not topics:
                continue
                
            print(f"   💡 Novos Tópicos Descobertos: {topics}")
            
            # 3. Process each topic
            for topic in topics:
                if topic in self.state['topics_covered']:
                    print(f"   ⏭️ Tópico já existe: {topic}")
                    continue
                
                print(f"   ✍️ Escrevendo sobre: {topic}...")
                content = self.generate_content(topic)
                
                if content and len(content) > 1000:
                    # 4. Index
                    metadata = {
                        'source': 'INFINITY_ENGINE',
                        'macro_domain': domain,
                        'topic': topic,
                        'type': 'AUTONOMOUS_KNOWLEDGE'
                    }
                    ids = self.store.index_text(content, metadata)
                    
                    # Updates
                    word_count = len(content.split())
                    self.state['total_words'] += word_count
                    self.state['topics_covered'].append(topic)
                    self._save_state()
                    
                    print(f"   ✅ Indexado! (+{word_count} palavras) | Total: {self.state['total_words']:,}")
                else:
                    print("   ❌ Conteúdo falhou ou muito curto.")
                
                # Sleep to respect limits
                time.sleep(5)
            
            print(f"\n📊 Status: {self.state['total_words']:,} / {TARGET_WORDS:,} palavras")
            print("   💤 Descansando 10s...\n")
            time.sleep(10)

if __name__ == "__main__":
    engine = InfinityEngine()
    engine.run()
