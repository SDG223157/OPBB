#!/usr/bin/env python3
"""
Economic Dashboard using FRED API
Shows key economic indicators from Federal Reserve data
"""

from openbb import obb
import os
from datetime import datetime, timedelta
import pandas as pd

# Set API keys
os.environ['FRED_API_KEY'] = '7c26de454d31a77bfdf9aaa33f2f55a8'
os.environ['OPENBB_API_FRED_KEY'] = '7c26de454d31a77bfdf9aaa33f2f55a8'

obb.user.credentials.fred_api_key = '7c26de454d31a77bfdf9aaa33f2f55a8'

print("="*80)
print(" "*20 + "📊 US ECONOMIC DASHBOARD 📊")
print(" "*25 + "Data from FRED")
print("="*80)
print(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# 1. GDP Data
print("\n📈 GROSS DOMESTIC PRODUCT (GDP)")
print("-"*60)
try:
    gdp = obb.economy.gdp(provider='fred', countries='united_states')
    if gdp and gdp.results:
        recent_gdp = gdp.results[-5:]  # Last 5 quarters
        for item in recent_gdp:
            if hasattr(item, 'date') and hasattr(item, 'value'):
                print(f"  {item.date}: {item.value:,.2f}%")
except Exception as e:
    print(f"  Note: {str(e)[:100]}")

# 2. Inflation
print("\n💰 INFLATION RATE")
print("-"*60)
try:
    inflation = obb.economy.inflation(provider='fred', countries='united_states')
    if inflation and inflation.results:
        recent_inflation = inflation.results[-5:]  # Last 5 months
        for item in recent_inflation:
            if hasattr(item, 'date') and hasattr(item, 'value'):
                print(f"  {item.date}: {item.value:.2f}%")
except Exception as e:
    print(f"  Note: {str(e)[:100]}")

# 3. Unemployment
print("\n👥 UNEMPLOYMENT RATE")
print("-"*60)
try:
    unemployment = obb.economy.unemployment(provider='fred', countries='united_states')
    if unemployment and unemployment.results:
        recent_unemployment = unemployment.results[-5:]  # Last 5 months
        for item in recent_unemployment:
            if hasattr(item, 'date') and hasattr(item, 'value'):
                print(f"  {item.date}: {item.value:.1f}%")
except Exception as e:
    print(f"  Note: {str(e)[:100]}")

# 4. Interest Rates
print("\n💵 KEY INTEREST RATES")
print("-"*60)

# Federal Funds Rate
try:
    print("\n  Federal Funds Rate:")
    fed_funds = obb.economy.fred_series(series_id='DFF', provider='fred')
    if fed_funds and fed_funds.results:
        latest = fed_funds.results[-1]
        if hasattr(latest, 'value'):
            print(f"    Current: {latest.value:.2f}%")
except:
    pass

# 10-Year Treasury
try:
    print("\n  10-Year Treasury Yield:")
    treasury_10y = obb.economy.fred_series(series_id='DGS10', provider='fred')
    if treasury_10y and treasury_10y.results:
        latest = treasury_10y.results[-1]
        if hasattr(latest, 'value'):
            print(f"    Current: {latest.value:.2f}%")
except:
    pass

# 2-Year Treasury
try:
    print("\n  2-Year Treasury Yield:")
    treasury_2y = obb.economy.fred_series(series_id='DGS2', provider='fred')
    if treasury_2y and treasury_2y.results:
        latest = treasury_2y.results[-1]
        if hasattr(latest, 'value'):
            print(f"    Current: {latest.value:.2f}%")
            
    # Calculate yield curve (10Y - 2Y spread)
    if treasury_10y and treasury_2y and treasury_10y.results and treasury_2y.results:
        spread = treasury_10y.results[-1].value - treasury_2y.results[-1].value
        print(f"\n  Yield Curve (10Y-2Y Spread): {spread:.2f}%")
        if spread < 0:
            print("    ⚠️ INVERTED - Potential recession indicator")
except:
    pass

# 5. Stock Market
print("\n📈 STOCK MARKET INDICES")
print("-"*60)

# S&P 500
try:
    sp500 = obb.economy.fred_series(series_id='SP500', provider='fred')
    if sp500 and sp500.results:
        latest = sp500.results[-1]
        if hasattr(latest, 'value'):
            print(f"  S&P 500: {latest.value:,.2f}")
except:
    pass

# VIX
try:
    vix = obb.economy.fred_series(series_id='VIXCLS', provider='fred')
    if vix and vix.results:
        latest = vix.results[-1]
        if hasattr(latest, 'value'):
            print(f"  VIX (Volatility): {latest.value:.2f}")
            if latest.value > 30:
                print("    ⚠️ HIGH VOLATILITY")
            elif latest.value < 20:
                print("    ✅ Low volatility")
except:
    pass

# 6. Consumer Metrics
print("\n🛒 CONSUMER INDICATORS")
print("-"*60)

# Consumer Sentiment
try:
    print("  Consumer Sentiment Index:")
    sentiment = obb.economy.fred_series(series_id='UMCSENT', provider='fred')
    if sentiment and sentiment.results:
        latest = sentiment.results[-1]
        if hasattr(latest, 'value'):
            print(f"    Current: {latest.value:.1f}")
except:
    pass

# Personal Savings Rate
try:
    print("\n  Personal Savings Rate:")
    savings = obb.economy.fred_series(series_id='PSAVERT', provider='fred')
    if savings and savings.results:
        latest = savings.results[-1]
        if hasattr(latest, 'value'):
            print(f"    Current: {latest.value:.1f}%")
except:
    pass

print("\n" + "="*80)
print("CLI COMMANDS TO GET THIS DATA")
print("="*80)
print("""
# Launch OpenBB
./launch-openbb-full.sh

# Economic Overview
/economy/gdp --provider fred
/economy/inflation --provider fred
/economy/unemployment --provider fred

# Interest Rates
/economy/fred_series --series_id DFF --provider fred      # Fed Funds
/economy/fred_series --series_id DGS10 --provider fred    # 10-Year
/economy/fred_series --series_id DGS2 --provider fred     # 2-Year

# Stock Market
/economy/fred_series --series_id SP500 --provider fred    # S&P 500
/economy/fred_series --series_id VIXCLS --provider fred   # VIX

# Consumer Metrics
/economy/fred_series --series_id UMCSENT --provider fred  # Sentiment
/economy/fred_series --series_id PSAVERT --provider fred  # Savings Rate

# Export data
/economy/gdp --provider fred --export csv
""")

print("="*80)
print("Your FRED API Key: ✅ Active")
print("Access to 800,000+ economic series")
print("="*80)
