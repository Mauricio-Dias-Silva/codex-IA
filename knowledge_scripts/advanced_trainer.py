
import os
import sys
import time
from typing import List
# Adiciona o diretório raiz ao path para importar módulos core
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

from codex_ia.core.vector_store import CodexVectorStore
import google.generativeai as genai

# Chave API Global (Replicada do trainer_base.py para consistência)
API_KEY = "AIzaSyBREWGg-uOUss7bZIoK0xqBU5svqvyCX6Y"

class DeepKnowledgeTrainer:
    """
    Versão aprimorada do treinador que realiza 'Deep Reflection' antes de salvar.
    Ele não apenas salva o conteúdo, mas pede para a IA conectar os pontos
    e encontrar padrões ocultos (Pattern Recognition) antes da vetorização.
    """
    
    def __init__(self, domain_prefix: str, model_name="gemini-2.5-pro"):
        self.domain_prefix = domain_prefix
        self.vector_store = CodexVectorStore()
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel(model_name)
        print(f"🚀 [DEEP TRAINER] Iniciado para domínio: {domain_prefix}")

    def ingest_topic(self, topic: str, context_persona: str):
        print(f"\n🔮 [{self.domain_prefix}] Analisando Profundamente: {topic}")
        
        # Passo 1: Geração de Conteúdo Bruto (Igual ao anterior)
        content_prompt = f"""
        Atue como {context_persona}.
        Explique profundamente o conceito de: "{topic}".
        Seja técnico, filosófico e prático. Use analogias avançadas.
        """
        response = self.model.generate_content(content_prompt)
        raw_content = response.text
        
        # Passo 2: Deep Reflection (O Upgrade) - Encontrar Conexões
        print(f"   ✨ Sintetizando padrões ocultos para '{topic}'...")
        reflection_prompt = f"""
        Analise o seguinte texto sobre {topic}:
        
        ---
        {raw_content[:4000]}
        ---
        
        AGORA, REALIZE UMA ANÁLISE DE PADRÕES (DEEP REFLECTION):
        1. Identifique os princípios fundamentais (First Principles) por trás disso.
        2. Conecte este conceito com outras áreas (História, Biologia, Matemática, Sociologia).
        3. Resuma o "Core Insight" em 3 axiomas imutáveis.
        
        Gere um texto consolidado que una a explicação técnica com essa reflexão profunda.
        """
        
        reflection_ops = self.model.generate_content(reflection_prompt)
        deep_content = reflection_ops.text
        
        # Passo 3: Vetorização do Conteúdo Enriquecido
        chunks = self._chunk_content(deep_content)
        print(f"   📐 Vetorizando {len(chunks)} fragmentos de conhecimento denso...")
        
        count = 0
        for chunk in chunks:
            # Adiciona metadados de 'Deep Learning'
            meta = f"Domain: {self.domain_prefix} | Type: DeepInsight | Topic: {topic}"
            final_text = f"{meta}\n\n{chunk}"
            
            # Indexa no ChromaDB
            self.vector_store.index_text(
                text=final_text,
                metadata={"source": "DeepTrainer", "domain": self.domain_prefix, "topic": topic}
            )
            count += 1
            print(f"   💎 Cristalizado fragmento {count}/{len(chunks)}")
            time.sleep(1) # Rate limit protection
            
        print(f"✅ CONHECIMENTO ABSOLUTO ADQUIRIDO: {topic}")

    def _chunk_content(self, text: str, chunk_size=1500) -> List[str]:
        # Chunking um pouco maior para manter o contexto das reflexões
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
