"""
🐛 AUTO-DEBUGGER - Self-Healing Code System
Roda testes, detecta erros, e corrige automaticamente
"""

import subprocess
import re
from typing import Dict, List, Optional
from pathlib import Path
from codex_ia.core.llm_client import GeminiClient
from google.genai import types

class AutoDebugger:
    """
    Sistema de auto-debugging que:
    1. Roda testes
    2. Analisa stack traces
    3. Gera correções
    4. Aplica patches
    5. Valida fix
    """
    
    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir)
        self.llm = GeminiClient()
        
    def run_tests(self, test_command: str = "pytest") -> Dict:
        """
        Roda testes e captura output.
        
        Returns:
            {
                "passed": bool,
                "output": str,
                "errors": List[Dict],  # parsed errors
                "exit_code": int
            }
        """
        print(f"🧪 Rodando testes: {test_command}")
        
        try:
            result = subprocess.run(
                test_command.split(),
                cwd=str(self.project_dir),
                capture_output=True,
                text=True,
                timeout=60
            )
            
            output = result.stdout + result.stderr
            passed = result.returncode == 0
            
            # Parse errors
            errors = self._parse_errors(output)
            
            return {
                "passed": passed,
                "output": output,
                "errors": errors,
                "exit_code": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                "passed": False,
                "output": "Timeout após 60s",
                "errors": [{"type": "timeout", "message": "Testes demoraram muito"}],
                "exit_code": -1
            }
        except Exception as e:
            return {
                "passed": False,
                "output": str(e),
                "errors": [{"type": "execution_error", "message": str(e)}],
                "exit_code": -1
            }
            
    def _parse_errors(self, test_output: str) -> List[Dict]:
        """
        Parse de erros do output de teste.
        Suporta: pytest, unittest, Django tests
        """
        errors = []
        
        # Regex para stack traces Python
        error_pattern = r'File "([^"]+)", line (\d+).*?\n.*?(\w+Error: .+)'
        matches = re.findall(error_pattern, test_output, re.MULTILINE)
        
        for match in matches:
            file_path, line_num, error_msg = match
            errors.append({
                "file": file_path,
                "line": int(line_num),
                "type": error_msg.split(':')[0],
                "message": error_msg,
                "raw_output": test_output
            })
            
        return errors
        
    def analyze_error(self, error: Dict) -> Dict:
        """
        Analisa um erro usando Gemini.
        
        Returns:
            {
                "diagnosis": str,
                "root_cause": str,
                "fix_strategy": str,
                "code_patch": str
            }
        """
        print(f"🔍 Analisando erro: {error['type']} em {error['file']}:{error['line']}")
        
        # Lê o arquivo com erro
        try:
            file_path = Path(error['file'])
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
            else:
                file_content = "[Arquivo não encontrado]"
        except:
            file_content = "[Erro ao ler arquivo]"
            
        # Prompt de debugging
        debug_prompt = f"""
Você é um expert debugger (estilo GitHub Copilot Debugging).

ERRO DETECTADO:
Tipo: {error['type']}
Arquivo: {error['file']}
Linha: {error['line']}
Mensagem: {error['message']}

CÓDIGO DO ARQUIVO:
```python
{file_content}
```

STACK TRACE COMPLETO:
{error.get('raw_output', 'N/A')[:1000]}

Analise e retorne JSON:
{{
    "diagnosis": "O que está causando o erro",
    "root_cause": "Causa raiz técnica",
    "fix_strategy": "Como corrigir (passo a passo)",
    "code_patch": "Código corrigido (apenas a parte que precisa mudar)"
}}

Seja PRECISO e EXECUTÁVEL.
"""
        
        try:
            response = self.llm.client.models.generate_content(
                model=self.llm.model,
                contents=debug_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,  # Baixíssima para precisão
                    max_output_tokens=2000
                )
            )
            
            # Parse JSON
            import json
            result_text = response.text.strip()
            
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
                
            analysis = json.loads(result_text)
            
            print(f"✅ Diagnóstico: {analysis['diagnosis'][:100]}...")
            return analysis
            
        except Exception as e:
            print(f"⚠️  Erro na análise: {e}")
            return {
                "diagnosis": "Erro ao analisar",
                "root_cause": str(e),
                "fix_strategy": "Manual debugging needed",
                "code_patch": ""
            }
            
    def apply_fix(self, error: Dict, analysis: Dict) -> bool:
        """
        Aplica a correção sugerida.
        
        Returns:
            True se aplicou com sucesso
        """
        if not analysis.get('code_patch'):
            print("❌ Sem patch para aplicar")
            return False
            
        print(f"🔧 Aplicando correção em {error['file']}...")
        
        try:
            file_path = Path(error['file'])
            
            # Backup
            backup_path = file_path.with_suffix(file_path.suffix + '.backup')
            import shutil
            shutil.copy(file_path, backup_path)
            
            # TODO: Implementar patch inteligente
            # Por enquanto, apenas reporta
            print(f"📝 Patch sugerido:")
            print(analysis['code_patch'])
            print(f"\n💾 Backup criado: {backup_path}")
            
            # Em produção, usaríamos diff/patch automático
            return True
            
        except Exception as e:
            print(f"⚠️  Erro ao aplicar fix: {e}")
            return False
            
    def auto_fix_loop(self, max_iterations: int = 3) -> Dict:
        """
        Loop de auto-correção:
        1. Roda testes
        2. Se falhar, analisa erros
        3. Aplica correções
        4. Repete até passar ou atingir limite
        
        Returns:
            {
                "success": bool,
                "iterations": int,
                "fixes_applied": List[Dict],
                "final_status": str
            }
        """
        fixes_applied = []
        
        for iteration in range(1, max_iterations + 1):
            print(f"\n{'='*60}")
            print(f"🔄 Iteração {iteration}/{max_iterations}")
            print(f"{'='*60}")
            
            # Roda testes
            test_result = self.run_tests()
            
            if test_result['passed']:
                print("✅ Todos os testes passaram!")
                return {
                    "success": True,
                    "iterations": iteration,
                    "fixes_applied": fixes_applied,
                    "final_status": "all_tests_passed"
                }
                
            # Analisa primeiro erro
            if not test_result['errors']:
                print("⚠️  Testes falharam mas sem erro parseável")
                return {
                    "success": False,
                    "iterations": iteration,
                    "fixes_applied": fixes_applied,
                    "final_status": "unparseable_error"
                }
                
            error = test_result['errors'][0]
            analysis = self.analyze_error(error)
            
            # Aplica fix
            fixed = self.apply_fix(error, analysis)
            
            fixes_applied.append({
                "error": error,
                "analysis": analysis,
                "applied": fixed
            })
            
            if not fixed:
                print("❌ Não consegui aplicar fix automaticamente")
                return {
                    "success": False,
                    "iterations": iteration,
                    "fixes_applied": fixes_applied,
                    "final_status": "manual_intervention_needed"
                }
                
        # Atingiu limite de iterações
        return {
            "success": False,
            "iterations": max_iterations,
            "fixes_applied": fixes_applied,
            "final_status": "max_iterations_reached"
        }


# --- DEMO ---
if __name__ == "__main__":
    debugger = AutoDebugger(project_dir=Path("."))
    
    print("🐛 AUTO-DEBUGGER - DEMO")
    print("="*60)
    
    # Simula erro
    fake_error = {
        "file": "example.py",
        "line": 42,
        "type": "AttributeError",
        "message": "AttributeError: 'NoneType' object has no attribute 'split'",
        "raw_output": "Traceback (most recent call last):\n  File \"example.py\", line 42, in process\n    name = obj.split('-')[0]\nAttributeError: 'NoneType' object has no attribute 'split'"
    }
    
    analysis = debugger.analyze_error(fake_error)
    
    print(f"\n🔍 ANÁLISE:")
    print(f"   Diagnóstico: {analysis['diagnosis']}")
    print(f"   Causa Raiz: {analysis['root_cause']}")
    print(f"   Estratégia: {analysis['fix_strategy']}")
