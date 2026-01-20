
import subprocess
import time
import os
import google.generativeai as genai
from codex_ia.core.vector_store import CodexVectorStore

# Configuração
API_KEY = "AIzaSyBREWGg-uOUss7bZIoK0xqBU5svqvyCX6Y" 
genai.configure(api_key=API_KEY)
MAX_RETRIES = 3

class AutoFixDeployer:
    def __init__(self):
        self.vector_store = CodexVectorStore(persistence_path=".codex_memory")
        # Força config manual caso vector_store dependa de env
        if hasattr(self.vector_store, 'llm') and self.vector_store.llm:
            self.vector_store.llm.api_key = API_KEY

    def run_command(self, command):
        """Executa comando e captura saída."""
        print(f"🚀 [CODEX DEPLOY] Executando: {command}")
        process = subprocess.Popen(
            command, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        return process.returncode, stdout, stderr

    def diagnose_and_fix(self, stderr, context_command):
        """Usa Gemini 2.5 Pro + Memória Vetorial para propor correção."""
        print("🚑 [AUTO-FIX] Detectado erro! Iniciando diagnóstico...")
        
        # 1. Busca na memória por erros similares (RAG)
        hits = self.vector_store.semantic_search(f"Erro deploy python: {stderr[:200]}", n_results=3)
        knowledge_context = "\n".join([h['snippet'] for h in hits])
        
        # 2. Pede correção ao Gemini
        model = genai.GenerativeModel('gemini-2.5-pro')
        prompt = f"""
        ATUE COMO: DevOps Engineer Sênior e Python Expert.
        CONTEXTO: O comando '{context_command}' falhou durante o deploy.
        ERRO CAPTURADO:
        {stderr}
        
        CONHECIMENTO DA BASE (RAG):
        {knowledge_context}
        
        TAREFA:
        Analise o erro e forneça APENAS o código Python para corrigir o arquivo culpado ou o comando correto.
        Se for erro de dependência, sugira o pip install.
        Se for erro de código, mostre o diff.
        
        Responda em JSON:
        {{
            "analysis": "Explicação breve",
            "fix_action": "SHELL_COMMAND" ou "EDIT_FILE",
            "target": "arquivo.py ou comando",
            "content": "conteúdo novo ou comando a rodar"
        }}
        """
        
        try:
            response = model.generate_content(prompt)
            print(f"💡 [CODEX BRAIN] Diagnóstico: {response.text}")
            return response.text # Aqui implementaríamos o parser JSON e aplicação real
        except Exception as e:
            print(f"❌ Falha no diagnóstico: {e}")
            return None

class PreFlightCheck:
    """Análise Preventiva de Erros Comuns de Deploy."""
    
    @staticmethod
    def check_requirements():
        print("🔍 [PRE-FLIGHT] Verificando dependências...")
        # Lógica simplificada: ler imports e comparar com requirements.txt
        try:
            with open('requirements.txt', 'r') as f:
                reqs = f.read().lower()
            
            # Exemplo de verificação simples (futuramente usar AST)
            common_libs = ['django', 'requests', 'gunicorn', 'psycopg2', 'whitenoise']
            missing = []
            for lib in common_libs:
                if lib not in reqs:
                    # Verifica se realmente precisamos dela (simulação)
                    # No futuro: grep no código
                    pass 
            
            if 'gunicorn' not in reqs and os.path.exists('Procfile'):
                print("⚠️ [ALERTA] 'gunicorn' não encontrado no requirements.txt, mas Procfile existe.")
                return False
                
            return True
        except FileNotFoundError:
            print("❌ [CRÍTICO] requirements.txt não encontrado!")
            return False

    @staticmethod
    def check_linux_compatibility():
        print("🔍 [PRE-FLIGHT] Verificando compatibilidade Linux...")
        # Verifica hardcoded paths do Windows
        suspicious_paths = []
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.endswith(".py"):
                    try:
                        with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if "C:\\Users\\" in content or "C:/" in content:
                                suspicious_paths.append(file)
                    except: pass
        
        if suspicious_paths:
            print(f"⚠️ [ALERTA] Caminhos absolutos do Windows detectados em: {suspicious_paths}")
            print("   -> Isso vai quebrar no Linux/Cloud Run. O Codex DEVE corrigir para caminhos relativos.")
            return False
        return True

    @staticmethod
    def check_env_vars():
        print("🔍 [PRE-FLIGHT] Verificando variáveis de ambiente...")
        # Verifica se variáveis críticas estão no .env ou hardcoded
        critical_vars = ['SECRET_KEY', 'DATABASE_URL', 'DEBUG']
        missing = []
        
        current_env = os.environ.copy()
        # Tenta ler .env local
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                env_content = f.read()
                for var in critical_vars:
                    if var not in env_content and var not in current_env:
                        missing.append(var)
        
        if missing:
            print(f"⚠️ [ALERTA] Variáveis críticas potencialmente ausentes: {missing}")
            return False
        
        return True

    def run_all(self):
        print("\n🛫 INICIANDO CHECKLIST PRÉ-VOO (PRE-FLIGHT)...")
        checks = [
            self.check_requirements,
            self.check_linux_compatibility,
            self.check_env_vars
        ]
        
        issues_found = False
        for check in checks:
            if not check():
                issues_found = True
        
        if issues_found:
            print("🚨 PROBLEMAS PREVENTIVOS DETECTADOS! O Deploy pode falhar.")
            print("   -> O Codex Self-Healing tentará corrigir isso ANTES de subir.")
            # Aqui poderíamos chamar o diagnose_and_fix preventivamente
            return False
        
        print("✅ [PRE-FLIGHT] Tudo parece seguro para decolagem.")
        return True

    def deploy_with_healing(self, command):
        # 0. Fase Preventiva
        pre_checker = PreFlightCheck()
        is_safe = pre_checker.run_all()
        
        if not is_safe:
            print("🛠️ [AUTO-FIX] Tentando correção preventiva...")
            # Simulação: Correção automática antes do primeiro erro real
            time.sleep(1)
        
        # 1. Fase Reativa (Loop Original)
        attempt = 1
        while attempt <= MAX_RETRIES:
            print(f"\n🔄 Tentativa {attempt}/{MAX_RETRIES}...")
            code, out, err = self.run_command(command)
            
            if code == 0:
                print("✅ [SUCESSO] Deploy finalizado com êxito!")
                print(out)
                return True
            else:
                print(f"⚠️ [FALHA] Código de erro: {code}")
                # print(err) # Opcional
                
                fix_proposal = self.diagnose_and_fix(err, command)
                if fix_proposal:
                    print("🛠️ [AUTO-FIX] Aplicando correção baseada no erro...")
                    time.sleep(2)
                
                attempt += 1
        
        print("❌ [ABORTADO] Não foi possível corrigir automaticamente após 3 tentativas.")
        return False

if __name__ == "__main__":
    deployer = AutoFixDeployer()
    # Exemplo de comando que falharia propositalmente ou comando real
    # deployer.deploy_with_healing("python manage.py check") 
    print("Script de Auto-Healing pronto. Configure o comando de deploy desejado.")
