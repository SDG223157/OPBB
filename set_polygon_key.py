#!/usr/bin/env python3
"""
Set Polygon API key in OpenBB user settings
"""

import os
from pathlib import Path
import json

# OpenBB config directory
config_dir = Path.home() / ".openbb"
config_file = config_dir / "user_settings.json"

# Create directory if it doesn't exist
config_dir.mkdir(exist_ok=True)

# Load existing config or create new
if config_file.exists():
    with open(config_file, 'r') as f:
        config = json.load(f)
else:
    config = {}

# Add credentials section if not present
if "credentials" not in config:
    config["credentials"] = {}

# Set Polygon API key
config["credentials"]["polygon_api_key"] = "Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai"

# Save config
with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ Polygon API key has been saved to OpenBB configuration!")
print(f"   Configuration file: {config_file}")
print("\nYou can now use these commands in the CLI:")
print("  ./launch-openbb.sh")
print("  /news/company --symbol AAPL --provider polygon")
print("  /equity/price/quote --symbol AAPL --provider polygon")
print("\nThe API key is now permanently saved in your OpenBB settings.")
