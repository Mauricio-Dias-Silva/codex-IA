
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
        
        # [OPTIMIZATION] Local Embeddings 🚀
        try:
            from chromadb.utils import embedding_functions
            self.emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        except:
            self.emb_fn = None

        self.collection = self.client.get_or_create_collection(
            name="project_codebase_local", 
            embedding_function=self.emb_fn
        )

    def get_embedding(self, text):
        # We don't need this anymore as Chroma handles it locally
        return None

    def check_exists(self, topic):
        """Check if topic already exists to save costs."""
        existing = self.collection.get(
            where={"topic": topic},
            limit=1
        )
        return len(existing['ids']) > 0

    def ingest_topic(self, topic, prompt_context):
        print(f"📚 [{self.domain}] Processando tópico: {topic}...")
        
        # 1. Verificação de Custo (Smart Skip) 🛡️
        if self.check_exists(topic):
            print(f"   ⏩ SKIPPING: '{topic}' já está na memória.")
            return

        # 2. Gerar Conteúdo
        try:
            # Seleção de modelo inteligente para custo
            model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
            model = genai.GenerativeModel(model_name)
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

        # 3. Vetorizar e Salvar (Localmente)
        print(f"📐 Indexando '{topic}'...")
        chunk_size = 1500 # Chunks maiores para contextos complexos
        chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
        
        ids = []
        documents = []
        metadatas = []
        
        virtual_filename = f"KNOWLEDGE_BASE/{self.domain}/{topic.replace(' ', '_')}.md"
        
        for idx, chunk in enumerate(chunks):
            ids.append(f"{self.domain}_{topic}_{idx}")
            documents.append(chunk)
            metadatas.append({
                "path": virtual_filename, 
                "chunk_index": idx,
                "domain": self.domain,
                "topic": topic
            })
        
        if ids:
            self.collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
            print(f"💾 SALVO! {len(ids)} fragmentos de sabedoria sobre {topic} inseridos na memória local.")
