import os
from dotenv import load_dotenv
load_dotenv(override=True)
from codex_ia.core.product_manager import ProductManagerAgent

# Setup
print(f"Testing Product Manager (Level 9)...\n")
pm = ProductManagerAgent()

# Simulated Data (e.g. from PostHog/Google Analytics)
simulated_metrics = {
    "daily_active_users": 1500,
    "churn_rate": "15%",
    "top_pages": ["/home", "/pricing"],
    "drop_off_points": {
        "/checkout/payment": "65% drop-off",
        "/signup": "40% drop-off"
    },
    "user_feedback": [
        "The dashboard is too slow on mobile.",
        "I can't find the logout button.",
        "Payment keeps failing with existing cards."
    ]
}

print("[ANALYSIS] Analyzing Simulated Metrics...")
roadmap = pm.analyze_metrics(simulated_metrics)

print("\n--- PRODUCT BACKLOG ---")
print(roadmap)
print("\n[OK] Product Manager Test Complete!")
