#!/bin/bash
# Install ROIC as an OpenBB Provider Extension

echo "================================================"
echo "   Installing ROIC as OpenBB Provider"
echo "================================================"
echo ""

# Navigate to OPBB directory
cd /Users/sdg223157/OPBB

# Step 1: Copy ROIC calculator to provider package
echo "📦 Step 1: Preparing provider package..."
cp openbb_roic_provider.py openbb_roic_provider_package/openbb_roic/utils.py

# Step 2: Install the provider package
echo ""
echo "🔧 Step 2: Installing ROIC provider..."
cd openbb_roic_provider_package

# Activate OpenBB environment
source ../openbb-env/bin/activate

# Install the package in development mode
pip install -e .

echo ""
echo "✅ ROIC provider installed!"

# Step 3: Test the installation
echo ""
echo "🧪 Step 3: Testing provider..."
python -c "
try:
    from openbb_roic import roic_provider
    print('✅ Provider imports successfully')
    print(f'   Name: {roic_provider.name}')
    print(f'   Display: {roic_provider.display_name}')
except Exception as e:
    print(f'❌ Error: {e}')
"

# Step 4: Create test script
echo ""
echo "📝 Step 4: Creating test script..."
cat > ../test_roic_provider.py << 'EOF'
#!/usr/bin/env python3
"""Test ROIC Provider in OpenBB"""

import sys
sys.path.insert(0, '/Users/sdg223157/OPBB/openbb_roic_provider_package')

try:
    from openbb import obb
    print("Testing ROIC provider integration...")
    
    # Try to use ROIC provider
    # Note: This will only work if OpenBB can discover the provider
    providers = obb.coverage.providers if hasattr(obb.coverage, 'providers') else []
    
    if 'roic' in providers:
        print("✅ ROIC provider is registered!")
        
        # Test getting data
        data = obb.equity.fundamental.metrics(symbol="AAPL", provider="roic")
        print(f"✅ ROIC data retrieved: {data}")
    else:
        print("⚠️  ROIC provider not yet registered in OpenBB")
        print("    You may need to restart OpenBB or rebuild from source")
        
except Exception as e:
    print(f"Note: {e}")
    print("\nTo fully integrate ROIC, you need to either:")
    print("1. Rebuild OpenBB from source with ROIC included")
    print("2. Wait for OpenBB to add plugin discovery")
    print("3. Use the standalone ROIC CLI tool")
EOF

echo ""
echo "================================================"
echo "   Installation Complete!"
echo "================================================"
echo ""
echo "ROIC provider package is installed."
echo ""
echo "To use ROIC in OpenBB:"
echo ""
echo "Option 1: If OpenBB supports dynamic providers:"
echo "  Launch OpenBB and use: --provider roic"
echo ""
echo "Option 2: Build OpenBB from source:"
echo "  ./build_openbb_with_roic.sh"
echo ""
echo "Option 3: Use standalone ROIC CLI:"
echo "  ./roic quality AAPL"
echo ""
echo "Test with: python test_roic_provider.py"
echo "================================================"
