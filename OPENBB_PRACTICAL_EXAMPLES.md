# 🎯 OpenBB Practical Examples - Real Use Cases

## 📈 Example 1: Complete Apple Analysis

```bash
# Launch OpenBB
./launch-openbb-premium.sh

# Step 1: Current situation
/equity/price/quote --symbol AAPL
# Output: Current price, day change, volume

# Step 2: Recent performance
/equity/price/historical --symbol AAPL --start_date 2024-10-01 --end_date 2024-11-19
# Output: Daily prices for last ~6 weeks

# Step 3: Financial health
/equity/fundamental/metrics --symbol AAPL --provider yfinance
# Output: P/E ratio, profit margins, ROE, debt ratios

# Step 4: Income statement
/equity/fundamental/income --symbol AAPL --limit 4
# Output: Last 4 quarters of revenue, profit, EPS

# Step 5: Analyst views
/equity/estimates/consensus --symbol AAPL
# Output: Price targets, recommendations

# Step 6: Recent news
/news/company --symbol AAPL --limit 5
# Output: Latest 5 news articles

# Step 7: Export everything
/equity/fundamental/income --symbol AAPL --export xlsx --sheet-name apple_analysis
```

## 🏦 Example 2: Bank Sector Analysis

```bash
# Major bank stocks
/equity/price/performance --symbol JPM BAC WFC GS MS C --period 1m
# Output: 1-month performance comparison

# Bank ETF analysis
/etf/holdings --symbol XLF
# Output: Financial sector ETF holdings

# Compare fundamentals
/equity/fundamental/metrics --symbol JPM BAC WFC --provider finviz
# Output: Side-by-side metrics

# Interest rate impact
/economy/fred --series DFF
# Output: Federal funds rate trend
```

## 🌍 Example 3: Tech Giants Comparison

```bash
# FAANG performance
/equity/price/performance --symbol META AAPL AMZN NFLX GOOGL --period ytd
# Output: Year-to-date returns

# Key metrics comparison
/equity/fundamental/metrics --symbol META AAPL AMZN NFLX GOOGL
# Output: P/E, margins, growth rates

# Revenue comparison
/equity/fundamental/income --symbol META AAPL AMZN --limit 1
# Output: Latest quarter revenues

# Export comparison
/equity/fundamental/metrics --symbol META AAPL AMZN NFLX GOOGL --export csv
```

## 💰 Example 4: Dividend Portfolio Check

```bash
# Dividend aristocrats
/equity/price/quote --symbol JNJ PG KO PEP MMM

# Dividend information
/equity/fundamental/metrics --symbol JNJ PG KO --provider yfinance
# Look for: dividend_yield, payout_ratio

# Historical stability
/equity/price/historical --symbol JNJ --start_date 2020-01-01 --interval 1M
# Output: Monthly prices showing stability

# Income generation
/equity/fundamental/income --symbol JNJ PG KO --limit 4
# Output: Earnings consistency
```

## 📊 Example 5: Pre-Market Routine

```bash
# Start your day
./launch-openbb-premium.sh

# 1. Market futures
/equity/price/quote --symbol ES=F NQ=F YM=F  # S&P, Nasdaq, Dow futures

# 2. Economic calendar
/economy/calendar --days 1
# Output: Today's economic events

# 3. Market news
/news/general --limit 10
# Output: Latest market news

# 4. Your watchlist
/equity/price/quote --symbol AAPL MSFT NVDA TSLA SPY QQQ

# 5. Pre-market movers (if available)
/equity/discovery/gainers --limit 10
/equity/discovery/losers --limit 10
```

## 🔬 Example 6: Earnings Season Analysis

```bash
# Company reporting today
/equity/fundamental/calendar --symbol NVDA

# Last quarter's results
/equity/fundamental/income --symbol NVDA --limit 1

# Analyst expectations
/equity/estimates/consensus --symbol NVDA

# Historical earnings performance
/equity/fundamental/income --symbol NVDA --limit 8 --provider polygon

# Peer comparison
/equity/fundamental/metrics --symbol NVDA AMD INTC
```

