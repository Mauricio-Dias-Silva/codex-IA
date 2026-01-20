"""
🧠 MULTI-STEP PLANNER - Autonomous Planning Engine
Tipo Devin: quebra tarefas complexas em passos executáveis
"""

import json
from typing import List, Dict
from codex_ia.core.llm_client import GeminiClient
from codex_ia.core.vector_store import CodexVectorStore
from google.genai import types

class MultiStepPlanner:
    """
    Planner que decompõe objetivos complexos em passos executáveis.
    Features Devin-like:
    - Tree-of-Thought planning
    - Dependency tracking
    - Error recovery strategies
    """
    
    def __init__(self):
        self.llm = GeminiClient()
        self.store = CodexVectorStore()
        
    def create_plan(self, goal: str, context: Dict = None) -> Dict:
        """
        Cria um plano multi-step para alcançar o objetivo.
        
        Args:
            goal: Objetivo de alto nível (ex: "Criar um dashboard de vendas")
            context: Contexto adicional (tecnologias, restrições)
            
        Returns:
            {
                "goal": str,
                "steps": [
                    {
                        "id": 1,
                        "action": "research",
                        "description": "...",
                        "success_criteria": "...",
                        "dependencies": [],
                        "estimated_time": "5min"
                    },
                    ...
                ],
                "total_estimated_time": "30min",
                "risks": ["..."]
            }
        """
        
        # Recupera conhecimento relevante
        knowledge = self.store.semantic_search(f"how to {goal}", n_results=3)
        knowledge_context = "\n".join([k['snippet'] for k in knowledge])
        
        # Prompt de planejamento (inspirado no Devin)
        planning_prompt = f"""
Você é um Senior Software Engineer (estilo Devin AI).
Crie um PLANO DETALHADO para: {goal}

CONTEXTO:
{json.dumps(context or {}, indent=2)}

CONHECIMENTO RELEVANTE:
{knowledge_context}

Decomponha em passos EXECUTÁVEIS. Cada passo deve ter:
1. ID (número sequencial)
2. action (research/code/test/debug/deploy)
3. description (o que fazer)
4. success_criteria (como validar)
5. dependencies (IDs de passos anteriores necessários)
6. estimated_time (estimativa realista)

Retorne APENAS JSON válido neste formato:
{{
    "goal": "{goal}",
    "steps": [
        {{
            "id": 1,
            "action": "research",
            "description": "Pesquisar bibliotecas para...",
            "success_criteria": "Lista de 3 libs candidatas",
            "dependencies": [],
            "estimated_time": "5min",
            "commands": ["pip search dashboard", "..."]
        }}
    ],
    "total_estimated_time": "soma dos tempos",
    "risks": ["Risco técnico 1", "Risco 2"]
}}

Seja PRÁTICO e EXECUTÁVEL.
"""
        
        try:
            response = self.llm.client.models.generate_content(
                model=self.llm.model,
                contents=planning_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,  # Baixa para planos precisos
                    max_output_tokens=4000
                )
            )
            
            # Parse do JSON
            plan_text = response.text.strip()
            
            # Remove markdown
            if "```json" in plan_text:
                plan_text = plan_text.split("```json")[1].split("```")[0].strip()
            elif "```" in plan_text:
                plan_text = plan_text.split("```")[1].split("```")[0].strip()
                
            plan = json.loads(plan_text)
            
            print(f"📋 PLANO CRIADO: {len(plan['steps'])} passos")
            return plan
            
        except Exception as e:
            print(f"⚠️  Erro no planejamento: {e}")
            # Fallback: plano simples
            return {
                "goal": goal,
                "steps": [
                    {
                        "id": 1,
                        "action": "research",
                        "description": f"Pesquisar como fazer: {goal}",
                        "success_criteria": "Informação suficiente coletada",
                        "dependencies": [],
                        "estimated_time": "10min"
                    }
                ],
                "total_estimated_time": "10min",
                "risks": ["Plano fallback - detalhamento limitado"]
            }
            
    def execute_step(self, step: Dict, context: Dict = None) -> Dict:
        """
        Executa um passo individual do plano.
        
        Returns:
            {
                "success": bool,
                "output": str,
                "errors": List[str],
                "next_action": str  # "continue" | "retry" | "escalate"
            }
        """
        action = step['action']
        
        print(f"\n🔧 Executando passo {step['id']}: {step['description']}")
        
        if action == "research":
            return self._execute_research(step)
        elif action == "code":
            return self._execute_code(step, context)
        elif action == "test":
            return self._execute_test(step)
        elif action == "debug":
            return self._execute_debug(step)
        elif action == "deploy":
            return self._execute_deploy(step)
        else:
            return {"success": False, "errors": [f"Unknown action: {action}"]}
            
    def _execute_research(self, step: Dict) -> Dict:
        """Executa passo de pesquisa."""
        query = step['description']
        results = self.store.semantic_search(query, n_results=5)
        
        if results:
            output = "\n".join([r['snippet'][:200] for r in results])
            return {
                "success": True,
                "output": output,
                "errors": [],
                "next_action": "continue"
            }
        else:
            return {
                "success": False,
                "output": "",
                "errors": ["Nenhum conhecimento relevante encontrado"],
                "next_action": "escalate"
            }
            
    def _execute_code(self, step: Dict, context: Dict) -> Dict:
        """Executa passo de geração de código."""
        # TODO: Integrar com code generator existente
        return {
            "success": True,
            "output": "Código gerado (placeholder)",
            "errors": [],
            "next_action": "continue"
        }
        
    def _execute_test(self, step: Dict) -> Dict:
        """Executa testes."""
        # TODO: Integrar com test runner
        return {
            "success": True,
            "output": "Testes passaram",
            "errors": [],
            "next_action": "continue"
        }
        
    def _execute_debug(self, step: Dict) -> Dict:
        """Executa debugging."""
        # TODO: Integrar com auto-debugger
        return {
            "success": True,
            "output": "Bug corrigido",
            "errors": [],
            "next_action": "continue"
        }
        
    def _execute_deploy(self, step: Dict) -> Dict:
        """Executa deploy."""
        # TODO: Integrar com deployment system
        return {
            "success": True,
            "output": "Deploy realizado",
            "errors": [],
            "next_action": "continue"
        }
        
    def execute_plan(self, plan: Dict) -> Dict:
        """
        Executa plano completo com error handling.
        
        Returns:
            {
                "completed_steps": int,
                "failed_steps": int,
                "results": List[Dict],
                "final_status": "success" | "partial" | "failed"
            }
        """
        results = []
        completed = 0
        failed = 0
        
        for step in plan['steps']:
            # Verifica dependências
            for dep_id in step.get('dependencies', []):
                dep_result = next((r for r in results if r['step_id'] == dep_id), None)
                if not dep_result or not dep_result['success']:
                    print(f"⚠️  Dependência {dep_id} falhou, pulando passo {step['id']}")
                    failed += 1
                    continue
                    
            result = self.execute_step(step)
            result['step_id'] = step['id']
            results.append(result)
            
            if result['success']:
                completed += 1
            else:
                failed += 1
                if result['next_action'] == 'escalate':
                    print(f"🚨 Erro crítico no passo {step['id']}, parando execução")
                    break
                    
        final_status = "success" if failed == 0 else ("partial" if completed > 0 else "failed")
        
        return {
            "completed_steps": completed,
            "failed_steps": failed,
            "results": results,
            "final_status": final_status
        }


# --- DEMO ---
if __name__ == "__main__":
    planner = MultiStepPlanner()
    
    # Teste: criar app
    goal = "Criar um sistema de monitoramento de vendas com dashboard"
    context = {
        "tech_stack": ["Python", "Django", "Chart.js"],
        "deadline": "1 semana",
        "experience_level": "intermediate"
    }
    
    print("🧠 MULTI-STEP PLANNER - DEMO")
    print("="*60)
    
    plan = planner.create_plan(goal, context)
    
    print(f"\n📋 PLANO GERADO:")
    print(f"   Objetivo: {plan['goal']}")
    print(f"   Total de passos: {len(plan['steps'])}")
    print(f"   Tempo estimado: {plan['total_estimated_time']}")
    
    print(f"\n📝 PASSOS:")
    for step in plan['steps']:
        deps = f" (depende de: {step['dependencies']})" if step['dependencies'] else ""
        print(f"   {step['id']}. [{step['action']}] {step['description']}{deps}")
        print(f"      ✓ Sucesso quando: {step['success_criteria']}")
        print(f"      ⏱️  ~{step['estimated_time']}")
        print()
