import logging
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

logger = logging.getLogger(__name__)

class TrendHunterAgent:
    """
    REAL Trend Hunter Agent.
    Connects to the outside world to find viral opportunities.
    """
    
    GOOGLE_TRENDS_RSS = "https://trends.google.com/trending/rss?geo={geo}"

    def __init__(self):
        self.role = "Trend Analyst"

    def scan_for_opportunities(self, language="pt-BR") -> list:
        """
        Fetches live trending searches from Google Trends.
        Returns a structured list of opportunities.
        """
        geo = "BR" if "pt" in language.lower() else "US"
        url = self.GOOGLE_TRENDS_RSS.format(geo=geo)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        logger.info(f"Hunter scanning Google Trends RSS: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            items = root.findall(".//item")
            
            opportunities = []
            
            for item in items:
                title = item.find("title").text if item.find("title") is not None else "Unknown"
                traffic = item.find(".//ht:approx_traffic", namespaces={'ht': 'https://trends.google.com/trends/trendingsearches/daily'})
                traffic_text = traffic.text if traffic is not None else "N/A"
                
                pub_date = item.find("pubDate").text if item.find("pubDate") is not None else ""
                description = item.find("description").text if item.find("description") is not None else ""
                news = item.find(".//ht:news_item_url", namespaces={'ht': 'https://trends.google.com/trends/trendingsearches/daily'})
                if news is not None and news.text:
                    news_url = news.text
                else:
                    # Fallback: Create a Google Search URL so Firecrawl can read the search results
                    from urllib.parse import quote
                    news_url = f"https://www.google.com/search?q={quote(title)}"

                score = 50
                if "M+" in traffic_text: score = 95
                elif "K+" in traffic_text:
                    try:
                        val = int(traffic_text.replace("K+", "").replace(",", ""))
                        if val > 500: score = 90
                        elif val > 100: score = 80
                        elif val > 50: score = 70
                    except: pass

                opportunities.append({
                    "trend_name": title,
                    "search_volume": traffic_text,
                    "virality_score": score,
                    "category": "General",
                    "description": description,
                    "source_url": news_url,
                    "timestamp": pub_date
                })
            
            opportunities.sort(key=lambda x: x['virality_score'], reverse=True)
            return opportunities

        except Exception as e:
            logger.error(f"Hunter failed to fetch trends: {e}")
            return []
