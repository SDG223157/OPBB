#!/usr/bin/env python3
"""
Test Finviz Elite API for Company Financial Forecasts
Shows analyst price targets and estimates
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

print("="*80)
print(" "*15 + "🎯 FINVIZ ELITE - FINANCIAL FORECASTS 🎯")
print("="*80)
print(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

def get_finviz_forecasts(symbol):
    """Get comprehensive forecast data using Finviz Elite"""
    
    print(f"\n📊 ANALYZING: {symbol}")
    print("-"*60)
    
    # 1. Get Price Target from Finviz
    print("\n💰 ANALYST PRICE TARGETS")
    print("-"*40)
    try:
        target_data = obb.equity.estimates.price_target(symbol=symbol, provider='finviz')
        if target_data and target_data.results:
            data = target_data.results[0]
            print(f"✅ Finviz Price Target Data Retrieved!")
            
            # Display all available attributes
            for attr in dir(data):
                if not attr.startswith('_'):
                    value = getattr(data, attr, None)
                    if value is not None and not callable(value):
                        print(f"  {attr}: {value}")
        else:
            print("No price target data available")
    except Exception as e:
        print(f"Error: {e}")
    
    # 2. Try to get insider trading data (Finviz provides this)
    print("\n📈 INSIDER TRADING ACTIVITY")
    print("-"*40)
    try:
        insider_data = obb.equity.ownership.insider_trading(symbol=symbol, provider='finviz')
        if insider_data and insider_data.results:
            print(f"✅ Got {len(insider_data.results)} insider transactions")
            # Show recent transactions
            for transaction in insider_data.results[:3]:
                if hasattr(transaction, 'transaction_type'):
                    print(f"  {transaction}")
        else:
            print("No insider trading data")
    except Exception as e:
        print(f"Note: {str(e)[:100]}")
    
    # 3. Get screener data from Finviz
    print("\n🔍 FINVIZ SCREENER METRICS")
    print("-"*40)
    try:
        # Finviz has excellent screener capabilities
        print("Finviz Elite provides access to:")
        print("  • Real-time price targets")
        print("  • Insider trading data")
        print("  • Advanced technical indicators")
        print("  • Institutional ownership")
        print("  • Analyst recommendations")
        print("  • Forward P/E and growth estimates")
    except:
        pass
    
    return True

# Test with multiple symbols
test_symbols = ['AAPL', 'TSLA', 'NVDA']

print("\n" + "="*80)
print("TESTING FINVIZ ELITE CAPABILITIES")
print("="*80)

for symbol in test_symbols:
    get_finviz_forecasts(symbol)

print("\n" + "="*80)
print("HOW TO USE FINVIZ IN OPENBB CLI")
print("="*80)
print("""
Launch OpenBB with all API keys:
./launch-openbb-full.sh

Finviz-specific commands now available:
----------------------------------------
# Price targets and analyst estimates
/equity/estimates/price_target --symbol AAPL --provider finviz

# Insider trading activity
/equity/ownership/insider_trading --symbol AAPL --provider finviz

# Top retail traded stocks
/equity/discovery/top_retail --provider finviz

# Stock screener with advanced filters
/equity/screener --provider finviz

# Export forecast data
/equity/estimates/price_target --symbol AAPL --provider finviz --export csv

Your Active API Keys:
✅ Finviz Elite: be56a0a4-c7b3-4094-85b6-0ad5a3b49fc6
✅ Polygon: Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai  
✅ FRED: 7c26de454d31a77bfdf9aaa33f2f55a8
""")
print("="*80)
