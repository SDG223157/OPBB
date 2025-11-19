#!/usr/bin/env python3
"""Simple commodity data test"""

from openbb import obb
import os

os.environ['POLYGON_API_KEY'] = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'
obb.user.credentials.polygon_api_key = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'

print('COMMODITY ETF PRICES (via Polygon)')
print('='*50)

# Test with major commodity ETFs
etfs = {
    'GLD': 'Gold',
    'SLV': 'Silver',
    'USO': 'Oil',
    'DBA': 'Agriculture'
}

for symbol, name in etfs.items():
    try:
        data = obb.equity.price.quote(symbol=symbol, provider='polygon')
        if data and data.results:
            result = data.results[0]
            print(f'{name:15} ({symbol}): ${result.last_price:.2f}')
    except Exception as e:
        # Try yfinance as fallback
        try:
            data = obb.equity.price.quote(symbol=symbol, provider='yfinance')
            if data and data.results:
                result = data.results[0]
                print(f'{name:15} ({symbol}): ${result.last_price:.2f}')
        except:
            print(f'{name:15} ({symbol}): Unable to fetch')

print('\n' + '='*50)
print('For direct commodity futures/spot prices:')
print('1. Get FRED API key: https://fred.stlouisfed.org')
print('2. Get EIA API key: https://www.eia.gov/opendata/')
print('='*50)
