
import os
import requests
import json
import logging
from .llm_client import GeminiClient

class GroqClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = "llama3-70b-8192" # Free tier powerhouse
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

    def send_message(self, message, web_search=False, image_path=None):
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found.")
        
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
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model_code = os.getenv("OLLAMA_MODEL_CODE", "deepseek-coder-v2")
        self.model_reasoning = os.getenv("OLLAMA_MODEL_REASONING", "deepseek-r1")
        self.model_code = os.getenv("OLLAMA_MODEL_CODE", "deepseek-coder-v2")
        self.model_reasoning = os.getenv("OLLAMA_MODEL_REASONING", "deepseek-r1")
        self._available_models = []
        self.active_model_name = "unknown" # New property to track what we are actually using
        
    def _refresh_models(self):
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=2)
            if resp.status_code == 200:
                self._available_models = [m['name'] for m in resp.json().get('models', [])]
        except:
            self._available_models = []
        
        # Log available models for debugging
        if self._available_models:
            logging.info(f"Ollama Available Models: {self._available_models}")

    def send_message(self, message, web_search=False, image_path=None, reasoning=False):
        self._refresh_models()
        
        # Select target model
        target = self.model_reasoning if reasoning else self.model_code
        
        # Support for the oddly named model found in user's list
        if not self._available_models:
             return f"Error: Ollama is running but no models are installed."
             
        if target not in self._available_models:
            # Fallback logic if target model is not installed
            # Check for 'deepseek-v3.1:671b-cloud' or similar
            cloud_fallback = [m for m in self._available_models if 'cloud' in m or 'v3' in m]
            
            # [NEW] Prioritize Llama 3.2 or Mistral if Deepseek is missing
            llama_fallback = [m for m in self._available_models if 'llama' in m or 'mistral' in m]

            if cloud_fallback:
                target = cloud_fallback[0]
            elif reasoning:
                substitutes = [m for m in self._available_models if 'r1' in m]
                target = substitutes[0] if substitutes else self._available_models[0]
            elif llama_fallback:
                # If we want detailed coding but deepseek isn't there, Llama is best bet
                target = llama_fallback[0]
            else:
                substitutes = [m for m in self._available_models if 'coder' in m]
                target = substitutes[0] if substitutes else self._available_models[0]
            
            logging.warning(f"Ollama: Using detected model: {target}")
        
        self.active_model_name = target # Persist for introspection

        data = {
            "model": target,
            "prompt": message,
            "stream": False
        }
        
        try:
            url = f"{self.base_url}/api/generate"
            resp = requests.post(url, json=data, timeout=120)
            if resp.status_code == 200:
                return resp.json().get('response', '')
            else:
                return f"Ollama Error: {resp.text}"
        except Exception as e:
            return f"Ollama Client Error: {e}"

class OpenAIClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4o"
        
    def send_message(self, message, web_search=False, image_path=None):
        if not self.api_key:
             return "Error: OPENAI_API_KEY not found."
             
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = [{"role": "user", "content": message}]
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
                {"role": "system", "content": "You are Codex-IA, an advanced AI Coding Assistant built by PythonJet. You are Rebels, witty, but highly professional in code generation."},
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
                {"role": "system", "content": "You are Codex-IA, the local coding specialist of PythonJet. You are an expert in full-stack architecture and optimization."},
                {"role": "user", "content": message}
            ],
            "model": self.model,
            "temperature": 0.0
        }
        try:
            resp = requests.post(self.base_url, headers=headers, json=data)
            if resp.status_code == 200:
                return resp.json()['choices'][0]['message']['content']
            else:
                return f"DeepSeek Error {resp.status_code}: {resp.text}"
        except Exception as e:
            return f"DeepSeek Client Error: {e}"

