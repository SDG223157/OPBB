#!/usr/bin/env python3
"""
Test FRED Economic Data Access
Shows how to retrieve economic indicators from FRED
"""

from openbb import obb
import os

# Set API key
os.environ['FRED_API_KEY'] = '7c26de454d31a77bfdf9aaa33f2f55a8'
os.environ['OPENBB_API_FRED_KEY'] = '7c26de454d31a77bfdf9aaa33f2f55a8'
obb.user.credentials.fred_api_key = '7c26de454d31a77bfdf9aaa33f2f55a8'

print("="*80)
print(" "*20 + "FRED ECONOMIC DATA TEST")
print("="*80)

# Test different economic series
test_series = {
    'UNRATE': 'Unemployment Rate',
    'CPIAUCSL': 'Consumer Price Index',
    'DFF': 'Federal Funds Rate',
    'GDPC1': 'Real GDP',
    'DGS10': '10-Year Treasury',
    'DGS2': '2-Year Treasury',
    'SP500': 'S&P 500 Index',
    'VIXCLS': 'VIX Volatility',
    'DCOILWTICO': 'WTI Oil Price',
    'MORTGAGE30US': '30-Year Mortgage Rate'
}

print("\nTesting FRED Series Access:\n")
print("-"*60)

for series_id, name in test_series.items():
    try:
        # Try to get the series data
        data = obb.economy.fred_series(series_id=series_id, provider='fred')
        
        if data and data.results and len(data.results) > 0:
            latest = data.results[-1]
            if hasattr(latest, 'value') and latest.value is not None:
                value = latest.value
                date = latest.date if hasattr(latest, 'date') else 'N/A'
                print(f"✅ {name:25} ({series_id:15}): {value:>10.2f}  [{date}]")
            else:
                print(f"⚠️  {name:25} ({series_id:15}): No value found")
        else:
            print(f"❌ {name:25} ({series_id:15}): No data returned")
            
    except Exception as e:
        error_msg = str(e)[:50]
        print(f"❌ {name:25} ({series_id:15}): {error_msg}")

print("\n" + "="*80)
print("HOW TO USE THESE IN OPENBB CLI:")
print("="*80)
print("""
1. Launch OpenBB with FRED API:
   ./launch-openbb-full.sh

2. Access economic data:
   /economy/fred_series --series_id UNRATE --provider fred
   /economy/fred_series --series_id CPIAUCSL --provider fred
   /economy/fred_series --series_id DFF --provider fred
   /economy/fred_series --series_id GDPC1 --provider fred
   
3. Get historical data:
   /economy/fred_series --series_id UNRATE --start_date 2020-01-01 --provider fred

4. Export data:
   /economy/fred_series --series_id SP500 --provider fred --export csv

Your FRED API Key: 7c26de454d31a77bfdf9aaa33f2f55a8 ✅
""")
print("="*80)
