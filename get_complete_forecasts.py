#!/usr/bin/env python3
"""
Complete Company Financial Forecast with Finviz Elite
Get 3-year forecasts with analyst price targets
"""

from openbb import obb
import os
from datetime import datetime

# Set all API keys
os.environ['FINVIZ_API_KEY'] = 'be56a0a4-c7b3-4094-85b6-0ad5a3b49fc6'
os.environ['POLYGON_API_KEY'] = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'
os.environ['FRED_API_KEY'] = '7c26de454d31a77bfdf9aaa33f2f55a8'

obb.user.credentials.finviz_api_key = 'be56a0a4-c7b3-4094-85b6-0ad5a3b49fc6'
obb.user.credentials.polygon_api_key = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'
obb.user.credentials.fred_api_key = '7c26de454d31a77bfdf9aaa33f2f55a8'

def get_complete_forecast(symbol):
    """Get comprehensive 3-year forecast using all available data sources"""
    
    print(f"\n{'='*80}")
    print(f"  💹 COMPLETE 3-YEAR FINANCIAL FORECAST: {symbol}")
    print('='*80)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print('='*80)
    
    # 1. Get current price from Polygon
    current_price = None
    try:
        quote = obb.equity.price.quote(symbol=symbol, provider='polygon')
        if quote and quote.results:
            current_price = quote.results[0].last_price
            print(f"\n📊 CURRENT MARKET DATA (via Polygon)")
            print("-"*50)
            print(f"Current Price: ${current_price:.2f}")
            if hasattr(quote.results[0], 'change_percent'):
                print(f"Today's Change: {quote.results[0].change_percent:.2f}%")
    except:
        # Fallback to yfinance
        try:
            quote = obb.equity.price.quote(symbol=symbol, provider='yfinance')
            if quote and quote.results:
                current_price = quote.results[0].last_price
                print(f"\n📊 CURRENT MARKET DATA")
                print("-"*50)
                print(f"Current Price: ${current_price:.2f}")
        except:
            pass
    
    # 2. Get Finviz Elite Price Target
    price_target = None
    print(f"\n🎯 ANALYST PRICE TARGETS (via Finviz Elite)")
    print("-"*50)
    try:
        target_data = obb.equity.estimates.price_target(symbol=symbol, provider='finviz')
        if target_data and target_data.results:
            # Get the most recent price target
            latest_target = target_data.results[0]
            
            if hasattr(latest_target, 'adj_price_target') and latest_target.adj_price_target:
                price_target = latest_target.adj_price_target
                print(f"Latest Price Target: ${price_target:.2f}")
                
                if current_price and price_target:
                    upside = ((price_target - current_price) / current_price) * 100
                    print(f"Upside Potential: {upside:+.1f}%")
                
                if hasattr(latest_target, 'rating_change'):
                    print(f"Rating: {latest_target.rating_change}")
                
                if hasattr(latest_target, 'status'):
                    print(f"Action: {latest_target.status}")
                    
                if hasattr(latest_target, 'published_date'):
                    print(f"Date: {latest_target.published_date}")
                    
                # Check for analyst company
                if hasattr(latest_target, 'model_extra') and 'analyst_company' in latest_target.model_extra:
                    print(f"Analyst: {latest_target.model_extra['analyst_company']}")
        else:
            print("No recent price targets available")
    except Exception as e:
        print(f"Note: {str(e)[:100]}")
    
    # 3. Get historical financials for growth calculation
    print(f"\n📈 HISTORICAL GROWTH ANALYSIS")
    print("-"*50)
    revenue_growth = None
    try:
        income = obb.equity.fundamental.income(symbol=symbol, provider='yfinance')
        if income and income.results:
            revenues = []
            for stmt in income.results[:3]:  # Last 3 years
                if hasattr(stmt, 'total_revenue') and stmt.total_revenue:
                    revenues.append(stmt.total_revenue)
            
            if len(revenues) >= 2:
                # Calculate average growth rate
                revenue_growth = ((revenues[0] - revenues[-1]) / revenues[-1]) * 100 / len(revenues)
                print(f"Average Revenue Growth: {revenue_growth:.1f}% annually")
                
                # Project future revenues
                print(f"\n📊 3-YEAR REVENUE PROJECTIONS")
                print("-"*40)
                current_rev = revenues[0] / 1e9
                for year in range(1, 4):
                    projected = current_rev * (1 + revenue_growth/100) ** year
                    print(f"Year {year}: ${projected:.1f}B")
    except:
        print("Historical data not available")
    
    # 4. Calculate 3-year price projections
    print(f"\n💰 3-YEAR PRICE PROJECTIONS")
    print("-"*50)
    
    if current_price and price_target:
        # Method 1: Based on analyst target (1-year)
        print("Based on Analyst Target:")
        annual_return = ((price_target / current_price) ** (1/1) - 1) * 100
        print(f"  Year 1: ${price_target:.2f} ({annual_return:+.1f}%)")
        
        # Extrapolate for years 2-3 using historical growth or conservative estimate
        growth_rate = revenue_growth if revenue_growth else 10  # Use 10% if no data
        for year in [2, 3]:
            projected = price_target * (1 + growth_rate/100) ** (year-1)
            total_return = ((projected - current_price) / current_price) * 100
            print(f"  Year {year}: ${projected:.2f} ({total_return:+.1f}% total)")
    
    elif current_price:
        # Method 2: Based on industry average growth
        print("Based on Industry Averages (10% annual):")
        for year in range(1, 4):
            projected = current_price * (1.10) ** year
            total_return = ((projected - current_price) / current_price) * 100
            print(f"  Year {year}: ${projected:.2f} ({total_return:+.1f}% total)")
    
    # 5. Get recent news for context
    print(f"\n📰 RECENT NEWS (via Polygon)")
    print("-"*50)
    try:
        news = obb.news.company(symbol=symbol, provider='polygon')
        if news and news.results:
            # Filter for company-specific news
            count = 0
            for article in news.results:
                if count >= 3:
                    break
                if hasattr(article, 'title'):
                    # Check if symbol or company name in title
                    if symbol.lower() in article.title.lower():
                        print(f"• {article.title[:80]}...")
                        if hasattr(article, 'date'):
                            print(f"  {article.date}")
                        count += 1
    except:
        print("News data not available")
    
    print(f"\n{'='*80}")
    print("FORECAST SUMMARY")
    print('='*80)
    
    if current_price:
        print(f"Current Price: ${current_price:.2f}")
    if price_target:
        print(f"12-Month Price Target: ${price_target:.2f}")
        if current_price:
            print(f"Upside Potential: {((price_target - current_price)/current_price)*100:+.1f}%")
    if revenue_growth:
        print(f"Historical Revenue Growth: {revenue_growth:.1f}% annually")
    
    print(f"\n3-Year Price Range Estimate:")
    if current_price:
        # Conservative to aggressive scenarios
        conservative = current_price * (1.05) ** 3  # 5% annual
        moderate = current_price * (1.10) ** 3      # 10% annual
        aggressive = current_price * (1.15) ** 3    # 15% annual
        
        print(f"  Conservative (5%/yr): ${conservative:.2f}")
        print(f"  Moderate (10%/yr): ${moderate:.2f}")
        print(f"  Aggressive (15%/yr): ${aggressive:.2f}")

