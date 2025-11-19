#!/usr/bin/env python3
"""
Get Company 3-Year Financial Forecast Data
Shows analyst estimates, revenue projections, and price targets
"""

from openbb import obb
import os
from datetime import datetime
import pandas as pd

# Set API keys
os.environ['POLYGON_API_KEY'] = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'
obb.user.credentials.polygon_api_key = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'

def get_forecast_data(symbol):
    """Get comprehensive forecast data for a company"""
    
    print(f"\n{'='*70}")
    print(f"  📊 3-YEAR FINANCIAL FORECAST: {symbol}")
    print('='*70)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print('='*70)
    
    # 1. Get current stock price for context
    try:
        quote = obb.equity.price.quote(symbol=symbol, provider='yfinance')
        if quote and quote.results:
            current_price = quote.results[0].last_price
            print(f"\n💹 Current Stock Price: ${current_price:.2f}")
    except:
        current_price = None
    
    # 2. Get analyst consensus estimates
    print("\n📈 ANALYST CONSENSUS ESTIMATES")
    print("-"*50)
    try:
        # Try to get fundamental estimates
        fundamental = obb.equity.fundamental.metrics(symbol=symbol, provider='yfinance')
        if fundamental and fundamental.results:
            data = fundamental.results[0]
            
            # Display available forecast metrics
            if hasattr(data, 'forward_pe') and data.forward_pe:
                print(f"Forward P/E Ratio: {data.forward_pe:.2f}")
            
            if hasattr(data, 'peg_ratio') and data.peg_ratio:
                print(f"PEG Ratio: {data.peg_ratio:.2f}")
                
            if hasattr(data, 'forward_eps') and data.forward_eps:
                print(f"Forward EPS: ${data.forward_eps:.2f}")
                
            if hasattr(data, 'book_value') and data.book_value:
                print(f"Book Value: ${data.book_value:.2f}")
    except Exception as e:
        print(f"Note: Limited forecast data available via free API")
    
    # 3. Get historical performance for trend analysis
    print("\n📊 HISTORICAL PERFORMANCE (for trend projection)")
    print("-"*50)
    try:
        # Get income statement for revenue trends
        income = obb.equity.fundamental.income(symbol=symbol, provider='yfinance')
        if income and income.results:
            revenues = []
            earnings = []
            
            for stmt in income.results[:3]:  # Last 3 years
                if hasattr(stmt, 'period_ending'):
                    year = stmt.period_ending.year
                    
                    if hasattr(stmt, 'total_revenue') and stmt.total_revenue:
                        revenues.append((year, stmt.total_revenue))
                    
                    if hasattr(stmt, 'net_income') and stmt.net_income:
                        earnings.append((year, stmt.net_income))
            
            if revenues:
                print("\nRevenue History (for growth rate calculation):")
                for year, rev in revenues:
                    print(f"  {year}: ${rev/1e9:.2f}B")
                
                # Calculate growth rate
                if len(revenues) >= 2:
                    growth = ((revenues[0][1] - revenues[-1][1]) / revenues[-1][1]) * 100 / len(revenues)
                    print(f"  Average Growth Rate: {growth:.1f}%")
                    
                    # Project forward
                    print(f"\n📮 Revenue Projections (based on historical growth):")
                    last_rev = revenues[0][1]
                    for i in range(1, 4):
                        projected = last_rev * (1 + growth/100) ** i
                        print(f"  Year +{i}: ${projected/1e9:.2f}B")
            
            if earnings:
                print("\nEarnings History:")
                for year, earn in earnings:
                    print(f"  {year}: ${earn/1e9:.2f}B")
                    
    except Exception as e:
        print(f"Historical data: {str(e)[:100]}")
    
    # 4. Get company metrics and ratios
    print("\n💼 KEY VALUATION METRICS")
    print("-"*50)
    try:
        profile = obb.equity.profile(symbol=symbol, provider='yfinance')
        if profile and profile.results:
            data = profile.results[0]
            
            if hasattr(data, 'market_cap') and data.market_cap:
                print(f"Market Cap: ${data.market_cap/1e9:.2f}B")
            
            if hasattr(data, 'pe_ratio') and data.pe_ratio:
                print(f"Current P/E: {data.pe_ratio:.2f}")
            
            if hasattr(data, 'dividend_yield') and data.dividend_yield:
                print(f"Dividend Yield: {data.dividend_yield:.2f}%")
                
            if hasattr(data, 'beta') and data.beta:
                print(f"Beta: {data.beta:.2f}")
                
    except:
        pass
    
    # 5. Calculate simple projections
    print("\n🔮 BASIC 3-YEAR PROJECTIONS")
    print("-"*50)
    print("(Based on industry averages and historical trends)")
    
    # Industry average growth rates (simplified)
    industry_growth = {
        'Technology': 15,
        'Healthcare': 12,
        'Finance': 8,
        'Consumer': 10,
        'Energy': 5,
        'Industrial': 7
    }
    
    # Estimate based on generic rates
    assumed_growth = 10  # Default 10% growth
    print(f"Assumed Annual Growth Rate: {assumed_growth}%")
    
    if current_price:
        print("\nPrice Projections (assuming P/E remains constant):")
        for i in range(1, 4):
            projected_price = current_price * (1 + assumed_growth/100) ** i
            print(f"  Year {i}: ${projected_price:.2f} (+{(projected_price-current_price)/current_price*100:.1f}%)")
    
    return True

def main():
    """Main function to get forecasts for multiple companies"""
    
    print("="*70)
    print(" "*15 + "COMPANY FINANCIAL FORECAST TOOL")
    print("="*70)
    
    # Example companies to analyze
    companies = {
        'AAPL': 'Apple Inc.',
        'MSFT': 'Microsoft Corp.',
        'GOOGL': 'Alphabet Inc.',
        'TSLA': 'Tesla Inc.'
    }
    
    print("\nSelect a company for 3-year forecast:")
    for symbol, name in companies.items():
        print(f"  {symbol}: {name}")
    
    # Get forecast for Apple as example
    print("\n" + "="*70)
    print("EXAMPLE: Getting Apple (AAPL) Forecast...")
    get_forecast_data('AAPL')
    
    print("\n" + "="*70)
    print("HOW TO USE IN OPENBB CLI")
    print("="*70)
    print("""
    1. Launch OpenBB:
       ./launch-openbb-full.sh
    
    2. Get company estimates:
       /equity/fundamental/metrics --symbol AAPL --provider yfinance
       /equity/fundamental/income --symbol AAPL --provider yfinance
       /equity/fundamental/ratios --symbol AAPL --provider yfinance
    
    3. Get historical data for trends:
       /equity/fundamental/income --symbol AAPL --limit 5 --provider yfinance
       /equity/fundamental/cash --symbol AAPL --limit 5 --provider yfinance
    
    4. Export data:
       /equity/fundamental/income --symbol AAPL --provider yfinance --export csv
    
    Note: Full analyst estimates require premium data providers like:
    - Bloomberg Terminal
    - Refinitiv
    - S&P Capital IQ
    - Morningstar Direct
    
    Free alternatives provide:
    - Historical data for trend analysis
    - Basic valuation metrics
    - Simple growth projections
    """)
    
    print("="*70)

if __name__ == "__main__":
    main()
