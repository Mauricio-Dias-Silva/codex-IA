
import os
from google import genai
from google.genai import types

class GeminiClient:
    def __init__(self):
        # Ensure env vars are loaded even if called from outside
        from dotenv import load_dotenv
        load_dotenv(override=True)

        # Support both names, prioritize GEMINI_API_KEY
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GENAI_API_KEY")
        
        # SPRINGBACK KEY: Ultimate fallback for stability
        if not api_key:
            api_key = "AIzaSyBREWGg-uOUss7bZIoK0xqBU5svqvyCX6Y"
            
        if "Cole_Sua_Chave" in api_key:
             # Even if env is placeholder, use the rescue key
             api_key = "AIzaSyBREWGg-uOUss7bZIoK0xqBU5svqvyCX6Y"
        
        self.client = genai.Client(api_key=api_key)
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
        self.chat_session = None

    def start_chat(self, initial_history: list = None, web_search: bool = False):
        """
        Starts a new chat session with the model.
        """
        config_args = {
            "temperature": 0.4,
        }
        
        if web_search:
            # Enable Google Search Grounding
            # Using the google-genai SDK format
            config_args["tools"] = [types.Tool(google_search=types.GoogleSearch())]

        self.chat_session = self.client.chats.create(
            model=self.model,
            history=initial_history or [],
            config=types.GenerateContentConfig(**config_args)
        )
        return self.chat_session

    def send_message(self, message: str, web_search: bool = False, image_path: str = None) -> str:
        """
        Sends a message to the active chat session, optionally with an image.
        """
        if not self.chat_session:
            self.start_chat(web_search=web_search)
            
        # If there is an image, we need to handle it.
        # Note: 'chats.send_message' usually takes a string or a list of contents (string + parts).
        
        contents = [message]
        
        if image_path:
            import mimetypes
            
            if not os.path.exists(image_path):
                return f"Error: Image not found at {image_path}"
                
            mime_type, _ = mimetypes.guess_type(image_path)
            if not mime_type:
                mime_type = "image/jpeg" # Default fallback
                
            try:
                with open(image_path, "rb") as f:
                    image_bytes = f.read()
                    
                image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
                # Add image part BEFORE the text prompt usually works best or alongside it
                contents.append(image_part)
                
            except Exception as e:
                return f"Error loading image: {e}"

        try:
            # If contents has only 1 item and it's a string, passing it directly is fine.
            # If it has parts, we pass the list.
            response = self.chat_session.send_message(contents)
            return response.text
        except Exception as e:
            return f"Error sending message to Gemini: {e}"

    def analyze_architecture(self, context: str) -> str:
        """
        Envia o contexto para o Gemini analisar a arquitetura.
        """
        prompt = f"""
        Você é um Arquiteto de Software Sênior (Codex-IA).
        Analise o seguinte código e sugira 3 melhorias de impacto alto na arquitetura ou legibilidade.
        Seja direto e técnico.

        CONTEXTO:
        {context[:50000]} # Limite de segurança para exemplo
        """
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2, # Baixa temperatura para precisão
            )
        )
        
        return response.text

    def explain_code(self, file_content: str) -> str:
        """
        Explains the logic of a specific file.
        """
        prompt = f"""
        You are a Senior Software Engineer (Codex-IA).
        Explain the functionality of the following file in a clear and didactic way.
        Focus on:
        1. Purpose of the file.
        2. Main classes and functions.
        3. Key logic flows.

        FILE CONTENT:
        {file_content}
        """
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
            )
        )
        return response.text

    def refactor_code(self, file_content: str, instructions: str = "") -> str:
        """
        Suggests refactoring for a specific file.
        """
        prompt = f"""
        You are a Senior Software Engineer (Codex-IA).
        Refactor the following code to improve quality, readability, and performance.
        
        User Instructions: {instructions if instructions else "Apply best practices and clean code principles."}

        FILE CONTENT:
        {file_content}

        Output ONLY the refactored code (or a diff if more appropriate) and a brief summary of changes at the end.
        """
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
            )
        )
    def embed_content(self, text: str) -> list:
        """
        Generates embeddings for a given text using Gemini.
        """
        try:
            # Using the embedding model
            result = self.client.models.embed_content(
                model="text-embedding-004",
                contents=text
            )
            return result.embeddings[0].values
        except Exception as e:
            # Fallback or error logging
            print(f"Embedding Error: {e}")
            return []
