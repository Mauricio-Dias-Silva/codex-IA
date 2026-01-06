from typing import List, Dict, Any
import os
from pathlib import Path
from codex_ia.core.context import ContextManager
from codex_ia.core.llm_client import GeminiClient

class EvolutionAgent:
    """
    [LEVEL 5] Autonomous Software Engineer.
    Role: Proactively scans the codebase for improvements without user prompting.
    """
    
    def __init__(self, root_path: str = "."):
        self.context_mgr = ContextManager(root_path)
        self.client = GeminiClient()
        self.root = Path(root_path).resolve()

    def scan_for_improvements(self) -> List[Dict[str, Any]]:
        """
        Scans the codebase for potential optimizations.
        Returns a list of 'Improvement Opportunities'.
        """
        opportunities = []
        all_files = self.context_mgr.list_files()
        
        for rel_path in all_files:
            file_path = self.root / rel_path
            
            # 1. Check for TODOs/FIXMEs
            if self._has_todo_comments(file_path):
                opportunities.append({
                    "type": "TECH_DEBT",
                    "file": rel_path,
                    "description": "Found TODO/FIXME comments requiring attention."
                })
                
            # 2. Check for complexity (Simple heuristic: file size > 300 lines)
            # A real implementation would use cyclomatic complexity tools.
            try:
                if file_path.suffix == '.py':
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        if len(f.readlines()) > 300:
                             opportunities.append({
                                "type": "COMPLEXITY",
                                "file": rel_path,
                                "description": "File is too large (>300 lines), consider splitting."
                            })
            except:
                pass

        return opportunities

    def _has_todo_comments(self, file_path: Path) -> bool:
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            return "TODO" in content or "FIXME" in content
        except:
            return False

    def auto_refactor(self, file_path_str: str) -> str:
        """
        Autonomously refactors a specific file.
        """
        context = self.context_mgr.get_file_context(file_path_str)
        
        instructions = """
        [AUTONOMOUS MODE]
        Analyze this file. Identify:
        1. Unused imports.
        2. Inefficient patterns.
        3. Missing type hints.
        
        Rewrite the code applying these fixes. Ensure functionality remains IDENTICAL.
        """
        
        refactored_code = self.client.refactor_code(context, instructions)
        return refactored_code

    def run_nightly_optimization(self) -> str:
        """
        Entry point for the 'Nightly' job.
        """
        opps = self.scan_for_improvements()
        if not opps:
            return "EvolutionAgent: No obvious improvements found. The codebase is healthy."
            
        # Pick the 'easiest' fix (Tech Debt) to demonstrate autonomy
        target = opps[0]
        report = f"EvolutionAgent Report:\nFound {len(opps)} opportunities.\n"
        report += f"Targeting: {target['file']} ({target['type']})\n"
        
        try:
            # In a real autonomy loop, we would create a branch, apply, test, and PR.
            # Here, we generate the diff and log it (Safety first!)
            new_code = self.auto_refactor(target['file'])
            report += f"\n--- PROPOSED REFACTOR FOR {target['file']} ---\n{new_code[:500]}...\n(Truncated)"
        except Exception as e:
            report += f"\nError attempting refactor: {e}"
            
        return report
