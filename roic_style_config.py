#!/usr/bin/env python3
"""
ROIC Display Style Configuration
Switch between custom style and OpenBB-style output
"""

import os
import json
from pathlib import Path

CONFIG_FILE = Path.home() / ".openbb" / "roic_config.json"

def set_display_style(style: str = "openbb"):
    """
    Set the display style for ROIC output
    
    Args:
        style: "custom" for original style, "openbb" for OpenBB-style tables
    """
    CONFIG_FILE.parent.mkdir(exist_ok=True)
    
    config = {"display_style": style}
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ ROIC display style set to: {style}")
    print(f"   Config saved to: {CONFIG_FILE}")

def get_display_style() -> str:
    """Get current display style"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config.get("display_style", "custom")
    return "custom"

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        style = sys.argv[1].lower()
        if style in ["custom", "openbb"]:
            set_display_style(style)
        else:
            print("Usage: python roic_style_config.py [custom|openbb]")
    else:
        current = get_display_style()
        print(f"Current ROIC display style: {current}")
        print("\nTo change:")
        print("  python roic_style_config.py openbb  # OpenBB-style tables")
        print("  python roic_style_config.py custom  # Original style")
