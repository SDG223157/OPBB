# 📊 Company Financial Forecast Guide - OpenBB CLI

## Overview
Get 3-year financial forecasts including analyst estimates, revenue projections, earnings forecasts, and consensus targets for any public company.

## Quick Start
```bash
cd /Users/sdg223157/OPBB
./launch-openbb-full.sh  # Launch with your API keys
```

## Available Forecast Commands

### 1. Analyst Consensus Estimates
```bash
# Earnings estimates (EPS) - next 3 years
/equity/estimates/consensus --symbol AAPL --provider yfinance

# Revenue estimates
/equity/estimates/consensus --symbol AAPL --estimize revenue --provider yfinance

# Multiple companies at once
/equity/estimates/consensus --symbol AAPL,MSFT,GOOGL --provider yfinance
```

### 2. Forward Earnings & Revenue
```bash
# Forward P/E ratio and earnings
/equity/estimates/forward_pe --symbol AAPL --provider yfinance

# Forward sales/revenue estimates
/equity/estimates/forward_sales --symbol AAPL --provider yfinance

# Forward EBITDA
/equity/estimates/forward_ebitda --symbol AAPL --provider yfinance
```

### 3. Price Targets & Recommendations
```bash
# Analyst price targets (12-month forecast)
/equity/estimates/price_target --symbol AAPL --provider yfinance

# Analyst recommendations (Buy/Hold/Sell)
/equity/estimates/recommendations --symbol AAPL --provider yfinance

# Historical price target changes
/equity/estimates/price_target_history --symbol AAPL --provider yfinance
```

### 4. Detailed Financial Projections
```bash
# Comprehensive analyst estimates
/equity/estimates/analyst --symbol AAPL --provider polygon

# EPS estimates by quarter (next 8 quarters)
/equity/estimates/forward_eps --symbol AAPL --provider yfinance

# Revenue growth projections
/equity/estimates/revenue_growth --symbol AAPL --provider yfinance
```

## Examples by Company

### Apple (AAPL) - 3-Year Forecast
```bash
# Current estimates
/equity/estimates/consensus --symbol AAPL --provider yfinance

# Forward metrics
/equity/estimates/forward_pe --symbol AAPL --provider yfinance
/equity/estimates/forward_sales --symbol AAPL --provider yfinance

# Price targets
/equity/estimates/price_target --symbol AAPL --provider yfinance

# Growth estimates
/equity/estimates/growth --symbol AAPL --provider yfinance
```

### Tesla (TSLA) - High Growth Forecasts
```bash
# Consensus estimates
/equity/estimates/consensus --symbol TSLA --provider yfinance

# Revenue projections
/equity/estimates/forward_sales --symbol TSLA --provider yfinance

# Analyst recommendations
/equity/estimates/recommendations --symbol TSLA --provider yfinance
```

### Microsoft (MSFT) - Tech Giant Projections
```bash
# Full estimate summary
/equity/estimates/consensus --symbol MSFT --provider yfinance
/equity/estimates/forward_pe --symbol MSFT --provider yfinance
/equity/estimates/price_target --symbol MSFT --provider yfinance
```

## Using Different Providers

### With YFinance (Free, No API Key)
```bash
/equity/estimates/consensus --symbol AAPL --provider yfinance
/equity/estimates/price_target --symbol AAPL --provider yfinance
```

### With Polygon (Your API Key)
```bash
/equity/estimates/consensus --symbol AAPL --provider polygon
```

### With FMP (Requires API Key)
```bash
/equity/estimates/consensus --symbol AAPL --provider fmp
/equity/estimates/analyst_estimates --symbol AAPL --provider fmp
```

## Getting Specific Forecast Periods

### Quarterly Estimates (Next 8 Quarters)
```bash
# EPS by quarter
/equity/estimates/quarterly_estimates --symbol AAPL --provider yfinance

# Revenue by quarter
/equity/estimates/quarterly_revenue --symbol AAPL --provider yfinance
```

### Annual Estimates (Next 3-5 Years)
```bash
# Annual EPS projections
/equity/estimates/annual_estimates --symbol AAPL --provider yfinance

# Annual revenue projections
/equity/estimates/annual_revenue --symbol AAPL --provider yfinance
```

## Key Metrics to Check

### 1. Earnings Per Share (EPS) Forecasts
- Current year EPS estimate
- Next year EPS estimate  
- 3-year EPS growth rate
- Quarterly EPS trends

### 2. Revenue Forecasts
- Current year revenue estimate
- Next year revenue estimate
- Revenue growth rate
- Quarterly revenue trends

### 3. Valuation Metrics
- Forward P/E ratio
- PEG ratio (P/E to Growth)
- Price to Sales (forward)
- EV/EBITDA (forward)

