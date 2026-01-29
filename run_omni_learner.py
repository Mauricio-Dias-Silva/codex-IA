import os
import time
import logging
from dotenv import load_dotenv

# Load environment variables (FIRECRAWL_API_KEY)
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("OmniLearner-Codex")

from codex_ia.core.trend_hunter import TrendHunterAgent
from codex_ia.scrapers.firecrawl_agent import FirecrawlAgent
from codex_ia.core.knowledge_agent import KnowledgeAgent

def main():
    print("🧠 STARTING OMNI-LEARNER (CODEX-IA EDITION)...")
    print("The AI is now scanning the Noosphere for knowledge...")
    
    # Initialize Agents
    hunter = TrendHunterAgent()
    scraper = FirecrawlAgent() # automatically pulls FIRECRAWL_API_KEY from os.environ
    
    # Initialize Memory (Persistent inside codex-IA folder)
    db_path = os.path.join(os.getcwd(), ".codex_memory_db")
    librarian = KnowledgeAgent("codex_core", persistence_path=db_path)

    while True:
        try:
            print("\n📡 Scanning Real World Trends (Brazil)...")
            opportunities = hunter.scan_for_opportunities(language="pt-BR")
            
            if not opportunities:
                print("No new trends found at this moment.")
                time.sleep(60)
                continue

            print(f"Found {len(opportunities)} active trends.")
            
            for opp in opportunities[:5]:
                topic = f"Trend: {opp['trend_name']}"
                print(f"   Analyzing: {topic} (Score: {opp['virality_score']})")
                
                # TEMPORARY TEST: Allow score >= 0 to verify Firecrawl
                if opp['virality_score'] < 0: 
                    continue

                url = opp['source_url']
                if not url or not url.startswith("http") or url == "#":
                    print(f"   -> Skipping invalid URL: {url}")
                    continue

                print(f"   🔍 Deep Scraping: {url}...")
                markdown_content = scraper.scrape_url(url)
                
                if not markdown_content:
                    print("   -> Scraping failed or returned empty.")
                    content_body = f"Context: {opp['description']}\n(Deep reading unavailable)"
                else:
                    print(f"   -> Read {len(markdown_content)} chars.")
                    content_body = markdown_content[:10000] # Increased limit for Codex-IA

                content = f"""
                [Auto-Learned from Firecrawl/Google]
                Date: {time.ctime()}
                Trend: {opp['trend_name']}
                Volume: {opp['search_volume']}
                Virality Score: {opp['virality_score']}
                Source: {url}
                
                === CONTENT ===
                {content_body}
                """
                
                # Ingest into Codex Memory
                chunks = librarian.ingest_text(topic, content)
                print(f"✅ ABSORBED: {topic} ({chunks} chunks saved)")
                
                time.sleep(5) 
            
            print("Sleeping for 5 minutes before next global scan...")
            time.sleep(300)

        except KeyboardInterrupt:
            print("\n🛑 Omni-Learner Stopped.")
            break
        except Exception as e:
            logger.error(f"Glitch in the Matrix: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
