
from trainer_base import KnowledgeTrainer

def train_psychology():
    print("🧠 Iniciando Treinamento Psicológico (PsicoCodex)...")
    trainer = KnowledgeTrainer("PSICOLOGIA_MENTE")
    
    topics = [
        "Psicanálise Freudiana: Id, Ego, Superego e Mecanismos de Defesa",
        "Psicologia Analítica de Jung: Arquétipos, Sombra e Inconsciente Coletivo",
        "Terapia Cognitivo-Comportamental (TCC): Distorções Cognitivas e Reestruturação",
        "Programação Neurolinguística (PNL): Modelagem de Excelência e Rapport",
        "Psicologia Social: Influência de Grupo e Comportamento de Massas",
        "Microexpressões Faciais e Linguagem Corporal (Paul Ekman)",
        "Neuroplasticidade: Como o Cérebro Aprende e se Modifica"
    ]
    
    context = "Doutor em Psicologia Clínica e Pesquisador de Neurociência. Foco em aplicação prática para entendimento humano."
    
    for topic in topics:
        trainer.ingest_topic(topic, context)

if __name__ == "__main__":
    train_psychology()