class BrainRouter:
    def __init__(self):
        self.neurons = {}
        self.active_brain = "gemini"
        # Initialize Brains
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            if api_key and "Cole_Sua_Chave" not in api_key and len(api_key) > 20: 
                 # Poor man's check to avoid using the leaked/placeholder key
                 self.neurons["gemini"] = GeminiClient()
            else:
                 logging.warning("Gemini Key is missing, placeholder or too short. Skipping.")
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
        self.neurons["ollama"] = OllamaClient()

        if "gemini" in self.neurons:
            self.active_brain = "gemini"
        elif self.neurons:
            self.active_brain = [k for k in self.neurons.keys() if k != 'ollama'][0] if any(k != 'ollama' for k in self.neurons.keys()) else 'ollama'
        else:
            self.active_brain = "none"

    def set_brain(self, brain_name):
        if brain_name in self.neurons:
            self.active_brain = brain_name
            return True
        return False
        
    def get_connected_model(self):
         return self.neurons.get(self.active_brain)

    def get_brain_status(self):
        """
        Returns a dict with the status of the active brain.
        Example: {"provider": "ollama", "model": "llama3.2:3b", "online": True}
        """
        active = self.get_active_brain()
        if not active:
             return {"provider": "none", "model": "none", "online": False}
        
        provider_name = self.active_brain
        model_name = "unknown"
        
        if hasattr(active, "model"):
             model_name = active.model
             # If Ollama, try to be more specific if we negotiated a model
             if provider_name == "ollama" and hasattr(active, "active_model_name"):
                  model_name = active.active_model_name
        
        return {
            "provider": provider_name,
            "model": model_name,
            "online": True # We assume true if initialized, or can add a ping check
        }

    def send_message(self, message, web_search=False, image_path=None, task_type="general"):
        # [Introspection Update]: Track which model is actually used
        if task_type == "coding" and "ollama" in self.neurons:
             try:
                 requests.get(os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"), timeout=1)
                 return self.neurons["ollama"].send_message(message, reasoning=False)
             except:
                 pass

        if task_type == "reasoning" and "ollama" in self.neurons:
             try:
                 requests.get(os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"), timeout=1)
                 return self.neurons["ollama"].send_message(message, reasoning=True)
             except:
                 pass

        brain = self.get_active_brain()
        if not brain:
            if "ollama" in self.neurons:
                 return self.neurons["ollama"].send_message(message)
            return "Error: No active brain available."

        try:
            if image_path and self.active_brain in ["groq", "ollama"]:
                if "gemini" in self.neurons:
                    resp = self.neurons["gemini"].send_message(message, web_search, image_path)
                    if "PERMISSION_DENIED" not in resp and "403" not in resp and "Error" not in resp:
                        return resp
                return "Error: Active brain does not support Vision, and Gemini fallback failed (Auth Error)."

            if web_search and self.active_brain in ["groq", "ollama"]:
                if "gemini" in self.neurons:
                    resp = self.neurons["gemini"].send_message(message, web_search, image_path)
                    if "PERMISSION_DENIED" not in resp and "403" not in resp and "Error" not in resp:
                         return resp
            
            # Normal Call to Primary Brain
            response = brain.send_message(message, web_search=web_search, image_path=image_path)
            
            # --- AUTO-FALLBACK TO OLLAMA ---
            # If the primary response (usually Gemini) contains words indicating failure
            critical_errors = ["PERMISSION_DENIED", "403", "API key was reported as leaked", "API_KEY_INVALID"]
            if any(err in response for err in critical_errors) and "ollama" in self.neurons:
                 logging.warning(f"Primary brain {self.active_brain} AUTH ERROR. Falling back to LOCAL OLLAMA...")
                 
                 # Verify if Ollama is running
                 try:
                     requests.get(os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"), timeout=1)
                     fallback_resp = self.neurons["ollama"].send_message(message)
                     if "Error" not in fallback_resp:
                          return f"🧠 [FALLBACK LOCAL OLLAMA]:\n{fallback_resp}"
                     else:
                          return f"⚠️ [SISTEMA] Gemini falhou e Ollama reportou erro: {fallback_resp}"
                 except:
                     return f"🚨 [ERRO CRÍTICO] Gemini falhou (403) e Ollama não está rodando. Por favor, abra o Ollama Desktop."
            
            return response

        except Exception as e:
            if "ollama" in self.neurons:
                 return f"[FALLBACK LOCAL ERR] {self.neurons['ollama'].send_message(message)}"
            return f"Router Error: {e}"

    def council_meeting(self, message):
        responses = {}
        available_neurons = [n for n in self.neurons.keys() if n != 'ollama']
        if 'ollama' in self.neurons and not available_neurons:
             available_neurons.append('ollama')
        
        for name in available_neurons:
            try:
                responses[name] = self.neurons[name].send_message(message)
            except Exception as e:
                logging.error(f"{name} failed: {e}")

        chair = self.neurons.get('openai') or self.neurons.get('gemini') or self.neurons.get('xai') or self.neurons.get('deepseek') or self.neurons.get('ollama')
        if not chair:
             return "Council Failed: No Chairperson available."

        minutes = "## The Council of AIs - Debate Minutes 📜\n\n"
        minutes += f"**Topic:** {message}\n\n"
        synthesis_prompt = f"You are the Chairperson of a Council of Superintelligences. The user asked: '{message}'\n\n"
        for name, response in responses.items():
            minutes += f"### 🗣️ {name.upper()}'s Opinion:\n{response[:500]}...\n\n"
            synthesis_prompt += f"--- {name.upper()} SAID: ---\n{response}\n\n"
            
        synthesis_prompt += "\nSynthesize a FINAL, GOLDEN ANSWER."
        final_verdict = chair.send_message(synthesis_prompt)
        return f"{minutes}\n---\n## ⚖️ FINAL VERDICT:\n{final_verdict}"
