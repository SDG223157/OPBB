#!/bin/bash
# Launch custom-built OpenBB with ROIC provider

echo "==========================================="
echo "   OpenBB Platform (Custom Build)"
echo "   With Integrated ROIC Provider"
echo "==========================================="
echo ""
echo "✅ ROIC provider integrated natively"
echo "✅ Available in provider dropdown"
echo "✅ Shows in OpenBB display interface"
echo ""

# Activate the custom build environment
source /Users/sdg223157/openbb-build/build-env/bin/activate

# Set API keys
export OPENBB_API_POLYGON_KEY="Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai"
export OPENBB_API_FINVIZ_KEY="be56a0a4-c7b3-4094-85b6-0ad5a3b49fc6"
export OPENBB_API_FRED_KEY="7c26de454d31a77bfdf9aaa33f2f55a8"
export OPENBB_API_ROIC_KEY="a365bff224a6419fac064dd52e1f80d9"

# Launch OpenBB
openbb "$@"
