import os
import sys
import chromadb
from chromadb.utils import embedding_functions

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def migrate():
    print("🚀 Starting Migration: Gemini Collections -> Local Collections")
    client = chromadb.PersistentClient(path=".codex_memory")
    
    try:
        old_coll = client.get_collection("project_codebase")
        print(f"📦 Found {old_coll.count()} fragments in 'project_codebase'.")
    except Exception as e:
        print(f"❌ Could not find old collection: {e}")
        return

    # Initialize local embedding function
    print("🧠 Initializing local model (all-MiniLM-L6-v2)...")
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    new_coll = client.get_or_create_collection(
        name="project_codebase_local",
        embedding_function=emb_fn
    )

    # Migrate in batches
    batch_size = 100
    total = old_coll.count()
    
    for i in range(0, total, batch_size):
        print(f"🔄 Migrating batch {i//batch_size + 1}/{(total//batch_size) + 1}...")
        
        data = old_coll.get(
            limit=batch_size,
            offset=i,
            include=["documents", "metadatas"]
        )
        
        if not data['ids']:
            break
            
        new_coll.upsert(
            ids=data['ids'],
            documents=data['documents'],
            metadatas=data['metadatas']
        )
    
    print(f"✅ Migration complete! New collection '{new_coll.name}' has {new_coll.count()} items.")

if __name__ == "__main__":
    migrate()
