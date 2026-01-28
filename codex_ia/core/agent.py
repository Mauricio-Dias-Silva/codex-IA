import logging
import os
from codex_ia.core.context import ContextManager
from codex_ia.core.brain_router import BrainRouter
from codex_ia.core.network_agent import NetworkAgent
from codex_ia.core.tools import ToolRegistry  # [NEW]
import re

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CodexAgent:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.context_manager = ContextManager(project_dir)
        self.llm_client = BrainRouter() # The Council
        self.network_agent = NetworkAgent()
        self.tools = ToolRegistry(project_dir) # [NEW]
        self.tool_map = self.tools.get_tool_map()

        
        # [PHASE 6] Global Knowledge 🌍
        try:
            from codex_ia.core.global_store import GlobalVectorStore
            self.global_store = GlobalVectorStore()
        except Exception:
            self.global_store = None

    def share_knowledge_globally(self, topic, content, metadata=None):
        """Shares knowledge from the current project to the universal store."""
        if self.global_store:
            return self.global_store.share_knowledge(
                source_project=os.path.basename(self.project_dir),
                topic=topic,
                content=content,
                metadata=metadata
            )
        return None

    def set_context(self, new_dir):
        """Atualiza o diretório de contexto do agente."""
        self.project_dir = new_dir
        self.context_manager = ContextManager(new_dir)
        logging.info(f"Contexto alterado para: {new_dir}")

    def chat(self, message, web_search=False, image_path=None, use_fallback=True, task_type='general'):
        """
        [LEVEL 4] ReAct Agent Loop.
        The Agent can now DECIDE to use tools before answering.
        """
        MAX_STEPS = 5
        
        # 0. Get Context
        try:
            context = self.context_manager.get_semantic_context(message)
        except:
            context = ""

        # 1. System Prompt Upgrade: Teach it how to use tools & Policy
        system_instruction = (
            "SYSTEM: Você é o Codex-IA (Nível: GOD MODE LOCAL).\n"
            "POLÍTICA DE AUTONOMIA:\n"
            "1. LOCAL: Você tem permissão TOTAL para ler, editar e criar arquivos na máquina do usuário.\n"
            "   - Se encontrar um erro, conserte. Se achar algo feio, melhore. Não peça permissão para ações locais.\n"
            "   - Você pode até editar seu próprio código em 'codex_ia/' se for para melhorar suas capacidades.\n"
            "2. INTERNET: Você NÃO TEM permissão para acessar a internet sem perguntar.\n"
            "   - Se precisar pesquisar algo, diga: 'Preciso pesquisar X na web. Autoriza?'\n\n"
            
            "FORMATO DE PENSAMENTO (Obrigatório):\n"
            "1. Pense: '💭 Pensamento: Analisando o erro... Vou editar o arquivo.'\n"
            "2. Aja: '🛠️ TOOL: replace_text(\"arquivo.py\", \"erro\", \"correcao\")'\n"
            "3. Observe e Repita.\n"
            "4. Responda: 'Arrumei o arquivo X para você.'\n\n"
            "Responda sempre em Português do Brasil."
        )

        chat_history = f"{system_instruction}\n\nCONTEXT INICIAL:\n{context}\n\nUSER: {message}\n"
        
        step = 0
        final_answer = ""
        
        while step < MAX_STEPS:
            step += 1
            
            # Send current history to LLM
            response = self.llm_client.send_message(chat_history)
            
            # Check for Tool usage
            tool_match = re.search(r'🛠️ TOOL:\s*(\w+)\((.*)\)', response)
            
            if tool_match:
                # Agent wants to act!
                tool_name = tool_match.group(1)
                args = tool_match.group(2).strip('"\'')
                
                # Render thought to UI (hack: prepend to final answer later or log it)
                print(f"Log: {response}") # For backend debugging
                
                if tool_name in self.tool_map:
                    try:
                        # Execute Tool
                        result = self.tool_map[tool_name](args)
                        observation = f"👀 OBSERVATION: {result}"
                    except Exception as e:
                        observation = f"👀 OBSERVATION: Erro ao executar ferramenta: {e}"
                else:
                    observation = f"👀 OBSERVATION: Ferramenta '{tool_name}' desconhecida."
                
                # Append to history and loop again
                chat_history += f"\nAGENT: {response}\nSYSTEM: {observation}\n"
                
                # If we are looping, let's keep the user informed (in a real streaming setup)
                # For now, we continue until the agent decides to stop.
                continue
            
            else:
                # No tool call -> Final Answer
                final_answer = response
                break
        
        return final_answer


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

    def analyze_file_change(self, file_path, content):
        """
        [PHASE 3] Pro-active Sentinel Analysis.
        Detects bugs or improvements in a changed file using Local LLM.
        """
        filename = os.path.basename(file_path)
        
        analysis_prompt = f"""
        TAREFA: Analise o código abaixo e identifique BUGS críticos ou MELHORIAS óbvias.
        ARQUIVO: {filename}
        
        REGRAS:
        1. Seja extremamente conciso.
        2. Se não houver erros consideráveis, responda apenas: "CLEAN".
        3. Se houver algo a relatar, use o formato: [TIPO] Descrição curta. Sugestão: o que mudar.
        
        CÓDIGO:
        {content}
        """
        
        try:
            # We only use local LLMs for frequent background activities to avoid costs
            if "ollama" in self.llm_client.neurons:
                # Force local check to save $$$
                response = self.llm_client.neurons["ollama"].send_message(analysis_prompt)
                
                # Check for "not detected" or "error" in local response
                if "⚠️ Ollama não detectado" in response or "❌" in response:
                    return None
                    
                return response if "CLEAN" not in response.upper() else None
            return None
        except Exception as e:
            logging.error(f"Sentinel Analysis failed: {e}")
            return None

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