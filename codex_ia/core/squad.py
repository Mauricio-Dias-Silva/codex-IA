from typing import Dict, Any, List
import logging
from codex_ia.core.context import ContextManager
from codex_ia.core.llm_client import GeminiClient
from codex_ia.core.network_agent import NetworkAgent

class BaseAgent:
    def __init__(self, role: str, system_prompt: str, client: Any = None):
        self.role = role
        self.client = client if client else GeminiClient()
        self.system_prompt = system_prompt
    
    def chat(self, user_msg: str) -> str:
        full_prompt = f"ROLE: {self.role}\n{self.system_prompt}\n\nUSER TASK:\n{user_msg}"
        return self.client.send_message(full_prompt)

class CoderAgent(BaseAgent):
    def __init__(self, client: Any = None):
        super().__init__(
            role="Senior Python Developer",
            system_prompt="You write clean, efficient, and typed Python code. Return ONLY the code block.",
            client=client
        )

class TesterAgent(BaseAgent):
    def __init__(self, client: Any = None):
        super().__init__(
            role="QA Engineer",
            system_prompt="You write pytest test cases for the provided code. Cover edge cases.",
            client=client
        )

class EngineerAgent(BaseAgent):
    def __init__(self, client: Any = None):
        super().__init__(
            role="DevOps Engineer",
            system_prompt="You are responsible for applying code changes to the file system. You receive code and file paths, and your job is to write them. You must confirm the file path is correct.",
            client=client
        )

    def apply_changes(self, root_path: str, file_path: str, code: str) -> str:
        """
        Writes the code to the specified file. 
        """
        import os
        full_path = os.path.join(root_path, file_path)
        
        try:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(code)
            return f"✅ Successfully wrote to {full_path}"
        except Exception as e:
            return f"❌ Failed to write to {full_path}: {e}"

class ExecutorAgent(BaseAgent):
    def __init__(self, client: Any = None):
        super().__init__(
            role="System Administrator",
            system_prompt="You execute system commands to verify code. You return the output.",
            client=client
        )

    def run_command(self, command: str, work_dir: str) -> Dict[str, Any]:
        import subprocess
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                cwd=work_dir, 
                capture_output=True, 
                text=True,
                timeout=60
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except Exception as e:
            return {"success": False, "stderr": str(e), "stdout": ""}

class ResearcherAgent(BaseAgent):
    def __init__(self, client: Any = None):
        super().__init__(
            role="Technical Researcher",
            system_prompt="You look up documentation and solutions online. You provide summaries and code snippets found on the web.",
            client=client
        )
    
    def research(self, query: str) -> str:
        """
        Uses Web Search to find answers.
        """
        # We need to access the client's underlying method with web_search=True
        return self.client.send_message(query, web_search=True)

