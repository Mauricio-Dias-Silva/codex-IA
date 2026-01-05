from typing import List, Dict, Any
from codex_ia.core.context import ContextManager
from codex_ia.core.llm_client import GeminiClient

class CodexAgent:
    def __init__(self, root_path: str = ".", auto_confirm: bool = False):
        self.context_mgr = ContextManager(root_path)
        self.client = GeminiClient()
        self.history = []
        self.auto_confirm = auto_confirm
        
        # Initial system instruction for the chat
        self._initialize_chat()

    def chat(self, user_input: str) -> str:
        """
        Main entry point for user interaction.
        """
        # Send user message to LLM
        response_text = self.client.send_message(user_input)
        
        # Tool Parsing Loop
        MAX_TURNS = 5
        turn = 0
        
        while turn < MAX_TURNS:
            import re
            
            # Check for READ_FILE
            match_read = re.search(r"READ_FILE:\s*([^\s\n]+)", response_text)
            
            # Check for WRITE_FILE using robust tags
            # Format: <<<<FILE: path>>>> content <<<<END_FILE>>>>
            # We use DOTALL to capture newlines in content
            match_write = re.search(r"<<<<FILE:\s*([^>]+)>>>>(.*?)<<<<END_FILE>>>>", response_text, re.DOTALL)
            
            if match_read:
                file_path = match_read.group(1).strip().strip("'\"")
                file_content = self.context_mgr.get_file_context(file_path)
                output_msg = f"SYSTEM_OBSERVATION: Content of {file_path}:\n{file_content}"
                response_text = self.client.send_message(output_msg)
                turn += 1
                
            elif match_write:
                file_path = match_write.group(1).strip()
                new_content = match_write.group(2).strip()
                
                # Remove markdown fences if the LLM wrapped the inner content in them
                if new_content.startswith("```"):
                    # Remove first line (```lang)
                    new_content = new_content.split("\n", 1)[1]
                if new_content.endswith("```"):
                     # Remove last line
                    new_content = new_content.rsplit("\n", 1)[0]
                
                # SAFETY CHECK
                if self._confirm_action(f"write to {file_path}"):
                    from pathlib import Path
                    full_path = Path(file_path).resolve()
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    output_msg = f"SYSTEM_SUCCESS: File {file_path} written successfully."
                else:
                    output_msg = f"SYSTEM_INFO: User denied write permission for {file_path}."
                    
                response_text = self.client.send_message(output_msg)
                turn += 1
            else:
                break
                
        return response_text
    
    def _confirm_action(self, action_desc: str) -> bool:
        """
        Asks the user for confirmation via the Console.
        """
        if self.auto_confirm:
            return True
            
        from rich.prompt import Confirm
        return Confirm.ask(f"[bold red]Codex-IA wants to {action_desc}. Allow?[/bold red]")

    def _initialize_chat(self):
        """
        Sets up the chat session with the initial system context.
        """
        files = self.context_mgr.list_files()
        file_list_str = "\n".join(files)
        
        system_instruction = f"""
        Você é o Codex-IA, um assistente de codificação inteligente e interativo.
        Você está rodando dentro de um diretório de projeto.
        
        ESTRUTURA DO PROJETO ATUAL:
        {file_list_str}
        
        SUAS CAPACIDADES:
        1. LISTAR ARQUIVOS: Você já tem a lista acima.
        2. LER ARQUIVOS: Para ler, escreva APENAS:
           READ_FILE: <caminho/do/arquivo>
        3. CRIAR/EDITAR ARQUIVOS: Para criar ou editar, você DEVE usar este formato exato:
           <<<<FILE: caminho/do/arquivo.ext>>>>
           conteudo do arquivo aqui...
           <<<<END_FILE>>>>
        
        REGRAS:
        - Responda sempre em Markdown.
        - Seja direto e técnico e fale PORTUGUÊS.
        - Se o usuário pedir para criar código, USE O FORMATO DE CRIAÇÃO DE ARQUIVO ACIMA.
        - Não peça permissão, apenas use a ferramenta. Eu cuidarei da confirmação.
        """
        
        self.client.start_chat(initial_history=[
            {"role": "user", "parts": [{"text": system_instruction}]},
            {"role": "model", "parts": [{"text": "Entendido. Aguardo suas instruções."}]}
        ])

    def add_file_to_context(self, file_path: str):
        """
        Manually injects a file content into the chat session as a system update.
        """
        content = self.context_mgr.get_file_context(file_path)
        if "Error" not in content:
            self.client.send_message(f"SYSTEM UPDATE: Here is the content of {file_path}:\n{content}")
            return True
        return False
