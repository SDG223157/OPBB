# 🏗️ Building OpenBB from Source with ROIC Provider

## Overview

This guide shows how to build OpenBB from source with ROIC integrated as a native provider, making it work exactly like Yahoo Finance and FRED in the OpenBB interface.

## 📋 Prerequisites

- Python 3.8+
- Git
- Virtual environment tool (venv)
- ~2GB disk space for build

## 🚀 Quick Build (Automated)

```bash
cd /Users/sdg223157/OPBB
chmod +x build_openbb_with_roic.sh
./build_openbb_with_roic.sh
```

## 📝 Manual Build Process

### Step 1: Clone OpenBB Source

```bash
# Clone OpenBB repository
git clone https://github.com/OpenBB-finance/OpenBB.git ~/openbb-source
cd ~/openbb-source
```

### Step 2: Install ROIC Provider Package

```bash
# Navigate to ROIC provider package
cd /Users/sdg223157/OPBB/openbb_roic_provider_package

# Install in development mode
pip install -e .
```

### Step 3: Build OpenBB with ROIC

```bash
# Create virtual environment for custom build
python3 -m venv ~/openbb-custom-env
source ~/openbb-custom-env/bin/activate

# Install OpenBB from source
cd ~/openbb-source
pip install -e .

# Install ROIC provider
pip install /Users/sdg223157/OPBB/openbb_roic_provider_package
```

### Step 4: Verify Installation

```python
# Test in Python
from openbb import obb

# List available providers
print(obb.coverage.providers)  # Should include 'roic'

# Test ROIC provider
data = obb.equity.fundamental.metrics(symbol="AAPL", provider="roic")
print(data)
```

## 🎯 Alternative: Lightweight Integration

If building from source is too complex, use this lightweight approach:

### Option A: Provider Extension Package

1. **Package the ROIC provider**:
```bash
cd /Users/sdg223157/OPBB/openbb_roic_provider_package
python -m build
```

2. **Install alongside OpenBB**:
```bash
pip install dist/openbb_roic-1.0.0-py3-none-any.whl
```

3. **OpenBB will auto-discover the provider**

### Option B: Monkey Patch Method

```python
# roic_integration.py
import sys
sys.path.append('/Users/sdg223157/OPBB')

from openbb import obb
from openbb_roic_provider_package.openbb_roic import roic_provider

# Register ROIC provider
obb.provider.register(roic_provider)

# Now ROIC is available
data = obb.equity.fundamental.metrics(symbol="AAPL", provider="roic")
```

## 📊 Using ROIC in OpenBB

### CLI Commands

```bash
# Launch custom OpenBB build
~/openbb-custom-env/bin/openbb

# Use ROIC provider
/equity/fundamental/metrics --symbol AAPL --provider roic
/equity/estimates/price_target --symbol MSFT --provider roic
```

### Python SDK

```python
from openbb import obb

# ROIC metrics
metrics = obb.equity.fundamental.metrics(
    symbol="AAPL",
    provider="roic"  # ← ROIC provider
)

# Quality forecast
forecast = obb.equity.estimates.price_target(
    symbol="AAPL",
    provider="roic"
)

# Compare providers
yahoo_data = obb.equity.fundamental.metrics("AAPL", provider="yfinance")
roic_data = obb.equity.fundamental.metrics("AAPL", provider="roic")
```

## 🔧 Troubleshooting

### Issue: ROIC provider not showing

**Solution 1**: Ensure provider is installed
```bash
pip list | grep openbb-roic
```

**Solution 2**: Check provider registration
```python
from openbb import obb
print(obb.coverage.providers)
```

**Solution 3**: Manually register
```python
from openbb_roic import roic_provider
obb.provider.register(roic_provider)
```

### Issue: Import errors

**Solution**: Fix Python path
```python
import sys
sys.path.append('/Users/sdg223157/OPBB/openbb_roic_provider_package')
```

## 📁 File Structure

```
openbb_roic_provider_package/
├── pyproject.toml           # Package configuration
├── setup.py                  # Setup script
├── README.md                 # Provider documentation
└── openbb_roic/
    ├── __init__.py          # Provider registration
    └── models/
        ├── __init__.py
        ├── fundamental_metrics.py  # ROIC metrics model
        └── quality_forecast.py     # Forecast model
```

## ✅ What You Get

Once built, ROIC will:
- ✅ Appear in provider dropdown
- ✅ Show in OpenBB's native display
- ✅ Work with all OpenBB features
- ✅ Export to CSV/JSON/Excel
- ✅ Support pagination and filtering

## 🎉 Success Indicators

You know it's working when:

1. **Provider appears in list**:
```python
obb.coverage.providers
# Output: [..., 'roic', ...]
```

2. **Commands work**:
```bash
/equity/fundamental/metrics --symbol AAPL --provider roic
# Shows ROIC data in OpenBB display
```

3. **Provider dropdown shows ROIC**:
```
--provider [yfinance | polygon | fred | roic]
                                         ^^^^
```

## 🚀 Launch Script

Create a launch script for the custom build:

```bash
#!/bin/bash
# launch-openbb-roic.sh

source ~/openbb-custom-env/bin/activate

# Set API keys
export OPENBB_API_ROIC_KEY="your_key"
export OPENBB_API_POLYGON_KEY="your_key"
export OPENBB_API_FINVIZ_KEY="your_key"
export OPENBB_API_FRED_KEY="your_key"

# Launch OpenBB with ROIC
openbb "$@"
```

## 📚 Additional Resources

- [OpenBB Provider Development](https://docs.openbb.co/platform/development/providers)
- [OpenBB Source Code](https://github.com/OpenBB-finance/OpenBB)
- [ROIC Provider Source](https://github.com/SDG223157/OPBB)

## Summary

Building OpenBB from source with ROIC gives you:
- Native integration like Yahoo/FRED
- Full OpenBB display features
- Provider dropdown inclusion
- Complete API compatibility

Choose the method that works best for your setup!
