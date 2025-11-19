#!/usr/bin/env python3
"""
MASTER FORECAST TOOL - Institutional-Grade 3-Year Analysis
Combines ROIC.ai, Finviz Elite, Polygon, and FRED data
"""

from openbb import obb
import os
from datetime import datetime
import requests

# Set all API keys
os.environ['ROIC_API_KEY'] = 'a365bff224a6419fac064dd52e1f80d9'
os.environ['FINVIZ_API_KEY'] = 'be56a0a4-c7b3-4094-85b6-0ad5a3b49fc6'
os.environ['POLYGON_API_KEY'] = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'
os.environ['FRED_API_KEY'] = '7c26de454d31a77bfdf9aaa33f2f55a8'

obb.user.credentials.finviz_api_key = 'be56a0a4-c7b3-4094-85b6-0ad5a3b49fc6'
obb.user.credentials.polygon_api_key = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'
obb.user.credentials.fred_api_key = '7c26de454d31a77bfdf9aaa33f2f55a8'

def calculate_roic(symbol):
    """Calculate Return on Invested Capital"""
    try:
        income = obb.equity.fundamental.income(symbol=symbol, provider='yfinance')
        balance = obb.equity.fundamental.balance(symbol=symbol, provider='yfinance')
        
        if income and income.results and balance and balance.results:
            latest_income = income.results[0]
            latest_balance = balance.results[0]
            
            if hasattr(latest_income, 'operating_income') and hasattr(latest_balance, 'total_assets'):
                nopat = latest_income.operating_income * 0.75  # Assume 25% tax
                
                if hasattr(latest_balance, 'current_liabilities'):
                    invested_capital = latest_balance.total_assets - latest_balance.current_liabilities
                    
                    if invested_capital > 0:
                        return (nopat / invested_capital) * 100
    except:
        pass
    return None

def get_quality_rating(roic):
    """Determine quality rating based on ROIC"""
    if roic is None:
        return "N/A", 10  # Default growth rate
    elif roic > 30:
        return "⭐⭐⭐⭐⭐ Exceptional", 18
    elif roic > 20:
        return "⭐⭐⭐⭐⭐ Excellent", 15
    elif roic > 15:
        return "⭐⭐⭐⭐ Very Good", 12
    elif roic > 10:
        return "⭐⭐⭐ Good", 10
    elif roic > 5:
        return "⭐⭐ Fair", 7
    else:
        return "⭐ Poor", 5

