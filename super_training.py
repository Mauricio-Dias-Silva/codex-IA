
import os
import json
import logging
import chromadb
import google.generativeai as genai

# Configuração de Logs
logging.basicConfig(level=logging.INFO)

# Chave API Poderosa
API_KEY = "AIzaSyBREWGg-uOUss7bZIoK0xqBU5svqvyCX6Y" 
genai.configure(api_key=API_KEY)

def generate_knowledge(topic: str):
    """Gera conhecimento profundo sobre um tópico usando Gemini 2.5 Pro."""
    print(f"🧠 Gerando Masterclass sobre: {topic}...")
    model = genai.GenerativeModel('gemini-2.5-pro')
    
    prompt = f"""
    Atue como um Engenheiro de Software Principal (Staff Engineer) do Google.
    Escreva um artigo técnico denso e profundo sobre: {topic}.
    
    O artigo deve conter:
    1. Conceitos avançados.
    2. Exemplos de código em Python (se aplicável).
    3. Anti-patterns a evitar.
    4. Melhores práticas modernas (2025+).
    
    Formato: Responda APENAS com o conteúdo do artigo em Markdown enriquecido.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Erro ao gerar conhecimento: {e}")
        return None

def get_embedding(text):
    """Gera embedding diretamente via API, bypassando classes internas."""
    try:
        # Modelo de embedding padrão do Gemini
        result = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_document",
            title="Knowledge Base"
        )
        return result['embedding']
    except Exception as e:
        print(f"Erro embedding: {e}")
        return None

def train_codex():
    print("🚀 Iniciando Super-Treinamento do Codex-IA (Direct Mode)...")
    
    # Conexão direta com ChromaDB
    client = chromadb.PersistentClient(path=".codex_memory")
    collection = client.get_or_create_collection(name="project_codebase")
    
    # 2. Tópicos para aprender
    topics = [
        "Arquitetura Limpa em Python (Clean Architecture)",
        "Design Patterns para Sistemas Distribuídos",
        "Otimização de Banco de Dados Django (ORM Performance)",
        "Segurança em APIs REST e GraphQL"
    ]
    
    for topic in topics:
        content = generate_knowledge(topic)
        if content:
            print(f"📐 Vetorizando conhecimento...")
            
            # Chunking simples
            chunk_size = 1000
            chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
            
            ids = []
            embeddings = []
            documents = []
            metadatas = []
            
            virtual_filename = f"KNOWLEDGE_BASE/{topic.replace(' ', '_')}.md"
            
            for idx, chunk in enumerate(chunks):
                vector = get_embedding(chunk)
                if vector:
                    ids.append(f"{virtual_filename}_{idx}")
                    embeddings.append(vector)
                    documents.append(chunk)
                    metadatas.append({"path": virtual_filename, "chunk_index": idx})
            
            if ids:
                collection.upsert(
                    ids=ids,
                    embeddings=embeddings,
                    documents=documents,
                    metadatas=metadatas
                )
                print(f"💾 Injetados {len(ids)} chunks sobre {topic} na memória neural.")
        else:
            print(f"❌ Falha ao aprender sobre {topic}")

    print("🎓 Treinamento Concluído! O Codex agora é um especialista nesses tópicos.")

if __name__ == "__main__":
    train_codex()
