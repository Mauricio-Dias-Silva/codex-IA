import os
import sys
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from codex_ia.core.vector_store import CodexVectorStore
from knowledge_scripts.mega_knowledge_builder import MegaKnowledgeBuilder

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_optimization():
    print("\n=== STARTING COST OPTIMIZATION VERIFICATION ===\n")
    
    # 1. Check Vector Store initialization (Local Embeddings)
    print("Testing Local Embeddings initialization...")
    try:
        store = CodexVectorStore()
        print(f"✅ Collection: {store.collection.name}")
        if hasattr(store, 'emb_fn') and store.emb_fn:
            print("✅ Local embedding model LOADED.")
        else:
            print("❌ Local embedding model NOT loaded.")
    except Exception as e:
        print(f"❌ Error initializing VectorStore: {e}")
        return

    # 2. Check Smart Skip in MegaKnowledgeBuilder
    print("\nTesting Smart Skip (Deduplication)...")
    builder = MegaKnowledgeBuilder()
    
    test_domain = "TEST_OPTIMIZATION_DOMAIN"
    test_prompt = "Generate a short text about AI optimization."
    test_metadata = {"domain": test_domain, "test": True}
    
    print(f"Step A: First run for '{test_domain}' (Should generate and index)")
    # Note: This will still call Gemini once for generation if it doesn't exist
    # To truly test skip without paying, we can mock the store check or just use a dummy
    
    builder.generate_and_index(test_domain, test_prompt, test_metadata)
    
    print(f"\nStep B: Second run for '{test_domain}' (Should skip AI call)")
    builder.generate_and_index(test_domain, test_prompt, test_metadata)
    
    print("\n=== VERIFICATION COMPLETE ===")

if __name__ == "__main__":
    test_optimization()
