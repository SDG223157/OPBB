#!/usr/bin/env python3
"""
Get Commodity Market Data using OpenBB
Shows real-time commodity prices using ETFs as proxies
"""

from openbb import obb
import os
from datetime import datetime
import pandas as pd

# Set API key if available
os.environ['POLYGON_API_KEY'] = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'
obb.user.credentials.polygon_api_key = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'

print("="*80)
print(" "*25 + "📊 COMMODITY MARKET DATA 📊")
print("="*80)
print(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Define commodity ETFs as proxies for commodity prices
commodity_categories = {
    "🥇 PRECIOUS METALS": {
        'GLD': 'Gold',
        'SLV': 'Silver',
        'PPLT': 'Platinum',
        'PALL': 'Palladium'
    },
    "⛽ ENERGY": {
        'USO': 'WTI Crude Oil',
        'BNO': 'Brent Oil', 
        'UNG': 'Natural Gas',
        'UGA': 'Gasoline'
    },
    "🌾 AGRICULTURE": {
        'DBA': 'Agriculture Index',
        'CORN': 'Corn',
        'WEAT': 'Wheat',
        'SOYB': 'Soybeans'
    },
    "🏗️ INDUSTRIAL METALS": {
        'DBB': 'Base Metals Index',
        'CPER': 'Copper',
        'JJU': 'Aluminum'
    }
}

# Fetch and display commodity data
for category, commodities in commodity_categories.items():
    print(f"\n{category}")
    print("-"*60)
    
    for symbol, name in commodities.items():
        try:
            # Get quote data
            quote = obb.equity.price.quote(symbol=symbol, provider='yfinance')
            
            if quote and quote.results:
                data = quote.results[0]
                
                # Format the display
                price_str = f"${data.last_price:8.2f}"
                
                # Calculate change if available
                change_str = ""
                if hasattr(data, 'change') and data.change is not None:
                    change_str = f"  Change: ${data.change:+7.2f}"
                
                # Calculate percent change if available
                pct_str = ""
                if hasattr(data, 'change_percent') and data.change_percent is not None:
                    pct_str = f" ({data.change_percent:+6.2f}%)"
                elif data.open and data.last_price:
                    # Calculate manually if not provided
                    pct_change = ((data.last_price - data.open) / data.open) * 100
                    pct_str = f" ({pct_change:+6.2f}%)"
                
                # Volume
                vol_str = ""
                if hasattr(data, 'volume') and data.volume:
                    vol_str = f"  Vol: {data.volume/1e6:6.1f}M"
                
                print(f"{name:20} ({symbol:5}): {price_str}{change_str}{pct_str}{vol_str}")
                
        except Exception as e:
            print(f"{name:20} ({symbol:5}): Data unavailable")

# Get some energy-specific data if EIA provider is available
print("\n" + "="*80)
print(" "*25 + "📈 MARKET INSIGHTS")
print("="*80)

try:
    # Try to get oil data specifically
    oil_data = obb.equity.price.quote(symbol='USO', provider='yfinance')
    if oil_data and oil_data.results:
        oil = oil_data.results[0]
        print(f"\n💡 Oil Price (USO ETF): ${oil.last_price:.2f}")
        if oil.high and oil.low:
            print(f"   Today's Range: ${oil.low:.2f} - ${oil.high:.2f}")
        if oil.volume:
            print(f"   Trading Volume: {oil.volume/1e6:.1f}M shares")
        
    # Gold/Oil ratio (economic indicator)
    gold_data = obb.equity.price.quote(symbol='GLD', provider='yfinance')
    if gold_data and gold_data.results and oil_data and oil_data.results:
        gold = gold_data.results[0]
        ratio = gold.last_price / oil.last_price
        print(f"\n📊 Gold/Oil Ratio: {ratio:.2f}")
        print(f"   (Historical average: ~15-20)")
        
except:
    pass

print("\n" + "="*80)
print("CLI COMMANDS TO GET THIS DATA:")
print("="*80)
print("""
# Launch OpenBB CLI
./launch-openbb.sh

# Get all precious metals at once
/equity/price/quote --symbol GLD,SLV,PPLT,PALL --provider yfinance

# Get energy commodities
/equity/price/quote --symbol USO,BNO,UNG,UGA --provider yfinance

# Get agriculture
/equity/price/quote --symbol DBA,CORN,WEAT,SOYB --provider yfinance

# Get historical data for gold
/equity/price/historical --symbol GLD --start_date 2024-01-01

# Export to CSV
/equity/price/historical --symbol USO --start_date 2024-01-01 --export csv
""")

print("="*80)
print("Note: ETF prices are proxies for commodity spot prices")
print("For actual futures/spot prices, specialized data providers are needed")
print("="*80)
