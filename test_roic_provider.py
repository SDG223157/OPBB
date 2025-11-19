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
