#!/usr/bin/env python3
"""
Simple ROIC Integration Tester
Tests all components without manual environment setup
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and display results"""
    print(f"\n{'='*60}")
    print(f"📊 {description}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout)
        return True
    else:
        print(f"❌ Error: {result.stderr}")
        return False

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║            ROIC INTEGRATION TEST SUITE                   ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: ROIC CLI - Quality Metrics
    tests_total += 1
    if run_command(
        "cd /Users/sdg223157/OPBB-1 && ./roic quality AAPL",
        "Test 1: ROIC CLI - Quality Metrics for AAPL"
    ):
        tests_passed += 1
        print("✅ ROIC CLI is working!")
    
    # Test 2: ROIC CLI - Forecast
    tests_total += 1
    if run_command(
        "cd /Users/sdg223157/OPBB-1 && ./roic forecast MSFT",
        "Test 2: ROIC CLI - Forecast for MSFT"
    ):
        tests_passed += 1
        print("✅ ROIC Forecast is working!")
    
    # Test 3: ROIC CLI - Compare
    tests_total += 1
    if run_command(
        "cd /Users/sdg223157/OPBB-1 && ./roic compare AAPL GOOGL",
        "Test 3: ROIC CLI - Compare AAPL vs GOOGL"
    ):
        tests_passed += 1
        print("✅ ROIC Compare is working!")
    
    # Test 4: Integration Test
    tests_total += 1
    if run_command(
        "cd /Users/sdg223157/OPBB-1 && python3 test_roic_integration.py",
        "Test 4: Full Integration Test"
    ):
        tests_passed += 1
        print("✅ Integration test passed!")
    
    # Test 5: ROIC Wrapper with OpenBB (requires env activation)
    tests_total += 1
    if run_command(
        "cd /Users/sdg223157/OPBB-1 && source /Users/sdg223157/OPBB/openbb-env/bin/activate && python3 roic_wrapper.py NVDA",
        "Test 5: ROIC + OpenBB Wrapper for NVDA"
    ):
        tests_passed += 1
        print("✅ ROIC + OpenBB wrapper is working!")
    
    # Summary
    print(f"""
╔══════════════════════════════════════════════════════════╗
║                    TEST RESULTS                          ║
╚══════════════════════════════════════════════════════════╝

    Tests Passed: {tests_passed}/{tests_total}
    Success Rate: {(tests_passed/tests_total)*100:.0f}%
    
    """)
    
    if tests_passed == tests_total:
        print("🎉 ALL TESTS PASSED! ROIC integration is fully functional!")
        print("\n📚 Quick Usage Guide:")
        print("─"*50)
        print("1. ROIC CLI (fastest):")
        print("   ./roic quality AAPL")
        print("   ./roic forecast MSFT")
        print("   ./roic compare AAPL GOOGL")
        print("\n2. With OpenBB data (comprehensive):")
        print("   source /Users/sdg223157/OPBB/openbb-env/bin/activate")
        print("   python3 roic_wrapper.py AAPL")
        print("\n3. Launch OpenBB with ROIC:")
        print("   ./launch-openbb-premium.sh")
    else:
        print(f"⚠️  Some tests failed ({tests_total - tests_passed} failures)")
        print("Please check the error messages above for details.")
    
    return tests_passed == tests_total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
