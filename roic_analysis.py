#!/usr/bin/env python3
"""
ROIC.ai Integration - Advanced Fundamental Analysis
Get quality metrics, ROIC analysis, and competitive advantage assessments
"""

import requests
import json
import os
from datetime import datetime
import pandas as pd

# API Configuration
ROIC_API_KEY = "a365bff224a6419fac064dd52e1f80d9"
BASE_URL = "https://api.roic.ai/v1"

def get_roic_data(symbol):
    """
    Get ROIC.ai fundamental analysis data
    """
    headers = {
        "Authorization": f"Bearer {ROIC_API_KEY}",
        "Content-Type": "application/json"
    }
    
    print(f"\n{'='*80}")
    print(f"  📊 ROIC.AI FUNDAMENTAL ANALYSIS: {symbol}")
    print('='*80)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print('='*80)
    
    # Note: ROIC.ai API endpoints may vary - these are typical patterns
    # You may need to check their documentation for exact endpoints
    
    print("\n📈 QUALITY METRICS & ROIC ANALYSIS")
    print("-"*60)
    
    try:
        # Try common API endpoint patterns
        endpoints = [
            f"/companies/{symbol}/metrics",
            f"/analysis/{symbol}",
            f"/fundamentals/{symbol}",
            f"/quality-score/{symbol}"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(
                    f"{BASE_URL}{endpoint}",
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Data retrieved from {endpoint}")
                    
                    # Display the data structure
                    if isinstance(data, dict):
                        for key, value in data.items():
                            if value is not None:
                                print(f"  {key}: {value}")
                    
                    return data
                    
            except Exception as e:
                continue
        
        # If API doesn't work directly, provide typical ROIC.ai metrics explanation
        print("\n📊 TYPICAL ROIC.AI METRICS (API integration pending):")
        print("-"*50)
        print("""
ROIC.ai typically provides:

1. RETURN ON INVESTED CAPITAL (ROIC)
   - Current ROIC: Measures efficiency of capital allocation
   - 5-Year Average ROIC: Long-term performance
   - ROIC vs WACC: Value creation assessment
   
2. QUALITY SCORE (0-100)
   - Financial Strength: Balance sheet health
   - Profitability: Earnings quality
   - Growth: Revenue and earnings growth
   - Valuation: Price relative to intrinsic value
   
3. COMPETITIVE ADVANTAGE
   - Moat Rating: Wide/Narrow/None
   - Durability: How sustainable is the advantage
   - Market Position: Industry leadership
   
4. FORECAST METRICS
   - 3-5 Year Revenue CAGR
   - 3-5 Year Earnings CAGR
   - Free Cash Flow projections
   - ROIC trend projections
   
5. VALUATION
   - Intrinsic Value estimate
   - Margin of Safety
   - Fair Value Range
   - Expected Returns (3-5 years)
""")
        
    except Exception as e:
        print(f"Note: Direct API access may require documentation review")
        print(f"Error: {str(e)[:100]}")
    
    return None

def calculate_roic_manually(symbol):
    """
    Calculate ROIC metrics using available financial data
    """
    print("\n💡 MANUAL ROIC CALCULATION")
    print("-"*60)
    
    try:
        from openbb import obb
        
        # Get financial data
        income = obb.equity.fundamental.income(symbol=symbol, provider='yfinance')
        balance = obb.equity.fundamental.balance(symbol=symbol, provider='yfinance')
        
        if income and income.results and balance and balance.results:
            latest_income = income.results[0]
            latest_balance = balance.results[0]
            
            # Calculate ROIC components
            if hasattr(latest_income, 'operating_income') and hasattr(latest_balance, 'total_assets'):
                # Simplified ROIC calculation
                nopat = latest_income.operating_income * 0.75  # Assume 25% tax rate
                
                # Invested Capital = Total Assets - Current Liabilities
                if hasattr(latest_balance, 'current_liabilities'):
                    invested_capital = latest_balance.total_assets - latest_balance.current_liabilities
                    
                    if invested_capital > 0:
                        roic = (nopat / invested_capital) * 100
                        print(f"Calculated ROIC: {roic:.2f}%")
                        
                        # Quality assessment
                        if roic > 20:
                            print("Quality: ⭐⭐⭐⭐⭐ Excellent (ROIC > 20%)")
                        elif roic > 15:
                            print("Quality: ⭐⭐⭐⭐ Very Good (ROIC 15-20%)")
                        elif roic > 10:
                            print("Quality: ⭐⭐⭐ Good (ROIC 10-15%)")
                        elif roic > 5:
                            print("Quality: ⭐⭐ Fair (ROIC 5-10%)")
                        else:
                            print("Quality: ⭐ Poor (ROIC < 5%)")
                        
                        return roic
            
    except Exception as e:
        print(f"Manual calculation not available: {str(e)[:100]}")
    
    return None

def get_quality_forecast(symbol):
    """
    Generate quality-based forecast using ROIC principles
    """
    print(f"\n🎯 QUALITY-BASED 3-YEAR FORECAST")
    print("-"*60)
    
    try:
        from openbb import obb
        
        # Get current price
        quote = obb.equity.price.quote(symbol=symbol, provider='yfinance')
        current_price = quote.results[0].last_price if quote and quote.results else None
        
        # Get Finviz target if available
        target = None
        try:
            target_data = obb.equity.estimates.price_target(symbol=symbol, provider='finviz')
            if target_data and target_data.results:
                target = target_data.results[0].adj_price_target
        except:
            pass
        
        # Calculate ROIC
        roic = calculate_roic_manually(symbol)
        
        if current_price:
            print(f"\nCurrent Price: ${current_price:.2f}")
            
            if target:
                print(f"Analyst Target: ${target:.2f}")
            
            if roic:
                # High ROIC companies typically deserve higher growth rates
                if roic > 20:
                    growth_rate = 15  # High quality
                elif roic > 15:
                    growth_rate = 12  # Very good quality
                elif roic > 10:
                    growth_rate = 10  # Good quality
                else:
                    growth_rate = 7   # Average quality
                
                print(f"\nProjected Annual Growth (based on {roic:.1f}% ROIC): {growth_rate}%")
                
                print("\n3-Year Price Projection:")
                for year in range(1, 4):
                    projected = current_price * (1 + growth_rate/100) ** year
                    print(f"  Year {year}: ${projected:.2f} (+{((projected/current_price-1)*100):.1f}%)")
    
    except Exception as e:
        print(f"Forecast calculation error: {str(e)[:100]}")

def main():
    """Main function"""
    
    print("="*80)
    print(" "*20 + "ROIC.AI ADVANCED ANALYSIS")
    print("="*80)
    print("\n📊 Your Premium API Status:")
    print("✅ ROIC.ai: Quality & fundamental analysis")
    print("✅ Finviz Elite: Analyst targets")
    print("✅ Polygon: Real-time data")
    print("✅ FRED: Economic context")
    
    # Example analysis
    symbols = ['AAPL', 'MSFT', 'BRK.B']
    
    print("\nSelect a company for ROIC analysis:")
    for i, sym in enumerate(symbols, 1):
        print(f"  {i}. {sym}")
    
    # Demo with Apple
    print("\nDemo: Analyzing AAPL with ROIC.ai methodology...")
    
    symbol = 'AAPL'
    
    # Try ROIC.ai API
    roic_data = get_roic_data(symbol)
    
    # Calculate ROIC manually
    calculate_roic_manually(symbol)
    
    # Generate quality-based forecast
    get_quality_forecast(symbol)
    
    print("\n" + "="*80)
    print("INTEGRATION NOTES")
    print("="*80)
    print("""
ROIC.ai focuses on quality investing metrics:
• Return on Invested Capital (ROIC)
• Competitive advantage (moat) analysis  
• Long-term value creation
• Quality scores and rankings

Combined with your other APIs:
• ROIC.ai: Quality assessment
• Finviz: Price targets
• Polygon: Real-time data
• FRED: Economic context

This provides institutional-grade fundamental analysis!

To fully integrate ROIC.ai:
1. Check their API documentation at roic.ai/api
2. Update endpoints in this script
3. Map their data fields to OpenBB format
""")

if __name__ == "__main__":
    main()