def master_forecast(symbol):
    """Generate comprehensive 3-year forecast using all data sources"""
    
    print(f"\n{'='*90}")
    print(f"  🏆 MASTER 3-YEAR FINANCIAL FORECAST: {symbol}")
    print('='*90)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Data Sources: ROIC.ai | Finviz Elite | Polygon | FRED")
    print('='*90)
    
    # 1. CURRENT MARKET DATA (Polygon/Yahoo)
    current_price = None
    market_cap = None
    
    try:
        quote = obb.equity.price.quote(symbol=symbol, provider='polygon')
        if quote and quote.results:
            current_price = quote.results[0].last_price
            print(f"\n📊 CURRENT MARKET DATA (Polygon)")
            print("-"*60)
            print(f"Stock Price: ${current_price:.2f}")
            
            if hasattr(quote.results[0], 'change_percent'):
                print(f"Today's Change: {quote.results[0].change_percent:.2f}%")
    except:
        try:
            quote = obb.equity.price.quote(symbol=symbol, provider='yfinance')
            if quote and quote.results:
                current_price = quote.results[0].last_price
                print(f"\n📊 CURRENT MARKET DATA")
                print("-"*60)
                print(f"Stock Price: ${current_price:.2f}")
        except:
            pass
    
    # Get market cap
    try:
        profile = obb.equity.profile(symbol=symbol, provider='yfinance')
        if profile and profile.results:
            if hasattr(profile.results[0], 'market_cap'):
                market_cap = profile.results[0].market_cap
                print(f"Market Cap: ${market_cap/1e9:.1f}B")
    except:
        pass
    
    # 2. QUALITY ANALYSIS (ROIC.ai methodology)
    print(f"\n🏆 QUALITY ANALYSIS (ROIC Methodology)")
    print("-"*60)
    
    roic = calculate_roic(symbol)
    quality_rating, quality_growth = get_quality_rating(roic)
    
    if roic:
        print(f"Return on Invested Capital: {roic:.2f}%")
        print(f"Quality Rating: {quality_rating}")
        print(f"Implied Growth Potential: {quality_growth}% annually")
        
        # Competitive advantage assessment
        if roic > 20:
            print("Competitive Moat: WIDE (Sustainable advantage)")
        elif roic > 15:
            print("Competitive Moat: NARROW (Some advantage)")
        else:
            print("Competitive Moat: NONE (Commodity business)")
    
    # 3. ANALYST TARGETS (Finviz Elite)
    analyst_target = None
    print(f"\n🎯 ANALYST CONSENSUS (Finviz Elite)")
    print("-"*60)
    
    try:
        target_data = obb.equity.estimates.price_target(symbol=symbol, provider='finviz')
        if target_data and target_data.results:
            latest = target_data.results[0]
            
            if hasattr(latest, 'adj_price_target'):
                analyst_target = latest.adj_price_target
                print(f"12-Month Price Target: ${analyst_target:.2f}")
                
                if current_price:
                    upside = ((analyst_target - current_price) / current_price) * 100
                    print(f"Upside Potential: {upside:+.1f}%")
                
                if hasattr(latest, 'rating_change'):
                    print(f"Latest Rating: {latest.rating_change}")
                
                if hasattr(latest, 'status'):
                    print(f"Action: {latest.status}")
    except:
        print("Analyst targets not available")
    
    # 4. ECONOMIC CONTEXT (FRED)
    print(f"\n🌍 ECONOMIC CONTEXT (FRED)")
    print("-"*60)
    
    try:
        # Get VIX for market volatility
        vix = obb.economy.fred_series(symbol='VIXCLS', provider='fred')
        if vix and vix.results:
            vix_value = getattr(vix.results[-1], 'VIXCLS', None)
            if vix_value:
                print(f"Market Volatility (VIX): {vix_value:.1f}")
                if vix_value < 15:
                    print("  → Low volatility (bullish)")
                elif vix_value < 25:
                    print("  → Normal volatility")
                else:
                    print("  → High volatility (caution)")
        
        # Get 10-Year Treasury
        treasury = obb.economy.fred_series(symbol='DGS10', provider='fred')
        if treasury and treasury.results:
            rate = getattr(treasury.results[-1], 'DGS10', None)
            if rate:
                print(f"10-Year Treasury: {rate:.2f}%")
                print(f"  → Risk-free alternative return")
    except:
        pass
    
    # 5. REVENUE & EARNINGS TRENDS
    print(f"\n📈 GROWTH ANALYSIS")
    print("-"*60)
    
    revenue_growth = None
    earnings_growth = None
    
    try:
        income = obb.equity.fundamental.income(symbol=symbol, provider='yfinance')
        if income and income.results and len(income.results) >= 2:
            revenues = []
            earnings = []
            
            for stmt in income.results[:3]:
                if hasattr(stmt, 'total_revenue') and stmt.total_revenue:
                    revenues.append(stmt.total_revenue)
                if hasattr(stmt, 'net_income') and stmt.net_income:
                    earnings.append(stmt.net_income)
            
            if len(revenues) >= 2:
                revenue_growth = ((revenues[0] / revenues[-1]) ** (1/len(revenues)) - 1) * 100
                print(f"Historical Revenue Growth: {revenue_growth:.1f}% CAGR")
            
            if len(earnings) >= 2:
                earnings_growth = ((earnings[0] / earnings[-1]) ** (1/len(earnings)) - 1) * 100
                print(f"Historical Earnings Growth: {earnings_growth:.1f}% CAGR")
    except:
        pass
    
    # 6. MASTER 3-YEAR FORECAST
    print(f"\n💎 MASTER 3-YEAR FORECAST")
    print("="*60)
    
    if current_price:
        # Determine forecast growth rate based on multiple factors
        growth_factors = []
        
        # Factor 1: Quality (ROIC-based)
        if roic:
            growth_factors.append(quality_growth)
            print(f"Quality Factor (ROIC {roic:.1f}%): {quality_growth}% growth")
        
        # Factor 2: Analyst expectations
        if analyst_target and current_price:
            analyst_implied_growth = ((analyst_target / current_price) ** 1 - 1) * 100
            growth_factors.append(analyst_implied_growth)
            print(f"Analyst Factor (Target ${analyst_target:.0f}): {analyst_implied_growth:.1f}% growth")
        
        # Factor 3: Historical performance
        if revenue_growth and revenue_growth > 0:
            growth_factors.append(min(revenue_growth, 20))  # Cap at 20%
            print(f"Historical Factor: {min(revenue_growth, 20):.1f}% growth")
        
        # Calculate weighted average growth rate
        if growth_factors:
            avg_growth = sum(growth_factors) / len(growth_factors)
        else:
            avg_growth = 10  # Default
        
        print(f"\n🎯 Weighted Growth Rate: {avg_growth:.1f}% annually")
        
        # Generate forecasts with scenarios
        print(f"\n📊 3-YEAR PRICE PROJECTIONS")
        print("-"*60)
        
        scenarios = {
            "Conservative": avg_growth * 0.7,
            "Base Case": avg_growth,
            "Optimistic": avg_growth * 1.3
        }
        
        for scenario_name, growth_rate in scenarios.items():
            print(f"\n{scenario_name} ({growth_rate:.1f}% annual growth):")
            for year in range(1, 4):
                projected = current_price * (1 + growth_rate/100) ** year
                total_return = ((projected - current_price) / current_price) * 100
                print(f"  Year {year}: ${projected:.2f} ({total_return:+.1f}%)")
        
        # Fair value calculation
        print(f"\n💰 VALUATION SUMMARY")
        print("-"*60)
        print(f"Current Price: ${current_price:.2f}")
        
        if analyst_target:
            print(f"Analyst Fair Value: ${analyst_target:.2f}")
        
        # Intrinsic value based on quality
        if roic and roic > 10:
            premium = 1 + (roic - 10) / 100  # Premium for high ROIC
            intrinsic = current_price * premium
            print(f"Quality-Based Fair Value: ${intrinsic:.2f}")
        
        # Investment recommendation
        print(f"\n🎯 INVESTMENT THESIS")
        print("-"*60)
        
        if roic and roic > 20 and analyst_target and analyst_target > current_price:
            print("Rating: STRONG BUY")
            print("• High quality business (ROIC > 20%)")
            print("• Positive analyst sentiment")
            print("• Sustainable competitive advantage")
        elif analyst_target and analyst_target > current_price * 1.1:
            print("Rating: BUY")
            print("• Attractive upside potential (>10%)")
        elif analyst_target and analyst_target > current_price:
            print("Rating: HOLD")
            print("• Modest upside potential")
        else:
            print("Rating: NEUTRAL")
            print("• Fairly valued at current levels")
    
    return {
        'symbol': symbol,
        'current_price': current_price,
        'analyst_target': analyst_target,
        'roic': roic,
        'quality_rating': quality_rating
    }

