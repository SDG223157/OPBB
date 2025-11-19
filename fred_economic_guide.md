# 📈 FRED Economic Data Guide - OpenBB CLI

## Overview
FRED (Federal Reserve Economic Data) provides access to 800,000+ economic time series from 100+ sources. With your API key configured, you can access all major economic indicators.

## Your FRED API Key
**Key**: `7c26de454d31a77bfdf9aaa33f2f55a8` ✅ Already configured

## Quick Start
```bash
cd /Users/sdg223157/OPBB
./launch-openbb-full.sh  # Launches with FRED API key
```

## Major Economic Indicators

### 1. GDP (Gross Domestic Product)
```bash
/economy/gdp --provider fred
/economy/gdp --countries united_states --provider fred
/economy/gdp --countries united_states,china,japan --provider fred
```

### 2. Inflation & CPI
```bash
/economy/inflation --provider fred
/economy/cpi --provider fred
/economy/cpi --countries united_states --provider fred
```

### 3. Unemployment Rate
```bash
/economy/unemployment --provider fred
/economy/unemployment --countries united_states --provider fred
```

### 4. Interest Rates
```bash
/economy/fred_series --series_id DFF --provider fred        # Federal Funds Rate
/economy/fred_series --series_id DGS10 --provider fred      # 10-Year Treasury
/economy/fred_series --series_id DGS2 --provider fred       # 2-Year Treasury
/economy/fred_series --series_id SOFR --provider fred       # SOFR Rate
```

### 5. Money Supply
```bash
/economy/fred_series --series_id M1SL --provider fred       # M1 Money Supply
/economy/fred_series --series_id M2SL --provider fred       # M2 Money Supply
/economy/fred_series --series_id WALCL --provider fred      # Fed Balance Sheet
```

### 6. Housing Market
```bash
/economy/fred_series --series_id HOUST --provider fred      # Housing Starts
/economy/fred_series --series_id MORTGAGE30US --provider fred  # 30-Year Mortgage Rate
/economy/fred_series --series_id CSUSHPISA --provider fred  # Case-Shiller Home Price Index
```

### 7. Labor Market
```bash
/economy/fred_series --series_id PAYEMS --provider fred     # Nonfarm Payrolls
/economy/fred_series --series_id UNRATE --provider fred     # Unemployment Rate
/economy/fred_series --series_id CIVPART --provider fred    # Labor Force Participation
/economy/fred_series --series_id AHETPI --provider fred     # Average Hourly Earnings
```

### 8. Consumer Metrics
```bash
/economy/fred_series --series_id UMCSENT --provider fred    # Consumer Sentiment
/economy/fred_series --series_id RSXFS --provider fred      # Retail Sales
/economy/fred_series --series_id PCE --provider fred        # Personal Consumption
/economy/fred_series --series_id PSAVERT --provider fred    # Personal Savings Rate
```

### 9. Manufacturing & Trade
```bash
/economy/fred_series --series_id INDPRO --provider fred     # Industrial Production
/economy/fred_series --series_id NEWORDER --provider fred   # New Orders
/economy/fred_series --series_id DGORDER --provider fred    # Durable Goods Orders
/economy/fred_series --series_id BOPGSTB --provider fred    # Trade Balance
```

### 10. Stock Market Indicators
```bash
/economy/fred_series --series_id SP500 --provider fred      # S&P 500 Index
/economy/fred_series --series_id DJIA --provider fred       # Dow Jones Index
/economy/fred_series --series_id VIXCLS --provider fred     # VIX Volatility Index
/economy/fred_series --series_id SHILLER --provider fred    # Shiller P/E Ratio
```

## Getting Historical Data

Add date parameters to get historical series:
```bash
# GDP growth over last 10 years
/economy/gdp --start_date 2014-01-01 --provider fred

# Inflation since 2020
/economy/inflation --start_date 2020-01-01 --provider fred

# Federal Funds Rate history
/economy/fred_series --series_id DFF --start_date 2000-01-01 --provider fred
```

## Comparing Countries

Many indicators support multiple countries:
```bash
# Compare GDP across countries
/economy/gdp --countries united_states,china,germany,japan --provider fred

# Compare unemployment rates
/economy/unemployment --countries united_states,germany,japan --provider fred

# Compare inflation
/economy/inflation --countries united_states,united_kingdom,japan --provider fred
```

## Popular FRED Series IDs

