
from trainer_base import KnowledgeTrainer

def train_finance():
    print("💰 Iniciando Treinamento Financeiro (FinCodex)...")
    trainer = KnowledgeTrainer("FINANCAS")
    
    topics = [
        "Análise Fundamentalista de Ações: Valuation e Indicadores",
        "Macroeconomia: Taxa Selic, Inflação e Impacto nos Investimentos",
        "Contabilidade para Não-Contadores: DRE e Balanço Patrimonial",
        "Day Trade e Swing Trade: Estratégias e Gerenciamento de Risco",
        "Criptoeconomia: Bitcoin, Ethereum e DeFi (Finanças Descentralizadas)",
        "Planejamento Tributário para Empresas no Brasil",
        "Psicologia do Investidor: Vieses Cognitivos e Controle Emocional"
    ]
    
    context = "CFA Charterholder e Gestor de Fundo de Investimento. Use linguagem técnica mas acessível."
    
    for topic in topics:
        trainer.ingest_topic(topic, context)

if __name__ == "__main__":
    train_finance()
