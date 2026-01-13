from typing import Dict, Any
import logging
from codex_ia.core.llm_client import GeminiClient

class FounderAgent:
    """
    [LEVEL 10] The Founder.
    Role: Identifies market gaps and creates the 'Business Wrapper' around code.
    Capabilities: Ideation, Pitching, Copywriting.
    """
    
from codex_ia.core.squad import SquadLeader, ResearcherAgent

class FounderAgent:
    """
    [LEVEL 10] The Founder.
    Role: Identifies market gaps and creates the 'Business Wrapper' around code.
    Capabilities: Ideation, Pitching, Copywriting, Squad Dispatch.
    """
    
    def __init__(self, root_path: str = "."):
        self.client = GeminiClient()
        self.logger = logging.getLogger(__name__)
        self.researcher = ResearcherAgent()
        self.squad = SquadLeader(root_path)

    def brainstorm_ideas(self, niche: str) -> Dict[str, str]:
        """
        Generates viable Micro-SaaS ideas for a specific niche using REAL MARKET DATA.
        """
        # 1. Research Phase
        yield f"🔎 Researching market trends for '{niche}'..."
        research_data = self.researcher.research(f"Market trends and SaaS opportunities in {niche} for 2025/2026")
        
        yield "💡 Brainstorming concepts based on data..."
        prompt = f"""
        ROLE: Serial Entrepreneur / Startup Founder (Level 10 AI).
        
        MARKET DATA:
        {research_data[:2000]}
        
        TASK:
        Generate 3 Viable Micro-SaaS Ideas for the '{niche}' niche.
        Focus on problems that can be solved with AI/Automation.
        
        For each idea:
        1. **Name**: Catchy & Short.
        2. **One-Liner**: The "Elevator Pitch".
        3. **Monetization**: How do we make money?
        4. **Tech Stack**: Brief suggestion.
        """
        
        ideas = self.client.send_message(prompt)
        yield ideas
        return ideas

    def build_landing_page(self, idea_context: str) -> str:
        """
        Dispatches the Squad to build the actual landing page file.
        """
        mission = f"""
        Create a high-converting Landing Page (index.html) for this business idea:
        
        {idea_context}
        
        REQUIREMENTS:
        - Single file HTML (index.html).
        - Use Tailwind CSS via CDN.
        - Modern, dark-mode aesthetic.
        - Sections: Hero, Features, Pricing, Footer.
        - Save it to 'landing_pages/index.html'.
        """
        
        # Dispatch Squad in Autopilot Mode
        report = self.squad.assign_mission(mission, apply=True, autopilot=True, verification_cmd="")
        
        return report
