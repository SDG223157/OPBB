# 📊 How to Get Company 3-Year Financial Forecast Data

## Quick Answer
OpenBB provides several ways to get financial forecasts, though full analyst estimates require premium data providers. Here's what you can access:

## ✅ Available Forecast Data (Free/With Your APIs)

### 1. Forward Estimates Commands
```bash
./launch-openbb-full.sh

# Forward earnings estimates
/equity/estimates/forward_eps --symbol AAPL --provider yfinance
/equity/estimates/forward_pe --symbol AAPL --provider yfinance

# Forward revenue/sales estimates  
/equity/estimates/forward_sales --symbol AAPL --provider yfinance

# Forward EBITDA estimates
/equity/estimates/forward_ebitda --symbol AAPL --provider yfinance

# Consensus estimates and price targets
/equity/estimates/consensus --symbol AAPL --provider yfinance
/equity/estimates/price_target --symbol AAPL --provider yfinance
```

### 2. Historical Data for Trend Projection
```bash
# Get 5 years of income statements to calculate growth rates
/equity/fundamental/income --symbol AAPL --limit 5 --provider yfinance

# Get balance sheet trends
/equity/fundamental/balance --symbol AAPL --limit 5 --provider yfinance

# Get cash flow trends
/equity/fundamental/cash --symbol AAPL --limit 5 --provider yfinance
```

### 3. Current Metrics with Forward Indicators
```bash
# Get fundamental metrics including forward P/E
/equity/fundamental/metrics --symbol AAPL --provider yfinance

# Get valuation ratios
/equity/fundamental/ratios --symbol AAPL --provider yfinance
```

## 📈 What You Can Calculate

Based on the Apple example:
- **Current Stock Price**: $267.44
- **Forward P/E**: 32.18 (implies forward earnings)
- **Historical Revenue Growth**: 2.9% annually
- **3-Year Revenue Projection**: $428B → $453B
- **Estimated Price Targets**: Based on P/E and growth

## 🎯 Best Commands for Forecasts

### Simple 3-Step Process:
```bash
# Step 1: Get forward estimates
/equity/estimates/forward_eps --symbol AAPL --provider yfinance
/equity/estimates/forward_sales --symbol AAPL --provider yfinance

# Step 2: Get consensus targets
/equity/estimates/consensus --symbol AAPL --provider yfinance
/equity/estimates/price_target --symbol AAPL --provider yfinance

# Step 3: Get historical trends
/equity/fundamental/income --symbol AAPL --limit 5 --provider yfinance
```

### Export Everything:
```bash
/equity/estimates/consensus --symbol AAPL --provider yfinance --export csv
/equity/fundamental/income --symbol AAPL --limit 5 --provider yfinance --export csv
```

## 🐍 Python Script for Automated Forecasts

Run this for complete forecast analysis:
```bash
python get_company_forecasts.py
```

This script:
- Fetches current price and metrics
- Calculates historical growth rates
- Projects 3-year revenue and earnings
- Estimates future stock prices

## 📊 Example Output (Apple)

**Revenue Projections (based on 2.9% historical growth):**
- 2025: $416B (actual)
- 2026: $428B (projected)
- 2027: $440B (projected)
- 2028: $453B (projected)

**Stock Price Projections (10% assumed growth):**
- Current: $267
- Year 1: $294 (+10%)
- Year 2: $324 (+21%)
- Year 3: $356 (+33%)

## ⚠️ Limitations

### What's Available:
✅ Forward P/E, EPS estimates (limited)
✅ Historical financials for trend analysis
✅ Basic consensus data
✅ Price targets (when available)

### What Requires Premium Providers:
❌ Detailed quarterly estimates for 3+ years
❌ Individual analyst forecasts
❌ Segment-level projections
❌ Full earnings model details

## 🏆 Best Free Approach

1. **Use Historical Growth**: Calculate growth rates from past 5 years
2. **Apply Industry Averages**: Tech ~15%, Finance ~8%, etc.
3. **Use Forward P/E**: Available in fundamental metrics
4. **Check Consensus**: When available via estimates commands

## 💰 Premium Alternatives

For comprehensive 3-year forecasts, consider:
- **Bloomberg Terminal**: $2,000/month - Full analyst models
- **Refinitiv Eikon**: $1,800/month - Detailed estimates
- **FactSet**: $1,500/month - Consensus forecasts
- **S&P Capital IQ**: $2,500/month - Comprehensive data
- **Morningstar Direct**: $1,000/month - Fair value estimates

## 🚀 Quick Start

```bash
# 1. Launch OpenBB
./launch-openbb-full.sh

# 2. Get all available forecasts for Apple
/equity/estimates/forward_eps --symbol AAPL --provider yfinance
/equity/estimates/consensus --symbol AAPL --provider yfinance
/equity/fundamental/income --symbol AAPL --limit 5 --provider yfinance

# 3. Or run the Python script
python get_company_forecasts.py
```

## Summary

While OpenBB doesn't provide full 3-year analyst models without premium subscriptions, you can:
- Access forward estimates and consensus data
- Calculate growth projections from historical data  
- Use forward valuation metrics
- Export data for your own modeling

Your current setup with Polygon and FRED APIs provides good market data, but detailed multi-year forecasts remain a premium feature across all financial data platforms.
