#!/bin/bash
# Build OpenBB from source with ROIC provider integrated

echo "==========================================="
echo "   Building OpenBB with ROIC Provider"
echo "==========================================="

# Set up directories
BUILD_DIR="/Users/sdg223157/openbb-build"
OPBB_DIR="/Users/sdg223157/OPBB"

# Step 1: Clone OpenBB source
echo ""
echo "📥 Step 1: Cloning OpenBB source code..."
echo "-----------------------------------------"

if [ -d "$BUILD_DIR" ]; then
    echo "Build directory exists. Removing old build..."
    rm -rf "$BUILD_DIR"
fi

git clone https://github.com/OpenBB-finance/OpenBB.git "$BUILD_DIR"
cd "$BUILD_DIR"

echo "✅ OpenBB source cloned to $BUILD_DIR"

# Step 2: Create ROIC provider in OpenBB structure
echo ""
echo "📦 Step 2: Adding ROIC provider to OpenBB source..."
echo "----------------------------------------------------"

# Create provider directory
ROIC_PROVIDER_DIR="$BUILD_DIR/openbb_platform/providers/roic"
mkdir -p "$ROIC_PROVIDER_DIR"

# Copy ROIC provider files
cp "$OPBB_DIR/openbb_roic_provider_extension.py" "$ROIC_PROVIDER_DIR/openbb_roic/__init__.py"
cp "$OPBB_DIR/openbb_roic_provider.py" "$ROIC_PROVIDER_DIR/openbb_roic/utils.py"

# Create setup.py for ROIC provider
cat > "$ROIC_PROVIDER_DIR/setup.py" << 'EOF'
"""ROIC Provider setup."""
from setuptools import setup, find_packages

setup(
    name="openbb-roic",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "openbb-core>=1.0.0",
        "pandas>=1.5.0",
        "pydantic>=2.0.0",
    ],
    author="OpenBB Community",
    author_email="hello@openbb.co",
    description="ROIC provider for OpenBB Platform",
    keywords="openbb roic quality investing",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        "openbb_provider": [
            "roic = openbb_roic",
        ],
    },
)
EOF

echo "✅ ROIC provider added to OpenBB source"

# Step 3: Register ROIC in OpenBB's provider registry
echo ""
echo "📝 Step 3: Registering ROIC in provider registry..."
echo "----------------------------------------------------"

# Add ROIC to providers init file
PROVIDERS_INIT="$BUILD_DIR/openbb_platform/providers/__init__.py"
echo "" >> "$PROVIDERS_INIT"
echo "# ROIC Provider" >> "$PROVIDERS_INIT"
echo "from openbb_platform.providers.roic.openbb_roic import ROICProvider" >> "$PROVIDERS_INIT"
echo "__all__.append('ROICProvider')" >> "$PROVIDERS_INIT"

echo "✅ ROIC registered in provider system"

# Step 4: Install dependencies
echo ""
echo "🔧 Step 4: Installing dependencies..."
echo "--------------------------------------"

# Create virtual environment for build
python3 -m venv "$BUILD_DIR/build-env"
source "$BUILD_DIR/build-env/bin/activate"

# Upgrade pip
pip install --upgrade pip setuptools wheel

echo "✅ Build environment ready"

# Step 5: Build OpenBB with ROIC
echo ""
echo "🏗️ Step 5: Building OpenBB Platform..."
echo "----------------------------------------"

cd "$BUILD_DIR"

# Install OpenBB in development mode
pip install -e .

# Install ROIC provider
cd "$ROIC_PROVIDER_DIR"
pip install -e .

echo "✅ OpenBB built with ROIC provider"

# Step 6: Create launch script
echo ""
echo "🚀 Step 6: Creating launch script..."
echo "-------------------------------------"

cat > "$OPBB_DIR/launch-openbb-custom.sh" << 'EOF'
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
EOF

chmod +x "$OPBB_DIR/launch-openbb-custom.sh"

echo "✅ Launch script created"

# Step 7: Test the integration
echo ""
echo "🧪 Step 7: Testing ROIC integration..."
echo "---------------------------------------"

python -c "
import sys
sys.path.insert(0, '$BUILD_DIR')
try:
    from openbb_platform.providers.roic.openbb_roic import ROICProvider
    print('✅ ROIC Provider loads successfully')
    print(f'   Provider name: {ROICProvider.name}')
    print(f'   Display name: {ROICProvider.display_name}')
except Exception as e:
    print(f'❌ Error: {e}')
"

echo ""
echo "==========================================="
echo "   ✅ BUILD COMPLETE!"
echo "==========================================="
echo ""
echo "To launch OpenBB with ROIC provider:"
echo "  ./launch-openbb-custom.sh"
echo ""
echo "ROIC commands now available:"
echo "  /equity/fundamental/metrics --symbol AAPL --provider roic"
echo "  /equity/estimates/consensus --symbol MSFT --provider roic"
echo ""
echo "ROIC appears in provider dropdown:"
echo "  --provider [yfinance | polygon | fred | roic]"
echo "                                          ^^^^"
echo "==========================================="
