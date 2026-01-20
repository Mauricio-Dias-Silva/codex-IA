
from trainer_base import KnowledgeTrainer

def train_education():
    print("🎓 Iniciando Treinamento Educacional (EduCodex - BNCC)...")
    trainer = KnowledgeTrainer("EDUCACAO_BNCC")
    
    # Matérias Base da BNCC (Ensino Médio e Fundamental)
    topics = [
        # Linguagens
        "Gramática Normativa Completa: Morfologia, Sintaxe e Semântica",
        "Literatura Brasileira e Portuguesa: Escolas Literárias e Principais Obras",
        "Redação Nota 1000: Estrutura Dissertativa-Argumentativa e Coesão",
        
        # Matemática
        "Matemática Básica: Frações, Porcentagem e Raciocínio Lógico",
        "Álgebra e Funções: Do 1º Grau a Exponencial e Logarítmica",
        "Geometria Plana, Espacial e Analítica: Fórmulas e Teoremas",
        "Estatística e Probabilidade: Análise Combinatória e Tratamento de Dados",
        
        # Ciências da Natureza
        "Física: Mecânica Clássica (Newton), Termodinâmica e Eletromagnetismo",
        "Química: Tabela Periódica, Estequiometria e Química Orgânica",
        "Biologia: Citologia, Genética (Mendel), Evolução e Ecologia",
        
        # Ciências Humanas
        "História do Brasil: Colônia, Império e República (Fatos e Causas)",
        "História Geral: Antiguidade, Idade Média, Moderna e Contemporânea",
        "Geografia: Geopolítica Mundial, Cartografia e Geografia Física do Brasil",
        "Filosofia e Sociologia: Principais Pensadores e Teorias Sociais"
    ]
    
    passo_a_passo = """
    ATUE COMO: Professor Titular com Doutorado em Educação.
    EXPLIQUE COMO: Se estivesse dando a melhor aula do mundo para um aluno de vestibular.
    ESTRUTURA: 
    1. Conceitos Chave (Definições precisas).
    2. O "Pulo do Gato" (Dicas que ninguém ensina).
    3. Erros Comuns em Provas.
    4. Conexões Interdisciplinares.
    """
    
    for topic in topics:
        trainer.ingest_topic(topic, passo_a_passo)

if __name__ == "__main__":
    train_education()