### 4. Analyst Sentiment
- Mean price target
- High/Low price targets
- Buy/Hold/Sell recommendations
- Number of analysts covering

## Export Forecast Data

```bash
# Export to CSV
/equity/estimates/consensus --symbol AAPL --provider yfinance --export csv

# Export multiple companies
/equity/estimates/consensus --symbol AAPL,MSFT,GOOGL --provider yfinance --export xlsx

# Export with historical data
/equity/estimates/history --symbol AAPL --provider yfinance --export csv
```

## Python Script for Comprehensive Forecasts

Create `company_forecasts.py`:
```python
#!/usr/bin/env python3
from openbb import obb
import os

# Set API keys
os.environ['POLYGON_API_KEY'] = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'
obb.user.credentials.polygon_api_key = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'

def get_company_forecasts(symbol):
    print(f"\n{'='*60}")
    print(f"3-YEAR FINANCIAL FORECAST: {symbol}")
    print('='*60)
    
    try:
        # Get consensus estimates
        consensus = obb.equity.estimates.consensus(symbol=symbol, provider='yfinance')
        if consensus and consensus.results:
            print("\n📊 Consensus Estimates:")
            for item in consensus.results[:5]:
                print(f"  {item}")
        
        # Get price target
        target = obb.equity.estimates.price_target(symbol=symbol, provider='yfinance')
        if target and target.results:
            data = target.results[0]
            print(f"\n🎯 Price Targets:")
            print(f"  Mean Target: ${data.target_mean:.2f}")
            print(f"  High Target: ${data.target_high:.2f}")
            print(f"  Low Target: ${data.target_low:.2f}")
        
        # Get recommendations
        recs = obb.equity.estimates.recommendations(symbol=symbol, provider='yfinance')
        if recs and recs.results:
            print(f"\n📈 Analyst Recommendations:")
            for rec in recs.results[:3]:
                print(f"  {rec}")
                
    except Exception as e:
        print(f"Error: {e}")

# Example usage
symbols = ['AAPL', 'MSFT', 'TSLA']
for symbol in symbols:
    get_company_forecasts(symbol)
```

## Common Forecast Analysis

### Growth Stock Analysis
```bash
# High growth companies (NVDA, TSLA, etc.)
/equity/estimates/consensus --symbol NVDA --provider yfinance
/equity/estimates/growth --symbol NVDA --provider yfinance
/equity/estimates/price_target --symbol NVDA --provider yfinance
```

### Value Stock Analysis
```bash
# Value companies (BRK.B, JPM, etc.)
/equity/estimates/consensus --symbol JPM --provider yfinance
/equity/estimates/forward_pe --symbol JPM --provider yfinance
```

### Sector Comparison
```bash
# Compare tech giants
/equity/estimates/consensus --symbol AAPL,MSFT,GOOGL,AMZN --provider yfinance

# Compare banks
/equity/estimates/consensus --symbol JPM,BAC,WFC,C --provider yfinance
```

## Important Metrics Explained

### Forward P/E Ratio
- Stock price divided by expected earnings
- Lower = potentially undervalued
- Compare to industry average

### PEG Ratio
- P/E divided by growth rate
- Under 1.0 = potentially undervalued
- Accounts for growth expectations

### EPS Growth Rate
- Expected earnings growth over 3-5 years
- Higher = more growth expected
- Compare to historical growth

### Revenue Growth Rate
- Expected sales growth
- Key for growth stocks
- Should exceed industry average

## Tips for Using Forecast Data

1. **Multiple Sources**: Check multiple analysts/providers
2. **Historical Accuracy**: Review past estimate accuracy
3. **Estimate Revisions**: Watch for recent changes
4. **Consensus vs Range**: Look at both average and range
5. **Industry Context**: Compare to sector peers

## Data Providers Comparison

| Provider | API Key Required | Forecast Years | Update Frequency |
|----------|-----------------|----------------|------------------|
| YFinance | No | 2-3 years | Daily |
| Polygon | Yes (you have it) | 2-3 years | Real-time |
| FMP | Yes | 3-5 years | Daily |
| Alpha Vantage | Yes | 2 years | Daily |

## Quick Commands Summary

```bash
# Most useful forecast commands (no API needed)
/equity/estimates/consensus --symbol AAPL --provider yfinance
/equity/estimates/price_target --symbol AAPL --provider yfinance
/equity/estimates/recommendations --symbol AAPL --provider yfinance

# Export all forecasts
/equity/estimates/consensus --symbol AAPL --provider yfinance --export csv
```

Your Setup:
✅ Polygon API configured for enhanced data
✅ YFinance available for free forecasts
✅ Can get 2-3 year projections for any US stock
