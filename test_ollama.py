import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
model_code = os.getenv("OLLAMA_MODEL_CODE", "deepseek-coder-v2")
model_think = os.getenv("OLLAMA_MODEL_REASONING", "deepseek-r1")

def test_model(model_name, prompt):
    print(f"\n--- Testing Model: {model_name} ---")
    data = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }
    try:
        resp = requests.post(f"{base_url}/api/generate", json=data, timeout=30)
        if resp.status_code == 200:
            print(f"SUCCESS! Response start: {resp.json().get('response', '')[:100]}...")
        else:
            print(f"FAILED: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"ERROR: {e}")

print(f"Checking if Ollama is running at {base_url}...")
try:
    requests.get(base_url)
    print("✅ Ollama is ONLINE.")
    
    test_model(model_code, "Write a hello world in Python")
    test_model(model_think, "Why is the sky blue? Answer with <think> tag logic.")
    
except Exception as e:
    print(f"❌ Ollama is OFFLINE or inaccessible: {e}")
    print("Please run 'ollama serve' and ensure models are downloaded.")
