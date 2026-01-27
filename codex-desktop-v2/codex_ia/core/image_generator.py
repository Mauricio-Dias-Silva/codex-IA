import os
import requests
import json
import base64
from io import BytesIO

class ImageGenerator:
    """
    Gerador de imagens usando DALL-E (OpenAI) com fallback para Stable Diffusion (HuggingFace).
    """
    
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.hf_key = os.getenv("HUGGINGFACE_API_KEY")
        
    def generate_dalle(self, prompt):
        """Gera imagem usando DALL-E 3 (OpenAI)"""
        if not self.openai_key:
            raise Exception("OpenAI API key não configurada")
        
        url = "https://api.openai.com/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "dall-e-3",
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024",
            "quality": "standard"
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result['data'][0]['url']
    
    def generate_stable_diffusion(self, prompt):
        """Gera imagem usando Stable Diffusion (HuggingFace - GRÁTIS)"""
        if not self.hf_key:
            raise Exception("HuggingFace API key não configurada")
        
        # Modelo gratuito Stable Diffusion (mais estável)
        model_id = "runwayml/stable-diffusion-v1-5"
        api_url = f"https://api-inference.huggingface.co/models/{model_id}"
        
        headers = {
            "Authorization": f"Bearer {self.hf_key}",
            "Content-Type": "application/json"
        }
        payload = {"inputs": prompt}
        
        response = requests.post(api_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        # Retorna imagem em base64
        image_bytes = response.content
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')
        return f"data:image/png;base64,{image_b64}"
    
    def generate(self, prompt):
        """
        Gera imagem com fallback automático:
        1. Tenta DALL-E (melhor qualidade)
        2. Se falhar, usa Stable Diffusion (grátis)
        """
        try:
            print("🎨 Tentando DALL-E (OpenAI)...")
            return {
                'status': 'success',
                'provider': 'DALL-E 3 (OpenAI)',
                'image_url': self.generate_dalle(prompt)
            }
        except Exception as e:
            print(f"⚠️ DALL-E falhou: {e}")
            print("🎨 Usando Stable Diffusion (HuggingFace)...")
            
            try:
                return {
                    'status': 'success',
                    'provider': 'Stable Diffusion XL (HuggingFace)',
                    'image_url': self.generate_stable_diffusion(prompt)
                }
            except Exception as e2:
                return {
                    'status': 'error',
                    'error': f"DALL-E: {str(e)[:100]} | Stable Diffusion: {str(e2)[:100]}"
                }
