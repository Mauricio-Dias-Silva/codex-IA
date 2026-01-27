import requests
import json
import logging
import os

class NeuralLink:
    """
    The Neural Link connects the Codex Desktop (Body) to the PythonJet Server (Brain).
    It allows the desktop app to invoke the Singularity Engine (God Mode).
    """
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.api_endpoint = f"{base_url}/api/codex/council"
        self.session = requests.Session()
        
        # Neural Link Security Protocol
        # Reads key from ENV or uses default dev key
        self.api_key = os.getenv("PYTHONJET_API_KEY", "neural-link-secret-key-2026")
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    def consult_council(self, topic):
        """
        Sends a topic to the Council (PythonJet) and awaits the God Mode verdict.
        """
        try:
            print(f"🔌 Neural Link: Transmitting thought '{topic}' to the Hive Mind...")
            
            payload = {
                "topic": topic,
                "complexity": "god_mode" # Signal to use deep research
            }
            
            response = self.session.post(self.api_endpoint, json=payload, timeout=300) # Long timeout for Deep Research
            
            if response.status_code == 200:
                data = response.json()
                verdict = data.get("verdict", "No verdict received.")
                return verdict
            else:
                return f"Neural Link Error {response.status_code}: {response.text}"
                
        except Exception as e:
            return f"Neural Link Severed: {e}"

    def check_connection(self):
        """
        Pings the server to verify the link.
        """
        try:
            resp = self.session.get(self.base_url)
            return resp.status_code == 200
        except:
            return False
