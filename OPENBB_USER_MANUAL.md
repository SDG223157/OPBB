# 📚 OpenBB Platform - Complete User Manual

## 🚀 Quick Start

### Launch OpenBB
```bash
# Basic launch
./launch-openbb.sh

# Premium features (with all API keys)
./launch-openbb-premium.sh

# With specific providers
./launch-openbb-with-polygon.sh
```

## 🎯 OpenBB CLI Navigation

### Understanding the Interface
```
2025 Nov 18, 23:50 (🦋) / $ 
         │          │   │
         │          │   └─ Your prompt (ready for commands)
         │          └─ Current menu path
         └─ OpenBB butterfly logo
```

### Basic Navigation Commands
| Command | Action |
|---------|--------|
| `TAB` | Auto-complete commands |
| `↑/↓` | Navigate command history |
| `/` | Go back to home menu |
| `exit` or `quit` | Exit OpenBB |
| `clear` | Clear screen |
| `help` or `?` | Show available commands |

## 📊 Core Data Categories

### 1. Equity Market Data (`/equity/`)
```bash
# Price data
/equity/price/historical --symbol AAPL --start_date 2024-01-01
/equity/price/quote --symbol AAPL
/equity/price/performance --symbol AAPL MSFT GOOGL

# Fundamental data
/equity/fundamental/income --symbol AAPL --provider polygon
/equity/fundamental/balance --symbol AAPL --provider yfinance
/equity/fundamental/cash --symbol AAPL --provider fmp
/equity/fundamental/metrics --symbol AAPL --provider finviz

# Analyst estimates
/equity/estimates/consensus --symbol AAPL --provider yfinance
/equity/estimates/analyst --symbol AAPL

# Ownership data
/equity/ownership/institutional --symbol AAPL
/equity/ownership/insider --symbol AAPL
```

### 2. Economic Data (`/economy/`)
```bash
# Economic indicators
/economy/gdp --country united_states
/economy/inflation --country united_states
/economy/unemployment --country united_states

# FRED data
/economy/fred --series GDP
/economy/fred --series UNRATE
/economy/fred --series DFF  # Federal funds rate

# Economic calendar
/economy/calendar --start 2024-11-01 --end 2024-11-30
```

### 3. Cryptocurrency (`/crypto/`)
```bash
# Crypto prices
/crypto/price/quote --symbol BTC --provider polygon
/crypto/price/historical --symbol ETH --start_date 2024-01-01

# Crypto stats
/crypto/stats --symbol BTC
```

### 4. ETF Data (`/etf/`)
```bash
# ETF information
/etf/info --symbol SPY
/etf/holdings --symbol QQQ
/etf/price/historical --symbol SPY --start_date 2024-01-01
```

### 5. News (`/news/`)
```bash
# Market news
/news/general --limit 10
/news/company --symbol AAPL --limit 5
/news/world --limit 10
```

### 6. Currency/Forex (`/currency/`)
```bash
# Exchange rates
/currency/price/quote --symbol EURUSD
/currency/price/historical --symbol GBPUSD --start_date 2024-01-01
```

### 7. Fixed Income (`/fixedincome/`)
```bash
# Treasury rates
/fixedincome/treasury/rates
/fixedincome/yield_curve
```

## 💾 Export Options

### Export Formats
```bash
# Export to CSV
/equity/fundamental/income --symbol AAPL --export csv

# Export to Excel
/equity/fundamental/balance --symbol AAPL --export xlsx

# Export to JSON
/equity/price/historical --symbol AAPL --export json

# Export with custom filename
/equity/fundamental/metrics --symbol AAPL --export csv --sheet-name aapl_metrics
```

## 🔧 Provider Selection

### Available Providers
- **yfinance**: Yahoo Finance (free, comprehensive)
- **polygon**: Polygon.io (requires API key, real-time)
- **fred**: Federal Reserve data (free, economic data)
- **fmp**: Financial Modeling Prep (requires API key)
- **intrinio**: Intrinio (requires API key)
- **finviz**: Finviz (some features need Elite)

### Using Specific Providers
```bash
# Specify provider with --provider flag
/equity/fundamental/income --symbol AAPL --provider polygon
/equity/fundamental/income --symbol AAPL --provider yfinance
/equity/fundamental/income --symbol AAPL --provider fmp
```

## 📈 Common Workflows

### Complete Stock Analysis
```bash
# 1. Get current quote
/equity/price/quote --symbol AAPL

# 2. View historical performance
/equity/price/historical --symbol AAPL --start_date 2024-01-01

# 3. Check fundamentals
/equity/fundamental/income --symbol AAPL
/equity/fundamental/balance --symbol AAPL
/equity/fundamental/metrics --symbol AAPL

# 4. Review analyst opinions
/equity/estimates/consensus --symbol AAPL

# 5. Check news
/news/company --symbol AAPL --limit 5
```

### Market Overview
```bash
# 1. Major indices
/equity/price/quote --symbol SPY QQQ DIA IWM

# 2. Sector performance
/equity/sectors/performance

# 3. Market news
/news/general --limit 10

# 4. Economic indicators
/economy/fred --series DFF
/economy/calendar --days 7
```

