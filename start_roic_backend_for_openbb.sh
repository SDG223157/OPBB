#!/bin/bash
# Start ROIC Backend for OpenBB Integration

echo "═══════════════════════════════════════════════════════"
echo "   Starting ROIC Backend for OpenBB Integration"
echo "═══════════════════════════════════════════════════════"
echo ""

# Navigate to OPBB directory
cd /Users/sdg223157/OPBB

# Check if virtual environment exists
if [ ! -d "openbb-env" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv openbb-env"
    exit 1
fi

# Activate virtual environment
source openbb-env/bin/activate

# Install required packages if needed
echo "📦 Checking dependencies..."
pip install -q fastapi uvicorn 2>/dev/null

# Set environment variables
export OPENBB_API_HOST="127.0.0.1"
export OPENBB_API_PORT="8000"

echo ""
echo "🚀 Starting ROIC Backend Server..."
echo "═══════════════════════════════════════════════════════"
echo ""
echo "📍 Server URL: http://127.0.0.1:8000"
echo "📊 API Docs:  http://127.0.0.1:8000/docs"
echo "📱 Apps JSON: http://127.0.0.1:8000/apps.json"
echo ""
echo "═══════════════════════════════════════════════════════"
echo "TO CONNECT IN OPENBB:"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "1. Make sure this server is running (keep this terminal open)"
echo "2. In OpenBB, use this URL: http://127.0.0.1:8000"
echo "   (NOT http://0.0.0.0:8000)"
echo "3. Set 'Validate widgets' to 'No' if you see errors"
echo "4. Click 'Test' to verify connection"
echo "5. Click 'Add' to add the backend"
echo ""
echo "Press Ctrl+C to stop the server"
echo "═══════════════════════════════════════════════════════"
echo ""

# Start the server
python openbb_roic_backend.py
