#!/bin/bash
# OpenBB CLI Launch Script with All API Keys
# This script activates the virtual environment and launches OpenBB with your API keys

# Set API Keys
export POLYGON_API_KEY="Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai"
export OPENBB_API_POLYGON_KEY="Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai"
export FRED_API_KEY="7c26de454d31a77bfdf9aaa33f2f55a8"
export OPENBB_API_FRED_KEY="7c26de454d31a77bfdf9aaa33f2f55a8"

echo "=========================================="
echo "OpenBB CLI - Full API Access Enabled"
echo "=========================================="
echo "✅ Polygon API key loaded (News & Market Data)"
echo "✅ FRED API key loaded (Commodities & Economic Data)"
echo ""
echo "📊 Commodity Commands Now Available:"
echo "   /commodity/price/spot --provider fred"
echo "   /economy/fred_series --series_id DCOILWTICO"  
echo "   /economy/fred_series --series_id GOLDAMGBD228NLBM"
echo ""
echo "📰 News Commands:"
echo "   /news/company --symbol AAPL --provider polygon"
echo "=========================================="
echo ""

# Activate the virtual environment
source /Users/sdg223157/OPBB/openbb-env/bin/activate

# Launch OpenBB CLI with all arguments passed to this script
openbb "$@"
