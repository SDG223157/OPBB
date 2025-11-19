#!/usr/bin/env python3
"""
Set Finviz Elite API key in OpenBB configuration
"""

import os
from pathlib import Path
import json

# Finviz Elite API key
finviz_key = "be56a0a4-c7b3-4094-85b6-0ad5a3b49fc6"

# Set environment variable
os.environ['FINVIZ_API_KEY'] = finviz_key
os.environ['OPENBB_API_FINVIZ_KEY'] = finviz_key

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
        
        # Add all API keys
        config["credentials"]["finviz_api_key"] = finviz_key
        config["credentials"]["polygon_api_key"] = "Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai"
        config["credentials"]["fred_api_key"] = "7c26de454d31a77bfdf9aaa33f2f55a8"
        
        # Save config
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Updated: {config_file}")
        
    except Exception as e:
        print(f"⚠️  Could not update {config_file}: {e}")

print("\n✅ Finviz Elite API key has been saved!")
print(f"   Key: {finviz_key}")
print("\n🎯 You can now use these forecast commands:")
print("  /equity/estimates/price_target --symbol AAPL --provider finviz")
print("  /equity/discovery/top_retail --provider finviz") 
print("  /equity/ownership/insider_trading --symbol AAPL --provider finviz")
print("\nThe API key is permanently saved in your OpenBB settings.")
