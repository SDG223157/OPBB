#!/usr/bin/env python3
"""
ROIC to OpenBB Display Bridge
Converts ROIC data to OpenBB format for display in the native interface
"""

from openbb import obb
import pandas as pd
from openbb_roic_provider import roic_metrics, roic_forecast
import json
from datetime import datetime

def roic_to_openbb_format(symbol: str):
    """
    Get ROIC data and format it for OpenBB display
    """
    # Get ROIC metrics
    roic_data = roic_metrics(symbol)
    
    # Create a DataFrame in OpenBB format
    df = pd.DataFrame([{
        'symbol': symbol,
        'asset_type': 'EQUITY',
        'name': f'{symbol} Quality Metrics',
        'exchange': 'ROIC.AI',
        'roic': roic_data.get('roic', 0),
        'quality_score': roic_data.get('quality_score', 0),
        'moat_rating': roic_data.get('moat_rating', 'Unknown'),
        'date': datetime.now().strftime('%Y-%m-%d')
    }])
    
    # Save to CSV that OpenBB can read
    csv_file = f'{symbol}_roic_metrics.csv'
    df.to_csv(csv_file, index=False)
    
    print(f"✅ ROIC data saved to: {csv_file}")
    print("\nTo view in OpenBB:")
    print(f"1. In OpenBB CLI, load the CSV:")
    print(f"   /import {csv_file}")
    print(f"2. Or use OpenBB Python:")
    print(f"   df = pd.read_csv('{csv_file}')")
    print(f"   obb.display(df)")
    
    return df

def create_openbb_compatible_view(symbols: list):
    """
    Create an OpenBB-compatible view of multiple stocks
    """
    all_data = []
    
    for symbol in symbols:
        roic_data = roic_metrics(symbol)
        forecast_data = roic_forecast(symbol)
        
        row = {
            'SYMBOL': symbol,
            'ASSET_TYPE': 'EQUITY',
            'NAME': f'{symbol}',
            'EXCHANGE': 'ROIC',
            'BID': forecast_data.get('current_price', 0),
            'BID_SIZE': 100,
            'ASK': forecast_data.get('current_price', 0) + 0.01,
            'ASK_SIZE': 100,
            'LAST_PRICE': forecast_data.get('current_price', 0),
            'ROIC_%': roic_data.get('roic', 0),
            'QUALITY': roic_data.get('quality_score', 0),
            'MOAT': roic_data.get('moat_rating', 'Unknown'),
            '1Y_TARGET': forecast_data.get('1_year_target', 0)
        }
        all_data.append(row)
    
    df = pd.DataFrame(all_data)
    
    # Display in OpenBB style
    print("\n" + "="*120)
    print(" "*40 + "ROIC QUALITY METRICS (OpenBB Format)")
    print("="*120)
    print(df.to_string(index=False))
    print("="*120)
    
    # Save for OpenBB import
    df.to_csv('roic_openbb_view.csv', index=False)
    print("\n✅ Saved to: roic_openbb_view.csv")
    print("Import in OpenBB with: /import roic_openbb_view.csv")
    
    return df

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("""
Usage:
  python roic_to_openbb.py SYMBOL           Convert single symbol
  python roic_to_openbb.py AAPL MSFT GOOGL  Convert multiple symbols
        
This creates CSV files that can be imported into OpenBB's display system.
""")
        sys.exit(1)
    
    symbols = [s.upper() for s in sys.argv[1:]]
    
    if len(symbols) == 1:
        roic_to_openbb_format(symbols[0])
    else:
        create_openbb_compatible_view(symbols)
