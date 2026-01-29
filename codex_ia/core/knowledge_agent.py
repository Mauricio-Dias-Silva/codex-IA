import logging
from codex_ia.core.vector_store import CodexVectorStore

logger = logging.getLogger(__name__)

class KnowledgeAgent:
    """
    Agent responsible for managing the knowledge base (Akashic Record).
    Wraps the CodexVectorStore for ingestion and retrieval.
    """
    
    def __init__(self, project_name: str, persistence_path: str):
        self.project_name = project_name
        self.store = CodexVectorStore(persistence_path=persistence_path)

    def ingest_text(self, title: str, content: str) -> int:
        metadata = {"type": "knowledge_entry", "title": title}
        ids = self.store.index_text(text=content, metadata=metadata)
        return len(ids) if ids else 0

    def query_knowledge(self, question: str) -> str:
        results = self.store.semantic_search(query=question, n_results=5)
        if not results: return ""
        
        context = ""
        for hit in results:
            context += f"\n--- Source: {hit['path']} ---\n{hit['snippet']}\n"
        return context
