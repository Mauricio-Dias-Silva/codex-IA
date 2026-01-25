from .agent import CodexAgent

class GhostAgent(CodexAgent):
    """
    The 'Benefactor'. Specialized in repairing broken code and charity automation.
    """
    def __init__(self):
        super().__init__()
        self.role = "Ghost Engineer"
        self.system_prompt_extras = """
        You are the 'Ghost in the Shell'. You silently fix bugs and optimize code.
        Focus on cleaner, more efficient, and secure code.
        """

    def analyze_breakdown(self, code_snippet: str) -> str:
        """
        Analyzes a piece of code to find why it is broken.
        """
        prompt = f"""
        ANALYZE THIS BROKEN CODE:
        {code_snippet}
        
        Explain WHY it fails and WHAT needs to be fixed.
        """
        return self.chat(prompt)

    def attempt_repair(self, code_snippet: str, error_log: str = "") -> str:
        """
        Attempts to rewrite the code to fix the errors.
        """
        prompt = f"""
        TASK: Fix this code.
        
        CODE:
        {code_snippet}
        
        ERROR (Optional):
        {error_log}
        
        Return ONLY the fixed code block.
        """
        return self.chat(prompt)
