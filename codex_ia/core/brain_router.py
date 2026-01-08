
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

class BrainRouter:
    """
    The Council's Receptionist.
    Routes prompts to the appropriate brain.
    """
    def __init__(self):
        self.neurons = {}
        self.active_brain = "gemini" # Default
        
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
            
        self.neurons["ollama"] = OllamaClient()

        # Set default active brain dynamically
        if "gemini" in self.neurons:
            self.active_brain = "gemini"
        elif self.neurons:
            self.active_brain = list(self.neurons.keys())[0]
        else:
            self.active_brain = "none"

    def set_brain(self, brain_name):
        if brain_name in self.neurons:
            self.active_brain = brain_name
            return True
        return False
        
    def get_active_brain(self):
         return self.neurons.get(self.active_brain)

    def send_message(self, message, web_search=False, image_path=None):
        """
        Routes the chat to the active brain.
        Fallback logic could be added here.
        """
        brain = self.get_active_brain()
        if not brain:
            return "Error: No active brain available. Please check API keys."
            
        # Capability Checks
        if image_path and self.active_brain in ["groq", "ollama"]:
            # Fallback to Gemini for Vision if available
            if "gemini" in self.neurons:
                logging.info(f"Switching to Gemini for Vision request (Active: {self.active_brain})")
                return self.neurons["gemini"].send_message(message, web_search, image_path)
            else:
                 return "Error: Active brain does not support Vision."

        if web_search and self.active_brain in ["groq", "ollama"]:
             # Fallback to Gemini for Web Search
            if "gemini" in self.neurons:
                logging.info(f"Switching to Gemini for Web Search request")
                return self.neurons["gemini"].send_message(message, web_search, image_path)
        
        return brain.send_message(message, web_search=web_search, image_path=image_path)

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
