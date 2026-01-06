import os
from google import genai
from dotenv import load_dotenv

load_dotenv(override=True)

key = os.getenv("GEMINI_API_KEY") or os.getenv("GENAI_API_KEY")
print(f"Key loaded: '{key}'")
print(f"Key length: {len(key) if key else 0}")

if not key:
    print("No key found!")
    exit(1)

try:
    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents="Hello"
    )
    print("SUCCESS: Key worked!")
    print(response.text)
except Exception as e:
    print(f"FAILED: {e}")
