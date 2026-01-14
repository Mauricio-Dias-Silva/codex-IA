
import os
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict
import logging

class CodexVectorStore:
    """
    [CODEX OS] Neural Memory 🧠
    Indexes project files for semantic search.
    """
    def __init__(self, persistence_path=".codex_memory"):
        self.client = chromadb.PersistentClient(path=persistence_path)
        
        # We will use Gemini for embeddings if possible, else default
        # For simplicity in V1, let's strictly use the LLM Client we just patched
        # But Chroma needs a function. We can wrap it.
        self.collection = self.client.get_or_create_collection(
            name="project_codebase",
            metadata={"hnsw:space": "cosine"}
        )
        
        try:
            from codex_ia.core.llm_client import GeminiClient
            self.llm = GeminiClient()
        except:
            self.llm = None

    def index_file(self, file_path: str, content: str):
        """Indexes a single file."""
        if not self.llm: return

        try:
            # Chunking (Naive splitting for V1)
            chunk_size = 1000
            chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
            
            ids = []
            embeddings = []
            metadatas = []
            documents = []
            
            for idx, chunk in enumerate(chunks):
                vector = self.llm.embed_content(chunk)
                if vector:
                    chunk_id = f"{file_path}_{idx}"
                    ids.append(chunk_id)
                    embeddings.append(vector)
                    documents.append(chunk)
                    metadatas.append({"path": file_path, "chunk_index": idx})
            
            if ids:
                self.collection.upsert(
                    ids=ids,
                    embeddings=embeddings,
                    documents=documents,
                    metadatas=metadatas
                )
                logging.info(f"Indexed {file_path} ({len(ids)} chunks)")
                
        except Exception as e:
            logging.error(f"Indexing failed for {file_path}: {e}")

    def semantic_search(self, query: str, n_results=5) -> List[Dict]:
        """Searches for relevant files."""
        if not self.llm: return []
        
        try:
            vector = self.llm.embed_content(query)
            if not vector: return []
            
            results = self.collection.query(
                query_embeddings=[vector],
                n_results=n_results
            )
            
            # Format results
            hits = []
            seen_paths = set()
            
            if results['ids']:
                for i, doc in enumerate(results['documents'][0]):
                    meta = results['metadatas'][0][i]
                    path = meta['path']
                    
                    if path not in seen_paths:
                        hits.append({
                            "path": path,
                            "snippet": doc[:200] + "...",
                            "score": results['distances'][0][i] if results['distances'] else 0
                        })
                        seen_paths.add(path)
            
            return hits
            
        except Exception as e:
            logging.error(f"Search failed: {e}")
            return []
