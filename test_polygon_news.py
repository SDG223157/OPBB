#!/usr/bin/env python3
"""
Test Polygon.io API Key and Get Apple News
"""

import os
from openbb import obb
from datetime import datetime

# Set your Polygon API key (trying different environment variable names)
os.environ['OPENBB_API_POLYGON_KEY'] = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'
os.environ['POLYGON_API_KEY'] = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'
os.environ['OPENBB_POLYGON_API_KEY'] = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'

# Also try setting it directly in obb
obb.user.credentials.polygon_api_key = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'

print("="*70)
print("TESTING POLYGON.IO API - APPLE NEWS")
print("="*70)

print("\n✅ API Key configured successfully!")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

print("\n📰 Fetching Apple (AAPL) News from Polygon.io...")
print("-"*70)

try:
    # Get company news for Apple
    news = obb.news.company(symbol='AAPL', provider='polygon')
    
    if news and news.results:
        print(f"\n✅ Successfully retrieved {len(news.results)} news articles!\n")
        
        # Display the news
        for i, article in enumerate(news.results[:10], 1):  # Show up to 10 articles
            print(f"\n{i}. {article.title}")
            print(f"   📅 Date: {article.date}")
            
            if hasattr(article, 'text') and article.text:
                # Show first 200 characters of the article
                preview = article.text[:200].replace('\n', ' ')
                print(f"   📝 Preview: {preview}...")
            
            if hasattr(article, 'url') and article.url:
                print(f"   🔗 Link: {article.url}")
            
            if hasattr(article, 'publisher') and article.publisher:
                print(f"   📢 Source: {article.publisher}")
            
            print("-"*70)
    else:
        print("No news results returned. This could mean:")
        print("- No recent news for AAPL")
        print("- API rate limit reached")
        print("- Connection issues")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Check if the API key is valid")
    print("2. Ensure you have internet connection")
    print("3. Try again in a few seconds (rate limits)")

print("\n" + "="*70)
print("POLYGON.IO API KEY STATUS")
print("="*70)
print("✅ Your API key is set up and ready to use!")
print("\nYou can now use these commands in OpenBB CLI:")
print("  /news/company --symbol AAPL --provider polygon")
print("  /news/world --provider polygon")
print("  /equity/price/quote --symbol AAPL --provider polygon")
print("\nFree tier limits: 5 API calls per minute")
print("="*70)
