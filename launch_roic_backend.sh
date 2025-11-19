#!/bin/bash
# Launch OpenBB ROIC Backend API Server

echo "╔════════════════════════════════════════════════════════╗"
echo "║          OpenBB ROIC Backend - Starting...             ║"
echo "╚════════════════════════════════════════════════════════╝"

# Navigate to OPBB directory
cd /Users/sdg223157/OPBB

# Activate virtual environment
source openbb-env/bin/activate

# Set API keys as environment variables
export OPENBB_API_POLYGON_KEY="Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai"
export OPENBB_API_FINVIZ_KEY="be56a0a4-c7b3-4094-85b6-0ad5a3b49fc6"
export OPENBB_API_FRED_KEY="7c26de454d31a77bfdf9aaa33f2f55a8"
export OPENBB_API_ROIC_KEY="a365bff224a6419fac064dd52e1f80d9"

# Optional: Configure host and port
export OPENBB_API_HOST="${OPENBB_API_HOST:-127.0.0.1}"
export OPENBB_API_PORT="${OPENBB_API_PORT:-8000}"

# Launch the backend
python openbb_roic_backend.py
