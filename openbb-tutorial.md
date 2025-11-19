# OpenBB CLI Tutorial & Usage Guide

## Starting OpenBB CLI

### Method 1: Using the Launch Script
```bash
cd /Users/sdg223157/OPBB
./launch-openbb.sh
```

### Method 2: Manual Activation
```bash
cd /Users/sdg223157/OPBB
source openbb-env/bin/activate
openbb
```

## Basic Navigation

OpenBB CLI uses a menu-based navigation system similar to a file system:
- **/** - Root menu
- **Tab** - Auto-complete commands
- **Enter** - Execute command
- **q** or **quit** - Exit current menu or quit OpenBB
- **help** - Show available commands in current menu
- **?** - Get help for a specific command

## Core Menus & Commands

### 1. Equity Analysis (`/equity`)
```bash
/equity                 # Enter equity menu
/equity/price           # Price data menu
/equity/fundamental     # Fundamental analysis
/equity/discovery       # Stock discovery tools
/equity/screener       # Stock screener
```

#### Example: Get Apple Stock Price
```bash
/equity/price/quote --symbol AAPL --provider yfinance
```

#### Example: Get Historical Data
```bash
/equity/price/historical --symbol MSFT --start_date 2024-01-01 --provider yfinance
```

### 2. Cryptocurrency (`/crypto`)
```bash
/crypto                 # Enter crypto menu
/crypto/price          # Crypto price data
/crypto/discovery      # Discover cryptocurrencies
```

#### Example: Get Bitcoin Price
```bash
/crypto/price/quote --symbol BTCUSD --provider yfinance
```

### 3. Economic Data (`/economy`)
```bash
/economy               # Enter economy menu
/economy/gdp          # GDP data
/economy/inflation    # Inflation data
/economy/unemployment # Unemployment data
```

#### Example: Get US GDP Data
```bash
/economy/gdp --country united_states --provider oecd
```

### 4. ETF Analysis (`/etf`)
```bash
/etf                   # Enter ETF menu
/etf/discovery        # ETF discovery
/etf/price           # ETF price data
```

#### Example: Get SPY ETF Information
```bash
/etf/price/quote --symbol SPY --provider yfinance
```

### 5. Fixed Income (`/fixedincome`)
```bash
/fixedincome          # Enter fixed income menu
/fixedincome/treasury # Treasury rates
```

#### Example: Get Treasury Rates
```bash
/fixedincome/treasury/rates --provider federal_reserve
```

### 6. Technical Analysis (`/technical`)
```bash
/technical            # Enter technical analysis menu
/technical/sma       # Simple Moving Average
/technical/rsi       # Relative Strength Index
/technical/macd      # MACD indicator
```

### 7. News (`/news`)
```bash
/news                 # Enter news menu
/news/world          # World news
/news/company        # Company-specific news
```

#### Example: Get News for a Company
```bash
/news/company --symbol TSLA --provider benzinga
```

## Advanced Features

### 1. Charting
OpenBB CLI can create charts for visualizing data:
```bash
/equity/price/historical --symbol AAPL --start_date 2024-01-01 --chart true
```

### 2. Exporting Data
Export data to various formats (CSV, JSON, XLSX):
```bash
/equity/price/historical --symbol GOOGL --export csv
```

### 3. Multiple Symbols
Many commands support multiple symbols:
```bash
/equity/price/quote --symbol AAPL,MSFT,GOOGL --provider yfinance
```

### 4. Setting Preferences
You can set default providers and preferences:
```bash
/account/preferences  # View and set preferences
```

## Practical Examples

### Example 1: Quick Stock Analysis
```bash
# Start OpenBB
./launch-openbb.sh

# Get quote for Apple
/equity/price/quote --symbol AAPL

# Get recent news
/news/company --symbol AAPL

# Get fundamental data
/equity/fundamental/income --symbol AAPL

# Exit
quit
```

### Example 2: Market Overview
```bash
# Start OpenBB
./launch-openbb.sh

# Check major indices
/index/price/quote --symbol SPX,DJI,NDX

# Get market movers
/equity/discovery/gainers

# Check economic indicators
/economy/inflation --country united_states

# Exit
quit
```

### Example 3: Crypto Analysis
```bash
# Start OpenBB
./launch-openbb.sh

# Get Bitcoin price
/crypto/price/quote --symbol BTCUSD

# Get historical data with chart
/crypto/price/historical --symbol BTCUSD --start_date 2024-01-01 --chart true

# Exit
quit
```

## Tips and Tricks

1. **Tab Completion**: Use Tab key extensively to discover commands and auto-complete
2. **Help Command**: Type `help` in any menu to see available commands
3. **Command History**: Use arrow keys to navigate command history
4. **Providers**: Different providers offer different data - experiment to find what works best
5. **Free vs Paid**: Most yfinance commands are free; some providers require API keys

## Common Providers

- **yfinance**: Free, no API key required (most common)
- **alpha_vantage**: Free with API key
- **polygon**: Requires API key
- **fmp**: Financial Modeling Prep (API key required)
- **fred**: Federal Reserve data (free)
- **oecd**: Economic data (free)

## Setting API Keys

If you want to use providers that require API keys:
```bash
# In OpenBB CLI
/account/credentials

# Or set in environment before starting
export OPENBB_API_POLYGON_KEY="your_key_here"
```

## Troubleshooting

1. **Command Not Found**: Make sure you're in the right menu
2. **No Data Returned**: Try a different provider
3. **Rate Limits**: Some free providers have rate limits
4. **Date Format**: Use YYYY-MM-DD format for dates

## Exit OpenBB

To exit OpenBB CLI:
- Type `quit` or `q`
- Or use Ctrl+D
