
from trainer_base import KnowledgeTrainer

def train_strategy():
    print("🦁 Iniciando Treinamento Estratégico (StratCodex)...")
    trainer = KnowledgeTrainer("ESTRATEGIA_NEGOCIOS")
    
    topics = [
        # Hunter (Vendas)
        "Spin Selling: A Arte de Fazer Perguntas de Situação, Problema, Implicação e Necessidade",
        "Negociação do FBI: Técnicas de Empatia Tática e Espelhamento (Chris Voss)",
        "Copywriting Persuasivo: Gatilhos Mentais e Jornada do Herói",
        
        # Shark Tank (Startups)
        "Valuation de Startups: DCF, Múltiplos e Venture Capital Arithmetic",
        "Lean Startup: MVP, Pivot e Ciclo Construir-Medir-Aprender",
        "Pitch Deck Vencedor: Estrutura Narrativa para Captar Investimento",
        "Growth Hacking: Funil AARRR e Estratégias de Crescimento Exponencial",
        
        # The Council (Mindset)
        "Estoicismo Aplicado aos Negócios: Gestão Emocional e Resiliência",
        "A Arte da Guerra (Sun Tzu) Aplicada ao Mercado Corporativo Moderno",
        "Modelos Mentais de Charlie Munger para Tomada de Decisão (Inversão, Círculo de Competência)"
    ]
    
    context = "Bilionário Self-Made e Estrategista Chefe. Use linguagem direta, pragmática e focada em resultados."
    
    for topic in topics:
        trainer.ingest_topic(topic, context)

if __name__ == "__main__":
    train_strategy()
