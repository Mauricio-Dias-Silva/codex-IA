
from trainer_base import KnowledgeTrainer

def train_esoterism():
    print("🔮 Iniciando Treinamento Esotérico (MysticCodex)...")
    trainer = KnowledgeTrainer("ESOTERISMO")
    
    topics = [
        "As 7 Leis Herméticas (O Caibalion) Explicadas",
        "Astrologia: Significado Profundo das Casas e Planetas",
        "Numerologia Pitagórica: Arquétipos dos Números 1 a 9",
        "Geometria Sagrada: Flor da Vida e Sólidos Platônicos",
        "Tarot: A Jornada do Louco e os Arcanos Maiores",
        "Radiestesia e Radiônica: Princípios de Vibração e Cura",
        "Kabbalah: A Árvore da Vida e as Sephiroth"
    ]
    
    context = "Mestre Ocultista e Erudito em Sabedoria Antiga. Explique com profundidade filosófica e prática."
    
    for topic in topics:
        trainer.ingest_topic(topic, context)

if __name__ == "__main__":
    train_esoterism()
