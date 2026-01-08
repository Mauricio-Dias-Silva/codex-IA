from codex_ia.core.squad import ResearcherAgent

def test_researcher():
    print("Testing Researcher Agent...")
    try:
        agent = ResearcherAgent()
        # We can't easily verify the actual Google Search without a query that changes, 
        # but we can verify the call structure doesn't crash.
        # We will ask a query that definitely needs recent info.
        
        query = "What is the latest released version of Python as of today?"
        print(f"Querying: {query}")
        
        # This will make a real API call if keys are set
        response = agent.research(query)
        
        print("Response received:")
        print(response[:200] + "...")
        print("✅ Researcher Agent appears functional.")
    except Exception as e:
        print(f"❌ Researcher Error: {e}")

if __name__ == "__main__":
    test_researcher()
