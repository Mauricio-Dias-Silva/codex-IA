import os
from dotenv import load_dotenv
load_dotenv(override=True)
from codex_ia.core.founder_agent import FounderAgent

print("Testing Founder Agent (Level 10)...\n")
founder = FounderAgent()

niche = "Real Estate Agents who struggle with social media"

print(f"[BRAINSTORM] Brainstorming ideas for: '{niche}'...")
ideas = founder.brainstorm_ideas(niche)
print("\n--- IDEAS GENERATED ---")
print(ideas[:1000] + "...")

# Pick one idea (simulated selection)
print("\n[GENERATOR] Generating Landing Page for the best idea...")
landing_page = founder.generate_landing_page("RealtyPost AI: Auto-generate Instagram reels from property listings.")

output_file = "FOUNDER_LANDING_PAGE.html"
with open(output_file, "w", encoding='utf-8') as f:
    f.write(landing_page)

print(f"\n[OK] Landing page saved to {output_file}")
