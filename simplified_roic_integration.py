#!/usr/bin/env python3
"""
Simplified ROIC Integration - Works with existing OpenBB installation
"""

import sys
import os
from pathlib import Path

print("="*60)
print("   SIMPLIFIED ROIC INTEGRATION")
print("="*60)

# Add ROIC package to path
sys.path.insert(0, '/Users/sdg223157/OPBB/openbb_roic_provider_package')
sys.path.insert(0, '/Users/sdg223157/OPBB')

def test_roic_standalone():
    """Test ROIC as standalone module"""
    print("\n📊 Testing ROIC Standalone...")
    try:
        from openbb_roic_provider import roic_provider
        
        # Test AAPL
        metrics = roic_provider.get_metrics("AAPL")
        print(f"✅ ROIC for AAPL: {metrics.get('roic', 'N/A')}%")
        print(f"   Quality Score: {metrics.get('quality_score', 'N/A')}/100")
        
        # Test forecast
        forecast = roic_provider.get_forecast("AAPL")
        print(f"   1-Year Target: ${forecast.get('1_year_target', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"❌ Standalone test failed: {e}")
        return False

def test_openbb_integration():
    """Test if ROIC can be used with OpenBB"""
    print("\n🔧 Testing OpenBB Integration...")
    try:
        from openbb import obb
        
        # Check if we can access standard providers
        providers = []
        if hasattr(obb, 'coverage') and hasattr(obb.coverage, 'providers'):
            providers = obb.coverage.providers
            print(f"✅ Available providers: {providers[:5]}...")
        
        # Try to manually use ROIC data
        print("\n📈 Manual ROIC Integration:")
        from openbb_roic_provider import roic_provider
        
        # Get data from both sources
        symbol = "AAPL"
        
        # Yahoo data
        yahoo_data = obb.equity.fundamental.metrics(symbol=symbol, provider='yfinance')
        print(f"✅ Yahoo P/E: {getattr(yahoo_data.results[0], 'pe_ratio', 'N/A') if yahoo_data.results else 'N/A'}")
        
        # ROIC data
        roic_data = roic_provider.get_metrics(symbol)
        print(f"✅ ROIC Score: {roic_data.get('roic', 'N/A')}%")
        
        return True
        
    except Exception as e:
        print(f"⚠️ Integration test: {e}")
        return False

def create_hybrid_launcher():
    """Create a hybrid launcher that combines OpenBB and ROIC"""
    print("\n🚀 Creating Hybrid Launcher...")
    
    launcher_content = '''#!/usr/bin/env python3
"""
Hybrid OpenBB + ROIC Launcher
Provides ROIC data alongside OpenBB
"""

import sys
import os

# Add ROIC to path
sys.path.insert(0, '/Users/sdg223157/OPBB/openbb_roic_provider_package')
sys.path.insert(0, '/Users/sdg223157/OPBB')

def roic_command(symbol):
    """Get ROIC data for a symbol"""
    from openbb_roic_provider import roic_provider
    
    metrics = roic_provider.get_metrics(symbol)
    forecast = roic_provider.get_forecast(symbol)
    
    print(f"""
{'='*50}
ROIC Analysis for {symbol}
{'='*50}
ROIC:           {metrics.get('roic', 'N/A')}%
Quality Score:  {metrics.get('quality_score', 'N/A')}/100
Moat Rating:    {metrics.get('moat_rating', 'N/A')}

Price Targets:
1 Year:  ${forecast.get('1_year_target', 'N/A')}
2 Year:  ${forecast.get('2_year_target', 'N/A')}
3 Year:  ${forecast.get('3_year_target', 'N/A')}
{'='*50}
""")

# Check command line args
if len(sys.argv) > 1:
    if sys.argv[1].lower() == 'roic' and len(sys.argv) > 2:
        roic_command(sys.argv[2].upper())
    else:
        # Launch normal OpenBB
        os.system('source /Users/sdg223157/OPBB/openbb-env/bin/activate && openbb')
else:
    print("""
Hybrid OpenBB + ROIC Launcher
=============================
Usage:
  python hybrid_launcher.py         # Launch OpenBB CLI
  python hybrid_launcher.py roic AAPL  # Get ROIC data
""")
'''
    
    launcher_path = "/Users/sdg223157/OPBB/hybrid_launcher.py"
    with open(launcher_path, 'w') as f:
        f.write(launcher_content)
    
    os.chmod(launcher_path, 0o755)
    print(f"✅ Created: {launcher_path}")
    
    return launcher_path

def create_integration_wrapper():
    """Create a wrapper that adds ROIC to OpenBB session"""
    print("\n🔄 Creating Integration Wrapper...")
    
    wrapper_content = '''#!/usr/bin/env python3
"""
ROIC + OpenBB Integration Wrapper
Use this to add ROIC data to your OpenBB session
"""

from openbb import obb
import sys
sys.path.insert(0, '/Users/sdg223157/OPBB')

from openbb_roic_provider import roic_provider

class ROICEnhancedOBB:
    """Enhanced OBB with ROIC methods"""
    
    def __init__(self):
        self.obb = obb
        self.roic = roic_provider
    
    def get_complete_metrics(self, symbol):
        """Get both OpenBB and ROIC metrics"""
        result = {
            'symbol': symbol,
            'openbb': {},
            'roic': {}
        }
        
        # Get OpenBB data
        try:
            metrics = self.obb.equity.fundamental.metrics(symbol=symbol, provider='yfinance')
            if metrics.results:
                data = metrics.results[0]
                result['openbb'] = {
                    'pe_ratio': getattr(data, 'pe_ratio', None),
                    'market_cap': getattr(data, 'market_cap', None),
                    'revenue': getattr(data, 'revenue', None),
                }
        except:
            pass
        
        # Get ROIC data
        try:
            roic_data = self.roic.get_metrics(symbol)
            result['roic'] = roic_data
        except:
            pass
        
        return result
    
    def display_analysis(self, symbol):
        """Display comprehensive analysis"""
        data = self.get_complete_metrics(symbol)
        
        print(f"""
{'='*60}
COMPREHENSIVE ANALYSIS: {symbol}
{'='*60}

OpenBB Metrics:
  P/E Ratio:    {data['openbb'].get('pe_ratio', 'N/A')}
  Market Cap:   {data['openbb'].get('market_cap', 'N/A')}

ROIC Metrics:
  ROIC:         {data['roic'].get('roic', 'N/A')}%
  Quality:      {data['roic'].get('quality_score', 'N/A')}/100
  Moat:         {data['roic'].get('moat_rating', 'N/A')}
{'='*60}
""")

# Create global instance
enhanced = ROICEnhancedOBB()

# Example usage
if __name__ == "__main__":
    if len(sys.argv) > 1:
        enhanced.display_analysis(sys.argv[1].upper())
    else:
        print("Usage: python roic_wrapper.py SYMBOL")
        print("Example: python roic_wrapper.py AAPL")
'''
    
    wrapper_path = "/Users/sdg223157/OPBB/roic_wrapper.py"
    with open(wrapper_path, 'w') as f:
        f.write(wrapper_content)
    
    print(f"✅ Created: {wrapper_path}")
    return wrapper_path

# Run tests
print("\n" + "="*60)
print("   TESTING INTEGRATION")
print("="*60)

# Test 1: Standalone ROIC
standalone_ok = test_roic_standalone()

# Test 2: OpenBB Integration  
integration_ok = test_openbb_integration()

# Create helpers
launcher = create_hybrid_launcher()
wrapper = create_integration_wrapper()

# Summary
print("\n" + "="*60)
print("   INTEGRATION SUMMARY")
print("="*60)

if standalone_ok and integration_ok:
    print("✅ ROIC works standalone and with OpenBB!")
elif standalone_ok:
    print("✅ ROIC works standalone")
    print("⚠️ Full OpenBB integration needs source rebuild")
else:
    print("⚠️ Some components need attention")

print(f"""
📊 Available Options:

1. USE ROIC CLI (Recommended):
   ./roic quality AAPL
   ./roic forecast MSFT

2. USE HYBRID LAUNCHER:
   python {launcher}
   python {launcher} roic AAPL

3. USE INTEGRATION WRAPPER:
   python {wrapper} AAPL

4. BUILD FROM SOURCE (Advanced):
   Retry with better network connection:
   ./build_openbb_with_roic.sh

The ROIC provider is ready for when OpenBB adds
plugin support in a future release!
""")
