
from advanced_trainer import DeepKnowledgeTrainer

def train_trends():
    print("👁️ Iniciando Treinamento de Tendências e Comportamento (TrendCodex)...")
    # Usando o novo algoritmo DeepKnowledgeTrainer
    trainer = DeepKnowledgeTrainer("ZEITGEIST_TRENDS")
    
    topics = [
        "Teoria Mimética (René Girard): O Desejo como Imitação Social",
        "Efeito de Rede (Network Effects) e Viralidade Digital",
        "Psicologia das Massas e Formação de Bolhas Especulativas (FOMO)",
        "Economia da Atenção: Como Algoritmos Moldam o Comportamento",
        "Coolhunting: Metodologias para Identificar Sinais Fracos de Mudança",
        "Arquétipos Junguianos no Branding e na Cultura Pop",
        "Ciclos de Hype Tecnológico (Gartner Hype Cycle) e Adoção de Inovação"
    ]
    
    context = "Futurista, Antropólogo Digital e Investidor de Venture Capital. Foco em identificar padrões antes da massa."
    
    for topic in topics:
        trainer.ingest_topic(topic, context)

if __name__ == "__main__":
    train_trends()
