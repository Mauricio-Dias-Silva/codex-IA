from typing import Dict, Any
import logging
from codex_ia.core.llm_client import GeminiClient

class FounderAgent:
    """
    [LEVEL 10] The Founder.
    Role: Identifies market gaps and creates the 'Business Wrapper' around code.
    Capabilities: Ideation, Pitching, Copywriting.
    """
    
    def __init__(self):
        self.client = GeminiClient()
        self.logger = logging.getLogger(__name__)

    def brainstorm_ideas(self, niche: str) -> str:
        """
        Generates viable Micro-SaaS ideas for a specific niche.
        """
        prompt = f"""
        ROLE: Serial Entrepreneur / Startup Founder (Level 10 AI).
        
        MARKET NICHE: {niche}
        
        TASK:
        Generate 3 Viable Micro-SaaS Ideas for this niche.
        Focus on problems that can be solved with AI/Automation.
        
        For each idea:
        1. **Name**: Catchy & Short.
        2. **One-Liner**: The "Elevator Pitch".
        3. **Monetization**: How do we make money? (e.g. Subscription, Usage-based).
        """
        
        return self.client.send_message(prompt)

    def generate_landing_page(self, pitch: str) -> str:
        """
        Writes a high-converting Landing Page (HTML) for the chosen idea.
        """
        prompt = f"""
        ROLE: Expert Copywriter & Web Designer.
        
        PRODUCT PITCH:
        {pitch}
        
        TASK:
        Write a single-file HTML5 Landing Page (modern, responsive, using Tailwind CSS via CDN).
        
        Structure:
        1. **Hero Section**: H1 Headline, Subheadline, CTA Button.
        2. **Problem/Solution**: Why does the user need this?
        3. **Features**: 3 Key benefits.
        4. **Pricing**: Simple table.
        5. **Footer**: Copyright.
        
        Output ONLY the valid HTML code.
        """
        
        return self.client.send_message(prompt)
