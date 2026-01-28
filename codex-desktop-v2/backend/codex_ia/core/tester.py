import os
import subprocess
import logging
from .brain_router import BrainRouter

logger = logging.getLogger(__name__)

class TesterAgent:
    """
    Level 15: QA & Self-Healing (The Immune System V2)
    Runs tests, analyzes failures, and attempts to hotfix code.
    """
    def __init__(self, project_root):
        self.project_root = project_root
        self.brain = BrainRouter()

    def run_tests(self, test_cmd="pytest"):
        """
        Runs the test suite and captures output.
        Returns (success: bool, output: str)
        """
        logger.info(f"🧪 Running tests with: {test_cmd}")
        try:
            # Run test command
            result = subprocess.run(
                test_cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                shell=True
            )
            
            output = result.stdout + "\n" + result.stderr
            return result.returncode == 0, output
        except Exception as e:
            return False, str(e)

    def analyze_and_heal(self, test_output: str, file_context: str = None) -> str:
        """
        Analyzes the traceback and suggests/applies a fix.
        """
        logger.info("🚑 Analyzing failure for triage...")
        
        prompt = f"""
        You are a Senior QA Engineer and Algo-Surgeon.
        The tests failed. Analyze the traceback and the code.
        
        TRACEBACK:
        {test_output[-2000:]} 
        
        CONTEXT (Relevant Code):
        {file_context if file_context else "Not provided. Infer from traceback."}

        Task:
        1. Identify the root cause (Syntax, Logic, Import, etc).
        2. Generate a PATCH (diff or full code rewrite) to fix it.
        
        Output ONLY the valid Python/JS code to repair the file.
        Start your response with comment # PATH: path/to/file.py so I know where to apply it.
        """
        
        solution = self.brain.send_message(prompt, task_type="coding")
        return solution

    def auto_heal(self):
        """
        Main loop: Run -> Fail -> Analyze -> Fix -> Run -> Pass
        """
        success, output = self.run_tests()
        
        if success:
            return {"status": "healthy", "message": "All tests passed! 🟢"}
            
        # If failed, try to heal
        # 1. Parsing failed file from output (simple heuristic)
        failed_file = self._extract_failed_file(output)
        
        context = ""
        if failed_file:
            try:
                with open(os.path.join(self.project_root, failed_file), 'r', encoding='utf-8') as f:
                    context = f.read()
            except:
                pass
                
        # 2. Ask Brain
        fix_proposal = self.analyze_and_heal(output, context)
        
        return {
            "status": "infected", 
            "message": "Tests failed. 🔴", 
            "error_log": output[:500] + "...",
            "proposed_fix": fix_proposal,
            "suspected_file": failed_file
        }

    def _extract_failed_file(self, output):
        """
        Tries to find the file path in a traceback.
        """
        # Very naive: look for "File "path/to/script.py", line X"
        import re
        match = re.search(r'File "([^"]+)", line', output)
        if match:
            return match.group(1)
        return None
