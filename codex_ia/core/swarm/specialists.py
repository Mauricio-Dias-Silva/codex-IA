
from .agent_base import SwarmAgent
import google.generativeai as genai
import os

# API Key Hardcoded for speed (Phase 3)
API_KEY = "AIzaSyBREWGg-uOUss7bZIoK0xqBU5svqvyCX6Y"
genai.configure(api_key=API_KEY)

class ArchitectAgent(SwarmAgent):
    def __init__(self):
        super().__init__("DaVinci", "Architect", "cyan")
        self.model = genai.GenerativeModel('gemini-2.5-pro')

    def process_message(self, message):
        self.log(f"Designing solution for: {message['content']}")
        prompt = f"ATUE COMO: Arquiteto de Software Sênior. Crie um plano técnico detalhado para: {message['content']}"
        response = self.model.generate_content(prompt)
        return response.text

class DeveloperAgent(SwarmAgent):
    def __init__(self):
        super().__init__("Alan", "Developer", "green")
        self.model = genai.GenerativeModel('gemini-2.5-pro')

    def process_message(self, message):
        self.log(f"Coding solution based on plan...")
        prompt = f"ATUE COMO: Desenvolvedor Python Expert. Escreva o código para este plano: {message['content']}"
        response = self.model.generate_content(prompt)
        return response.text

class QAAgent(SwarmAgent):
    def __init__(self):
        super().__init__("Grace", "QA_Tester", "red")
        self.model = genai.GenerativeModel('gemini-2.5-pro')

    def process_message(self, message):
        self.log(f"Testing solution...")
        prompt = f"ATUE COMO: QA Tester. Analise este código em busca de bugs e segurança: {message['content']}"
        response = self.model.generate_content(prompt)
        return response.text
