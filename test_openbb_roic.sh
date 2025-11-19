#!/bin/bash
# Test ROIC commands in OpenBB CLI

echo "======================================"
echo "  Testing ROIC in OpenBB CLI"
echo "======================================"
echo ""
echo "This script will launch OpenBB and run ROIC commands"
echo ""

# Create a temporary OpenBB script
cat > /tmp/openbb_roic_test.openbb << 'EOF'
# Test ROIC provider commands
/equity/fundamental/metrics --symbol AAPL --provider roic
/equity/fundamental/metrics --symbol MSFT --provider roic
/equity/estimates/consensus --symbol AAPL --provider roic
exit
EOF

echo "Running OpenBB with ROIC commands..."
echo "--------------------------------------"

# Launch OpenBB with the script
cd /Users/sdg223157/OPBB-1
source /Users/sdg223157/OPBB/openbb-env/bin/activate
openbb < /tmp/openbb_roic_test.openbb

echo ""
echo "======================================"
echo "  Test Complete!"
echo "======================================"
echo ""
echo "To use ROIC in OpenBB CLI manually:"
echo "1. Launch OpenBB: ./launch-openbb-premium.sh"
echo "2. Run: /equity/fundamental/metrics --symbol AAPL --provider roic"
echo ""
