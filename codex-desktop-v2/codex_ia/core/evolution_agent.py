from typing import List, Dict, Any
import os
from pathlib import Path
from codex_ia.core.context import ContextManager
from codex_ia.core.llm_client import GeminiClient

from codex_ia.core.squad import SquadLeader

class EvolutionAgent:
    """
    [LEVEL 5] Autonomous Software Engineer.
    Role: Proactively scans the codebase for improvements and dispatches Squads to fix them.
    """
    
    def __init__(self, root_path: str = "."):
        self.context_mgr = ContextManager(root_path)
        self.client = GeminiClient()
        self.root = Path(root_path).resolve()
        self.root_path = root_path

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

    def start_night_shift(self, max_missions: int = 3, verification_cmd: str = "") -> Generator[str, None, None]:
        """
        [THE NIGHT SHIFT]
        Continuously scans and fixes issues.
        Yields log messages for the UI.
        """
        yield "🌙 Night Shift started. Scanning codebase..."
        
        opps = self.scan_for_improvements()
        if not opps:
            yield "✅ No issues found. The codebase is clean. Going to sleep."
            return

        yield f"🧐 Found {len(opps)} opportunities for improvement."
        
        missions_run = 0
        squad = SquadLeader(self.root_path)
        
        for opp in opps:
            if missions_run >= max_missions:
                yield "🛑 Max missions reached for this shift."
                break
                
            target_file = opp['file']
            issue_type = opp['type']
            yield f"🎯 Targeting: {target_file} ({issue_type})"
            
            mission = f"Fix the {issue_type} in {target_file}. {opp['description']}"
            yield f"🚀 Dispatching Squad: '{mission}'"
            
            # Dispatch Squad in Autopilot
            report = squad.assign_mission(
                mission, 
                apply=True, 
                autopilot=True if verification_cmd else False, 
                verification_cmd=verification_cmd
            )
            
            yield f"📋 Squad Result: {report.get('autopilot_status', 'Done')}"
            yield f"✅ Fix applied to {target_file}"
            
            missions_run += 1
            
        yield "☀️ Night Shift shift ended."
