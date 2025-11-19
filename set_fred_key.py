#!/usr/bin/env python3
"""
Set FRED API key in OpenBB configuration
"""

import os
from pathlib import Path
import json

# FRED API key
fred_key = "7c26de454d31a77bfdf9aaa33f2f55a8"

# Set environment variable
os.environ['FRED_API_KEY'] = fred_key
os.environ['OPENBB_API_FRED_KEY'] = fred_key

# Update OpenBB configuration files
config_locations = [
    Path.home() / ".openbb" / "user_settings.json",
    Path.home() / ".openbb_platform" / "user_settings.json",
    Path.home() / ".openbb_cli" / "user_settings.json"
]

for config_file in config_locations:
    try:
        # Create directory if needed
        config_file.parent.mkdir(exist_ok=True)
        
        # Load existing config or create new
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
        else:
            config = {}
        
        # Add credentials section if not present
        if "credentials" not in config:
            config["credentials"] = {}
        
        # Add FRED API key
        config["credentials"]["fred_api_key"] = fred_key
        
        # Keep existing Polygon key if present
        config["credentials"]["polygon_api_key"] = "Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai"
        
        # Save config
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Updated: {config_file}")
        
    except Exception as e:
        print(f"⚠️  Could not update {config_file}: {e}")

print("\n✅ FRED API key has been saved!")
print(f"   Key: {fred_key}")
print("\nYou can now use these commands:")
print("  /commodity/price/spot --provider fred")
print("  /economy/gdp --provider fred")
print("  /economy/inflation --provider fred")
print("\nThe API key is permanently saved in your OpenBB settings.")
