# OpenBB ROIC Provider

A native provider extension for OpenBB Platform that adds ROIC (Return on Invested Capital) and quality investing metrics.

## Features

- **ROIC Calculation**: Automated Return on Invested Capital metrics
- **Quality Scoring**: 0-100 quality scores based on fundamentals
- **Moat Analysis**: Competitive advantage assessment
- **Smart Forecasting**: Quality-based 3-year price projections
- **Native Integration**: Works exactly like Yahoo Finance and FRED providers

## Installation

### Option 1: Install from Package
```bash
pip install openbb-roic
```

### Option 2: Install from Source
```bash
git clone https://github.com/SDG223157/OPBB.git
cd OPBB/openbb_roic_provider_package
pip install -e .
```

## Usage

Once installed, ROIC will be available as a provider in OpenBB:

```python
from openbb import obb

# Get ROIC metrics
metrics = obb.equity.fundamental.metrics(
    symbol="AAPL",
    provider="roic"
)

# Get quality-based forecast
forecast = obb.equity.estimates.price_target(
    symbol="AAPL", 
    provider="roic"
)
```

### CLI Usage

```bash
# In OpenBB CLI
/equity/fundamental/metrics --symbol AAPL --provider roic
/equity/estimates/price_target --symbol MSFT --provider roic
```

## Provider Endpoints

| Endpoint | Description |
|----------|-------------|
| `/equity/fundamental/metrics` | ROIC and quality metrics |
| `/equity/estimates/price_target` | Quality-based price targets |

## Metrics Provided

- **ROIC**: Return on Invested Capital (%)
- **Quality Score**: 0-100 scale based on fundamentals
- **Moat Rating**: Wide/Narrow/None competitive advantage
- **Growth Rate**: Quality-implied growth rate
- **Price Targets**: 1, 2, and 3-year targets based on quality

## Requirements

- OpenBB Platform >= 1.0.0
- Python >= 3.8
- pandas >= 1.5.0
- pydantic >= 2.0.0

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions welcome! This provider demonstrates how to extend OpenBB with custom data sources.
