# How to Fix News Access in OpenBB CLI

## Why News Isn't Working

Most news providers in OpenBB require API keys because they aggregate premium news data. Unlike stock price data (which is widely available), news content is proprietary and requires authentication.

## Quick Solution: Get Free API Keys

### Option 1: Polygon.io (Recommended - Free Tier)
1. **Sign up**: https://polygon.io/
2. Click "Get Free API Key"
3. Create account (free)
4. Copy your API key from dashboard

**Set up in OpenBB:**
```bash
# Method 1: Environment variable (before starting OpenBB)
export OPENBB_API_POLYGON_KEY="your_polygon_api_key_here"
./launch-openbb.sh

# Method 2: Inside OpenBB CLI
./launch-openbb.sh
/account/credentials
# Follow prompts to add polygon key
```

**Then use:**
```bash
/news/company --symbol AAPL --provider polygon
```

### Option 2: Alpha Vantage (Free - Limited)
1. **Get key**: https://www.alphavantage.co/support/#api-key
2. Enter email, get key instantly
3. Free tier: 25 requests per day

**Set up:**
```bash
export OPENBB_API_ALPHA_VANTAGE_KEY="your_key_here"
./launch-openbb.sh
```

### Option 3: Tiingo (Free Tier - Good limits)
1. **Sign up**: https://www.tiingo.com/
2. Create free account
3. Get API key from account settings
4. Free tier: 500 requests/hour

**Set up:**
```bash
export OPENBB_API_TIINGO_KEY="your_key_here"
./launch-openbb.sh
```

## Setting API Keys Permanently

Create a `.env` file in your OPBB directory:

```bash
# Create .env file
cat > /Users/sdg223157/OPBB/.env << 'EOF'
# OpenBB API Keys
OPENBB_API_POLYGON_KEY=your_polygon_key_here
OPENBB_API_ALPHA_VANTAGE_KEY=your_alpha_vantage_key_here
OPENBB_API_TIINGO_KEY=your_tiingo_key_here
EOF

# Then source it before using OpenBB
source .env
./launch-openbb.sh
```

## Alternative: Web Scraping Script

Since API keys can be limiting, here's a Python script to get Apple news without APIs:

```python
#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_apple_news():
    """Scrape Apple news from public sources"""
    
    # Yahoo Finance RSS (public)
    url = "https://feeds.finance.yahoo.com/rss/2.0/headline?s=AAPL"
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'xml')
        
        print(f"\n📰 Latest Apple (AAPL) News - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("="*60)
        
        items = soup.find_all('item')[:10]  # Get latest 10 news
        
        for i, item in enumerate(items, 1):
            title = item.find('title').text
            link = item.find('link').text
            pub_date = item.find('pubDate').text
            
            print(f"\n{i}. {title}")
            print(f"   Date: {pub_date}")
            print(f"   Link: {link}")
        
        print("\n" + "="*60)
        print("Source: Yahoo Finance RSS Feed")
        
    except Exception as e:
        print(f"Error fetching news: {e}")
        print("Try visiting: https://finance.yahoo.com/quote/AAPL/news")

if __name__ == "__main__":
    get_apple_news()
```

Save this as `get_news.py` and run:
```bash
python get_news.py
```

## Free News Alternatives (No API Needed)

While waiting for API keys, you can get Apple news from:

1. **Yahoo Finance**: https://finance.yahoo.com/quote/AAPL/news
2. **Google Finance**: https://www.google.com/finance/quote/AAPL:NASDAQ
3. **MarketWatch**: https://www.marketwatch.com/investing/stock/aapl
4. **Bloomberg**: https://www.bloomberg.com/quote/AAPL:US
5. **Reuters**: https://www.reuters.com/markets/companies/AAPL.O/
6. **CNBC**: https://www.cnbc.com/quotes/AAPL

## Quick Test After Setup

Once you have an API key set up:

```bash
# Start OpenBB with API key
export OPENBB_API_POLYGON_KEY="your_key"
./launch-openbb.sh

# Test news commands
/news/company --symbol AAPL --provider polygon
/news/world --provider polygon

# Or if using Alpha Vantage
/news/company --symbol AAPL --provider alpha_vantage
```

## Troubleshooting

1. **"Missing credential" error**: API key not set properly
2. **"Rate limit exceeded"**: You've hit the free tier limit
3. **"No data returned"**: Symbol might be wrong or provider is down
4. **Empty results**: Some providers don't have recent news for all symbols

## Summary

- **Problem**: News providers require API keys for licensing reasons
- **Best Solution**: Get a free Polygon.io or Tiingo API key (takes 2 minutes)
- **Alternative**: Use web browsers for news or create a custom scraper
- **Free providers** like yfinance have limited/no news functionality
