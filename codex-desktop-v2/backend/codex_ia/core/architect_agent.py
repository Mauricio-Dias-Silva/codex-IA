from typing import List, Dict, Any
import logging
from codex_ia.core.context import ContextManager
from codex_ia.core.llm_client import GeminiClient

class ArchitectAgent:
    """
    [LEVEL 7] The Architect.
    Role: Generates detailed technical design documents (RFC/PRD) from high-level requirements.
    """
    
    def __init__(self, root_path: str = "."):
        self.context_mgr = ContextManager(root_path)
        self.client = GeminiClient()
        self.logger = logging.getLogger(__name__)

    def generate_design_doc(self, requirements: str) -> str:
        """
        Drafts a design document based on requirements.
        """
        # Get existing context to ensure design is compatible
        graph = self.context_mgr.build_graph()
        
        prompt = f"""
        ROLE: Software Architect (Level 7 AI).
        
        EXISTING SYSTEM CONTEXT:
        {graph[:4000]}... (Truncated)
        
        REQUIREMENTS:
        {requirements}
        
        TASK:
        Create a detailed Technical Design Document (Markdown) for this requirement.
        Include:
        1. **Overview**: What are we building?
        2. **System Architecture**: Diagrams (Mermaid), Components, Data Flow.
        3. **Data Model**: Database schemas, JSON structures.
        4. **API Design**: Endpoints, Signatures.
        5. **Implementation Plan**: Step-by-step breakdown.
        
        Review the existing context to ensure the new design fits seamlessly.
        """
        
        design_doc = self.client.send_message(prompt)
        return design_doc