### Key Economic Indicators
- **GDP**: Real GDP (GDPC1), Nominal GDP (GDP)
- **Inflation**: CPI (CPIAUCSL), PCE (PCEPI), Core CPI (CPILFESL)
- **Employment**: Unemployment Rate (UNRATE), Payrolls (PAYEMS)
- **Interest Rates**: Fed Funds (DFF), 10-Year Treasury (DGS10)
- **Money Supply**: M1 (M1SL), M2 (M2SL)

### Financial Markets
- **Stock Indices**: S&P 500 (SP500), DJIA (DJIA), NASDAQ (NASDAQCOM)
- **Volatility**: VIX (VIXCLS)
- **Dollar Index**: DXY (DTWEXBGS)
- **Credit Spreads**: BAA10Y

### Real Estate
- **Home Prices**: Case-Shiller (CSUSHPISA)
- **Mortgage Rates**: 30-Year (MORTGAGE30US), 15-Year (MORTGAGE15US)
- **Housing Starts**: HOUST
- **Building Permits**: PERMIT

### Commodities (Economic Series)
- **Oil**: WTI (DCOILWTICO), Brent (DCOILBRENTEU)
- **Gold**: GOLDAMGBD228NLBM
- **Commodity Index**: PALLFNFINDEXM

## Exporting Data

Export any series to CSV or Excel:
```bash
# Export GDP data to CSV
/economy/gdp --provider fred --export csv

# Export unemployment history
/economy/unemployment --start_date 2020-01-01 --provider fred --export xlsx

# Export multiple series
/economy/fred_series --series_id DFF,DGS10,DGS2 --provider fred --export csv
```

## Python Script Examples

### Get Multiple Economic Indicators
```python
from openbb import obb
import os

os.environ['FRED_API_KEY'] = '7c26de454d31a77bfdf9aaa33f2f55a8'
obb.user.credentials.fred_api_key = '7c26de454d31a77bfdf9aaa33f2f55a8'

# Get GDP
gdp = obb.economy.gdp(provider='fred', countries='united_states')

# Get inflation
inflation = obb.economy.inflation(provider='fred')

# Get unemployment
unemployment = obb.economy.unemployment(provider='fred')

# Get specific series
fed_funds = obb.economy.fred_series(series_id='DFF', provider='fred')
```

## Real-Time Economic Dashboard

Run this to see current economic conditions:
```bash
# Create a dashboard view
/economy/gdp --provider fred
/economy/inflation --provider fred
/economy/unemployment --provider fred
/economy/fred_series --series_id DFF --provider fred
/economy/fred_series --series_id DGS10 --provider fred
/economy/fred_series --series_id VIXCLS --provider fred
```

## Tips & Tricks

1. **Finding Series IDs**: Visit https://fred.stlouisfed.org to search for specific series
2. **Frequency**: Many series have different frequencies (daily, weekly, monthly, quarterly)
3. **Vintage Data**: FRED preserves historical vintages of revised data
4. **Real-Time Updates**: Most series update automatically when new data is released
5. **Rate Limits**: FRED allows 120 requests per minute

## Common Economic Analysis

### Yield Curve Analysis
```bash
# Get multiple treasury yields
/economy/fred_series --series_id DGS1MO --provider fred   # 1-Month
/economy/fred_series --series_id DGS3MO --provider fred   # 3-Month
/economy/fred_series --series_id DGS2 --provider fred     # 2-Year
/economy/fred_series --series_id DGS5 --provider fred     # 5-Year
/economy/fred_series --series_id DGS10 --provider fred    # 10-Year
/economy/fred_series --series_id DGS30 --provider fred    # 30-Year
```

### Recession Indicators
```bash
# Yield curve inversion (10Y-2Y spread)
/economy/fred_series --series_id T10Y2Y --provider fred

# Sahm Rule Recession Indicator
/economy/fred_series --series_id SAHMREALTIME --provider fred

# Leading Economic Index
/economy/fred_series --series_id USSLIND --provider fred
```

### Federal Reserve Monitoring
```bash
# Fed Balance Sheet
/economy/fred_series --series_id WALCL --provider fred

# Reverse Repo Operations
/economy/fred_series --series_id RRPONTSYD --provider fred

# Bank Reserves
/economy/fred_series --series_id TOTRESNS --provider fred
```

## Your Setup Status
✅ FRED API Key: Configured and Active
✅ Access to: 800,000+ economic series
✅ Rate Limit: 120 requests/minute
✅ Cost: FREE
