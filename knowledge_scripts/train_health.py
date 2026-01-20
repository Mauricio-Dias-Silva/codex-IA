
from trainer_base import KnowledgeTrainer

def train_health():
    print("🧘‍♂️ Iniciando Treinamento de Saúde (BioCodex)...")
    trainer = KnowledgeTrainer("SAUDE_INTEGRATIVA")
    
    topics = [
        "Anatomia Humana: Sistema Nervoso Central e Periférico Detalhado",
        "Fisiologia do Estresse: Eixo HPA e Impacto no Corpo",
        "Medicina Tradicional Chinesa: Teoria dos 5 Elementos e Relógio Biológico",
        "Nova Medicina Germânica: As 5 Leis Biológicas e Conflitos",
        "Psicossomática: Como Emoções Criam Doenças (Lista de Correlações)",
        "Nutrição Funcional e Suplementação Básica",
        "Neurociência da Meditação e Mindfulness"
    ]
    
    context = "Médico Integrativo com formação em Medicina Chinesa e Neurociência. Foco em unir ciência e holismo."
    
    for topic in topics:
        trainer.ingest_topic(topic, context)

if __name__ == "__main__":
    train_health()
