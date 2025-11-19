# 🚀 OPBB - OpenBB Platform with ROIC Integration

Advanced financial analysis platform combining OpenBB's market data capabilities with custom ROIC (Return on Invested Capital) quality metrics.

## 📊 Features

- **OpenBB CLI Integration**: Full OpenBB platform for market data, news, and analysis
- **ROIC Quality Metrics**: Custom CLI tool for fundamental quality analysis
- **🆕 Unified Analysis**: Master tool combining OpenBB + ROIC data seamlessly
- **Multi-Provider Support**: Yahoo Finance, Polygon, Finviz Elite, FRED, and ROIC.ai
- **Historical Analysis**: 10-year ROIC trends for any stock (including Chinese A-shares)
- **Smart Forecasting**: Quality-based 3-year price projections
- **Professional Display**: Both terminal and OpenBB-style table formats
- **🆕 Integration Wrappers**: Python scripts that merge OpenBB and ROIC metrics

## 🎯 Quick Start

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/SDG223157/OPBB.git
cd OPBB
```

2. **Set up virtual environment**
```bash
python3 -m venv openbb-env
source openbb-env/bin/activate
pip install openbb-cli
```

3. **Launch OpenBB**
```bash
./launch-openbb-premium.sh
```

### 🆕 Master Analysis Tool

```bash
# Complete analysis combining OpenBB + ROIC
./analyze AAPL              # Full analysis
./analyze MSFT roic         # ROIC metrics only
./analyze NVDA forecast     # Price targets
./analyze compare AAPL GOOGL MSFT  # Compare multiple
```

### Using ROIC Tools

```bash
# Quality metrics
./roic quality AAPL

# 3-year forecast
./roic forecast MSFT

# Compare companies
./roic compare AAPL MSFT GOOGL

# Historical analysis
./roic historical 600519.SS --years 10
```

### Integration Features

```bash
# Combined OpenBB + ROIC data
python roic_wrapper.py AAPL

# Hybrid launcher
python hybrid_launcher.py roic AAPL  # ROIC data
python hybrid_launcher.py            # Launch OpenBB
```

## 📈 Available Commands

### OpenBB Commands
- `/equity/price/quote --symbol AAPL --provider yfinance`
- `/news/company --symbol AAPL --provider polygon`
- `/economy/fred_series --symbol VIXCLS --provider fred`
- `/equity/estimates/price_target --symbol AAPL --provider finviz`

### ROIC Commands
- `./roic quality [SYMBOL]` - Get ROIC and quality metrics
- `./roic forecast [SYMBOL]` - Quality-based 3-year forecast
- `./roic compare [SYMBOLS...]` - Compare multiple stocks
- `./roic historical [SYMBOL]` - Historical ROIC analysis
- `./roic style [openbb|custom]` - Switch display style

## 🔑 API Configuration

### Required API Keys
- **Polygon.io**: Real-time market data and news
- **Finviz Elite**: Analyst price targets
- **FRED**: Economic indicators and commodity prices
- **ROIC.ai**: Quality metrics (optional)

### Setting API Keys
```bash
# Run setup scripts
python set_polygon_key.py
python set_finviz_key.py
python set_fred_key.py
python set_roic_key.py
```

## 📊 Example Analysis

### Apple (AAPL) Quality Metrics
```
ROIC: 51.54%
Quality Score: 95/100
Competitive Moat: Wide
3-Year Target: $439 (+64%)
```

### Chinese Stocks Support
```bash
# Kweichow Moutai
./roic historical 600519.SS

# BYD
./roic quality 002594.SZ
```

## 🏗️ Project Structure

```
OPBB/
├── openbb-env/              # Virtual environment
├── launch-openbb-*.sh       # Launch scripts with API keys
├── roic*                    # ROIC CLI tool and modules
├── get_*.py                 # Data fetching scripts
├── master_forecast.py       # Comprehensive analysis tool
├── commodity_dashboard*.py  # Commodity market tools
├── *.md                     # Documentation
└── API setup scripts
```

## 💡 Key Features

### 1. Master Forecast Tool
Combines all data sources for institutional-grade analysis:
```bash
python master_forecast.py
```

### 2. Display Styles
Switch between custom and OpenBB-style output:
```bash
./roic style openbb  # Professional tables
./roic style custom  # Clean text format
```

### 3. Export Capabilities
All tools support data export:
```bash
./roic quality AAPL --export csv
./roic historical MSFT --export xlsx
```

## 📚 Documentation

- [ROIC CLI Integration](ROIC_CLI_INTEGRATION.md)
- [API Setup Guide](API_KEYS_SETUP.md)
- [Display Styles](ROIC_DISPLAY_STYLES.md)
- [Chinese Stocks Guide](get_chinese_stock_data.py)
- [Commodity Guide](commodity_guide.md)
- [FRED Economic Guide](fred_economic_guide.md)

## 🤝 Contributing

Contributions are welcome! This project demonstrates:
- Custom OpenBB provider development
- CLI tool integration
- Financial data analysis
- Multi-API orchestration

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- OpenBB Platform for the excellent financial data framework
- ROIC.ai for quality investing methodology
- All data providers (Yahoo, Polygon, Finviz, FRED)

## 📞 Contact

- GitHub: [@SDG223157](https://github.com/SDG223157)
- Project: [OPBB Repository](https://github.com/SDG223157/OPBB)

---
*Built with ❤️ for quality-focused financial analysis*