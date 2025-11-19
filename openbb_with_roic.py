#!/usr/bin/env python3
"""
Use OpenBB with ROIC Provider
"""

import sys
sys.path.insert(0, '/Users/sdg223157/openbb-build-v2/openbb-roic-provider')

from openbb import obb
from openbb_roic import ROICProvider

def analyze_with_roic(symbol):
    """Analyze a stock with both OpenBB and ROIC"""
    print(f"\n{'='*60}")
    print(f"Analysis for {symbol}")
    print(f"{'='*60}")
    
    # OpenBB data
    try:
        quote = obb.equity.price.quote(symbol=symbol, provider='yfinance')
        if quote.results:
            data = quote.results[0]
            print(f"\nOpenBB Data:")
            print(f"  Current Price: ${getattr(data, 'last_price', 'N/A')}")
            print(f"  Market Cap: {getattr(data, 'market_cap', 'N/A')}")
    except Exception as e:
        print(f"OpenBB error: {e}")
    
    # ROIC data
    try:
        metrics = ROICProvider.get_metrics(symbol)
        forecast = ROICProvider.get_forecast(symbol)
        
        print(f"\nROIC Analysis:")
        print(f"  ROIC: {metrics['roic']}%")
        print(f"  Quality Score: {metrics['quality_score']}/100")
        print(f"  Moat Rating: {metrics['moat_rating']}")
        print(f"\nPrice Targets:")
        print(f"  1 Year: ${forecast['1_year_target']}")
        print(f"  2 Year: ${forecast['2_year_target']}")
        print(f"  3 Year: ${forecast['3_year_target']}")
    except Exception as e:
        print(f"ROIC error: {e}")
    
    print(f"{'='*60}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze_with_roic(sys.argv[1])
    else:
        print("Usage: python3 openbb_with_roic.py SYMBOL")
        print("Example: python3 openbb_with_roic.py AAPL")
        print("\nTesting with AAPL...")
        analyze_with_roic("AAPL")
