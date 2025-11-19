#!/usr/bin/env python3
"""
Get Apple (AAPL) News without API keys
Using public RSS feeds and web scraping
"""

import requests
from xml.etree import ElementTree
from datetime import datetime
import re

def clean_html(text):
    """Remove HTML tags from text"""
    return re.sub('<.*?>', '', text)

def get_yahoo_finance_news():
    """Get news from Yahoo Finance RSS feed (public, no API needed)"""
    print("\n📰 APPLE (AAPL) NEWS - Yahoo Finance")
    print("="*70)
    
    url = "https://feeds.finance.yahoo.com/rss/2.0/headline?s=AAPL&region=US&lang=en-US"
    
    try:
        response = requests.get(url, timeout=10)
        root = ElementTree.fromstring(response.content)
        
        items = root.findall('.//item')[:10]  # Get latest 10 news items
        
        if not items:
            print("No recent news found.")
            return
        
        for i, item in enumerate(items, 1):
            title = item.find('title').text
            link = item.find('link').text
            pub_date = item.find('pubDate').text
            
            # Parse and format date
            try:
                # Convert RSS date format to readable format
                from email.utils import parsedate_to_datetime
                dt = parsedate_to_datetime(pub_date)
                formatted_date = dt.strftime('%Y-%m-%d %H:%M')
            except:
                formatted_date = pub_date[:16]
            
            print(f"\n{i}. {title[:100]}")
            print(f"   📅 {formatted_date}")
            if len(title) > 100:
                print(f"   {title[100:]}")
            print(f"   🔗 {link[:70]}...")
        
        print("\n" + "-"*70)
        print("Source: Yahoo Finance RSS Feed (Public)")
        
    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        print("\nAlternative: Visit https://finance.yahoo.com/quote/AAPL/news")
    except Exception as e:
        print(f"Error parsing news: {e}")

def get_seeking_alpha_news():
    """Try to get news from Seeking Alpha (sometimes works without API)"""
    print("\n📊 MARKET ANALYSIS - Seeking Alpha")
    print("="*70)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        # Seeking Alpha public feed
        url = "https://seekingalpha.com/symbol/AAPL"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("For detailed analysis, visit:")
            print("🔗 https://seekingalpha.com/symbol/AAPL/news")
            print("🔗 https://seekingalpha.com/symbol/AAPL/analysis")
        else:
            print("Unable to fetch Seeking Alpha content directly.")
            print("Visit: https://seekingalpha.com/symbol/AAPL")
    except:
        print("Visit: https://seekingalpha.com/symbol/AAPL for analysis")

def get_news_summary():
    """Get a summary of news sources"""
    print("\n📱 APPLE NEWS SOURCES")
    print("="*70)
    
    sources = {
        "Yahoo Finance": "https://finance.yahoo.com/quote/AAPL/news",
        "Google Finance": "https://www.google.com/finance/quote/AAPL:NASDAQ",
        "MarketWatch": "https://www.marketwatch.com/investing/stock/aapl/news",
        "Bloomberg": "https://www.bloomberg.com/quote/AAPL:US",
        "Reuters": "https://www.reuters.com/markets/companies/AAPL.O/",
        "CNBC": "https://www.cnbc.com/quotes/AAPL?tab=news",
        "MacRumors": "https://www.macrumors.com/",
        "9to5Mac": "https://9to5mac.com/guides/aapl/"
    }
    
    print("\n📌 Quick Links to Apple News:")
    print("-"*70)
    
    for source, url in sources.items():
        print(f"• {source:15} → {url}")
    
    print("\n💡 TIP: For automated news in OpenBB, get a free API key:")
    print("   1. Polygon.io: https://polygon.io/ (Free tier available)")
    print("   2. Alpha Vantage: https://www.alphavantage.co/support/#api-key (Free)")
    print("   3. See setup-news-api.md for instructions")

def main():
    print("="*70)
    print("            APPLE (AAPL) NEWS AGGREGATOR")
    print("             No API Keys Required")
    print("="*70)
    
    # Get news from Yahoo Finance RSS
    get_yahoo_finance_news()
    
    # Show additional sources
    get_news_summary()
    
    print("\n" + "="*70)
    print("Updated:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("="*70)

if __name__ == "__main__":
    main()
