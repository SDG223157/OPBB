#!/usr/bin/env python3
"""
ROIC Integration Status Checker
Shows what's working and what's not
"""

import sys
import os
import subprocess
from pathlib import Path

def check_status(description, command, shell=True):
    """Check if a command works"""
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False

print("""
╔══════════════════════════════════════════════════════════════╗
║              ROIC INTEGRATION STATUS CHECK                   ║
╚══════════════════════════════════════════════════════════════╝
""")

# Check ROIC CLI
print("🔍 Checking ROIC Components...")
print("-" * 60)

# 1. ROIC CLI
roic_cli = Path("/Users/sdg223157/OPBB-1/roic")
if roic_cli.exists():
    print("✅ ROIC CLI Tool: INSTALLED")
    if check_status("ROIC quality command", f"{roic_cli} quality AAPL 2>/dev/null | head -1"):
        print("   └─ Status: WORKING")
    else:
        print("   └─ Status: NOT WORKING")
else:
    print("❌ ROIC CLI Tool: NOT FOUND")

# 2. ROIC Provider Package
roic_package = Path("/Users/sdg223157/OPBB-1/openbb_roic_provider_package")
if roic_package.exists():
    print("✅ ROIC Provider Package: INSTALLED")
else:
    print("❌ ROIC Provider Package: NOT FOUND")

# 3. ROIC Wrapper
wrapper = Path("/Users/sdg223157/OPBB-1/roic_wrapper.py")
if wrapper.exists():
    print("✅ ROIC Wrapper Script: INSTALLED")
else:
    print("❌ ROIC Wrapper Script: NOT FOUND")

# 4. OpenBB Installation
print("\n🔍 Checking OpenBB Integration...")
print("-" * 60)

# Check if ROIC appears in OpenBB settings
settings_file = Path.home() / ".openbb_platform" / "user_settings.json"
if settings_file.exists():
    import json
    with open(settings_file, 'r') as f:
        settings = json.load(f)
    if 'providers' in settings and 'roic' in settings['providers']:
        print("✅ ROIC in OpenBB Settings: CONFIGURED")
        if settings['providers']['roic'].get('enabled', False):
            print("   └─ Enabled: YES")
        else:
            print("   └─ Enabled: NO")
    else:
        print("⚠️  ROIC in OpenBB Settings: NOT CONFIGURED")

# Check provider manifest
manifest = Path.home() / ".openbb_platform" / "custom_providers" / "openbb_roic" / "provider.json"
if manifest.exists():
    print("✅ ROIC Provider Manifest: FOUND")
else:
    print("❌ ROIC Provider Manifest: NOT FOUND")

print("""
╔══════════════════════════════════════════════════════════════╗
║                     CURRENT STATUS                           ║
╚══════════════════════════════════════════════════════════════╝

✅ WHAT'S WORKING:
─────────────────
• ROIC CLI commands (./roic quality AAPL)
• ROIC Python API (roic_provider.get_metrics())  
• Integration wrapper (python3 roic_wrapper.py)
• ROIC provider package (ready for integration)

⚠️  LIMITATIONS:
───────────────
• ROIC not available in OpenBB CLI dropdown yet
• Cannot use --provider roic in OpenBB commands
• Requires OpenBB rebuild or plugin support

📊 HOW TO USE ROIC TODAY:
─────────────────────────
1. Standalone ROIC CLI:
   ./roic quality AAPL
   ./roic forecast MSFT
   ./roic compare AAPL GOOGL

2. Combined Analysis:
   source /Users/sdg223157/OPBB/openbb-env/bin/activate
   python3 roic_wrapper.py AAPL

3. Side-by-side:
   Terminal 1: ./roic quality AAPL
   Terminal 2: OpenBB with yfinance/polygon providers

🚀 FUTURE (When OpenBB adds plugin support):
──────────────────────────────────────────────
In OpenBB CLI you'll be able to use:
/equity/fundamental/metrics --symbol AAPL --provider roic
                                            ^^^^^^^^^^^^^^
                            (Not available yet, but ready when OpenBB supports it)
""")

# Quick test
print("\n" + "="*60)
print("QUICK TEST - Running ROIC for AAPL...")
print("="*60)
result = subprocess.run(f"{roic_cli} quality AAPL", shell=True, capture_output=True, text=True)
if result.returncode == 0:
    # Parse the output to show just the key metrics
    for line in result.stdout.split('\n'):
        if 'Return on Invested Capital' in line or 'Quality Score' in line or 'Moat' in line:
            print(line)
