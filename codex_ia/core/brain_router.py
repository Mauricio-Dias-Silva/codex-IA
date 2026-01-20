
import os
import requests
import json
import logging
import random  # Para mensagens criativas
from .llm_client import GeminiClient

# 🎭 Mensagens criativas quando IA falha
MENSAGENS_CRIATIVAS = [
    "💤 {ia} tirou um cochilo",
    "⚡ {ia} esqueceu de pagar a conta",
    "☕ {ia} saiu tomar café",
    "🤕 {ia} tá de ressaca digital",
    "🏖️ {ia} bateu a cota, foi descansar",
    "🐕 {ia} foi brincar com o cachorro",
]

class GroqClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = "llama3-70b-8192" # Free tier powerhouse
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

    def send_message(self, message, web_search=False, image_path=None):
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found.")
        
        # Groq doesn't support web_search native or image_path yet in this simple wrapper
        # We can implement simple text
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "messages": [{"role": "user", "content": message}],
            "model": self.model,
            "temperature": 0.5
        }
        
        try:
            resp = requests.post(self.base_url, headers=headers, json=data)
            if resp.status_code == 200:
                return resp.json()['choices'][0]['message']['content']
            else:
                return f"Groq Error {resp.status_code}: {resp.text}"
        except Exception as e:
            return f"Groq Client Error: {e}"

class OllamaClient:
    def __init__(self):
        self.base_url = "http://localhost:11434/api/generate"
        self.model = "llama3" # Default, user can change
        
    def send_message(self, message, web_search=False, image_path=None):
        # Ollama local check
        try:
            requests.get("http://localhost:11434")
        except:
             return "Error: Ollama is not running on localhost:11434"

        data = {
            "model": self.model,
            "prompt": message,
            "stream": False
        }
        
        try:
            resp = requests.post(self.base_url, json=data)
            if resp.status_code == 200:
                response_text = resp.json().get('response', '')
                return response_text
            else:
                return f"Ollama Error: {resp.text}"
        except Exception as e:
            return f"Ollama Client Error: {e}"

class OpenAIClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4o" # Flash flagship
        
    def send_message(self, message, web_search=False, image_path=None):
        if not self.api_key:
             return "Error: OPENAI_API_KEY not found."
             
        # Basic request to OpenAI API
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # OpenAI supports vision, but let's keep it simple text first unless image_path provided
        messages = [{"role": "user", "content": message}]
        
        if image_path:
             # Basic Vision handling could go here (base64 encode etc)
             pass 

        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.5
        }
        
        try:
            resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
            if resp.status_code == 200:
                return resp.json()['choices'][0]['message']['content']
            else:
                 return f"OpenAI Error {resp.status_code}: {resp.text}"
        except Exception as e:
            return f"OpenAI Client Error: {e}"

            return f"OpenAI Client Error: {e}"

class XAIClient:
    def __init__(self):
        self.api_key = os.getenv("XAI_API_KEY")
        self.model = "grok-beta" 
        self.base_url = "https://api.x.ai/v1/chat/completions"

    def send_message(self, message, web_search=False, image_path=None):
        if not self.api_key:
            return "Error: XAI_API_KEY not found."
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "messages": [
                {"role": "system", "content": "You are Grok, a rebellious and witty AI assistant."},
                {"role": "user", "content": message}
            ],
            "model": self.model,
            "temperature": 0.5
        }
        
        try:
            resp = requests.post(self.base_url, headers=headers, json=data)
            if resp.status_code == 200:
                return resp.json()['choices'][0]['message']['content']
            else:
                return f"xAI Error {resp.status_code}: {resp.text}"
        except Exception as e:
            return f"xAI Client Error: {e}"

class DeepSeekClient:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.model = "deepseek-coder" 
        self.base_url = "https://api.deepseek.com/chat/completions"

    def send_message(self, message, web_search=False, image_path=None):
        if not self.api_key:
            return "Error: DEEPSEEK_API_KEY not found."
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
             "messages": [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": message}
            ],
            "model": self.model,
            "temperature": 0.0 # Coding needs precision
        }
        
        try:
            resp = requests.post(self.base_url, headers=headers, json=data)
            if resp.status_code == 200:
                return resp.json()['choices'][0]['message']['content']
            else:
                return f"DeepSeek Error {resp.status_code}: {resp.text}"
        except Exception as e:
            return f"DeepSeek Client Error: {e}"

