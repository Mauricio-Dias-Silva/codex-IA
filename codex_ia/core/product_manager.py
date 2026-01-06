from typing import Dict, Any, List
import logging
import json
from codex_ia.core.llm_client import GeminiClient

class ProductManagerAgent:
    """
    [LEVEL 9] The Product Manager.
    Role: Analyzes data (metrics, feedback) to define WHAT to build.
    """
    
    def __init__(self):
        self.client = GeminiClient()
        self.logger = logging.getLogger(__name__)

    def analyze_metrics(self, metrics_data: Dict[str, Any]) -> str:
        """
        Analyzes a metrics dictionary/JSON and produces a Feature Roadmap.
        """
        prompt = f"""
        ROLE: Senior Product Manager (Level 9 AI).
        
        DATA SOURCE (Usage Metrics / User Feedback):
        {json.dumps(metrics_data, indent=2)}
        
        TASK:
        Analyze this data to identify user pain points and opportunities.
        Create a Prioritized Product Backlog (Top 3 Items).
        
        For each item, specify:
        1. **Problem Statement**: What is wrong? (Cite data)
        2. **Proposed Solution**: What feature/fix do we build?
        3. **Business Value**: Why is this important?
        4. **Priority**: High/Medium/Low
        """
        
        roadmap = self.client.send_message(prompt)
        return roadmap

    def draft_user_stories(self, feature_request: str) -> str:
        """
        Converts a feature idea into structured User Stories.
        """
        prompt = f"""
        ROLE: Product Manager.
        TASK: Convert this feature request into Gherkin-style User Stories (As a... I want to... So that...).
        
        FEATURE: {feature_request}
        """
        return self.client.send_message(prompt)
