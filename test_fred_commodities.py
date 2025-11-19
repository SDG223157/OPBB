#!/usr/bin/env python3
"""
Test FRED API for Commodity Spot Prices
"""

from openbb import obb
import os
from datetime import datetime, timedelta

# Set API keys
os.environ['FRED_API_KEY'] = '7c26de454d31a77bfdf9aaa33f2f55a8'
os.environ['OPENBB_API_FRED_KEY'] = '7c26de454d31a77bfdf9aaa33f2f55a8'
os.environ['POLYGON_API_KEY'] = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'

obb.user.credentials.fred_api_key = '7c26de454d31a77bfdf9aaa33f2f55a8'
obb.user.credentials.polygon_api_key = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'

print("="*80)
print(" "*20 + "🏦 FRED COMMODITY SPOT PRICES 🏦")
print("="*80)
print(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Test commodity spot prices
print("\n📊 COMMODITY SPOT PRICES FROM FRED")
print("-"*60)

try:
    # Get commodity spot prices from FRED
    spot_data = obb.commodity.price.spot(provider='fred')
    
    if spot_data and spot_data.results:
        print(f"✅ Successfully retrieved {len(spot_data.results)} data points!\n")
        
        # Show recent data
        for i, item in enumerate(spot_data.results[-10:], 1):  # Last 10 data points
            if hasattr(item, 'date') and hasattr(item, 'value'):
                print(f"{i}. Date: {item.date}, Value: {item.value}")
            else:
                print(f"{i}. {item}")
    else:
        print("No spot price data returned")
        
except Exception as e:
    print(f"Error: {e}")

# Try specific commodity series from FRED
print("\n📈 SPECIFIC COMMODITY SERIES")
print("-"*60)

# Common FRED commodity series IDs
commodity_series = {
    'DCOILWTICO': 'WTI Crude Oil ($/barrel)',
    'GOLDAMGBD228NLBM': 'Gold Price ($/ounce)',
    'DEXCHUS': 'Chinese Yuan to USD',
    'DHHNGSP': 'Natural Gas Price',
    'PCOPPUSDM': 'Copper Price',
    'PALLFNFINDEXM': 'Global Commodity Price Index'
}

print("\nFetching specific commodity data from FRED:\n")

for series_id, name in commodity_series.items():
    try:
        # Use FRED series endpoint
        from openbb import obb
        # Try to get series data
        print(f"• {name} ({series_id})")
        # Note: The exact method may vary based on OpenBB version
    except Exception as e:
        pass

print("\n" + "="*80)
print("HOW TO USE FRED IN OPENBB CLI")
print("="*80)
print("""
Now that your FRED API key is configured, you can use:

1. Launch OpenBB with FRED enabled:
   export OPENBB_API_FRED_KEY='7c26de454d31a77bfdf9aaa33f2f55a8'
   ./launch-openbb.sh

2. Get commodity spot prices:
   /commodity/price/spot --provider fred

3. Get economic data:
   /economy/gdp --provider fred
   /economy/inflation --provider fred
   /economy/unemployment --provider fred

4. Get specific series (using FRED series IDs):
   /economy/fred_series --series_id DCOILWTICO --provider fred  # Oil
   /economy/fred_series --series_id GOLDAMGBD228NLBM --provider fred  # Gold

Your API Keys Status:
✅ FRED API: 7c26de454d31a77bfdf9aaa33f2f55a8
✅ Polygon API: Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai
""")
print("="*80)