class SquadLeader:
    """
    [LEVEL 8] The Squad Leader.
    Orchestrates specialized agents to complete a feature request.
    [LEVEL 13 UPGRADE] Integrated with NetworkAgent for Feedback Loops.
    """
    def __init__(self, root_path: str = ".", llm_client: Any = None):
        self.root_path = root_path
        self.context_mgr = ContextManager(root_path)
        self.client = llm_client if llm_client else GeminiClient()
        
        self.coder = CoderAgent(client=self.client)
        self.tester = TesterAgent(client=self.client)
        self.engineer = EngineerAgent(client=self.client)
        self.executor = ExecutorAgent(client=self.client)
        self.researcher = ResearcherAgent(client=self.client)
        
        # Connect to Exocortex
        self.network = NetworkAgent()
    
    def set_target(self, new_path: str):
        """Changes the active target directory for the squad."""
        self.root_path = new_path
        self.context_mgr = ContextManager(new_path)

    def assign_mission(self, mission: str, apply: bool = False, autopilot: bool = False, verification_cmd: str = "", web_search: bool = False) -> Dict[str, str]:
        """
        Executes a mission by coordinating Coder, Tester, and Engineer.
        Supports Autopilot (Write -> Verify -> Fix user loop).
        Supports Web Search (Researcher -> Coder).
        Supports Recursive Memory (NetworkAgent).
        """
        report = {}
        report['mission'] = mission
        report['target_dir'] = self.root_path
        
        # 0. Retrieval Phase (Exocortex)
        # We derive some tags from the mission string (naive approach)
        tags = [w for w in mission.split() if len(w) > 4]
        wisdom = self.network.retrieve_wisdom(tags)
        report['wisdom'] = wisdom
        
        research_context = ""
        if web_search:
            # 0.5 Research Phase
            research_query = f"Research necessary info for: {mission}"
            research_context = self.researcher.research(research_query)
            report['research'] = research_context
        
        # 1. Plan
        plan_prompt = f"MISSION: {mission}\n"
        
        if wisdom:
            plan_prompt += f"\nMEMORY INJECTION (PREVIOUS LESSONS):\n{wisdom}\n"
            
        if research_context:
            plan_prompt += f"RESEARCH CONTEXT:\n{research_context}\n"
            
        plan_prompt += "Break this down into technical requirements for the Coder. If the mission implies editing a specific file, mention it clearly."
        plan = self.client.send_message(plan_prompt)
        report['plan'] = plan
        
        max_retries = 3 if autopilot else 1
        current_attempt = 0
        current_feedback = ""
        final_success = False
        
        while current_attempt < max_retries:
            current_attempt += 1
            
            # 2. Code
            if current_feedback:
                code_prompt = f"PREVIOUS ATTEMPT FAILED.\nFeedback/Error:\n{current_feedback}\n\nFix the code based on this feedback. Return ONLY the code."
            else:
                code_prompt = f"Implement this based on the plan:\n{plan}\n\nIMPORTANT: Return ONLY the code block. If multiple files, use standard separation. For this v1, focus on the main file content."
            
            if research_context:
                code_prompt += f"\n\nUse this research to guide implementation:\n{research_context}"
                
            code = self.coder.chat(code_prompt)
            clean_code = code.replace("```python", "").replace("```", "").strip()
            report['code'] = clean_code
            
            # 3. Test (Unit Test Generation - just for documentation/reference)
            tests = self.tester.chat(f"Write tests for this code:\n{clean_code}")
            report['tests'] = tests
            
            # 4. Apply (The Engineer)
            if apply:
                filename_prompt = f"Based on this plan: {plan}\nWhat is the relative file path to write this code to? Return ONLY the filepath (e.g., 'core/utils.py')."
                target_file = self.client.send_message(filename_prompt).strip()
                result = self.engineer.apply_changes(self.root_path, target_file, clean_code)
                report['apply_status'] = result
            else:
                report['apply_status'] = "Dry Run"
                # If dry run, wait for manual verify or just break
                break

            # 5. Autopilot Verification
            if autopilot and verification_cmd:
                exec_result = self.executor.run_command(verification_cmd, self.root_path)
                report['verification_out'] = exec_result['stdout'] + "\n" + exec_result['stderr']
                
                if exec_result['success']:
                    report['autopilot_status'] = "✅ Verification Passed"
                    final_success = True
                    break # Success!
                else:
                    report['autopilot_status'] = f"❌ Attempt {current_attempt} Failed"
                    current_feedback = f"Command '{verification_cmd}' failed.\nSTDERR:\n{exec_result['stderr']}\nSTDOUT:\n{exec_result['stdout']}"
                    # Loop continues...
            else:
                # No verification command means we assume one-shot success for now
                final_success = True
                break
        
        # 6. Store Experience (Feedback Loop)
        if autopilot:
            self.network.store_experience(
                context=mission,
                action=plan,
                outcome=report.get('autopilot_status', 'Unknown'),
                success=final_success,
                tags=tags
            )
            
        return report
