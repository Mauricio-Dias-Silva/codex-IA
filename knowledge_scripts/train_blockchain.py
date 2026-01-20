
from advanced_trainer import DeepKnowledgeTrainer

def train_blockchain():
    print("⛓️ Iniciando Treinamento Blockchain Fundamental (GenesisCodex)...")
    # Usando o novo algoritmo DeepKnowledgeTrainer
    trainer = DeepKnowledgeTrainer("BLOCKCHAIN_CORE")
    
    topics = [
        "Criptografia de Curva Elíptica (secp256k1) e Assinaturas Digitais",
        "Funções Hash SHA-256: A Matemática da Imutabilidade",
        "O Problema dos Generais Bizantinos e Consenso Descentralizado",
        "Proof of Work (Nakamoto Consensus) vs Proof of Stake",
        "Estrutura da Merkle Tree e Validação de Blocos",
        "Smart Contracts e a Ethereum Virtual Machine (EVM) - Turing Completeness",
        "DeFi (Finanças Descentralizadas): Liquidity Pools e Automated Market Makers (AMMs)"
    ]
    
    context = "Criptógrafo Cypherpunk e Arquiteto de Software Distribuído. Foco em segurança matemática e teoria dos jogos."
    
    for topic in topics:
        trainer.ingest_topic(topic, context)

if __name__ == "__main__":
    train_blockchain()
