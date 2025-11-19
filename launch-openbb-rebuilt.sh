#!/bin/bash
# Launch OpenBB with ROIC Provider Support

echo "==========================================="
echo "   OpenBB Platform + ROIC Integration"
echo "==========================================="
echo ""

# Add ROIC provider to Python path
export PYTHONPATH="/Users/sdg223157/openbb-build-v2/openbb-roic-provider:$PYTHONPATH"

# Set API keys
export OPENBB_API_POLYGON_KEY="Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai"
export OPENBB_API_FINVIZ_KEY="be56a0a4-c7b3-4094-85b6-0ad5a3b49fc6"
export OPENBB_API_FRED_KEY="7c26de454d31a77bfdf9aaa33f2f55a8"
export OPENBB_API_ROIC_KEY="a365bff224a6419fac064dd52e1f80d9"

# Launch OpenBB
if command -v openbb &> /dev/null; then
    echo "✅ Launching OpenBB with ROIC support..."
    echo ""
    echo "Note: ROIC provider functions are available via Python API"
    echo "Example: from openbb_roic import ROICProvider"
    echo ""
    openbb "$@"
else
    echo "⚠️ OpenBB CLI not found. Installing..."
    pip install openbb
    openbb "$@"
fi
