# 🚀 OpenBB Quick Reference Guide

## 🔥 Most Used Commands

### Launch OpenBB
```bash
./launch-openbb-premium.sh
```

### Essential Stock Commands
```bash
# Current price
/equity/price/quote --symbol AAPL

# Historical prices
/equity/price/historical --symbol AAPL --start 2024-01-01

# Key metrics
/equity/fundamental/metrics --symbol AAPL --provider yfinance

# Financial statements
/equity/fundamental/income --symbol AAPL
/equity/fundamental/balance --symbol AAPL
/equity/fundamental/cash --symbol AAPL

# News
/news/company --symbol AAPL --limit 5
```

### Economic Data
```bash
# Key indicators
/economy/fred --series GDP      # GDP
/economy/fred --series UNRATE   # Unemployment
/economy/fred --series DFF      # Fed funds rate
/economy/calendar --days 7      # Economic calendar
```

### Export Data
```bash
# Add to any command
--export csv
--export xlsx
--export json
```

## ⌨️ Navigation Shortcuts

| Key | Action |
|-----|--------|
| `TAB` | Auto-complete |
| `↑/↓` | Command history |
| `/` | Home menu |
| `exit` | Quit OpenBB |
| `?` | Help |

## 🏷️ Provider Options

```bash
--provider yfinance   # Free, reliable
--provider polygon    # Real-time (needs key)
--provider fred      # Economic data
--provider finviz    # Screener data
```

## 📊 Quick Analysis Workflow

```bash
# 1. Quick overview
/equity/price/quote --symbol AAPL

# 2. Fundamentals check
/equity/fundamental/metrics --symbol AAPL

# 3. Recent news
/news/company --symbol AAPL --limit 3

# 4. Export results
/equity/fundamental/income --symbol AAPL --export csv
```

## 🎯 Compare Stocks

```bash
# Multiple symbols
/equity/price/performance --symbol AAPL MSFT GOOGL
/equity/fundamental/metrics --symbol AAPL MSFT GOOGL
```

## 💡 Pro Tips

1. **TAB everything** - Auto-complete saves time
2. **Chain commands** - Use `;` between commands
3. **Export often** - Keep records with `--export csv`
4. **Try providers** - Different providers have different data

## 🔧 Fix Common Issues

**No data?** → Try different provider
**Command error?** → Use TAB to auto-complete
**Need help?** → Add `--help` to any command

## 📱 ROIC Quality Check (Custom)

```bash
# Exit OpenBB first, then:
./roic quality AAPL
./roic forecast MSFT
python3 roic_wrapper.py AAPL
```

---
*Keep this guide handy for quick reference!*
