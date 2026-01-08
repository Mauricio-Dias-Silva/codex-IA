import os
from dotenv import dotenv_values

print("--- ENV DIAGNOSTIC ---")
try:
    env = dotenv_values(".env")
    print(f"Loaded {len(env)} keys from .env")
    for k, v in env.items():
        print(f"KEY: {repr(k)} | VALUE_LEN: {len(v) if v else 0} | START: {repr(v[:5]) if v else 'None'}")
        if not k or not v:
            print(f"⚠️  WARNING: Empty key or value detected for {repr(k)}")
    
    print("\n--- CHECKING API KEYS ---")
    keys = ["GEMINI_API_KEY", "OPENAI_API_KEY", "GROQ_API_KEY", "XAI_API_KEY", "DEEPSEEK_API_KEY"]
    for key in keys:
        loaded = env.get(key)
        print(f"{key}: {'✅ FOUND' if loaded else '❌ MISSING'}")
        
except Exception as e:
    print(f"FATAL: {e}")
