#!/bin/bash
# OpenBB CLI Launch Script with ALL API Keys
# Includes Finviz Elite, Polygon, and FRED

# Set all API Keys
export FINVIZ_API_KEY="be56a0a4-c7b3-4094-85b6-0ad5a3b49fc6"
export OPENBB_API_FINVIZ_KEY="be56a0a4-c7b3-4094-85b6-0ad5a3b49fc6"
export POLYGON_API_KEY="Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai"
export OPENBB_API_POLYGON_KEY="Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai"
export FRED_API_KEY="7c26de454d31a77bfdf9aaa33f2f55a8"
export OPENBB_API_FRED_KEY="7c26de454d31a77bfdf9aaa33f2f55a8"

echo "=========================================="
echo "   OpenBB CLI - Complete Edition"
echo "=========================================="
echo "✅ Finviz Elite API loaded (Price Targets & Forecasts)"
echo "✅ Polygon API loaded (News & Market Data)"
echo "✅ FRED API loaded (Economic & Commodity Data)"
echo ""
echo "📊 NEW FORECAST COMMANDS AVAILABLE:"
echo "   /equity/estimates/price_target --symbol AAPL --provider finviz"
echo "   /equity/discovery/top_retail --provider finviz"
echo "   /equity/screener --provider finviz"
echo ""
echo "📈 EXAMPLE WORKFLOW:"
echo "   1. Get price target: /equity/estimates/price_target --symbol AAPL --provider finviz"
echo "   2. Get news: /news/company --symbol AAPL --provider polygon"
echo "   3. Get fundamentals: /equity/fundamental/income --symbol AAPL --provider yfinance"
echo "=========================================="
echo ""

# Activate the virtual environment
source /Users/sdg223157/OPBB/openbb-env/bin/activate

# Launch OpenBB CLI with all arguments passed to this script
openbb "$@"
