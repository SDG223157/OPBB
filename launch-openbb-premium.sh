#!/bin/bash
# OpenBB CLI Launch Script - PREMIUM EDITION
# Includes ALL Premium APIs: ROIC.ai, Finviz Elite, Polygon, and FRED

# Set all API Keys
export ROIC_API_KEY="a365bff224a6419fac064dd52e1f80d9"
export OPENBB_API_ROIC_KEY="a365bff224a6419fac064dd52e1f80d9"
export FINVIZ_API_KEY="be56a0a4-c7b3-4094-85b6-0ad5a3b49fc6"
export OPENBB_API_FINVIZ_KEY="be56a0a4-c7b3-4094-85b6-0ad5a3b49fc6"
export POLYGON_API_KEY="Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai"
export OPENBB_API_POLYGON_KEY="Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai"
export FRED_API_KEY="7c26de454d31a77bfdf9aaa33f2f55a8"
export OPENBB_API_FRED_KEY="7c26de454d31a77bfdf9aaa33f2f55a8"

echo "=============================================="
echo "   OpenBB CLI - PREMIUM EDITION"
echo "   With Advanced Fundamental Analysis"
echo "=============================================="
echo "✅ ROIC.ai: Quality & ROIC Analysis"
echo "✅ Finviz Elite: Analyst Price Targets"
echo "✅ Polygon: Real-time Market Data"
echo "✅ FRED: Economic Indicators"
echo ""
echo "📊 ADVANCED FORECAST CAPABILITIES:"
echo "   • Quality-based valuations (ROIC > 50% = Premium)"
echo "   • Professional analyst targets (12-month)"
echo "   • Real-time market sentiment"
echo "   • Economic context analysis"
echo ""
echo "🎯 PREMIUM COMMANDS:"
echo "   /equity/estimates/price_target --symbol AAPL --provider finviz"
echo "   /news/company --symbol AAPL --provider polygon"
echo "   /economy/fred_series --symbol SP500 --provider fred"
echo "   python roic_analysis.py  # For ROIC metrics"
echo "=============================================="
echo ""

# Activate the virtual environment
source /Users/sdg223157/OPBB/openbb-env/bin/activate

# Launch OpenBB CLI with all arguments passed to this script
openbb "$@"
