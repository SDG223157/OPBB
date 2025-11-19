#!/usr/bin/env python3
"""
Get Apple-specific news using Polygon.io API
"""

import os
from openbb import obb
from datetime import datetime

# Set Polygon API key
os.environ['POLYGON_API_KEY'] = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'
obb.user.credentials.polygon_api_key = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'

print("="*80)
print(" "*20 + "🍎 APPLE (AAPL) NEWS - POLYGON.IO 🍎")
print("="*80)
print(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

try:
    # Get news specifically for Apple
    news = obb.news.company(symbol='AAPL', provider='polygon')
    
    if news and news.results:
        # Filter for Apple-specific news (looking for Apple, AAPL, iPhone, etc. in title)
        apple_keywords = ['apple', 'aapl', 'iphone', 'ipad', 'mac', 'ios', 'tim cook', 
                         'cupertino', 'app store', 'airpods', 'apple watch', 'vision pro']
        
        apple_news = []
        for article in news.results:
            title_lower = article.title.lower() if article.title else ""
            text_lower = article.text.lower() if hasattr(article, 'text') and article.text else ""
            
            # Check if any Apple keyword is in the title or text
            if any(keyword in title_lower or keyword in text_lower for keyword in apple_keywords):
                apple_news.append(article)
        
        if apple_news:
            print(f"\n📰 Found {len(apple_news)} Apple-specific articles (out of {len(news.results)} total)\n")
            
            # Display Apple news
            for i, article in enumerate(apple_news[:15], 1):  # Show up to 15 articles
                print(f"\n{i}. {article.title}")
                print("   " + "="*75)
                
                # Date
                if article.date:
                    date_str = str(article.date)[:19]  # Format date
                    print(f"   📅 Date: {date_str}")
                
                # Publisher
                if hasattr(article, 'publisher') and article.publisher:
                    publisher_name = article.publisher.name if hasattr(article.publisher, 'name') else str(article.publisher)
                    print(f"   📢 Source: {publisher_name}")
                
                # Preview text
                if hasattr(article, 'text') and article.text:
                    preview = article.text[:250].replace('\n', ' ')
                    print(f"   📝 Preview: {preview}...")
                
                # URL
                if hasattr(article, 'url') and article.url:
                    print(f"   🔗 Link: {article.url[:80]}...")
                
                print("   " + "-"*75)
        else:
            print("\n📊 No Apple-specific news found in recent articles.")
            print("\nShowing general market news that might be relevant:\n")
            
            # Show some general news
            for i, article in enumerate(news.results[:5], 1):
                print(f"\n{i}. {article.title}")
                if article.date:
                    print(f"   📅 {str(article.date)[:19]}")
                if hasattr(article, 'publisher') and article.publisher:
                    publisher_name = article.publisher.name if hasattr(article.publisher, 'name') else str(article.publisher)
                    print(f"   📢 {publisher_name}")
    else:
        print("\n❌ No news data retrieved. This could be due to rate limits or connection issues.")
        
except Exception as e:
    print(f"\n❌ Error: {e}")

# Also get stock data for context
print("\n" + "="*80)
print(" "*25 + "📊 APPLE STOCK DATA 📊")
print("="*80)

try:
    quote = obb.equity.price.quote(symbol='AAPL', provider='polygon')
    if quote and quote.results:
        data = quote.results[0]
        print(f"\n💹 Current Price: ${data.last_price:.2f}")
        if hasattr(data, 'change') and data.change:
            print(f"📈 Change Today: ${data.change:.2f}")
        if hasattr(data, 'change_percent') and data.change_percent:
            print(f"📊 Change %: {data.change_percent:.2f}%")
        if hasattr(data, 'volume') and data.volume:
            print(f"📊 Volume: {data.volume:,}")
        if hasattr(data, 'high') and data.high:
            print(f"📈 Day High: ${data.high:.2f}")
        if hasattr(data, 'low') and data.low:
            print(f"📉 Day Low: ${data.low:.2f}")
except:
    pass

print("\n" + "="*80)
print("💡 TIP: Use './launch-openbb-with-polygon.sh' to start OpenBB with Polygon API")
print("="*80)
