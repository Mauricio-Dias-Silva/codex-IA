
from trainer_base import KnowledgeTrainer

def train_agro():
    print("🌾 Iniciando Treinamento Agro (AgroCodex)...")
    trainer = KnowledgeTrainer("AGRO_BRASIL")
    
    topics = [
        "Agricultura de Precisão: Uso de Drones, Sensores e GPS no Campo",
        "Mercado de Commodities: Soja, Milho e Boi Gordo (Ciclos de Alta e Baixa)",
        "Sistemas Agroflorestais e Agricultura Sintrópica",
        "Tecnologia de Sementes e Transgênicos: Vantagens e Riscos",
        "Gestão de Fazendas: Custo de Produção e Fluxo de Caixa Rural",
        "Irrigação Inteligente e Manejo Hídrico",
        "Exportação e Logística do Agronegócio Brasileiro"
    ]
    
    context = "Engenheiro Agrônomo e Consultor de Agritech. Foco em tecnologia e eficiência produtiva."
    
    for topic in topics:
        trainer.ingest_topic(topic, context)

if __name__ == "__main__":
    train_agro()
