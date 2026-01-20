"""
🧪 TESTE PhD: Pergunta Interdisciplinar para o Codex
"""

from codex_ia.core.vector_store import CodexVectorStore
from codex_ia.core.llm_client import GeminiClient

store = CodexVectorStore()
llm = GeminiClient()

# Busca contexto acadêmico
query = "Resource-Based View Effectuation Blue Ocean Strategy Circular Economy sustainable competitive advantage"
context_results = store.semantic_search(query, n_results=5)

# Monta contexto
context_text = "\n\n".join([
    f"FONTE {i+1}:\n{r['snippet']}" 
    for i, r in enumerate(context_results)
])

# Pergunta desafiadora
question = """
DESAFIO PhD-LEVEL:

Como uma startup de economia circular pode usar SIMULTANEAMENTE:

1. EFFECTUATION THEORY (Saras Sarasvathy) para navegar incerteza inicial
2. RESOURCE-BASED VIEW (Jay Barney) para construir vantagens VRIN inimitáveis
3. BLUE OCEAN STRATEGY (Kim & Mauborgne) para criar mercados não-contestados

Desenvolva um FRAMEWORK INTEGRADO que:
- Mostre como essas 3 teorias se complementam (não conflitam)
- Dê um exemplo REAL de empresa que fez isso
- Explique as fases de desenvolvimento (early-stage → scale-up)

Responda com rigor acadêmico.
"""

# Gera resposta
llm.start_chat()
response = llm.send_message(f"""
CONTEXTO ACADÊMICO RECUPERADO DO VECTOR STORE:
{context_text}

{question}
""")

print("\n" + "="*80)
print("🎓 RESPOSTA DO CODEX (Teste PhD-Level)")
print("="*80)
print(response)
print("\n" + "="*80)
