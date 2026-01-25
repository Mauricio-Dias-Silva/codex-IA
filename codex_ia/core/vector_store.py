
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
        
        # [OPTIMIZATION] Strict Local Embeddings 🔒
        # We enforce usage of SentenceTransformers to ensure ZERO COST for embeddings.
        # If this fails, we prefer to error out rather than sneakily use paid APIs.
        try:
            from chromadb.utils import embedding_functions
            # Uses a small, fast local model (384 dim)
            self.emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
            logging.info("🧠 Neural Memory: Local Embeddings Active (Cost-Free)")
        except Exception as e:
            logging.error(f"❌ CRITICAL: Could not load local embeddings. Install sentence-transformers! Error: {e}")
            # We set to None, allowing Chroma to use its default ONNX if available, 
            # but we warn heavily. We DO NOT fallback to Gemini here.
            self.emb_fn = None

        self.collection = self.client.get_or_create_collection(
            name="project_codebase_local", 
            metadata={"hnsw:space": "cosine"},
            embedding_function=self.emb_fn
        )
        
        try:
            from codex_ia.core.llm_client import GeminiClient
            self.llm = GeminiClient()
        except:
            self.llm = None

    def index_chat(self, sender: str, message: str):
        """Indexes a chat message for episodic memory."""
        if not self.llm: return

        try:
            # Timestamp for chronologic context
            import datetime
            timestamp = datetime.datetime.now().isoformat()
            
            # Upsert WITHOUT manual embeddings (Chroma handles it locally now)
            msg_id = f"chat_{timestamp}_{sender}"
            self.collection.upsert(
                ids=[msg_id],
                documents=[message],
                metadatas=[{
                    "type": "chat_history",
                    "sender": sender,
                    "timestamp": timestamp,
                    "path": "memory_stream"
                }]
            )
            logging.info(f"💾 Memorized chat from {sender}")
                
        except Exception as e:
            logging.error(f"Chat indexing failed: {e}")

    def index_text(self, text: str, metadata: Dict = None):
        """Indexes a raw string directly."""
        if not self.llm: return

        try:
            # Chunking 
            chunk_size = 1000
            chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
            
            ids = []
            metadatas = []
            documents = []
            
            import datetime
            timestamp = datetime.datetime.now().isoformat()
            
            for idx, chunk in enumerate(chunks):
                chunk_id = f"text_{timestamp}_{idx}"
                ids.append(chunk_id)
                documents.append(chunk)
                
                # Merge default metadata with provided metadata
                base_meta = {"path": "virtual_memory", "chunk_index": idx, "timestamp": timestamp}
                if metadata:
                    base_meta.update(metadata)
                
                metadatas.append(base_meta)
            
            if ids:
                self.collection.upsert(
                    ids=ids,
                    documents=documents,
                    metadatas=metadatas
                )
                logging.info(f"Indexed raw text ({len(ids)} chunks locally)")
                return ids
                
        except Exception as e:
            logging.error(f"Text indexing failed: {e}")
            return None

    def index_file(self, file_path: str, content: str):
        """Indexes a single file."""
        if not self.llm: return

        try:
            # Chunking (Naive splitting for V1)
            chunk_size = 1000
            chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
            
            ids = []
            metadatas = []
            documents = []
            
            for idx, chunk in enumerate(chunks):
                chunk_id = f"{file_path}_{idx}"
                ids.append(chunk_id)
                documents.append(chunk)
                metadatas.append({"path": file_path, "chunk_index": idx})
            
            if ids:
                self.collection.upsert(
                    ids=ids,
                    documents=documents,
                    metadatas=metadatas
                )
                logging.info(f"Indexed {file_path} ({len(ids)} chunks locally)")
                
        except Exception as e:
            logging.error(f"Indexing failed for {file_path}: {e}")

    def semantic_search(self, query: str, n_results=10) -> List[Dict]:
        """Searches for relevant files (Optimized V2 using Smart Retrieval)."""
        if not self.llm: return []
        
        try:
            # Fetch more candidates using the local embedding function (handled by Chroma)
            results = self.collection.query(
                query_texts=[query],
                n_results=20  # High Recall Strategy
            )
            
            hits = []
            seen_paths = set()
            
            if results['ids']:
                for i, doc in enumerate(results['documents'][0]):
                    score = results['distances'][0][i] if results['distances'] else 0
                    meta = results['metadatas'][0][i]
                    path = meta.get('path', 'unknown')
                    
                    # Deduplication logic
                    if path not in seen_paths:
                        hits.append({
                            "path": path,
                            # Expanded context window for better AI comprehension
                            "snippet": doc[:500] + "...", 
                            "score": score
                        })
                        seen_paths.add(path)
            
            # Return top N requested
            return hits[:n_results]
            
        except Exception as e:
            logging.error(f"Search failed: {e}")
            return []

    def clear_memory(self):
        """Wipes the local collection for the current project."""
        try:
            self.client.delete_collection(name="project_codebase_local")
            self.collection = self.client.get_or_create_collection(
                name="project_codebase_local", 
                embedding_function=self.emb_fn
            )
            logging.info("🧹 Neural Memory cleared successfully.")
            return True
        except Exception as e:
            logging.error(f"Error clearing memory: {e}")
            return False
