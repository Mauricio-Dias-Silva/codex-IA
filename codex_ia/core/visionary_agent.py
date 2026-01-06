from typing import List, Dict, Any
import json
import logging
from codex_ia.core.context import ContextManager
from codex_ia.core.llm_client import GeminiClient

class VisionaryAgent:
    """
    [LEVEL 6] The Visionary.
    Role: Suggests strategic code changes based on Business Goals.
    """
    
    def __init__(self, root_path: str = "."):
        self.context_mgr = ContextManager(root_path)
        self.client = GeminiClient()
        self.logger = logging.getLogger(__name__)

    def load_business_goals(self) -> List[Dict]:
        """Loads business goals from a JSON file."""
        try:
            with open("business_goals.json", "r") as f:
                return json.load(f)
        except Exception:
            return []

    def align_code_with_goals(self) -> str:
        """
        Analyzes the codebase in the context of business goals.
        """
        goals = self.load_business_goals()
        if not goals:
            return "No 'business_goals.json' found. Cannot be a Visionary without a Vision."

        # Get high-level architecture
        graph = self.context_mgr.build_graph()
        
        prompt = f"""
        ROLE: Visionary Software Architect (Level 6 AI).
        
        BUSINESS GOALS:
        {json.dumps(goals, indent=2)}
        
        CURRENT ARCHITECTURE:
        {graph[:5000]}
        
        TASK:
        Propose 3 High-Impact Technical Initiatives that directly support these business goals.
        For each initiative, explain:
        1. The Technical Change (e.g., "Implement Redis Caching").
        2. The Business Impact (e.g., "Reduces load time by 40%, improving retention").
        3. Implementation Difficulty (1-10).
        """
        
        proposal = self.client.send_message(prompt)
        return f"--- VISIONARY PROPOSAL ---\n{proposal}"
