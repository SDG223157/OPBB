# 📊 ROIC + OpenBB Current Workflow

## ✅ What Works Today

### Quick Analysis (3 seconds)
```bash
# In terminal (NOT in OpenBB CLI):
./roic quality AAPL
```

### Detailed Analysis (10 seconds)
```bash
# Step 1: Get ROIC metrics
./roic quality AAPL

# Step 2: Get forecast
./roic forecast AAPL

# Step 3: Compare with peers
./roic compare AAPL MSFT GOOGL
```

### Combined OpenBB + ROIC Data
```bash
# Activate environment
source /Users/sdg223157/OPBB/openbb-env/bin/activate

# Get both data sources
python3 roic_wrapper.py AAPL
```
Output:
```
OpenBB Metrics:
  P/E Ratio:    35.85
  Market Cap:   $3.97T

ROIC Metrics:
  ROIC:         51.54%
  Quality:      95/100
  Moat:         Wide
```

## 🔄 Complete Analysis Workflow

### Example: Full Apple Analysis
```bash
# Terminal 1: ROIC Analysis
./roic quality AAPL
./roic forecast AAPL
./roic historical AAPL --years 5

# Terminal 2: OpenBB Analysis  
./launch-openbb-premium.sh
/equity/fundamental/income --symbol AAPL --provider polygon
/equity/fundamental/balance --symbol AAPL --provider yfinance
/equity/fundamental/metrics --symbol AAPL --provider finviz
/equity/price/historical --symbol AAPL --start 2024-01-01
exit
```

## 📈 Export Data

### ROIC Data Export
```bash
# Export to CSV
./roic quality AAPL > aapl_roic.csv

# Export multiple stocks
for stock in AAPL MSFT GOOGL NVDA; do
  ./roic quality $stock >> tech_giants_roic.csv
done
```

### OpenBB Data Export
```bash
# In OpenBB CLI:
/equity/fundamental/metrics --symbol AAPL --provider yfinance --export csv
/equity/fundamental/income --symbol AAPL --provider polygon --export xlsx
```

## 🎯 Quick Reference

| What You Want | Command to Use | Where to Run |
|--------------|----------------|--------------|
| ROIC Score | `./roic quality AAPL` | Terminal |
| Price Target | `./roic forecast AAPL` | Terminal |
| Compare Stocks | `./roic compare AAPL MSFT` | Terminal |
| Combined Analysis | `python3 roic_wrapper.py AAPL` | Terminal (with env) |
| OpenBB Financials | `/equity/fundamental/income --symbol AAPL` | OpenBB CLI |

## ⚠️ Common Mistake
**DON'T** type `./roic` commands inside OpenBB CLI (🦋 prompt)
**DO** type `./roic` commands in regular terminal ($ or % prompt)

## 🚀 Future State
When OpenBB adds plugin support (v2.0+):
- ROIC will appear in `--provider roic` dropdown
- You'll use: `/equity/fundamental/metrics --symbol AAPL --provider roic`
- Everything will be integrated in one CLI

**Until then:** Use the workflow above for best results!