### Comparative Analysis
```bash
# Compare multiple stocks
/equity/price/performance --symbol AAPL MSFT GOOGL AMZN --period 1y
/equity/fundamental/metrics --symbol AAPL MSFT GOOGL
/equity/compare/peers --symbol AAPL
```

### Economic Research
```bash
# US Economic data
/economy/gdp --country united_states
/economy/inflation --country united_states
/economy/fred --series UNRATE

# Global comparison
/economy/gdp --country united_states china japan germany
```

## 🎨 Display Options

### Charting
```bash
# Display charts (when available)
/equity/price/historical --symbol AAPL --chart

# Technical indicators
/technical/sma --symbol AAPL --period 20
/technical/rsi --symbol AAPL
/technical/macd --symbol AAPL
```

### Table Formatting
```bash
# Limit results
/equity/fundamental/income --symbol AAPL --limit 4

# Sort results
/equity/price/performance --symbol AAPL MSFT GOOGL --sort returns
```

## ⚙️ Settings & Preferences

### Configure Settings
```bash
# View current settings
/settings

# Set preferences
/account/preferences

# API key management
/account/keys
```

## 📝 Recording & Automation

### Create Routines
```bash
# Start recording
/record

# Perform your analysis steps...
# (all commands are recorded)

# Stop and save
/stop --name my_analysis

# Execute saved routine
/exe --file my_analysis.openbb
```

## 🔍 Advanced Features

### Technical Analysis
```bash
# Moving averages
/technical/sma --symbol AAPL --period 50
/technical/ema --symbol AAPL --period 20

# Oscillators
/technical/rsi --symbol AAPL
/technical/stoch --symbol AAPL

# Trend indicators
/technical/adx --symbol AAPL
/technical/macd --symbol AAPL
```

### Quantitative Analysis
```bash
# Statistical measures
/quantitative/stats --symbol AAPL
/quantitative/correlation --symbols AAPL MSFT
/quantitative/volatility --symbol AAPL
```

### Econometrics
```bash
# Regression analysis
/econometrics/regression --dependent AAPL --independent SPY
/econometrics/correlation --data AAPL MSFT GOOGL
```

## 🌍 International Markets

### Access Global Data
```bash
# European stocks
/equity/price/quote --symbol ASML.AS  # ASML (Amsterdam)
/equity/price/quote --symbol MC.PA    # LVMH (Paris)

# Asian markets
/equity/price/quote --symbol 7203.T   # Toyota (Tokyo)
/equity/price/quote --symbol 005930.KS # Samsung (Korea)

# Chinese stocks (if supported)
/equity/price/quote --symbol 600519.SS # Kweichow Moutai
/equity/price/quote --symbol BABA      # Alibaba
```

## 💡 Pro Tips

### 1. Keyboard Shortcuts
- `TAB`: Auto-complete commands
- `CTRL+C`: Cancel current command
- `CTRL+D`: Exit OpenBB
- `CTRL+L`: Clear screen

### 2. Command Chaining
```bash
# Execute multiple commands in sequence
/equity/price/quote --symbol AAPL; /equity/fundamental/metrics --symbol AAPL
```

### 3. Wildcards & Multiple Symbols
```bash
# Multiple symbols at once
/equity/price/quote --symbol AAPL MSFT GOOGL AMZN

# Sector ETFs
/etf/price/performance --symbol XLK XLF XLE XLV XLI
```

### 4. Custom Export Paths
```bash
# Export to specific directory
/equity/fundamental/income --symbol AAPL --export csv --export-dir ~/Documents/
```

## 🚫 Common Issues & Solutions

### Issue: Command not recognized
**Solution**: Check spelling, use TAB for auto-complete

### Issue: No data returned
**Solution**: Check if API key is needed, verify symbol format

### Issue: Provider error
**Solution**: Try different provider, check API limits

### Issue: Export failed
**Solution**: Check write permissions, verify export path

## 📌 Quick Reference Card

### Most Used Commands
```bash
# Quick stock check
/equity/price/quote --symbol AAPL

# Historical data
/equity/price/historical --symbol AAPL --start_date 2024-01-01

# Fundamentals
/equity/fundamental/metrics --symbol AAPL

# News
/news/company --symbol AAPL

# Export data
--export csv
--export xlsx
--export json

# Exit
exit
```

## 🎯 ROIC Integration (Custom)

### Using ROIC Data
```bash
# Outside OpenBB (in terminal)
./roic quality AAPL
./roic forecast MSFT

# Combined analysis
source /Users/sdg223157/OPBB/openbb-env/bin/activate
python3 roic_wrapper.py AAPL
```

## 📚 Additional Resources

- **OpenBB Documentation**: https://docs.openbb.co
- **API Provider Docs**: Check each provider's documentation
- **Community Forum**: https://openbb.co/community
- **GitHub**: https://github.com/OpenBB-finance/OpenBBTerminal

## 🔄 Update & Maintenance

```bash
# Check version
/version

# Update OpenBB (outside CLI)
pip install --upgrade openbb

# Clear cache
/clear_cache
```

---

## 📋 Command Template

```
/category/subcategory/action --symbol SYMBOL --parameter VALUE --export FORMAT
```

**Remember**: 
- Always start commands with `/`
- Use `--help` with any command for detailed options
- TAB is your friend for auto-completion
- Export your analysis for record keeping

Happy analyzing! 🚀
