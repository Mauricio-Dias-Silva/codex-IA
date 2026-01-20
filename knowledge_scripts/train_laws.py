
from trainer_base import KnowledgeTrainer

def train_laws():
    print("⚖️ Iniciando Treinamento Jurídico (LexCodex)...")
    trainer = KnowledgeTrainer("LEIS_BRASIL")
    
    topics = [
        "Constituição Federal de 1988: Princípios Fundamentais e Direitos Garantidos",
        "Código Civil Brasileiro: Direito das Obrigações e Contratos",
        "Código de Defesa do Consumidor: Direitos Básicos e Práticas Abusivas",
        "Lei Geral de Proteção de Dados (LGPD): Fundamentos e Aplicação Prática",
        "Direito Trabalhista CLT: Direitos do Empregado e Deveres do Empregador",
        "Processo Civil: Prazos, Recursos e Tutelas de Urgência",
        "Direito Digital e Crimes Cibernéticos no Brasil"
    ]
    
    context = "Juiz Federal e Doutor em Direito Constitucional. Especialista em simplificar o juridiquês mantendo a precisão técnica."
    
    for topic in topics:
        trainer.ingest_topic(topic, context)

if __name__ == "__main__":
    train_laws()
