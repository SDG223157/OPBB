#!/usr/bin/env python3
"""
Test and demonstrate commodity market data access in OpenBB
"""

from openbb import obb
import pandas as pd
from datetime import datetime
import os

# Set up API key for Polygon (if needed for some commodity data)
os.environ['POLYGON_API_KEY'] = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'
obb.user.credentials.polygon_api_key = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'

print("="*80)
print(" "*20 + "COMMODITY MARKET DATA - OPENBB")
print("="*80)
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# 1. Get commodity spot prices
print("\n📊 COMMODITY SPOT PRICES")
print("-"*60)
try:
    # Try different providers for commodity data
    providers = ['yfinance', 'fred', 'us_eia']
    
    for provider in providers:
        print(f"\nTrying provider: {provider}")
        try:
            spot_prices = obb.commodity.price.spot(provider=provider)
            if spot_prices and spot_prices.results:
                print(f"✅ Success with {provider}!")
                df = pd.DataFrame([d.model_dump() for d in spot_prices.results[:10]])
                print(df.to_string())
                break
        except Exception as e:
            print(f"  ❌ {provider}: {str(e)[:100]}")
    
except Exception as e:
    print(f"Error getting spot prices: {e}")

# 2. Get petroleum status report
print("\n⛽ PETROLEUM STATUS REPORT")
print("-"*60)
try:
    petroleum = obb.commodity.petroleum_status_report(provider='us_eia')
    if petroleum and petroleum.results:
        print("✅ Petroleum data retrieved!")
        data = petroleum.results[0]
        # Display key petroleum metrics
        for key, value in data.model_dump().items():
            if value is not None:
                print(f"  {key}: {value}")
                if len(str(key)) > 5:  # Just show first few items
                    break
except Exception as e:
    print(f"Error: {str(e)[:200]}")

# 3. Energy outlook
print("\n🔋 SHORT-TERM ENERGY OUTLOOK")
print("-"*60)
try:
    energy = obb.commodity.short_term_energy_outlook(provider='us_eia')
    if energy and energy.results:
        print("✅ Energy outlook data retrieved!")
        # Show first few data points
        for i, item in enumerate(energy.results[:3]):
            print(f"\n{i+1}. {item}")
except Exception as e:
    print(f"Error: {str(e)[:200]}")

# 4. Try commodity ETFs as proxy
print("\n📈 COMMODITY ETFs (Alternative Data Source)")
print("-"*60)
commodity_etfs = {
    'GLD': 'Gold',
    'SLV': 'Silver', 
    'USO': 'Oil',
    'DBA': 'Agriculture',
    'DBB': 'Base Metals',
    'UNG': 'Natural Gas',
    'CORN': 'Corn',
    'WEAT': 'Wheat',
    'SOYB': 'Soybeans',
    'CPER': 'Copper'
}

print("Getting commodity ETF prices as proxy for commodity prices:\n")
for symbol, name in commodity_etfs.items():
    try:
        quote = obb.equity.price.quote(symbol=symbol, provider='yfinance')
        if quote and quote.results:
            data = quote.results[0]
            print(f"{name:15} ({symbol:5}): ${data.last_price:8.2f}")
            if hasattr(data, 'change_percent') and data.change_percent:
                print(f"{'':15} Change: {data.change_percent:+6.2f}%")
    except:
        pass

print("\n" + "="*80)
print("COMMODITY DATA SOURCES IN OPENBB CLI")
print("="*80)
print("""
Available Commands:
-------------------
/commodity/price/spot              - Get spot prices for commodities
/commodity/petroleum_status_report - EIA petroleum data
/commodity/short_term_energy_outlook - Energy forecasts

Providers:
----------
- yfinance: Free, commodity ETFs
- fred: Federal Reserve data (free)
- us_eia: US Energy Information Admin (free)
- polygon: With API key

Tips:
-----
- Use commodity ETFs for real-time prices (GLD, SLV, USO, etc.)
- EIA data is best for energy commodities
- FRED has historical commodity data
""")
print("="*80)
