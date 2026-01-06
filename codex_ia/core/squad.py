from typing import Dict, Any
import logging
from codex_ia.core.context import ContextManager
from codex_ia.core.llm_client import GeminiClient

class BaseAgent:
    def __init__(self, role: str, system_prompt: str):
        self.role = role
        self.client = GeminiClient()
        self.system_prompt = system_prompt
    
    def chat(self, user_msg: str) -> str:
        full_prompt = f"ROLE: {self.role}\n{self.system_prompt}\n\nUSER TASK:\n{user_msg}"
        return self.client.send_message(full_prompt)

class CoderAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Senior Python Developer",
            system_prompt="You write clean, efficient, and typed Python code. Return ONLY the code block."
        )

class TesterAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="QA Engineer",
            system_prompt="You write pytest test cases for the provided code. Cover edge cases."
        )

class SquadLeader:
    """
    [LEVEL 8] The Squad Leader.
    Orchestrates specialized agents to complete a feature request.
    """
    def __init__(self, root_path: str = "."):
        self.context_mgr = ContextManager(root_path)
        self.coder = CoderAgent()
        self.tester = TesterAgent()
        self.client = GeminiClient()
    
    def assign_mission(self, mission: str) -> Dict[str, str]:
        """
        Executes a mission by coordinating Coder and Tester.
        """
        report = {}
        report['mission'] = mission
        
        # 1. Plan
        plan_prompt = f"MISSION: {mission}\nBreak this down into technical requirements for the Coder."
        plan = self.client.send_message(plan_prompt)
        report['plan'] = plan
        
        # 2. Code
        code = self.coder.chat(f"Implement this based on the plan:\n{plan}")
        report['code'] = code
        
        # 3. Test
        tests = self.tester.chat(f"Write tests for this code:\n{code}")
        report['tests'] = tests
        
        return report