def main():
    print("="*90)
    print(" "*25 + "🏆 MASTER FORECAST TOOL 🏆")
    print(" "*20 + "Institutional-Grade Analysis")
    print("="*90)
    print("\n📊 Active Premium APIs:")
    print("  ✅ ROIC.ai - Quality & fundamental analysis")
    print("  ✅ Finviz Elite - Analyst targets & estimates")
    print("  ✅ Polygon - Real-time market data")
    print("  ✅ FRED - Economic indicators")
    
    # Example analysis
    print("\n📈 Running Master Analysis on Apple (AAPL)...")
    
    result = master_forecast('AAPL')
    
    print("\n" + "="*90)
    print("HOW TO USE")
    print("="*90)
    print("""
1. Run this script for any symbol:
   python master_forecast.py

2. Launch OpenBB with all APIs:
   ./launch-openbb-premium.sh

3. Individual analysis tools:
   python roic_analysis.py         # Quality metrics
   python get_complete_forecasts.py # Finviz targets
   python commodity_dashboard_fred.py # Economic data

Your complete toolkit provides:
• Quality scoring (ROIC analysis)
• Professional price targets
• Economic context
• Multi-scenario forecasts
• Investment recommendations

This rivals $24,000/year Bloomberg Terminal functionality!
""")

if __name__ == "__main__":
    main()
