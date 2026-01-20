
from trainer_base import KnowledgeTrainer

def train_marketing():
    print("📣 Iniciando Treinamento de Marketing (GrowthCodex)...")
    trainer = KnowledgeTrainer("MARKETING_DIGITAL")
    
    topics = [
        "Fórmula de Lançamento: 6 em 7, CPLs e Abertura de Carrinho",
        "Tráfego Pago Avançado: Estrutura de Campanhas Meta Ads e Google Ads",
        "Copywriting de Conversão: Cartas de Vendas, Headlines e AIDA",
        "Branding e Posicionamento de Marca: Arquétipos de Marca",
        "Funis de Vendas Automáticos (Evergreen): Estratégia e Implementação",
        "SEO Técnico e de Conteúdo: Rankeamento no Google (White Hat)",
        "Marketing de Influência e Comunidades: Construção de Tribos"
    ]
    
    context = "CMO (Chief Marketing Officer) de Startup Unicórnio. Focada em métricas, CAC, LTV e ROI."
    
    for topic in topics:
        trainer.ingest_topic(topic, context)

if __name__ == "__main__":
    train_marketing()
