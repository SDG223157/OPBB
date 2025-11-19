#!/usr/bin/env python3
"""
Commodity Dashboard using FRED API
Shows real commodity spot prices from Federal Reserve Economic Data
"""

from openbb import obb
import os
from datetime import datetime
import pandas as pd

# Set API keys
os.environ['FRED_API_KEY'] = '7c26de454d31a77bfdf9aaa33f2f55a8'
os.environ['OPENBB_API_FRED_KEY'] = '7c26de454d31a77bfdf9aaa33f2f55a8'
os.environ['POLYGON_API_KEY'] = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'

obb.user.credentials.fred_api_key = '7c26de454d31a77bfdf9aaa33f2f55a8'
obb.user.credentials.polygon_api_key = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'

print("="*80)
print(" "*20 + "📊 COMMODITY MARKET DASHBOARD 📊")
print(" "*25 + "Powered by FRED API")
print("="*80)
print(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Get commodity spot prices from FRED
print("\n🏦 LATEST COMMODITY SPOT PRICES (from FRED)")
print("-"*60)

try:
    spot_data = obb.commodity.price.spot(provider='fred')
    
    if spot_data and spot_data.results:
        # Organize data by commodity type
        commodities = {}
        
        # Get the most recent data for each commodity
        for item in spot_data.results:
            if hasattr(item, 'commodity') and hasattr(item, 'price'):
                commodity_name = item.commodity
                if commodity_name not in commodities or item.date > commodities[commodity_name]['date']:
                    commodities[commodity_name] = {
                        'date': item.date,
                        'price': item.price,
                        'unit': item.unit if hasattr(item, 'unit') else '',
                        'symbol': item.symbol if hasattr(item, 'symbol') else ''
                    }
        
        # Group and display by category
        energy_keywords = ['Oil', 'Gas', 'Fuel', 'Heating', 'Propane', 'Crude', 'Natural Gas']
        metals_keywords = ['Gold', 'Silver', 'Copper', 'Aluminum', 'Platinum']
        
        # Energy Commodities
        print("\n⛽ ENERGY COMMODITIES")
        print("-"*40)
        for name, data in sorted(commodities.items()):
            if any(keyword in name for keyword in energy_keywords):
                price_str = f"${data['price']:.2f}" if data['price'] else "N/A"
                unit_str = data['unit'] if data['unit'] else ""
                print(f"• {name[:45]:45} {price_str:>10} {unit_str}")
        
        # Display most recent update date
        if commodities:
            latest_date = max(c['date'] for c in commodities.values())
            print(f"\n📅 Latest Update: {latest_date}")
            
        print(f"\n✅ Total commodity series available: {len(commodities)}")
        
except Exception as e:
    print(f"Error fetching FRED data: {e}")

# Show key commodity series IDs for direct access
print("\n" + "="*80)
print("KEY FRED COMMODITY SERIES")
print("="*80)
print("""
Direct FRED Series IDs for Major Commodities:
----------------------------------------------
Oil & Energy:
• DCOILWTICO     - WTI Crude Oil ($/barrel)
• DCOILBRENTEU   - Brent Crude Oil ($/barrel)
• DHHNGSP        - Henry Hub Natural Gas ($/MMBTU)
• DGASUSGULF     - Gasoline US Gulf Coast ($/gallon)

Precious Metals:
• GOLDAMGBD228NLBM - Gold Price London Fix ($/ounce)
• SLVPRUSD         - Silver Price ($/ounce)

Base Metals:
• PCOPPUSDM        - Copper Price ($/metric ton)
• PALUMUSDM        - Aluminum Price ($/metric ton)

Agricultural:
• PWHEATUSDM       - Wheat Price ($/metric ton)
• PCORNUSDM        - Corn Price ($/metric ton)
• PRICENPUSDM      - Rice Price ($/metric ton)

Indices:
• PALLFNFINDEXM    - All Commodity Price Index
• PNRGINDEXM       - Energy Price Index
""")

print("="*80)
print("HOW TO USE IN OPENBB CLI")
print("="*80)
print("""
With your FRED API key configured, you can now:

1. Launch OpenBB with full API access:
   ./launch-openbb-full.sh

2. Get all commodity spot prices:
   /commodity/price/spot --provider fred

3. Get specific commodity series:
   /economy/fred_series --series_id DCOILWTICO --provider fred
   /economy/fred_series --series_id GOLDAMGBD228NLBM --provider fred

4. Get historical data:
   /economy/fred_series --series_id DCOILWTICO --start_date 2024-01-01 --provider fred

5. Export to CSV:
   /commodity/price/spot --provider fred --export csv

Your Active API Keys:
✅ FRED: 7c26de454d31a77bfdf9aaa33f2f55a8 (Commodities & Economic Data)
✅ Polygon: Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai (News & Market Data)
""")
print("="*80)
