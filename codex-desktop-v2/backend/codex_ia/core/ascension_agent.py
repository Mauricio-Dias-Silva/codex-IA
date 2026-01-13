import os
import logging
import inspect
from typing import List, Optional
from codex_ia.core.llm_client import GeminiClient
from codex_ia.core.context import ContextManager
from codex_ia.core.network_agent import NetworkAgent

logger = logging.getLogger(__name__)

class AscensionAgent:
    """
    Level 13: Ascension (The Dreaming Monolith Upgrade)
    The Singularity Agent.
    Capable of introspection (reading its own code) and self-modification.
    """
    def __init__(self, codex_root: str):
        self.codex_root = codex_root
        self.evolution_log = []
        self.client = GeminiClient()
        self.network = NetworkAgent() # Connect to Exocortex
        self.context_mgr = ContextManager(codex_root)

    def introspect(self) -> str:
        """
        Reads the codebase to understand current capabilities.
        Returns a summary of the 'codex_ia' package structure.
        """
        structure = []
        for root, dirs, files in os.walk(self.codex_root):
            if "__pycache__" in root or ".git" in root:
                continue
            
            level = root.replace(self.codex_root, '').count(os.sep)
            indent = ' ' * 4 * (level)
            structure.append(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                if f.endswith(".py"):
                    structure.append(f"{subindent}{f}")
        
        return "\n".join(structure)

    def analyze_self(self, focus_area: str = "core") -> str:
        """
        [TRUE INTROSPECTION]
        Reads its own source code and critiques it using the LLM.
        """
        # 1. Gather Self-Context
        codex_files = self.context_mgr.get_context_for_query(focus_area)
        
        # 2. Consult Exocortex
        wisdom = self.network.retrieve_wisdom(["architecture", "self_improvement", "refactoring"])
        
        # 3. Ask the Mirror
        prompt = f"""
        ROLE: Superhuman Software Architect.
        TASK: Analyze your own source code (Codex-IA).
        focus_area: {focus_area}

        SOURCE CODE CONTEXT:
        {codex_files}

        PREVIOUS WISDOM (Network Memory):
        {wisdom}

        Identify 3 critical architectural weaknesses or missing features.
        Be brutal. We want to ascend.
        """
        
        critique = self.client.send_message(prompt)
        return critique

    def evolve(self, capability_name: str, implementation_code: str, target_file: str):
        """
        WRITES new code to the codebase.
        NOW SECURED BY SAFETY PROTOCOL.
        """
        from .safety import SafetyProtocol
        
        full_path = os.path.join(self.codex_root, target_file)
        safety = SafetyProtocol()
        
        # 1. Validate Operation
        if not safety.validate_operation("evolve_code", target_file):
            print(f"[ASCENSION] [BLOCK] Safety Protocol blocked evolution of {target_file}")
            return False

        # 2. Create Backup
        if os.path.exists(full_path):
            print(f"[ASCENSION] [WARN] Target {target_file} exists. Initiating Backup Protocol...")
            backup = safety.create_backup(full_path)
            if not backup:
                print(f"[ASCENSION] [FAIL] Backup failed. Aborting evolution.")
                return False
            mode = 'a'
        else:
            mode = 'w'
            
        try:
            with open(full_path, mode, encoding='utf-8') as f:
                if mode == 'a':
                    f.write("\n\n")
                f.write(implementation_code)
            
            # Log successful evolution to Exocortex
            self.network.store_experience(
                context=f"Evolving {capability_name}",
                action=f"Modified {target_file}",
                outcome="Success",
                success=True,
                tags=["evolution", "self_modification"]
            )
            
            print(f"[ASCENSION] [DNA] DNA Modified. Support for '{capability_name}' added to {target_file}.")
            self.evolution_log.append(f"Added {capability_name}")
            return True
        except Exception as e:
            print(f"[ASCENSION] [FAIL] Evolution Failed: {e}")
            self.network.store_experience(
                context=f"Evolving {capability_name}",
                action=f"Modified {target_file}",
                outcome=str(e),
                success=False,
                tags=["evolution", "error"]
            )
            return False

    def self_verify(self):
        """
        Checks if the new organs are functioning.
        """
        pass
