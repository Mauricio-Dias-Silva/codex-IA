from typing import Dict, Any, Generator, List
import logging
import json
import os
import re
import time
import random
from datetime import datetime
from codex_ia.core.brain_router import BrainRouter
from codex_ia.core.squad import SquadLeader, ResearcherAgent

class SupplierInterface:
    """
    Mock Interface for AliExpress/CJ Dropshipping/Zendrop.
    """
    def check_stock(self, product_id: str) -> int:
        return random.randint(50, 500)
        
    def fulfill_order(self, order_details: Dict[str, Any]) -> str:
        """
        Simulates sending order to supplier.
        """
        # In real life, this would be an API POST
        tracking_number = f"CN{random.randint(10000000, 99999999)}TR"
        return tracking_number

class NotificationService:
    """
    Handles alerts via Telegram/WhatsApp (Simulated).
    """
    def send_alert(self, message: str):
        # Placeholder for Telegram Bot API
        # requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", ...)
        print(f"🔔 [NOTIFICATION]: {message}")

class SalesManager:
    """
    Simulates or tracks sales.
    """
    def __init__(self):
        self.orders = []
        self.revenue = 0.0
        
    def simulate_sale(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a fake order for testing.
        """
        price = float(product_data.get('price_point', '$0').replace('$', ''))
        order = {
            "order_id": f"ORD-{random.randint(1000, 9999)}",
            "product": product_data['product_name'],
            "amount": price,
            "customer": {
                "name": "John Doe",
                "address": "123 Main St, New York, NY",
                "email": "customer@example.com"
            },
            "timestamp": datetime.now().isoformat()
        }
        self.orders.append(order)
        self.revenue += price
        return order

class EcommerceAgent:
    """
    [PHASE 3: THE ENDGAME]
    Role: Autonomous Dropshipping Business Builder.
    Capabilities: Niche Research -> Product Selection -> Store Generation -> Ad Creative -> Sales -> Fulfillment.
    """
    
    def __init__(self, root_path: str = "."):
        self.router = BrainRouter()
        self.researcher = ResearcherAgent()
        self.squad = SquadLeader(root_path)
        self.logger = logging.getLogger(__name__)
        
        # Sub-modules
        self.supplier = SupplierInterface()
        self.notifier = NotificationService()
        self.sales_manager = SalesManager()
        
        self.active_product = None

    def find_winning_product(self, niche: str) -> Generator[str, None, Dict[str, Any]]:
        """
        Uses The Council to brainstorm high-converting product ideas.
        """
        yield f"🕵️‍♂️ Investigating Niche: '{niche}'..."
        
        # 1. Market Research (Web Access via Researcher if available, else Logic)
        trend_data = self.researcher.research(f"Trending dropshipping products in {niche} niche 2025")
        
        yield "🧠 Convening Council for Product Selection..."
        
        prompt = f"""
        ROLE: Expert eCommerce Buyer & Trend Hunter.
        
        MARKET DATA:
        {trend_data[:1500]}
        
        TASK:
        Identify 1 WINNING Product to sell in the '{niche}' niche.
        Must be: High Margin, "Wow" Factor, Problem Solver.
        
        RETURN JSON ONLY:
        {{
            "product_name": "Name",
            "tagline": "Marketing Hook",
            "target_audience": "Who buys this?",
            "price_point": "$XX.XX",
            "features": ["Feature 1", "Feature 2", "Feature 3"],
            "pain_point": "What suffering does it end?",
            "visual_style": "Dark/Playful/Medical/etc",
            "supplier_id": "12345"
        }}
        """
        
        # We force Gemini or OpenAI for JSON struct
        response_str = self.router.send_message(prompt)
        yield "✅ Product Identified. Parsing Strategy..."
        
        try:
            # Robust JSON Extraction using Regex
            json_match = re.search(r'\{.*\}', response_str, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                product_data = json.loads(json_str)
                self.active_product = product_data # Store as active
                yield f"🏆 WINNER: {product_data['product_name']} ({product_data['price_point']})"
                yield product_data 
            else:
                 raise ValueError("No JSON object found in response.")
                 
        except Exception as e:
            self.logger.error(f"Failed to parse product JSON: {e}\nRaw Response: {response_str}")
            yield f"⚠️ JSON Parse Error: {e}. Raw len: {len(response_str)}"
            return None

    def build_storefront(self, product_data: Dict[str, Any]) -> str:
        """
        Dispatches the Squad to build the HTML Landing Page.
        """
        product_name = product_data.get('product_name', 'Mystery Product')
        
        mission = f"""
        BUILD A HIGH-CONVERSION LANDING PAGE for: {product_name}
        
        DETAILS:
        - Price: {product_data.get('price_point')}
        - Tagline: {product_data.get('tagline')}
        - Audience: {product_data.get('target_audience')}
        - Style: {product_data.get('visual_style')}
        
        REQUIREMENTS:
        1. Single file 'ecommerce/index.html'.
        2. Use Tailwind CSS (CDN).
        3. Sections: Hero (Image placeholder), "Problem vs Solution", Features, Testimonials (Fake), Sticky "Buy Now" CTA.
        4. Colors: High contrast, trusted feel.
        5. Copywriting: Persuasive, urgency (fictional limited stock).
        
        EXECUTE NOW.
        """
        
        return self.squad.assign_mission(mission, apply=True, autopilot=True)

    def generate_ads(self, product_data: Dict[str, Any]) -> str:
        """
        Generates Ad Scripts and Image Prompts.
        """
        prompt = f"""
        Create 3 Facebook Ad creatives for {product_data.get('product_name')}.
        
        1. **Video Script** (TikTok style, hook in 3s).
        2. **Image Prompt** (For Midjourney/DALL-E).
        3. **Ad Copy** (Headline + Primary Text).
        """
        return self.router.send_message(prompt)

    def run_business_cycle(self) -> Generator[str, None, None]:
        """
        AUTONOMOUS LOOP:
        1. Check for orders (Simulated).
        2. Fulfill orders.
        3. Calculate Profit.
        4. Notify User.
        """
        if not self.active_product:
            yield "❌ No active product. Run find_winning_product() first."
            return

        yield "🔄 cycles: Checking for new sales..."
        
        # Simulate 1-3 random sales
        new_sales_count = random.randint(0, 3)
        
        if new_sales_count == 0:
            yield "💤 No new sales this cycle."
        else:
            yield f"💰 KA-CHING! {new_sales_count} new orders detected!"
            
            for _ in range(new_sales_count):
                order = self.sales_manager.simulate_sale(self.active_product)
                
                # Fulfill
                tracking = self.supplier.fulfill_order(order)
                
                msg = f"📦 Order {order['order_id']} fulfilled! Tracking: {tracking}. Profit: +{order['amount']}"
                yield msg
                self.notifier.send_alert(msg)
                
            yield f"💵 Total Revenue: ${self.sales_manager.revenue:.2f}"
