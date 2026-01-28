import os
import logging
import json
from typing import List, Dict

try:
    import chromadb
    from chromadb.config import Settings
    HAS_CHROMA = True
except ImportError:
    HAS_CHROMA = False

class NeuralAgent:
    """
    Level 14: Neural Memory (The Hippocampus)
    Indexes code from various projects into a Vector Database for cross-project recall.
    """
    def __init__(self, persistence_path):
        self.persistence_path = persistence_path
        self.chroma_client = None
        self.collection = None
        
        if HAS_CHROMA:
            try:
                self.chroma_client = chromadb.PersistentClient(path=os.path.join(persistence_path, "chroma_db"))
                self.collection = self.chroma_client.get_or_create_collection(name="codex_neural_memory")
                logging.info("🧠 ChromaDB initialized successfully.")
            except Exception as e:
                logging.error(f"🧠 Failed to init ChromaDB: {e}")
                HAS_CHROMA = False
        
        if not HAS_CHROMA:
            logging.warning("🧠 ChromaDB not found/failed. Using JSON fallback (Lobotomized Mode).")
            # Fallback structure
            self.fallback_memory = []

    def absorb_project(self, project_path: str):
        """
        Scans a project and embeds its code into the vector store.
        """
        logging.info(f"🧠 Absorbing project: {project_path}")
        file_count = 0
        
        # Walk and chunk
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if d not in ['.git', 'venv', '__pycache__', 'node_modules']]
            
            for file in files:
                if file.endswith(('.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.md')):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, project_path)
                    
                    try:
                        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                        # Chunking strategy (Naive: by function or max chars)
                        # For now, simplistic chunking
                        chunks = self._chunk_content(content)
                        
                        ids = [f"{project_path}::{rel_path}::{i}" for i in range(len(chunks))]
                        metadatas = [{"source": rel_path, "project": project_path, "type": "code"} for _ in chunks]
                        
                        if HAS_CHROMA and self.collection:
                             self.collection.upsert(
                                 ids=ids,
                                 documents=chunks,
                                 metadatas=metadatas
                             )
                        else:
                             # Fallback
                             for i, c in enumerate(chunks):
                                 self.fallback_memory.append({"content": c, "meta": metadatas[i]})
                                 
                        file_count += 1
                    except Exception as e:
                        logging.error(f"Failed to absorb {rel_path}: {e}")
                        
        return f"Absorbed {file_count} files from {project_path}."

    def recall(self, query: str, n_results=3) -> List[str]:
        """
        Retrieves relevant code snippets.
        """
        results = []
        if HAS_CHROMA and self.collection:
            try:
                query_res = self.collection.query(
                    query_texts=[query],
                    n_results=n_results
                )
                # Flatten
                if query_res['documents']:
                    results = query_res['documents'][0]
            except Exception as e:
                logging.error(f"Recall failed: {e}")
        else:
            # TF-IDF or Keyword search fallback
            # Simple keyword matching
            hits = [m['content'] for m in self.fallback_memory if any(w in m['content'].lower() for w in query.lower().split())]
            results = hits[:n_results]
            
        return results

    def _chunk_content(self, content, chunk_size=1000, overlap=100):
        # Naive sliding window
        return [content[i:i+chunk_size] for i in range(0, len(content), chunk_size-overlap)]