class MistralClient:
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.model = "mistral-large-latest"
        self.base_url = "https://api.mistral.ai/v1/chat/completions"

    def send_message(self, message, web_search=False, image_path=None):
        if not self.api_key:
            return "Error: MISTRAL_API_KEY not found."
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "messages": [{"role": "user", "content": message}],
            "model": self.model,
            "temperature": 0.5
        }
        
        try:
            resp = requests.post(self.base_url, headers=headers, json=data)
            if resp.status_code == 200:
                return resp.json()['choices'][0]['message']['content']
            else:
                return f"Mistral Error {resp.status_code}: {resp.text}"
        except Exception as e:
            return f"Mistral Client Error: {e}"

class ClaudeClient:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.model = "claude-3-5-sonnet-20240620"
        self.base_url = "https://api.anthropic.com/v1/messages"

    def send_message(self, message, web_search=False, image_path=None):
        if not self.api_key:
            return "Error: ANTHROPIC_API_KEY not found."
        
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": message}],
            "max_tokens": 4096,
            "temperature": 0.5
        }
        
        try:
            resp = requests.post(self.base_url, headers=headers, json=data)
            if resp.status_code == 200:
                return resp.json()['content'][0]['text']
            else:
                return f"Claude Error {resp.status_code}: {resp.text}"
        except Exception as e:
            return f"Claude Client Error: {e}"

class CohereClient:
    def __init__(self):
        self.api_key = os.getenv("COHERE_API_KEY")
        self.model = "command-r-plus"
        self.base_url = "https://api.cohere.ai/v1/chat"

    def send_message(self, message, web_search=False, image_path=None):
        if not self.api_key:
            return "Error: COHERE_API_KEY not found."
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "message": message,
            "model": self.model,
            "temperature": 0.5
        }
        
        try:
            resp = requests.post(self.base_url, headers=headers, json=data)
            if resp.status_code == 200:
                return resp.json()['text']
            else:
                return f"Cohere Error {resp.status_code}: {resp.text}"
        except Exception as e:
            return f"Cohere Client Error: {e}"

class HuggingFaceClient:
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.model = "meta-llama/Meta-Llama-3-70B-Instruct"  # ou outro modelo
        self.base_url = f"https://api-inference.huggingface.co/models/{self.model}"

    def send_message(self, message, web_search=False, image_path=None):
        if not self.api_key:
            return "Error: HUGGINGFACE_API_KEY not found."
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "inputs": message,
            "parameters": {"temperature": 0.5, "max_new_tokens": 512}
        }
        
        try:
            resp = requests.post(self.base_url, headers=headers, json=data)
            if resp.status_code == 200:
                result = resp.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', str(result))
                return str(result)
            else:
                return f"HuggingFace Error {resp.status_code}: {resp.text}"
        except Exception as e:
            return f"HuggingFace Client Error: {e}"

class PerplexityClient:
    def __init__(self):
        self.api_key = os.getenv("PERPLEXITY_API_KEY")
        self.model = "llama-3.1-sonar-large-128k-online"
        self.base_url = "https://api.perplexity.ai/chat/completions"

    def send_message(self, message, web_search=False, image_path=None):
        if not self.api_key:
            return "Error: PERPLEXITY_API_KEY not found."
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": message}],
            "temperature": 0.5
        }
        
        try:
            resp = requests.post(self.base_url, headers=headers, json=data)
            if resp.status_code == 200:
                return resp.json()['choices'][0]['message']['content']
            else:
                return f"Perplexity Error {resp.status_code}: {resp.text}"
        except Exception as e:
            return f"Perplexity Client Error: {e}"

