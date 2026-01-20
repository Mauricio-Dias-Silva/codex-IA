
import os
import chromadb
import google.generativeai as genai
import time

# Chave API Global
API_KEY = "AIzaSyBREWGg-uOUss7bZIoK0xqBU5svqvyCX6Y" 
genai.configure(api_key=API_KEY)

class KnowledgeTrainer:
    def __init__(self, domain_name):
        self.domain = domain_name
        self.client = chromadb.PersistentClient(path=".codex_memory")
        self.collection = self.client.get_or_create_collection(name="project_codebase") # Base unificada

    def get_embedding(self, text):
        try:
            result = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_document",
                title=f"{self.domain} Knowledge"
            )
            return result['embedding']
        except Exception as e:
            print(f"⚠️ Erro embedding: {e}. Tentando novamente em 2s...")
            time.sleep(2)
            try:
                # Retry simples
                result = genai.embed_content(
                    model="models/embedding-001",
                    content=text,
                    task_type="retrieval_document",
                    title=f"{self.domain} Knowledge"
                )
                return result['embedding']
            except:
                return None

    def ingest_topic(self, topic, prompt_context):
        print(f"📚 [{self.domain}] Processando tópico: {topic}...")
        
        # 1. Gerar Conteúdo
        try:
            model = genai.GenerativeModel('gemini-2.5-pro')
            final_prompt = f"""
            ATUE COMO: {prompt_context}
            TAREFA: Crie um documento técnico/jurídico/científico completo e detalhado sobre: '{topic}'.
            
            REQUISITOS:
            - Profundidade máxima (nível especialista/doutorado).
            - Se for LEI: cite artigos, parágrafos, jurisprudência e interpretações.
            - Se for SAÚDE: use terminologia médica precisa e protocolos.
            - Estrutura clara com Títulos e Subtítulos.
            - Mínimo de 1000 palavras de puro conteúdo útil.
            
            SAÍDA: Apenas o texto em Markdown.
            """
            response = model.generate_content(final_prompt)
            content = response.text
        except Exception as e:
            print(f"❌ Erro ao gerar conteúdo: {e}")
            return

        # 2. Vetorizar e Salvar
        print(f"📐 Vetorizando '{topic}'...")
        chunk_size = 1500 # Chunks maiores para contextos complexos
        chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
        
        ids = []
        embeddings = []
        documents = []
        metadatas = []
        
        virtual_filename = f"KNOWLEDGE_BASE/{self.domain}/{topic.replace(' ', '_')}.md"
        
        for idx, chunk in enumerate(chunks):
            vector = self.get_embedding(chunk)
            if vector:
                ids.append(f"{self.domain}_{topic}_{idx}")
                embeddings.append(vector)
                documents.append(chunk)
                metadatas.append({
                    "path": virtual_filename, 
                    "chunk_index": idx,
                    "domain": self.domain,
                    "topic": topic
                })
        
        if ids:
            self.collection.upsert(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)
            print(f"💾 SALVO! {len(ids)} fragmentos de sabedoria sobre {topic} inseridos na memória.")
