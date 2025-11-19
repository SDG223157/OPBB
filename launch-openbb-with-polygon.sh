#!/bin/bash
# OpenBB CLI Launch Script with Polygon API Key
# This script activates the virtual environment and launches the OpenBB CLI with your API key

# Set Polygon API Key
export POLYGON_API_KEY="Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai"
export OPENBB_API_POLYGON_KEY="Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai"
export OPENBB_POLYGON_API_KEY="Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai"

echo "=========================================="
echo "OpenBB CLI - Polygon.io API Enabled"
echo "=========================================="
echo "✅ Polygon API key loaded"
echo "📰 News commands now available:"
echo "   /news/company --symbol AAPL --provider polygon"
echo "   /news/world --provider polygon"
echo "=========================================="
echo ""

# Activate the virtual environment
source /Users/sdg223157/OPBB/openbb-env/bin/activate

# Launch OpenBB CLI with all arguments passed to this script
openbb "$@"
