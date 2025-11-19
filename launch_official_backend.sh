#!/bin/bash
# Launch Official Pattern ROIC Backend for OpenBB

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Starting ROIC Backend (Official OpenBB Pattern)         ║"
echo "║   Based on: backends-for-openbb repository                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Navigate to OPBB directory
cd /Users/sdg223157/OPBB

# Activate virtual environment
source openbb-env/bin/activate

# Install dependencies if needed
pip install -q fastapi uvicorn 2>/dev/null

echo "🚀 Starting backend server..."
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "TO CONNECT IN OPENBB WORKSPACE:"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "1. Go to 'Add apps by connecting a backend'"
echo "2. Enter these details:"
echo "   • Name: ROIC Quality Metrics"
echo "   • URL: http://127.0.0.1:8000"
echo "   • Validate widgets: No"
echo ""
echo "3. Click 'Test' then 'Add'"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "Server starting at: http://127.0.0.1:8000"
echo "Widgets config at:  http://127.0.0.1:8000/widgets.json"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Run the official pattern backend
python openbb_roic_backend_official.py
