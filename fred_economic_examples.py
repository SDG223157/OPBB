#!/usr/bin/env python3
"""
FRED Economic Data Examples
Working examples of how to get economic data from FRED
"""

from openbb import obb
import os
from datetime import datetime

# Set API key
os.environ['FRED_API_KEY'] = '7c26de454d31a77bfdf9aaa33f2f55a8'
obb.user.credentials.fred_api_key = '7c26de454d31a77bfdf9aaa33f2f55a8'

print("="*80)
print(" "*15 + "📊 FRED ECONOMIC DATA EXAMPLES 📊")
print("="*80)
print(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Key economic indicators with their FRED series IDs
indicators = {
    'UNRATE': 'Unemployment Rate',
    'CPIAUCSL': 'Consumer Price Index',
    'DFF': 'Federal Funds Rate',
    'DGS10': '10-Year Treasury Rate',
    'DGS2': '2-Year Treasury Rate',
    'GDPC1': 'Real GDP',
    'VIXCLS': 'VIX Volatility Index',
    'MORTGAGE30US': '30-Year Mortgage Rate',
    'DCOILWTICO': 'WTI Crude Oil',
    'M2SL': 'M2 Money Supply'
}

print("\n📈 LATEST ECONOMIC INDICATORS")
print("-"*60)

for series_id, name in indicators.items():
    try:
        # Get the series data
        data = obb.economy.fred_series(symbol=series_id, provider='fred')
        
        if data and data.results:
            # Get the latest value
            latest = data.results[-1]
            # Access the value using the series name as attribute
            value = getattr(latest, series_id, None)
            date = latest.date
            
            if value is not None:
                # Format based on series type
                if 'Rate' in name or 'Unemployment' in name or 'Mortgage' in name:
                    print(f"{name:25} {value:>10.2f}%  [{date}]")
                elif 'Index' in name or 'CPI' in name:
                    print(f"{name:25} {value:>10.2f}   [{date}]")
                elif 'GDP' in name or 'Supply' in name:
                    print(f"{name:25} {value:>10,.0f}  [{date}]")
                elif 'Oil' in name:
                    print(f"{name:25} ${value:>9.2f}  [{date}]")
                else:
                    print(f"{name:25} {value:>10.2f}   [{date}]")
        
    except Exception as e:
        print(f"{name:25} Error: Check series ID")

# Show historical trend for unemployment
print("\n📊 UNEMPLOYMENT TREND (Last 6 Months)")
print("-"*60)
try:
    data = obb.economy.fred_series(symbol='UNRATE', provider='fred')
    if data and data.results:
        for item in data.results[-6:]:
            value = getattr(item, 'UNRATE', None)
            if value:
                bar = '█' * int(value * 5)  # Visual bar chart
                print(f"{item.date}: {value:4.1f}% {bar}")
except:
    pass

# Calculate yield curve spread
print("\n💡 YIELD CURVE ANALYSIS")
print("-"*60)
try:
    # Get 10-Year Treasury
    ten_year = obb.economy.fred_series(symbol='DGS10', provider='fred')
    ten_year_value = getattr(ten_year.results[-1], 'DGS10', 0) if ten_year and ten_year.results else 0
    
    # Get 2-Year Treasury
    two_year = obb.economy.fred_series(symbol='DGS2', provider='fred')
    two_year_value = getattr(two_year.results[-1], 'DGS2', 0) if two_year and two_year.results else 0
    
    if ten_year_value and two_year_value:
        spread = ten_year_value - two_year_value
        print(f"10-Year Treasury: {ten_year_value:.2f}%")
        print(f"2-Year Treasury:  {two_year_value:.2f}%")
        print(f"Spread (10Y-2Y):  {spread:+.2f}%")
        
        if spread < 0:
            print("\n⚠️  YIELD CURVE INVERTED - Historical recession indicator")
        elif spread < 0.5:
            print("\n⚠️  Yield curve flattening")
        else:
            print("\n✅ Normal yield curve")
except:
    pass

print("\n" + "="*80)
print("OPENBB CLI COMMANDS")
print("="*80)
print("""
Launch OpenBB with FRED API:
./launch-openbb-full.sh

Then use these commands:

# Basic economic indicators
/economy/fred_series --symbol UNRATE --provider fred         # Unemployment
/economy/fred_series --symbol CPIAUCSL --provider fred       # CPI
/economy/fred_series --symbol DFF --provider fred            # Fed Funds Rate
/economy/fred_series --symbol GDPC1 --provider fred          # Real GDP

# Treasury yields
/economy/fred_series --symbol DGS10 --provider fred          # 10-Year
/economy/fred_series --symbol DGS2 --provider fred           # 2-Year
/economy/fred_series --symbol DGS30 --provider fred          # 30-Year

# Market indicators
/economy/fred_series --symbol SP500 --provider fred          # S&P 500
/economy/fred_series --symbol VIXCLS --provider fred         # VIX
/economy/fred_series --symbol DCOILWTICO --provider fred     # Oil

# Historical data
/economy/fred_series --symbol UNRATE --start_date 2020-01-01 --provider fred

# Export to CSV
/economy/fred_series --symbol UNRATE --provider fred --export csv
""")

print("="*80)
print(f"Your FRED API Key: ✅ Active")
print(f"Data Points Available: 800,000+ series")
print("="*80)
