import os
import sys
import django
from django.conf import settings

# Setup Django standalone
sys.path.append('/opt/codex-ia')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codex_web.settings')
django.setup()

from django.test import RequestFactory
from core.views import api_chat
import json

print("\n--- TEST: DJANGO API CHAT ---")

# Mock request
factory = RequestFactory()
data = {'message': 'Olá, teste de diagnóstico'}
request = factory.post(
    '/api/chat/', 
    data=json.dumps(data), 
    content_type='application/json'
)

print(f"Request created: {data}")

try:
    print("Calling view...")
    response = api_chat(request)
    print(f"Response Status: {response.status_code}")
    print(f"Response Content: {response.content.decode('utf-8')[:500]}") # Show first 500 chars
except Exception as e:
    print(f"\nCRITICAL ERROR IN VIEW execution: {e}")
    import traceback
    traceback.print_exc()

print("--- TEST END ---")