## 📉 Example 7: Risk Assessment

```bash
# Volatility check
/equity/price/historical --symbol AAPL --start_date 2024-01-01
# Calculate standard deviation manually or observe price swings

# Market correlation
/equity/price/performance --symbol AAPL SPY --period 3m
# Compare movements

# Financial stability
/equity/fundamental/balance --symbol AAPL --limit 1
# Check: debt_to_equity, current_ratio

# Recent insider trading
/equity/ownership/insider --symbol AAPL
```

## 🌐 Example 8: Global Macro View

```bash
# US indicators
/economy/fred --series GDP
/economy/fred --series UNRATE
/economy/fred --series CPIAUCSL  # Inflation

# Currency movements
/currency/price/quote --symbol EURUSD
/currency/price/quote --symbol USDJPY
/currency/price/quote --symbol GBPUSD

# Global indices
/equity/price/quote --symbol ^GSPC ^IXIC ^DJI ^FTSE ^N225

# Commodities impact
/commodity/price/quote --symbol GC=F CL=F  # Gold, Oil
```

## 💼 Example 9: ETF Strategy Research

```bash
# Sector ETFs performance
/etf/price/performance --symbol XLK XLF XLV XLE XLI XLY --period 1m

# Top ETF holdings
/etf/holdings --symbol SPY --limit 10
/etf/holdings --symbol QQQ --limit 10

# Thematic ETFs
/etf/info --symbol ARKK  # Innovation
/etf/info --symbol ICLN  # Clean energy
/etf/info --symbol JETS  # Airlines

# Compare expense ratios
/etf/info --symbol SPY VOO IVV  # S&P 500 ETFs
```

## 🚀 Example 10: IPO/New Stock Research

```bash
# New IPO basic info
/equity/profile --symbol NEWSTOCK

# First day trading
/equity/price/historical --symbol NEWSTOCK --start_date [IPO_DATE]

# Comparison with sector
/equity/compare/peers --symbol NEWSTOCK

# Financial data (if available)
/equity/fundamental/income --symbol NEWSTOCK
```

## 📱 Example 11: Quick Morning Briefing Script

Save this as a routine:
```bash
/record
/economy/calendar --days 1
/news/general --limit 5
/equity/price/quote --symbol SPY QQQ DIA IWM
/equity/price/quote --symbol AAPL MSFT GOOGL AMZN NVDA
/economy/fred --series DFF
/stop --name morning_brief

# Run daily with:
/exe --file morning_brief.openbb
```

## 🔄 Example 12: Weekly Portfolio Review

```bash
# Your holdings (example)
/equity/price/performance --symbol AAPL MSFT VTI SCHD --period 1w

# Detailed metrics
/equity/fundamental/metrics --symbol AAPL MSFT VTI SCHD

# Any news on holdings
/news/company --symbol AAPL --limit 3
/news/company --symbol MSFT --limit 3

# Export for records
/equity/price/performance --symbol AAPL MSFT VTI SCHD --period 1w --export xlsx
```

## 💡 Combining with ROIC Analysis

```bash
# In OpenBB: Get financials
/equity/fundamental/income --symbol AAPL --export csv
exit

# In terminal: Get quality score
./roic quality AAPL
./roic forecast AAPL

# Combined view
python3 roic_wrapper.py AAPL
```

## 📝 Tips for Each Example

1. **Always export important analyses** - Add `--export csv` or `--export xlsx`
2. **Adjust time periods** - Change `--start` and `--end` dates as needed
3. **Try different providers** - Some have unique data points
4. **Save routines** - Use `/record` and `/stop` for repeated workflows
5. **Combine analyses** - Use multiple commands for complete picture

---

*These examples show real-world usage patterns. Modify symbols, dates, and parameters for your specific needs!*
