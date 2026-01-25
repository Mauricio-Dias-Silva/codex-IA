import logging
from codex_ia.core.context import ContextManager
from codex_ia.core.brain_router import BrainRouter
from codex_ia.core.network_agent import NetworkAgent

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CodexAgent:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.context_manager = ContextManager(project_dir)
        self.llm_client = BrainRouter() # The Council
        self.network_agent = NetworkAgent()

    def set_context(self, new_dir):
        """Atualiza o diretório de contexto do agente."""
        self.project_dir = new_dir
        self.context_manager = ContextManager(new_dir)
        logging.info(f"Contexto alterado para: {new_dir}")

    def chat(self, message, web_search=False, image_path=None, task_type="general"):
        """
        Interage com o agente Codex.
        """
        try:
            system_instruction = (
                "You are Codex, an advanced AI Coding Assistant built by PythonJet. "
                "You are specialized in Python, React, and Electron development. "
                "Do NOT identify as ChatGPT, Claude, or Gemini. You are Codex. "
            )
            
            context = self.context_manager.get_context()
            full_message = f"{system_instruction}\n\nCONTEXT:\n{context}\n\nUSER MESSAGE:\n{message}"
            
            response = self.llm_client.send_message(full_message, web_search=web_search, image_path=image_path, task_type=task_type)
            return response
        except Exception as e:
            logging.error(f"Erro durante o chat: {e}")
            return f"Ocorreu um erro: {e}"

    def generate_codebase(self, prompt):
        """
        Gera uma nova codebase.
        """
        try:
            logging.info(f"Gerando codebase com o prompt: {prompt}")
            response = self.llm_client.send_message(prompt)
            return response
        except Exception as e:
            logging.error(f"Erro ao gerar codebase: {e}")
            return f"Ocorreu um erro: {e}"

    def add_file_to_context(self, file_path):
        """
        Adiciona um arquivo ao contexto.
        """
        try:
            logging.info(f"Adicionando arquivo ao contexto: {file_path}")
            self.context_manager.get_file_context(file_path)
        except Exception as e:
            logging.error(f"Erro ao adicionar arquivo ao contexto: {e}")
            return f"Ocorreu um erro: {e}"