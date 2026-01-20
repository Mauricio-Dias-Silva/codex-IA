
from trainer_base import KnowledgeTrainer

def train_exams():
    print("📝 Iniciando Treinamento de Concursos (ExamCodex)...")
    trainer = KnowledgeTrainer("CONCURSOS_VESTIBULARES")
    
    topics = [
        "Metodologia de Resolução de Questões de Múltipla Escolha (Engenharia Reversa)",
        "Técnicas de Chute Científico e Eliminação de Alternativas",
        "Como a Banca Cespe/Cebraspe Pensa (Certo/Errado)",
        "Como a Banca FGV Cobra Língua Portuguesa (Interpretação e Pegadinhas)",
        "Memorização de Leis Secas: Técnicas Mnemônicas e Palácios da Memória",
        "Gerenciamento de Tempo em Prova e Controle de Ansiedade",
        "Matriz de Referência do ENEM: As 5 Competências Explicadas",
        "Raciocínio Lógico Matemático para Concursos Públicos (Tabela Verdade, Silogismos)"
    ]
    
    context = "Coach de Alta Performance em Concursos e Analista de Bancas Examinadoras. Foco em estratégia de aprovação, não apenas conteúdo."
    
    for topic in topics:
        trainer.ingest_topic(topic, context)

if __name__ == "__main__":
    train_exams()
