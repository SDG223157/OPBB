# 📊 Commodity Market Data Guide - OpenBB CLI

## Overview
OpenBB provides access to commodity market data through various commands and providers. Here's how to get commodity prices, energy data, and more.

## Quick Start Commands

### Launch OpenBB CLI
```bash
cd /Users/sdg223157/OPBB
./launch-openbb-with-polygon.sh  # Or ./launch-openbb.sh
```

## Available Commodity Commands

### 1. Commodity Spot Prices
```bash
/commodity/price/spot --provider fred
```
- **Provider**: FRED (requires free API key)
- **Data**: Historical commodity spot prices

### 2. Petroleum Status Report
```bash
/commodity/petroleum_status_report --provider eia
```
- **Provider**: EIA (US Energy Information Administration)
- **Data**: Weekly petroleum inventory, production, and consumption data

### 3. Short-Term Energy Outlook
```bash
/commodity/short_term_energy_outlook --provider eia
```
- **Provider**: EIA
- **Data**: 18-month projections for energy markets

## Alternative: Commodity ETFs (No API Key Required)

Since direct commodity spot prices often require API keys, you can use commodity ETFs as proxies:

### Gold & Precious Metals
```bash
/equity/price/quote --symbol GLD --provider yfinance   # Gold
/equity/price/quote --symbol SLV --provider yfinance   # Silver
/equity/price/quote --symbol PPLT --provider yfinance  # Platinum
/equity/price/quote --symbol PALL --provider yfinance  # Palladium
```

### Energy Commodities
```bash
/equity/price/quote --symbol USO --provider yfinance   # Oil (WTI Crude)
/equity/price/quote --symbol BNO --provider yfinance   # Brent Oil
/equity/price/quote --symbol UNG --provider yfinance   # Natural Gas
/equity/price/quote --symbol UGA --provider yfinance   # Gasoline
```

### Agricultural Commodities
```bash
/equity/price/quote --symbol DBA --provider yfinance   # Agriculture Basket
/equity/price/quote --symbol CORN --provider yfinance  # Corn
/equity/price/quote --symbol WEAT --provider yfinance  # Wheat
/equity/price/quote --symbol SOYB --provider yfinance  # Soybeans
/equity/price/quote --symbol COW --provider yfinance   # Livestock
```

### Industrial Metals
```bash
/equity/price/quote --symbol DBB --provider yfinance   # Base Metals
/equity/price/quote --symbol CPER --provider yfinance  # Copper
/equity/price/quote --symbol JJU --provider yfinance   # Aluminum
/equity/price/quote --symbol JJN --provider yfinance   # Nickel
```

## Multiple Commodities at Once

Get multiple commodity ETF prices in one command:
```bash
/equity/price/quote --symbol GLD,SLV,USO,DBA,DBB --provider yfinance
```

## Historical Commodity Data

Get historical prices for commodity ETFs:
```bash
# Gold historical data (last 30 days)
/equity/price/historical --symbol GLD --start_date 2024-10-01 --provider yfinance

# Oil historical data with chart
/equity/price/historical --symbol USO --start_date 2024-09-01 --chart true
```

## Export Commodity Data

Export data to CSV for analysis:
```bash
/equity/price/historical --symbol GLD,SLV,USO --start_date 2024-01-01 --export csv
```

## Python Script for Commodity Dashboard

Create `commodity_dashboard.py`:
```python
#!/usr/bin/env python3
from openbb import obb
import os

# Set API key if you have one
os.environ['POLYGON_API_KEY'] = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'
obb.user.credentials.polygon_api_key = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'

# Commodity ETF symbols
commodities = {
    'GLD': 'Gold',
    'SLV': 'Silver',
    'USO': 'WTI Oil',
    'UNG': 'Natural Gas',
    'CORN': 'Corn',
    'WEAT': 'Wheat',
    'CPER': 'Copper'
}

print("COMMODITY DASHBOARD")
print("=" * 50)

for symbol, name in commodities.items():
    try:
        data = obb.equity.price.quote(symbol=symbol, provider='yfinance').results[0]
        print(f"{name:15} ${data.last_price:8.2f} ({data.change_percent:+.2f}%)")
    except:
        pass
```

## Getting Free API Keys for More Data

### FRED (Federal Reserve Economic Data)
1. Visit: https://fred.stlouisfed.org/docs/api/api_key.html
2. Create free account
3. Get API key instantly
4. Set in OpenBB:
```bash
export OPENBB_API_FRED_KEY="your_fred_key"
./launch-openbb.sh
```

### EIA (Energy Information Administration)
1. Visit: https://www.eia.gov/opendata/register.php
2. Register for free
3. Get API key
4. Set in OpenBB:
```bash
export OPENBB_API_EIA_KEY="your_eia_key"
./launch-openbb.sh
```

## Example Workflow

```bash
# 1. Launch OpenBB
./launch-openbb-with-polygon.sh

# 2. Check energy commodities
/equity/price/quote --symbol USO,UNG,BNO --provider yfinance

# 3. Get precious metals
/equity/price/quote --symbol GLD,SLV,PPLT --provider yfinance

# 4. Agriculture basket
/equity/price/quote --symbol DBA --provider yfinance

# 5. Get historical oil prices
/equity/price/historical --symbol USO --start_date 2024-10-01

# 6. Export data
/equity/price/historical --symbol GLD --start_date 2024-01-01 --export csv

# 7. Exit
quit
```

## Commodity Futures (with proper API keys)

If you have appropriate API keys, you can access futures data:
```bash
# With Interactive Brokers or other futures data provider
/derivatives/futures/curve --symbol CL --provider ibkr  # Crude Oil futures
/derivatives/futures/curve --symbol GC --provider ibkr  # Gold futures
```

## Tips & Best Practices

1. **ETFs vs Futures**: ETFs are easier to access (no special API needed) but may have slight tracking differences from spot prices
2. **Market Hours**: Commodity ETFs trade during stock market hours (9:30 AM - 4:00 PM EST)
3. **Real Commodities**: For actual spot prices, you'll need FRED or specialized commodity data providers
4. **Energy Focus**: For detailed energy data, get a free EIA API key
5. **Metals**: London Metal Exchange (LME) data requires specialized providers

## Summary

While direct commodity spot prices require API keys, you can:
- Use commodity ETFs as proxies (free with yfinance)
- Get free API keys from FRED and EIA for official data
- Access energy-specific data through EIA
- Use Polygon API (which you have) for some commodity data

The easiest approach is using commodity ETFs through yfinance, which provides real-time prices without any API key requirements.
