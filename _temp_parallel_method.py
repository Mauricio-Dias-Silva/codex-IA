import threading
import queue
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def parallel_execution_method(self, message, max_workers=None):
    """
    Divide uma tarefa entre múltiplas IAs em paralelo.
    Cada IA processa a MESMA pergunta de perspectivas diferentes.
    Depois sintetiza em uma resposta final.
    
    Args:
        message: A pergunta/tarefa do usuário
        max_workers: Número máximo de IAs em paralelo (None = todas disponíveis)
    
    Returns:
        dict: {
            'status': 'success',
            'active_ais': ['gemini', 'gpt', ...],
            'partial_results': {'gemini': '...', 'gpt': '...'},
            'synthesis': 'Resposta final sintetizada',
            'processing_time': 5.2
        }
    """
    import time
    start_time = time.time()
    
    # Filtrar IAs disponíveis (que não estão dormindo)
    available_ais = [name for name in self.neurons.keys() 
                     if name not in self.sleeping_brains and name != 'ollama']
    
    if not available_ais:
        return {
            'status': 'error',
            'error': 'Nenhuma IA disponível. Todas estão em rate limit.',
            'active_ais': [],
            'partial_results': {},
            'synthesis': ''
        }
    
    # Limitar workers se especificado
    if max_workers:
        available_ais = available_ais[:max_workers]
    
    logging.info(f"🚀 Processamento Paralelo com {len(available_ais)} IAs: {available_ais}")
    
    partial_results = {}
    errors = {}
    
    # Função para cada worker thread
    def query_ai(ai_name):
        try:
            brain = self.neurons[ai_name]
            response = brain.send_message(message)
            return (ai_name, response, None)
        except Exception as e:
            return (ai_name, None, str(e))
    
    # Executar em paralelo
    with ThreadPoolExecutor(max_workers=len(available_ais)) as executor:
        future_to_ai = {executor.submit(query_ai, ai_name): ai_name 
                        for ai_name in available_ais}
        
        for future in as_completed(future_to_ai):
            ai_name, response, error = future.result()
            if error:
                errors[ai_name] = error
                logging.warning(f"❌ {ai_name} falhou: {error}")
            else:
                partial_results[ai_name] = response
                logging.info(f"✅ {ai_name} completou")
    
    # Se todas falharam
    if not partial_results:
        return {
            'status': 'error',
            'error': 'Todas as IAs falharam',
            'active_ais': available_ais,
            'partial_results': {},
            'errors': errors,
            'synthesis': ''
        }
    
    # Síntese Final
    synthesis_prompt = f"""
    Você é o sintetizador de um consórcio de IAs.
    
    PERGUNTA ORIGINAL: "{message}"
    
    RESPOSTAS DAS IAs:
    """
    
    for ai_name, response in partial_results.items():
        synthesis_prompt += f"\n\n--- {ai_name.upper()} respondeu: ---\n{response}\n"
    
    synthesis_prompt += """
    
    --- FIM DAS RESPOSTAS ---
    
    SUA MISSÃO:
    1. Analise as respostas acima buscando COMPLEMENTARIDADE (não repetição)
    2. Identifique insights únicos de cada IA
    3. Sintetize uma resposta FINAL em português que:
       - Combine o melhor de cada perspectiva
       - Seja coerente e objetiva
       - Destaque consensos E divergências importantes
       - Seja mais completa que qualquer resposta individual
    
    Retorne APENAS a síntese final, sem meta-comentários.
    """
    
    # Escolher sintetizador (preferir Claude/GPT para síntese)
    synthesizer = (self.neurons.get('claude') or 
                   self.neurons.get('openai') or 
                   self.neurons.get('gemini') or 
                   list(self.neurons.values())[0])
    
    try:
        synthesis = synthesizer.send_message(synthesis_prompt)
    except Exception as e:
        synthesis = f"Erro na síntese: {e}\n\n" + "\n\n".join([f"**{k}**: {v[:200]}..." for k,v in partial_results.items()])
    
    processing_time = time.time() - start_time
    
    return {
        'status': 'success',
        'active_ais': list(partial_results.keys()),
        'partial_results': partial_results,
        'synthesis': synthesis,
        'processing_time': round(processing_time, 2),
        'errors': errors if errors else {}
    }

# Adicionar este método à classe BrainRouter
BrainRouter.parallel_execution = parallel_execution_method