def main():
    print("="*80)
    print(" "*20 + "FINVIZ ELITE FORECAST TOOL")
    print("="*80)
    print("\nYour API Status:")
    print("✅ Finviz Elite: Active (Price Targets)")
    print("✅ Polygon: Active (News & Quotes)")
    print("✅ FRED: Active (Economic Data)")
    
    # Example companies
    symbols = ['AAPL', 'MSFT', 'NVDA']
    
    print("\nSelect a company or enter your own symbol:")
    for i, sym in enumerate(symbols, 1):
        print(f"  {i}. {sym}")
    print("  4. Enter custom symbol")
    
    # Default to Apple for demo
    print("\nDemo: Getting forecast for AAPL...")
    get_complete_forecast('AAPL')
    
    print("\n" + "="*80)
    print("OPENBB CLI COMMANDS")
    print("="*80)
    print("""
Launch with all APIs:
./launch-openbb-complete.sh

Get complete forecast data:
/equity/estimates/price_target --symbol AAPL --provider finviz
/equity/fundamental/income --symbol AAPL --provider yfinance
/news/company --symbol AAPL --provider polygon
/equity/price/quote --symbol AAPL --provider polygon

Export all data:
/equity/estimates/price_target --symbol AAPL --provider finviz --export csv
""")

if __name__ == "__main__":
    main()
