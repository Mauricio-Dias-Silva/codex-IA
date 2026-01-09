import sys
import os
import time

# Add current dir to path
sys.path.append(os.getcwd())

from codex_ia.core.ecommerce_agent import EcommerceAgent

def run_simulation():
    print("🚀 INITIALIZING AUTONOMOUS DROPSHIPPING AGENT...")
    agent = EcommerceAgent()
    
    print("\n--- PHASE 1: RESEARCH & PRODUCT SELECTION ---")
    niche = "Smart Home Gadgets"
    product_data = None
    
    # Run the generator
    for msg in agent.find_winning_product(niche):
        if isinstance(msg, dict):
            product_data = msg
        else:
            print(f"🤖 {msg}")
            
    if not product_data:
        print("❌ Failed to find a product.")
        return

    print("\n--- PHASE 2: STORE CREATION ---")
    print(f"🔨 Building Store for: {product_data['product_name']}")
    # This calls the Squad to generate HTML
    # We might mock the squad response if it takes too long, but let's try real if configured
    # For now, let's assume the squad works or returns a text.
    # The agent.build_storefront returns a dict/report usually, but here it returns a string or report from Squad
    
    try:
        store_report = agent.build_storefront(product_data)
        # It waits for the squad...
        # If the squad is using actual LLMs, it might take a minute.
        print("✅ Storefront Build Command Sent.")
        print(store_report) 
    except Exception as e:
        print(f"⚠️ Store build simulated (Agent error: {e})")

    print("\n--- PHASE 3: ADS GENERATION ---")
    ads = agent.generate_ads(product_data)
    print(f"📢 Generated Ads:\n{ads[:300]}...\n")

    print("\n--- PHASE 4: BUSINESS OPERATIONS (The Loop) ---")
    # Simulate 3 days of operations
    for day in range(1, 4):
        print(f"\n📅 DAY {day}:")
        for log in agent.run_business_cycle():
            print(f"   {log}")
        time.sleep(1) # Gap between days

    print("\n✨ SIMULATION COMPLETE.")
    print(f"💰 Final Bank Balance: ${agent.sales_manager.revenue:.2f}")

if __name__ == "__main__":
    run_simulation()