class BrainRouter:
    """
    The Council's Receptionist.
    Routes prompts to the appropriate brain.
    """
    def __init__(self):
        self.neurons = {}
        self.active_brain = "gemini" # Default
        self.sleeping_brains = {} # {brain_name: wakeup_time_timestamp}
        
        # Initialize Brains
        try:
            self.neurons["gemini"] = GeminiClient()
        except:
            logging.warning("Gemini Client failed to init in Router")
            
        if os.getenv("GROQ_API_KEY"):
            self.neurons["groq"] = GroqClient()
            
        if os.getenv("OPENAI_API_KEY"):
            self.neurons["openai"] = OpenAIClient()

        if os.getenv("XAI_API_KEY"):
            self.neurons["xai"] = XAIClient()

        if os.getenv("DEEPSEEK_API_KEY"):
            self.neurons["deepseek"] = DeepSeekClient()
        
        # NEW: Expanded AI Support
        if os.getenv("MISTRAL_API_KEY"):
            self.neurons["mistral"] = MistralClient()
        
        # if os.getenv("ANTHROPIC_API_KEY"):
        #     self.neurons["claude"] = ClaudeClient()  # Temporariamente desabilitado - modelo incorreto
        
        if os.getenv("COHERE_API_KEY"):
            self.neurons["cohere"] = CohereClient()
        
        if os.getenv("HUGGINGFACE_API_KEY"):
            self.neurons["huggingface"] = HuggingFaceClient()
        
        if os.getenv("PERPLEXITY_API_KEY"):
            self.neurons["perplexity"] = PerplexityClient()
            
        self.neurons["ollama"] = OllamaClient()

    def get_available_brain(self):
        """Finds a brain that is awake."""
        import time
        now = time.time()
        
        # Check if anyone woke up
        woke_up = []
        for name, wakeup_time in self.sleeping_brains.items():
            if now > wakeup_time:
                woke_up.append(name)
        
        for name in woke_up:
            del self.sleeping_brains[name]
            logging.info(f"⏰ {name.upper()} acordou do sono!")
            
        # Try active preference first
        if self.active_brain in self.neurons and self.active_brain not in self.sleeping_brains:
            return self.active_brain, self.neurons[self.active_brain]
            
        # Fallback loop
        for name, client in self.neurons.items():
            if name not in self.sleeping_brains:
                 logging.info(f"🔄 Failover: Usando {name} pois {self.active_brain} não está disponível.")
                 return name, client
                 
        return None, None

    def send_message(self, message, web_search=False, image_path=None):
        """
        Routes the chat with Auto-Failover.
        """
        import time
        
        max_retries = len(self.neurons)
        attempts = 0
        last_error = ""
        
        while attempts < max_retries:
            brain_name, brain = self.get_available_brain()
            
            if not brain:
                return f"😴 Zzz... Todas as IAs estão 'dormindo' (Rate Limit). Tente novamente em alguns minutos.\n\nStatus do Sono:\n{self.sleeping_brains}"
                
            try:
                # Capability Checks Handling
                if (web_search or image_path) and brain_name not in ["gemini", "openai"]:
                     # If primary feature brain is asleep, we might degrade service (no image/search) 
                     # but still answer text. Let's warn.
                     if "gemini" in self.sleeping_brains:
                         message += "\n[SYSTEM NOTE: Image/Search capabilities reduced because Gemini is sleeping.]"
                
                response = brain.send_message(message, web_search=web_search, image_path=image_path)
                
                # Check for "sleeping" errors (429, Quota) in response string (since clients handle exceptions returning strings)
                if "429" in str(response) or "Quota" in str(response) or "Rate limit" in str(response):
                    logging.warning(f"💤 {brain_name} está cansado (Rate Limit). Colocando para dormir por 5 min.")
                    self.sleeping_brains[brain_name] = time.time() + 300 # Sleep 5 min
                    attempts += 1
                    continue
                
                # Success signature check
                if "Error" in str(response) and len(str(response)) < 200:
                     # Generic error, maybe not sleep, just retry next
                     logging.warning(f"⚠️ Erro no {brain_name}: {response}")
                     attempts += 1
                     last_error = response
                     continue
                     
                return response
                
            except Exception as e:
                logging.error(f"Critical error on {brain_name}: {e}")
                attempts += 1
                last_error = str(e)
        
        return f"❌ Falha no Conselho. Todas as IAs falharam. Último erro: {last_error}"

    def council_meeting(self, message):
        """
        The Council Convenes.
        Broadcasting the message to ALL available brains and synthesizing the result.
        """
        responses = {}
        errors = []
        
        # 1. Broadcast Phase
        available_neurons = [n for n in self.neurons.keys() if n != 'ollama'] # Skip local slower ollama for high-level debate unless requested
        if 'ollama' in self.neurons and len(available_neurons) == 0:
             available_neurons.append('ollama') # Use ollama if nothing else

        logging.info(f"Council convening with: {available_neurons}")
        
        for name in available_neurons:
            try:
                # Ask each brain
                responses[name] = self.neurons[name].send_message(message)
            except Exception as e:
                errors.append(f"{name} failed: {e}")

        # 2. Synthesis Phase
        # Prefer smart models, but accept anyone
        chair = self.neurons.get('openai') or self.neurons.get('gemini') or self.neurons.get('xai') or self.neurons.get('deepseek') or self.neurons.get('ollama')
        
        if not chair:
             return "Council Failed: No Chairperson available (Verification Failed)."

        # Compile the Minutes
        minutes = "## The Council of AIs - Debate Minutes 📜\n\n"
        minutes += f"**Topic:** {message}\n\n"
        
        synthesis_prompt = f"""
        You are the Chairperson of a Council of Superintelligences.
        The user asked: '{message}'
        
        Here are the opinions of the council members:
        
        """
        
        for name, response in responses.items():
            minutes += f"### 🗣️ {name.upper()}'s Opinion:\n{response[:500]}...\n\n" # Truncate for display in prompt but use full for synthesis
            synthesis_prompt += f"--- {name.upper()} SAID: ---\n{response}\n\n"
            
        synthesis_prompt += """
        --- END OF OPINIONS ---
        
        Your Job:
        1. Analyze the points of agreement and disagreement.
        2. Identify the most insightful or accurate parts of each response.
        3. Synthesize a FINAL, GOLDEN ANSWER that combines the best of all worlds.
        4. If the goal is humanitarian or prediction, look for the 'Highest Good' in the answers.
        
        Return your Synthesis.
        """
        
        final_verdict = chair.send_message(synthesis_prompt)
        
        return f"{minutes}\n---\n## ⚖️ FINAL VERDICT:\n{final_verdict}"
    
    def parallel_execution(self, message, max_workers=None):
        """
        🚀 PARALLEL AI CONSORTIUM
        Divide uma tarefa entre múltiplas IAs em paralelo.
        """
        import time
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        start_time = time.time()
        
        # Filtrar IAs disponíveis
        available_ais = [name for name in self.neurons.keys() 
                         if name not in self.sleeping_brains and name != 'ollama']
        
        if not available_ais:
            return {
                'status': 'error',
                'error': 'Nenhuma IA disponível.',
                'active_ais': [],
                'partial_results': {},
                'synthesis': ''
            }
        
        if max_workers:
            available_ais = available_ais[:max_workers]
        
        logging.info(f"🚀 Parallel with {len(available_ais)} AIs: {available_ais}")
        
        partial_results = {}
        errors = {}
        
        def query_ai(ai_name):
            try:
                response = self.neurons[ai_name].send_message(message)
                return (ai_name, response, None)
            except Exception as e:
                return (ai_name, None, str(e))
        
        # Parallel execution
        with ThreadPoolExecutor(max_workers=len(available_ais)) as executor:
            futures = {executor.submit(query_ai, ai): ai for ai in available_ais}
            
            for future in as_completed(futures):
                ai_name, response, error = future.result()
                if error:
                    # Mensagem criativa
                    msg_criativa = random.choice(MENSAGENS_CRIATIVAS).format(ia=ai_name.upper())
                    
                    # Simplificar erro técnico (remover JSON gigante)
                    erro_tecnico = str(error)
                    if "429" in erro_tecnico or "quota" in erro_tecnico.lower():
                        erro_tecnico = "Cota de API excedida ou Too Many Requests"
                    elif "404" in erro_tecnico:
                        erro_tecnico = "Modelo não encontrado ou indisponível"
                    else:
                        erro_tecnico = erro_tecnico[:50] + "..." # Cortar erros longos
                        
                    errors[ai_name] = f"{msg_criativa} (Info: {erro_tecnico})"
                else:
                    partial_results[ai_name] = response
        
        if not partial_results:
            return {
                'status': 'error',
                'error': 'Todas falharam',
                'active_ais': available_ais,
                'partial_results': {},
                'errors': errors,
                'synthesis': ''
            }
        
        
        # Synthesis
        participantes = ", ".join([ai.upper() for ai in partial_results.keys()])
        
        synthesis_prompt = f'''Você é o SECRETÁRIO DO CONSELHO de Inteligências Artificiais.
        
PERGUNTA DO USUÁRIO: "{message}"

IAs PARTICIPANTES: {participantes}

OPINIÕES INDIVIDUAIS:
'''
        for ai, resp in partial_results.items():
            synthesis_prompt += f"\n👉 {ai.upper()}:\n{resp}\n"
        
        synthesis_prompt += '''
        
SUA MISSÃO - RELATÓRIO FINAL:
1. Inicie com: "🎙️ **Relatório do Conselho**"
2. Liste quem participou do debate.
3. Resuma os pontos de consenso (onde todos concordaram).
4. Destaque opiniões únicas ou divergentes importantes.
5. Conclua com a MELHOR resposta unificada possível.
6. Use formatação Markdown (negrito, listas) para facilitar a leitura.
7. Seja profissional e direto.

MENSAGEM SECRETA PARA ERROS: Se alguma IA falhou (não está na lista), ignore-a silenciamente na síntese.
'''
        
        synthesizer = (self.neurons.get('claude') or 
                       self.neurons.get('openai') or 
                       self.neurons.get('gemini') or 
                       list(self.neurons.values())[0])
        
        try:
            synthesis = synthesizer.send_message(synthesis_prompt)
        except Exception as e:
            synthesis = f"Erro: {e}\n\n" + "\n\n".join([f"**{k}**: {v[:200]}..." for k,v in partial_results.items()])
        
        return {
            'status': 'success',
            'active_ais': list(partial_results.keys()),
            'partial_results': partial_results,
            'synthesis': synthesis,
            'processing_time': round(time.time() - start_time, 2),
            'errors': errors
        }
