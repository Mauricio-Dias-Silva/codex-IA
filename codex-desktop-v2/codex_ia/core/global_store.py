import os
import logging
import chromadb
from pathlib import Path

class GlobalVectorStore:
    """
    [PHASE 6] Universal Memory - Cross-Project Knowledge Sharing.
    Stores knowledge in a central location (~/.codex_ia_global).
    """
    def __init__(self):
        # Determine global path (platform independent)
        global_root = Path(os.path.expanduser("~")) / ".codex_ia_global"
        os.makedirs(global_root, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=str(global_root))
        
        # Local Embedding Function (Re-using the same from local store)
        try:
            from chromadb.utils import embedding_functions
            self.emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
            logging.info("🧠 Global Store using local embeddings")
        except:
            self.emb_fn = None

        self.collection = self.client.get_or_create_collection(
            name="universal_memory",
            metadata={"hnsw:space": "cosine"},
            embedding_function=self.emb_fn
        )

    def share_knowledge(self, source_project, topic, content, metadata=None):
        """Indexes knowledge into the global store."""
        try:
            doc_id = f"global_{source_project}_{topic}".replace(" ", "_")
            
            meta = {
                "source": source_project,
                "topic": topic,
                "type": "global_shared"
            }
            if metadata: meta.update(metadata)

            self.collection.upsert(
                ids=[doc_id],
                documents=[content],
                metadatas=[meta]
            )
            logging.info(f"🌍 Shared {topic} from {source_project} to Universal Memory.")
            return doc_id
        except Exception as e:
            logging.error(f"Global indexing failed: {e}")
            return None

    def search_universal(self, query, n_results=5):
        """Queries the global knowledge base."""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            hits = []
            if results['ids']:
                for i, doc in enumerate(results['documents'][0]):
                    meta = results['metadatas'][0][i]
                    hits.append({
                        "source": meta.get("source", "unknown"),
                        "topic": meta.get("topic", "unknown"),
                        "snippet": doc[:500] + "...",
                        "score": results['distances'][0][i] if results['distances'] else 0
                    })
            return hits
        except Exception as e:
            logging.error(f"Global search failed: {e}")
            return []
