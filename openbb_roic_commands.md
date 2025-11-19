# 🦋 OpenBB CLI - ROIC Provider Commands

## Inside OpenBB CLI Commands

When you see the `(🦋) / $` prompt, you can use these commands:

### 📈 Basic ROIC Commands

```bash
# Get ROIC metrics for Apple
/equity/fundamental/metrics --symbol AAPL --provider roic

# Get ROIC metrics for Microsoft  
/equity/fundamental/metrics --symbol MSFT --provider roic

# Get ROIC metrics for Nvidia
/equity/fundamental/metrics --symbol NVDA --provider roic

# Get ROIC-based estimates
/equity/estimates/consensus --symbol AAPL --provider roic
```

### 🔄 Compare with Other Providers

```bash
# Compare ROIC with Yahoo Finance
/equity/fundamental/metrics --symbol AAPL --provider roic
/equity/fundamental/metrics --symbol AAPL --provider yfinance

# Compare ROIC with Polygon
/equity/fundamental/metrics --symbol AAPL --provider roic
/equity/fundamental/metrics --symbol AAPL --provider polygon
```

### 📊 Export ROIC Data

```bash
# Export ROIC data to CSV
/equity/fundamental/metrics --symbol AAPL --provider roic --export csv

# Export to JSON
/equity/fundamental/metrics --symbol AAPL --provider roic --export json

# Export to Excel
/equity/fundamental/metrics --symbol AAPL --provider roic --export xlsx
```

### 🎯 Batch Analysis

```bash
# Analyze multiple stocks with ROIC
/equity/fundamental/metrics --symbol AAPL --provider roic
/equity/fundamental/metrics --symbol MSFT --provider roic
/equity/fundamental/metrics --symbol GOOGL --provider roic
/equity/fundamental/metrics --symbol NVDA --provider roic
```

### 💡 Advanced Usage

```bash
# Get ROIC for Chinese stocks
/equity/fundamental/metrics --symbol 600519.SS --provider roic

# Get ROIC for ETFs
/equity/fundamental/metrics --symbol SPY --provider roic

# Set ROIC as default provider for session
/account/preferences --provider roic
```

## 📝 Expected Output Format

When you run `/equity/fundamental/metrics --symbol AAPL --provider roic`, you should see:

```
                    ROIC Fundamental Metrics                    
┏━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┓
┃ symbol ┃ roic        ┃ quality_score ┃ moat_rating┃ date    ┃
┡━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━┩
│ AAPL   │ 51.54%      │ 95            │ Wide       │ 2025-11 │
└────────┴─────────────┴───────────────┴────────────┴─────────┘
```

## ⚡ Quick Tips

1. **Tab Completion**: Type `/equity/fundamental/met` and press TAB
2. **Help**: Use `--help` with any command for options
3. **History**: Press ↑ arrow to recall previous commands
4. **Clear**: Type `/clear` to clear screen

## 🔍 Check Available Providers

```bash
# List all available providers
/account/providers

# Check if ROIC is available
/coverage/providers

# Get help on ROIC provider
/equity/fundamental/metrics --help
```

## ❓ Troubleshooting

If ROIC provider doesn't appear:
1. Exit OpenBB: `exit`
2. Check integration: `python3 test_roic_integration.py`
3. Relaunch OpenBB: `./launch-openbb-premium.sh`

## 🚀 Complete Workflow Example

```bash
# In OpenBB CLI:
/equity/fundamental/metrics --symbol AAPL --provider roic
/equity/price/historical --symbol AAPL --start 2024-01-01
/equity/fundamental/income --symbol AAPL --provider polygon
/equity/estimates/consensus --symbol AAPL --provider roic
/equity/fundamental/metrics --symbol AAPL --provider roic --export csv
```

This gives you a complete analysis using ROIC quality metrics alongside OpenBB's comprehensive financial data!
